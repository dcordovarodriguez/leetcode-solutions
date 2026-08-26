#!/usr/bin/env python3
"""Update NeetCode roadmap progress without requiring a completed solution file."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from neetcode_utils import (
    REPO_ROOT,
    load_solutions,
    normalize_neetcode_status,
    upsert_neetcode_problem,
    validate_neetcode_category,
)
from update_readme import render_readme


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=check)


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update NeetCode roadmap progress.")
    parser.add_argument("--number")
    parser.add_argument("--title")
    parser.add_argument("--difficulty", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--list", default="NeetCode 150")
    parser.add_argument("--category")
    parser.add_argument("--status")
    parser.add_argument("--order")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    inside = run(["git", "rev-parse", "--show-toplevel"]).stdout.strip()
    if Path(inside).resolve() != REPO_ROOT:
        print("Refusing to run outside the dedicated leetcode-solutions repository.", file=sys.stderr)
        return 1

    number = int(args.number or prompt("Problem number"))
    title = args.title or prompt("Problem title")
    category = validate_neetcode_category(args.category or prompt("NeetCode category"))
    status = normalize_neetcode_status(args.status or prompt("Status", "in-progress"))
    order = args.order or prompt("Order within category/list (optional)")

    matching_solution = next((item for item in load_solutions() if int(item["number"]) == number), None)
    problem = {
        "number": number,
        "title": title,
        "difficulty": args.difficulty or (matching_solution or {}).get("difficulty", ""),
        "url": args.url or (matching_solution or {}).get("url", ""),
        "neetcodeList": args.list,
        "neetcodeCategory": category,
        "neetcodeStatus": status,
        "directory": (matching_solution or {}).get("directory", ""),
    }
    if order:
        problem["neetcodeOrder"] = int(order)

    if args.dry_run:
        print(problem)
        return 0

    upsert_neetcode_problem(problem)
    (REPO_ROOT / "README.md").write_text(render_readme(load_solutions()), encoding="utf-8")

    if not args.no_commit:
        run(["git", "add", "data/neetcode_progress.json", "README.md"])
        commit = run(["git", "commit", "-m", f"neetcode: update {number} {title}"], check=False)
        if commit.returncode not in (0, 1):
            sys.stderr.write(commit.stdout)
            sys.stderr.write(commit.stderr)
            return commit.returncode
        if commit.returncode == 0 and not args.no_push:
            run(["git", "push"])

    print(f"Updated NeetCode progress: {number}. {title} -> {status}")
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
