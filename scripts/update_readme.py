#!/usr/bin/env python3
"""Generate README.md from scripts/leetcode_progress.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRESS_PATH = REPO_ROOT / "scripts" / "leetcode_progress.json"
README_PATH = REPO_ROOT / "README.md"
DIFFICULTIES = ("Easy", "Medium", "Hard")
TOPICS = (
    "Arrays",
    "Hash Maps",
    "Two Pointers",
    "Sliding Window",
    "Linked Lists",
    "Trees",
    "Graphs",
    "Dynamic Programming",
    "Binary Search",
    "Backtracking",
)


def load_solutions() -> list[dict]:
    if not PROGRESS_PATH.exists():
        return []
    data = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    return sorted(data.get("solutions", []), key=lambda item: int(item["number"]))


def badge(label: str, value: int, color: str) -> str:
    safe_label = label.replace(" ", "%20")
    return f"![{label}](https://img.shields.io/badge/{safe_label}-{value}-{color})"


def render_readme(solutions: list[dict]) -> str:
    counts = Counter(item["difficulty"] for item in solutions)
    languages = sorted({item["language"] for item in solutions})
    total = len(solutions)

    lines = [
        "# LeetCode Solutions",
        "",
        badge("Total solved", total, "blue"),
        badge("Easy", counts["Easy"], "brightgreen"),
        badge("Medium", counts["Medium"], "yellow"),
        badge("Hard", counts["Hard"], "red"),
        "",
        "This repository tracks my LeetCode practice and documents my progress with data structures, algorithms, and problem-solving patterns.",
        "",
        "Solutions are added with a local script and committed through my own GitHub CLI authentication. This avoids granting a third-party browser extension broad access to my GitHub repositories while keeping the repo useful as a professional portfolio record.",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "## Statistics",
        "",
        "| Difficulty | Solved |",
        "| --- | ---: |",
    ]

    for difficulty in DIFFICULTIES:
        lines.append(f"| {difficulty} | {counts[difficulty]} |")
    lines.extend(
        [
            f"| **Total** | **{total}** |",
            "",
            "## Languages Used",
            "",
        ]
    )

    if languages:
        lines.extend(f"- {language}" for language in languages)
    else:
        lines.append("No solutions added yet.")

    lines.extend(
        [
            "",
            "## Topics Practiced",
            "",
        ]
    )
    lines.extend(f"- {topic}" for topic in TOPICS)
    lines.extend(
        [
            "",
            "## Completed Problems",
            "",
            "| # | Problem | Difficulty | Language | Solution |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )

    if solutions:
        for item in solutions:
            title = item["title"]
            link = item["directory"]
            lines.append(
                f"| {int(item['number'])} | {title} | {item['difficulty']} | {item['language']} | [View Solution]({link}) |"
            )
    else:
        lines.append("| - | No solutions added yet. | - | - | - |")

    lines.extend(
        [
            "",
            "## Adding a Solution",
            "",
            "Run:",
            "",
            "```bash",
            "python3 scripts/add_solution.py",
            "```",
            "",
            "Or, if you prefer npm:",
            "",
            "```bash",
            "npm run leetcode:add",
            "```",
            "",
            "The script creates the correct problem directory, copies your solution file, generates the per-problem README, updates this main README, stages only the relevant files, commits, and pushes to GitHub.",
            "",
            "Per-problem notes include the problem number, title, difficulty, LeetCode URL, language, completion date, approach, time complexity, and space complexity. Full LeetCode problem statements are intentionally not copied into this repository.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if README.md is not current")
    args = parser.parse_args()

    rendered = render_readme(load_solutions())
    if args.check:
        current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
        if current != rendered:
            print("README.md is out of date. Run: python3 scripts/update_readme.py", file=sys.stderr)
            return 1
        return 0

    README_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

