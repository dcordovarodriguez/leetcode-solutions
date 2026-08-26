#!/usr/bin/env python3
"""Add a LeetCode solution, update README statistics, commit, and push."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from neetcode_utils import (
    LEETCODE_PROGRESS_PATH,
    REPO_ROOT,
    load_solutions,
    normalize_neetcode_status,
    save_leetcode_progress,
    upsert_neetcode_problem,
    validate_neetcode_category,
)
from update_readme import render_readme


LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
    "java": ".java",
    "c++": ".cpp",
    "cpp": ".cpp",
    "c": ".c",
    "go": ".go",
    "rust": ".rs",
    "swift": ".swift",
    "kotlin": ".kt",
}


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=check)


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def prompt_yes_no(label: str, default: bool = False) -> bool:
    default_text = "y" if default else "n"
    value = prompt(f"{label} (y/n)", default_text).lower()
    return value in {"y", "yes", "true", "1"}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def normalize_difficulty(value: str) -> str:
    normalized = value.strip().lower()
    mapping = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
    if normalized not in mapping:
        raise ValueError("Difficulty must be Easy, Medium, or Hard.")
    return mapping[normalized]


def infer_extension(language: str, source_path: Path) -> str:
    if source_path.suffix:
        return source_path.suffix
    return LANGUAGE_EXTENSIONS.get(language.strip().lower(), ".txt")


def render_problem_readme(item: dict) -> str:
    return f"""# {item['number']}. {item['title']}

| Field | Value |
| --- | --- |
| Problem | {item['number']} |
| Difficulty | {item['difficulty']} |
| Language | {item['language']} |
| Completed | {item['completed_date']} |
| LeetCode | [{item['url']}]({item['url']}) |
| NeetCode | {render_neetcode_field(item)} |

## Approach

{item['approach']}

## Complexity

- Time: `{item['time_complexity']}`
- Space: `{item['space_complexity']}`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
"""


def render_neetcode_field(item: dict) -> str:
    if not item.get("neetcode"):
        return "No"
    parts = [
        item.get("neetcodeList", "NeetCode"),
        item.get("neetcodeCategory", "Uncategorized"),
        item.get("neetcodeStatus", "solved"),
    ]
    if item.get("neetcodeOrder") not in (None, ""):
        parts.append(f"order {item['neetcodeOrder']}")
    return " / ".join(str(part) for part in parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add a LeetCode solution to this repository.")
    parser.add_argument("--number")
    parser.add_argument("--title")
    parser.add_argument("--difficulty")
    parser.add_argument("--url")
    parser.add_argument("--language")
    parser.add_argument("--solution-path")
    parser.add_argument("--approach")
    parser.add_argument("--time-complexity")
    parser.add_argument("--space-complexity")
    parser.add_argument("--neetcode", choices=("yes", "no", "true", "false"))
    parser.add_argument("--neetcode-list", default="NeetCode 150")
    parser.add_argument("--neetcode-category")
    parser.add_argument("--neetcode-status", default="solved")
    parser.add_argument("--neetcode-order")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--no-push", action="store_true", help="commit locally but do not push")
    parser.add_argument("--dry-run", action="store_true", help="show what would be created without writing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    inside = run(["git", "rev-parse", "--show-toplevel"]).stdout.strip()
    if Path(inside).resolve() != REPO_ROOT:
        print("Refusing to run outside the dedicated leetcode-solutions repository.", file=sys.stderr)
        return 1

    number = args.number or prompt("Problem number")
    title = args.title or prompt("Problem title")
    difficulty = normalize_difficulty(args.difficulty or prompt("Difficulty (Easy/Medium/Hard)"))
    url = args.url or prompt("LeetCode URL")
    language = args.language or prompt("Programming language")
    solution_path = Path(args.solution_path or prompt("Solution file path")).expanduser()
    approach = args.approach or prompt("Brief approach")
    time_complexity = args.time_complexity or prompt("Time complexity", "O(n)")
    space_complexity = args.space_complexity or prompt("Space complexity", "O(1)")
    neetcode = (
        args.neetcode.lower() in {"yes", "true"}
        if args.neetcode is not None
        else prompt_yes_no("Is this part of NeetCode?", False)
    )
    neetcode_list = ""
    neetcode_category = ""
    neetcode_status = ""
    neetcode_order = ""
    if neetcode:
        neetcode_list = args.neetcode_list or prompt("NeetCode list", "NeetCode 150")
        neetcode_category = validate_neetcode_category(
            args.neetcode_category or prompt("NeetCode category")
        )
        neetcode_status = normalize_neetcode_status(
            args.neetcode_status or prompt("Status", "solved")
        )
        neetcode_order = args.neetcode_order or prompt("Order within category/list (optional)")

    if not solution_path.exists() or not solution_path.is_file():
        print(f"Solution file not found: {solution_path}", file=sys.stderr)
        return 1

    number_int = int(number)
    problem_slug = f"{number_int:04d}-{slugify(title)}"
    difficulty_dir = difficulty.lower()
    target_dir = REPO_ROOT / "solutions" / difficulty_dir / problem_slug
    extension = infer_extension(language, solution_path)
    target_solution = target_dir / f"solution{extension}"

    existing = load_solutions()
    if any(int(item["number"]) == number_int for item in existing):
        print(f"Problem {number_int} is already present in metadata.", file=sys.stderr)
        return 1

    item = {
        "number": number_int,
        "title": title,
        "difficulty": difficulty,
        "url": url,
        "language": language,
        "completed_date": args.date,
        "approach": approach,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "directory": str(target_dir.relative_to(REPO_ROOT)),
        "solution_file": str(target_solution.relative_to(REPO_ROOT)),
        "neetcode": neetcode,
    }
    if neetcode:
        item.update(
            {
                "neetcodeList": neetcode_list,
                "neetcodeCategory": neetcode_category,
                "neetcodeStatus": neetcode_status,
            }
        )
        if neetcode_order:
            item["neetcodeOrder"] = int(neetcode_order)

    if args.dry_run:
        print(json.dumps(item, indent=2))
        return 0

    target_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(solution_path, target_solution)
    (target_dir / "README.md").write_text(render_problem_readme(item), encoding="utf-8")

    updated = existing + [item]
    save_leetcode_progress({"solutions": updated})
    if neetcode:
        upsert_neetcode_problem(item)
    (REPO_ROOT / "README.md").write_text(render_readme(updated), encoding="utf-8")

    staged_paths = [
        str(target_solution.relative_to(REPO_ROOT)),
        str((target_dir / "README.md").relative_to(REPO_ROOT)),
        "scripts/leetcode_progress.json",
        "data/neetcode_progress.json",
        "README.md",
    ]
    run(["git", "add", *staged_paths])
    run(["git", "commit", "-m", f"leetcode: add {number_int} {title}"])
    if not args.no_push:
        run(["git", "push"])

    print(f"Added {number_int}. {title}")
    print(target_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stdout)
        sys.stderr.write(exc.stderr)
        raise SystemExit(exc.returncode)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
