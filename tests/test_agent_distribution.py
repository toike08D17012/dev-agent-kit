"""Tests for distributing shared agent-source assets."""

from __future__ import annotations

import tomllib
from pathlib import Path

from dev_agent_kit.cli import main
from dev_agent_kit.distribution import DistributionConflictError, DistributionOptions, distribute


def test_default_distribution_creates_all_host_layouts(tmp_path: Path) -> None:
    """Default distribution writes Copilot, Codex, and Claude Code outputs."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"

    result = distribute(DistributionOptions(source_dir=source_dir, target_dir=target_dir))

    assert result.generated_files
    assert result.generated_files.count(target_dir / "AGENTS.md") == 1
    assert result.generated_files.count(target_dir / ".agents" / "skills" / "example-skill" / "SKILL.md") == 1
    assert not (target_dir / ".github" / "copilot-instructions.md").exists()
    assert not (target_dir / ".github" / "skills").exists()
    assert (target_dir / ".github" / "agents" / "example-agent.agent.md").is_file()
    assert (target_dir / "AGENTS.md").read_text(encoding="utf-8") == "# Shared\n"
    assert (target_dir / ".agents" / "skills" / "example-skill" / "SKILL.md").is_file()
    assert (target_dir / ".agents" / "skills" / "example-skill" / "template.md").is_file()
    assert (target_dir / ".codex" / "agents" / "example-agent.toml").is_file()
    assert (target_dir / ".claude" / "CLAUDE.md").is_file()
    assert (target_dir / ".claude" / "skills" / "example-skill" / "SKILL.md").is_file()
    assert (target_dir / ".claude" / "agents" / "example-agent.md").is_file()
    assert not (target_dir / "CLAUDE.md").exists()


def test_disable_flags_suppress_exclusive_outputs(tmp_path: Path) -> None:
    """Each disable flag suppresses files exclusive to the corresponding host."""
    source_dir = _write_agent_source(tmp_path / "agent-source")

    no_copilot_dir = tmp_path / "no-copilot"
    distribute(DistributionOptions(source_dir=source_dir, target_dir=no_copilot_dir, enable_copilot=False))
    assert not (no_copilot_dir / ".github").exists()
    assert (no_copilot_dir / "AGENTS.md").read_text(encoding="utf-8") == "# Shared\n"
    assert (no_copilot_dir / ".agents" / "skills" / "example-skill" / "SKILL.md").is_file()

    no_codex_dir = tmp_path / "no-codex"
    distribute(DistributionOptions(source_dir=source_dir, target_dir=no_codex_dir, enable_codex=False))
    assert (no_codex_dir / "AGENTS.md").read_text(encoding="utf-8") == "# Shared\n"
    assert not (no_codex_dir / ".github" / "copilot-instructions.md").exists()
    assert not (no_codex_dir / ".github" / "skills").exists()
    assert (no_codex_dir / ".agents" / "skills" / "example-skill" / "SKILL.md").is_file()
    assert not (no_codex_dir / ".codex").exists()
    assert "@../AGENTS.md" in (no_codex_dir / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")

    no_claude_dir = tmp_path / "no-claude"
    distribute(DistributionOptions(source_dir=source_dir, target_dir=no_claude_dir, enable_claude_code=False))
    assert not (no_claude_dir / ".claude").exists()


def test_copilot_only_output_creates_shared_agents_assets(tmp_path: Path) -> None:
    """Copilot-only output writes shared AGENTS.md and skills without Codex or Claude files."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"

    distribute(
        DistributionOptions(
            source_dir=source_dir,
            target_dir=target_dir,
            enable_codex=False,
            enable_claude_code=False,
        )
    )

    assert (target_dir / "AGENTS.md").read_text(encoding="utf-8") == "# Shared\n"
    assert not (target_dir / ".github" / "copilot-instructions.md").exists()
    assert not (target_dir / ".github" / "skills").exists()
    assert (target_dir / ".agents" / "skills" / "example-skill" / "SKILL.md").is_file()
    assert (target_dir / ".agents" / "skills" / "example-skill" / "template.md").is_file()
    assert (target_dir / ".github" / "agents" / "example-agent.agent.md").is_file()
    assert not (target_dir / ".codex").exists()
    assert not (target_dir / ".claude").exists()


def test_cli_writes_to_target_directory(tmp_path: Path) -> None:
    """The CLI honors --source-dir and --target-dir."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "custom-target"

    exit_code = main(["--source-dir", str(source_dir), "--target-dir", str(target_dir), "--disable-copilot"])

    assert exit_code == 0
    assert (target_dir / "AGENTS.md").is_file()
    assert (target_dir / ".agents" / "skills" / "example-skill" / "SKILL.md").is_file()
    assert (target_dir / ".claude" / "CLAUDE.md").is_file()
    assert not (target_dir / ".github").exists()


def test_copilot_agents_use_agent_suffix_and_normalized_tools(tmp_path: Path) -> None:
    """Copilot agent output uses .agent.md files and normalized tool aliases."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"

    distribute(DistributionOptions(source_dir=source_dir, target_dir=target_dir))

    agent_content = (target_dir / ".github" / "agents" / "example-agent.agent.md").read_text(encoding="utf-8")
    assert "  - read\n" in agent_content
    assert "  - search\n" in agent_content
    assert "  - edit\n" in agent_content
    assert "  - execute\n" in agent_content
    assert "  - Grep\n" not in agent_content
    assert "  - Glob\n" not in agent_content
    assert "# Example Agent\n" in agent_content


def test_codex_agent_files_are_valid_toml(tmp_path: Path) -> None:
    """Codex agent output is valid TOML with developer instructions."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"

    distribute(DistributionOptions(source_dir=source_dir, target_dir=target_dir))

    toml_content = (target_dir / ".codex" / "agents" / "example-agent.toml").read_text(encoding="utf-8")
    parsed_agent = tomllib.loads(toml_content)
    assert parsed_agent["name"] == "example-agent"
    assert parsed_agent["description"] == "Use this agent to test distribution."
    assert "# Example Agent\n" in parsed_agent["developer_instructions"]


def test_claude_only_output_inlines_shared_instructions_without_root_agents(tmp_path: Path) -> None:
    """Claude-only output does not create root AGENTS.md and inlines shared instructions."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"

    distribute(
        DistributionOptions(
            source_dir=source_dir,
            target_dir=target_dir,
            enable_copilot=False,
            enable_codex=False,
            enable_claude_code=True,
        )
    )

    claude_content = (target_dir / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")
    assert not (target_dir / "AGENTS.md").exists()
    assert not (target_dir / ".agents").exists()
    assert not (target_dir / "CLAUDE.md").exists()
    assert "# Shared\n" in claude_content
    assert "Claude-only rule" in claude_content
    assert "@../AGENTS.md" not in claude_content


def test_conflicting_destination_requires_force(tmp_path: Path) -> None:
    """Different existing destination files fail unless force is enabled."""
    source_dir = _write_agent_source(tmp_path / "agent-source")
    target_dir = tmp_path / "target"
    destination = target_dir / ".github" / "agents" / "example-agent.agent.md"
    destination.parent.mkdir(parents=True)
    destination.write_text("different\n", encoding="utf-8")

    try:
        distribute(DistributionOptions(source_dir=source_dir, target_dir=target_dir))
    except DistributionConflictError:
        pass
    else:
        raise AssertionError("Expected a distribution conflict")

    distribute(DistributionOptions(source_dir=source_dir, target_dir=target_dir, force=True))
    agent_content = destination.read_text(encoding="utf-8")
    assert "name: example-agent\n" in agent_content
    assert "# Example Agent\n" in agent_content


def _write_agent_source(source_dir: Path) -> Path:
    """Create a small agent-source fixture."""
    (source_dir / "instructions").mkdir(parents=True)
    (source_dir / "instructions" / "AGENTS.md").write_text("# Shared\r\n", encoding="utf-8")
    (source_dir / "instructions" / "CLAUDE.md").write_text(
        "# .claude/CLAUDE.md\n\n@../AGENTS.md\n\n## Claude Code\n\n- Claude-only rule\n",
        encoding="utf-8",
    )

    skill_dir = source_dir / "skills" / "example-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Skill\r\n", encoding="utf-8")
    (skill_dir / "template.md").write_text("# Template\n", encoding="utf-8")

    agents_dir = source_dir / "agents"
    agents_dir.mkdir(parents=True)
    (agents_dir / "example-agent.md").write_text(
        "\n".join(
            [
                "---",
                "name: example-agent",
                "description: Use this agent to test distribution.",
                "tools:",
                "  - Read",
                "  - Grep",
                "  - Glob",
                "  - Edit",
                "  - Bash",
                "---",
                "",
                "# Example Agent",
                "",
                "Use this agent for tests.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return source_dir
