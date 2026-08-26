#!/usr/bin/env python3
"""Generate README.md from LeetCode and NeetCode progress data."""

from __future__ import annotations

import argparse
import sys
from collections import Counter

from neetcode_utils import (
    REPO_ROOT,
    load_leetcode_progress,
    load_solutions,
    neetcode_summary,
)


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


def badge(label: str, value: int | str, color: str) -> str:
    safe_label = label.replace(" ", "%20")
    safe_value = str(value).replace(" ", "%20").replace("/", "%2F").replace("-", "--")
    return f"![{label}](https://img.shields.io/badge/{safe_label}-{safe_value}-{color})"


def progress_bar(done: int, total: int, width: int = 12) -> str:
    if total <= 0:
        return "`------------`"
    filled = round(done / total * width)
    return f"`{'#' * filled}{'-' * (width - filled)}`"


def render_leetcode_section(solutions: list[dict]) -> list[str]:
    counts = Counter(item["difficulty"] for item in solutions)
    languages = sorted({item["language"] for item in solutions})
    total = len(solutions)

    lines = [
        "## LeetCode Progress",
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
            "### Languages Used",
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
            "### Topics Practiced",
            "",
        ]
    )
    lines.extend(f"- {topic}" for topic in TOPICS)
    lines.extend(
        [
            "",
            "### Completed Problems",
            "",
            "| # | Problem | Difficulty | Language | Solution |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )

    if solutions:
        for item in solutions:
            lines.append(
                f"| {int(item['number'])} | {item['title']} | {item['difficulty']} | {item['language']} | [View Solution]({item['directory']}) |"
            )
    else:
        lines.append("| - | No solutions added yet. | - | - | - |")
    return lines


def render_neetcode_section() -> list[str]:
    summary = neetcode_summary()
    list_name = summary["list"]
    total = summary["total"]
    solved = summary["solved"]
    percent = summary["percent"]

    lines = [
        "## NeetCode Progress",
        "",
        f"**{list_name}: {solved} / {total} - {percent}%**",
        "",
        "| Category | Solved | Total | Progress |",
        "| --- | ---: | ---: | --- |",
    ]

    for category, category_total in summary["categoryTotals"].items():
        category_solved = summary["solvedByCategory"][category]
        lines.append(
            f"| {category} | {category_solved} | {category_total} | {progress_bar(category_solved, int(category_total))} |"
        )

    lines.extend(
        [
            "",
            "### Tracked NeetCode Problems",
            "",
            "| # | Problem | Category | Status | Solution |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )

    tracked = []
    for problems in summary["trackedByCategory"].values():
        tracked.extend(problems)
    tracked.sort(key=lambda item: (item.get("category", ""), int(item.get("order", 9999)), int(item["number"])))

    if tracked:
        for item in tracked:
            link = f"[View Solution]({item['directory']})" if item.get("directory") else "-"
            lines.append(f"| {int(item['number'])} | {item['title']} | {item['category']} | {item['status']} | {link} |")
    else:
        lines.append("| - | No NeetCode problems tracked yet. | - | - | - |")

    return lines


def render_readme(solutions: list[dict]) -> str:
    counts = Counter(item["difficulty"] for item in solutions)
    lc_total = len(solutions)
    nc_summary = neetcode_summary()
    progress = load_leetcode_progress()
    last_updated = max(progress.get("lastUpdated", ""), nc_summary.get("lastUpdated", ""))

    lines = [
        "# LeetCode Solutions",
        "",
        badge("LeetCode solved", lc_total, "blue"),
        badge("Easy", counts["Easy"], "brightgreen"),
        badge("Medium", counts["Medium"], "yellow"),
        badge("Hard", counts["Hard"], "red"),
        badge("NeetCode", f"{nc_summary['solved']}/{nc_summary['total']}", "purple"),
        "",
        "This repository tracks my LeetCode practice and NeetCode roadmap progress in one portfolio-ready system.",
        "",
        "Solutions are added with a local script and committed through my own GitHub CLI authentication. This avoids granting a third-party browser extension broad access to my GitHub repositories while keeping the repo useful as a professional portfolio record.",
        "",
        f"Last updated: {last_updated or '2026-08-26'}",
        "",
    ]
    lines.extend(render_leetcode_section(solutions))
    lines.append("")
    lines.extend(render_neetcode_section())
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
            "The script creates the correct problem directory, copies your solution file, generates the per-problem README, updates LeetCode and optional NeetCode metadata, updates this main README, stages only the relevant files, commits, and pushes to GitHub.",
            "",
            "To update NeetCode roadmap progress without adding a completed solution, run:",
            "",
            "```bash",
            "npm run neetcode:update",
            "```",
            "",
            "To print a terminal progress summary, run:",
            "",
            "```bash",
            "npm run neetcode:status",
            "```",
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
