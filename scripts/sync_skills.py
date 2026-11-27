"""Copy the agent skills from .claude/skills/ (the source) to .github/skills/ (the copy GitHub Copilot reads).

Claude Code reads skills from .claude/skills/ and GitHub Copilot from .github/skills/. The kit keeps one
source and generates the copy, so the two never drift.

Usage, from the repository root:
    python scripts/sync_skills.py          copy .claude/skills/ to .github/skills/
    python scripts/sync_skills.py --check  report differences and exit 1 if the copy is out of date

Works on Windows, macOS and Linux. Uses the Python standard library only.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".claude" / "skills"
TARGET = ROOT / ".github" / "skills"
KEEP = {"README.md"}  # files in TARGET that are not generated


def read_normalised(path: Path) -> bytes:
    """File content with line endings normalised, so a CRLF checkout does not count as a difference."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def relative_files(base: Path) -> set:
    if not base.exists():
        return set()
    return {
        p.relative_to(base).as_posix()
        for p in base.rglob("*")
        if p.is_file() and p.relative_to(base).as_posix() not in KEEP
    }


def differences() -> list:
    source_files = relative_files(SOURCE)
    target_files = relative_files(TARGET)
    found = []
    for name in sorted(source_files - target_files):
        found.append(f"missing from .github/skills: {name}")
    for name in sorted(target_files - source_files):
        found.append(f"not in .claude/skills: {name}")
    for name in sorted(source_files & target_files):
        if read_normalised(SOURCE / name) != read_normalised(TARGET / name):
            found.append(f"differs: {name}")
    return found


def sync() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for entry in TARGET.iterdir():
        if entry.name in KEEP:
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    for skill in sorted(p for p in SOURCE.iterdir() if p.is_dir()):
        shutil.copytree(skill, TARGET / skill.name)
        print(f"copied {skill.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report differences without copying")
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print(f"source folder not found: {SOURCE}", file=sys.stderr)
        return 2

    if args.check:
        found = differences()
        if found:
            print(".github/skills is out of date. Run: python scripts/sync_skills.py")
            for line in found:
                print(f"  {line}")
            return 1
        print(".github/skills matches .claude/skills")
        return 0

    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main())
