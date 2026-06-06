"""Distribution adapters for shared coding-agent source assets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final, cast


class DistributionError(Exception):
    """Base error for distribution failures."""


class DistributionConflictError(DistributionError):
    """Raised when an existing destination file differs and force is disabled."""


@dataclass(frozen=True)
class DistributionOptions:
    """Options for distributing agent-source assets.

    Attributes:
        source_dir: Shared source asset directory.
        target_dir: Destination repository root.
        enable_copilot: Whether to generate GitHub Copilot files.
        enable_codex: Whether to generate Codex files.
        enable_claude_code: Whether to generate Claude Code files.
        force: Whether to overwrite different existing destination files.
    """

    source_dir: Path
    target_dir: Path
    enable_copilot: bool = True
    enable_codex: bool = True
    enable_claude_code: bool = True
    force: bool = False


@dataclass(frozen=True)
class DistributionResult:
    """Summary of files processed by a distribution run."""

    generated_files: tuple[Path, ...]


@dataclass(frozen=True)
class _AgentProfile:
    """Parsed agent profile source."""

    source_path: Path
    slug: str
    name: str
    description: str
    tools: tuple[str, ...]
    body: str


_COPILOT_TOOL_ALIASES: Final[dict[str, str]] = {
    "bash": "execute",
    "edit": "edit",
    "glob": "search",
    "grep": "search",
    "multiedit": "edit",
    "read": "read",
    "shell": "execute",
    "write": "edit",
}


class _DestinationWriter:
    """Writes generated files while enforcing conflict handling."""

    def __init__(self, force: bool) -> None:
        """Initialize the writer.

        Args:
            force: Whether to overwrite different existing files.
        """
        self._force = force
        self._generated_files: list[Path] = []

    @property
    def generated_files(self) -> tuple[Path, ...]:
        """Destination files processed by this writer."""
        return tuple(self._generated_files)

    def write_text(self, destination: Path, content: str) -> None:
        """Write normalized UTF-8 text to a destination path."""
        self.write_bytes(destination, _normalize_text(content).encode("utf-8"))

    def write_bytes(self, destination: Path, content: bytes) -> None:
        """Write bytes to a destination path.

        Args:
            destination: Destination file path.
            content: Bytes to write.

        Raises:
            DistributionConflictError: If the destination differs and force is disabled.
            DistributionError: If a directory blocks the destination file.
        """
        if destination.exists():
            if destination.is_dir():
                raise DistributionError(f"Destination path is a directory: {destination}")
            if destination.read_bytes() != content:
                if not self._force:
                    raise DistributionConflictError(
                        f"Destination file already exists with different content: {destination}. "
                        "Use --force to overwrite it."
                    )
                destination.write_bytes(content)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

        self._generated_files.append(destination)


def distribute(options: DistributionOptions) -> DistributionResult:
    """Distribute shared agent-source assets into enabled host layouts.

    Args:
        options: Distribution options.

    Returns:
        Summary of processed destination files.

    Raises:
        DistributionError: If required source files are missing or invalid.
        DistributionConflictError: If a destination file differs and force is disabled.
    """
    writer = _DestinationWriter(force=options.force)
    shared_agent_assets_enabled = options.enable_copilot or options.enable_codex

    if shared_agent_assets_enabled:
        _distribute_shared_agent_assets(options.source_dir, options.target_dir, writer)

    if options.enable_copilot:
        _distribute_copilot(options.source_dir, options.target_dir, writer)
    if options.enable_codex:
        _distribute_codex(options.source_dir, options.target_dir, writer)
    if options.enable_claude_code:
        _distribute_claude_code(
            options.source_dir,
            options.target_dir,
            writer,
            shared_agent_assets_enabled=shared_agent_assets_enabled,
        )

    return DistributionResult(generated_files=writer.generated_files)


def _distribute_shared_agent_assets(source_dir: Path, target_dir: Path, writer: _DestinationWriter) -> None:
    """Generate assets shared by GitHub Copilot and Codex."""
    shared_instructions = _read_required_text(source_dir / "instructions" / "AGENTS.md")
    writer.write_text(target_dir / "AGENTS.md", shared_instructions)
    _copy_skill_directories(source_dir / "skills", target_dir / ".agents" / "skills", writer)


def _distribute_copilot(source_dir: Path, target_dir: Path, writer: _DestinationWriter) -> None:
    """Generate GitHub Copilot repository assets."""
    for profile in _iter_agent_profiles(source_dir / "agents"):
        destination = target_dir / ".github" / "agents" / f"{profile.slug}.agent.md"
        writer.write_text(destination, _format_markdown_agent(profile, _normalize_copilot_tools(profile.tools)))


def _distribute_codex(source_dir: Path, target_dir: Path, writer: _DestinationWriter) -> None:
    """Generate Codex repository assets."""
    for profile in _iter_agent_profiles(source_dir / "agents"):
        destination = target_dir / ".codex" / "agents" / f"{profile.slug}.toml"
        writer.write_text(destination, _format_codex_agent(profile))


def _distribute_claude_code(
    source_dir: Path,
    target_dir: Path,
    writer: _DestinationWriter,
    *,
    shared_agent_assets_enabled: bool,
) -> None:
    """Generate Claude Code repository assets."""
    shared_instructions = _read_required_text(source_dir / "instructions" / "AGENTS.md")
    claude_instructions = _read_required_text(source_dir / "instructions" / "CLAUDE.md")
    writer.write_text(
        target_dir / ".claude" / "CLAUDE.md",
        _format_claude_instructions(
            shared_instructions,
            claude_instructions,
            shared_instructions_enabled=shared_agent_assets_enabled,
        ),
    )

    _copy_skill_directories(source_dir / "skills", target_dir / ".claude" / "skills", writer)

    for profile_path in _iter_agent_source_files(source_dir / "agents"):
        destination = target_dir / ".claude" / "agents" / profile_path.name
        writer.write_text(destination, _read_required_text(profile_path))


def _copy_skill_directories(source_skills_dir: Path, target_skills_dir: Path, writer: _DestinationWriter) -> None:
    """Copy all skill directories into a host-specific skill directory."""
    if not source_skills_dir.exists():
        return
    if not source_skills_dir.is_dir():
        raise DistributionError(f"Skills source path is not a directory: {source_skills_dir}")

    for skill_dir in sorted(source_skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        _copy_directory_files(skill_dir, target_skills_dir / skill_dir.name, writer)


def _copy_directory_files(source_dir: Path, target_dir: Path, writer: _DestinationWriter) -> None:
    """Copy files from one directory tree without deleting unrelated destination files."""
    for source_path in sorted(source_dir.rglob("*")):
        if source_path.is_symlink():
            raise DistributionError(f"Symlinked skill files are not supported: {source_path}")
        if source_path.is_dir():
            continue
        relative_path = source_path.relative_to(source_dir)
        writer.write_bytes(target_dir / relative_path, _read_source_file_bytes(source_path))


def _read_source_file_bytes(source_path: Path) -> bytes:
    """Read a source file, normalizing UTF-8 text files to LF newlines."""
    content = source_path.read_bytes()
    try:
        return _normalize_text(content.decode("utf-8")).encode("utf-8")
    except UnicodeDecodeError:
        return content


def _read_required_text(source_path: Path) -> str:
    """Read a required UTF-8 text source file."""
    if not source_path.is_file():
        raise DistributionError(f"Required source file is missing: {source_path}")
    return _normalize_text(source_path.read_text(encoding="utf-8"))


def _iter_agent_profiles(agents_dir: Path) -> tuple[_AgentProfile, ...]:
    """Parse all Markdown agent profiles from a source directory."""
    return tuple(_read_agent_profile(path) for path in _iter_agent_source_files(agents_dir))


def _iter_agent_source_files(agents_dir: Path) -> tuple[Path, ...]:
    """Return sorted Markdown agent source files."""
    if not agents_dir.exists():
        return ()
    if not agents_dir.is_dir():
        raise DistributionError(f"Agents source path is not a directory: {agents_dir}")
    return tuple(sorted(path for path in agents_dir.glob("*.md") if path.is_file()))


def _read_agent_profile(source_path: Path) -> _AgentProfile:
    """Read and parse one Markdown agent profile."""
    content = _read_required_text(source_path)
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise DistributionError(f"Agent profile is missing YAML frontmatter: {source_path}")

    closing_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise DistributionError(f"Agent profile frontmatter is not closed: {source_path}")

    metadata = _parse_simple_frontmatter("".join(lines[1:closing_index]), source_path)
    body = "".join(lines[closing_index + 1 :])

    return _AgentProfile(
        source_path=source_path,
        slug=source_path.stem,
        name=_metadata_string(metadata, "name", source_path),
        description=_metadata_string(metadata, "description", source_path),
        tools=_metadata_string_list(metadata, "tools", source_path),
        body=body,
    )


def _parse_simple_frontmatter(source: str, source_path: Path) -> dict[str, str | list[str]]:
    """Parse the simple YAML subset used by source agent files."""
    metadata: dict[str, str | list[str]] = {}
    active_list_key: str | None = None

    for line_number, line in enumerate(source.splitlines(), start=1):
        if not line.strip():
            continue
        if line.startswith("  - "):
            if active_list_key is None:
                raise DistributionError(f"List item without a key in {source_path}:{line_number}")
            values = metadata[active_list_key]
            if not isinstance(values, list):
                raise DistributionError(f"Frontmatter key is not a list in {source_path}:{line_number}")
            values.append(_parse_scalar(line[4:]))
            continue
        if line.startswith((" ", "\t")):
            raise DistributionError(f"Unsupported frontmatter indentation in {source_path}:{line_number}")

        key, separator, raw_value = line.partition(":")
        if not separator or not key.strip():
            raise DistributionError(f"Invalid frontmatter line in {source_path}:{line_number}")

        value = raw_value.strip()
        if value:
            metadata[key.strip()] = _parse_scalar(value)
            active_list_key = None
        else:
            metadata[key.strip()] = []
            active_list_key = key.strip()

    return metadata


def _parse_scalar(value: str) -> str:
    """Parse a scalar value from the supported YAML subset."""
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return stripped[1:-1]
    return stripped


def _metadata_string(metadata: dict[str, str | list[str]], key: str, source_path: Path) -> str:
    """Read a required string metadata field."""
    value = metadata.get(key)
    if not isinstance(value, str) or not value:
        raise DistributionError(f"Agent profile requires a string {key!r} field: {source_path}")
    return value


def _metadata_string_list(metadata: dict[str, str | list[str]], key: str, source_path: Path) -> tuple[str, ...]:
    """Read a required string list metadata field."""
    value = metadata.get(key)
    if not isinstance(value, list):
        raise DistributionError(f"Agent profile requires a list {key!r} field: {source_path}")
    values = cast(list[str], value)
    return tuple(item for item in values if item)


def _normalize_copilot_tools(tools: tuple[str, ...]) -> tuple[str, ...]:
    """Normalize common source tool names to GitHub Copilot aliases."""
    normalized_tools: list[str] = []
    seen_tools: set[str] = set()

    for tool in tools:
        normalized_tool = _COPILOT_TOOL_ALIASES.get(tool.strip().lower(), tool.strip())
        dedupe_key = normalized_tool.lower()
        if dedupe_key in seen_tools:
            continue
        seen_tools.add(dedupe_key)
        normalized_tools.append(normalized_tool)

    return tuple(normalized_tools)


def _format_markdown_agent(profile: _AgentProfile, tools: tuple[str, ...]) -> str:
    """Format a Markdown agent profile with the supplied tools."""
    frontmatter_lines = [
        "---",
        f"name: {profile.name}",
        f"description: {profile.description}",
        "tools:",
        *(f"  - {tool}" for tool in tools),
        "---",
    ]
    return "\n".join(frontmatter_lines) + "\n" + profile.body


def _format_codex_agent(profile: _AgentProfile) -> str:
    """Format a Codex project agent TOML file."""
    return "\n".join(
        [
            f"name = {_format_toml_string(profile.name)}",
            f"description = {_format_toml_string(profile.description)}",
            f"developer_instructions = {_format_toml_multiline_literal(profile.body)}",
            "",
        ]
    )


def _format_toml_string(value: str) -> str:
    """Format a TOML basic string."""
    return json.dumps(value, ensure_ascii=False)


def _format_toml_multiline_literal(value: str) -> str:
    """Format a TOML multiline literal string when possible."""
    normalized_value = _normalize_text(value)
    if "'''" in normalized_value:
        return _format_toml_string(normalized_value)
    if not normalized_value.endswith("\n"):
        normalized_value += "\n"
    return "'''\n" + normalized_value + "'''"


def _format_claude_instructions(
    shared_instructions: str,
    claude_instructions: str,
    *,
    shared_instructions_enabled: bool,
) -> str:
    """Format the Claude Code instruction file for the selected target combination."""
    if shared_instructions_enabled:
        return _ensure_claude_import_path(claude_instructions)

    return _ensure_final_newline(
        "\n\n".join(
            [
                shared_instructions.strip(),
                _remove_claude_shared_import(claude_instructions).strip(),
            ]
        )
    )


def _ensure_claude_import_path(claude_instructions: str) -> str:
    """Ensure the Claude instruction file imports root AGENTS.md from .claude/."""
    lines = _normalize_text(claude_instructions).splitlines()
    adjusted_lines: list[str] = []
    has_shared_import = False

    for line in lines:
        if line.strip() in {"@AGENTS.md", "@./AGENTS.md", "@../AGENTS.md"}:
            adjusted_lines.append("@../AGENTS.md")
            has_shared_import = True
        else:
            adjusted_lines.append(line)

    if not has_shared_import:
        adjusted_lines = ["@../AGENTS.md", "", *adjusted_lines]

    return _ensure_final_newline("\n".join(adjusted_lines))


def _remove_claude_shared_import(claude_instructions: str) -> str:
    """Remove shared AGENTS imports from Claude instructions when AGENTS.md is not generated."""
    lines = _normalize_text(claude_instructions).splitlines()
    return _ensure_final_newline(
        "\n".join(line for line in lines if line.strip() not in {"@AGENTS.md", "@./AGENTS.md", "@../AGENTS.md"})
    )


def _normalize_text(content: str) -> str:
    """Normalize text to LF newlines."""
    return content.replace("\r\n", "\n").replace("\r", "\n")


def _ensure_final_newline(content: str) -> str:
    """Ensure text ends with one LF newline."""
    return content.rstrip("\n") + "\n"
