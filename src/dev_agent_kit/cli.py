"""Command-line interface for distributing shared coding-agent assets."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from dev_agent_kit.distribution import DistributionError, DistributionOptions, distribute


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="dev-agent-kit",
        description="Distribute agent-source assets into host-specific coding-agent layouts.",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("agent-source"),
        help="Shared agent source directory. Defaults to ./agent-source.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path.cwd(),
        help="Destination repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--disable-copilot",
        action="store_true",
        help="Do not generate GitHub Copilot files.",
    )
    parser.add_argument(
        "--disable-codex",
        action="store_true",
        help="Do not generate Codex files.",
    )
    parser.add_argument(
        "--disable-claude-code",
        action="store_true",
        help="Do not generate Claude Code files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated destination files that already exist with different content.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the distribution CLI.

    Args:
        argv: Optional argument sequence. Uses ``sys.argv`` when omitted.

    Returns:
        Process exit code.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    options = DistributionOptions(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        enable_copilot=not args.disable_copilot,
        enable_codex=not args.disable_codex,
        enable_claude_code=not args.disable_claude_code,
        force=args.force,
    )

    try:
        result = distribute(options)
    except DistributionError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Distributed {len(result.generated_files)} files to {options.target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
