#!/usr/bin/env python3
"""Print current pending solution files in the LeetCode inbox."""

from __future__ import annotations

from pathlib import Path

from neetcode_utils import REPO_ROOT


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".swift",
    ".kt",
}


def inbox_files() -> list[Path]:
    inbox = REPO_ROOT / "inbox"
    inbox.mkdir(exist_ok=True)
    return sorted(
        path
        for path in inbox.iterdir()
        if path.is_file()
        and path.name != ".gitkeep"
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def main() -> int:
    files = inbox_files()
    print("LeetCode Inbox")
    print("--------------")
    print()
    if not files:
        print("Inbox is empty.")
        return 0

    for path in files:
        print(path.name)
    print()
    label = "solution" if len(files) == 1 else "solutions"
    print(f"{len(files)} pending {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

