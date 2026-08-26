#!/usr/bin/env python3
"""Shared helpers for NeetCode progress tracking."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
LEETCODE_PROGRESS_PATH = REPO_ROOT / "scripts" / "leetcode_progress.json"
NEETCODE_CATEGORIES_PATH = DATA_DIR / "neetcode_categories.json"
NEETCODE_PROGRESS_PATH = DATA_DIR / "neetcode_progress.json"

VALID_NEETCODE_STATUSES = ("not-started", "in-progress", "solved", "review")


def read_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def today() -> str:
    return date.today().isoformat()


def normalize_problem_number(value: int | str) -> int:
    return int(str(value).strip())


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def normalize_neetcode_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in VALID_NEETCODE_STATUSES:
        raise ValueError(f"Status must be one of: {', '.join(VALID_NEETCODE_STATUSES)}")
    return normalized


def load_leetcode_progress() -> dict:
    return read_json(LEETCODE_PROGRESS_PATH, {"lastUpdated": today(), "solutions": []})


def save_leetcode_progress(data: dict) -> None:
    data["lastUpdated"] = today()
    write_json(LEETCODE_PROGRESS_PATH, data)


def load_solutions() -> list[dict]:
    data = load_leetcode_progress()
    return sorted(data.get("solutions", []), key=lambda item: int(item["number"]))


def load_neetcode_categories() -> dict:
    return read_json(NEETCODE_CATEGORIES_PATH, {"defaultList": "NeetCode 150", "categories": {}})


def load_neetcode_progress() -> dict:
    return read_json(NEETCODE_PROGRESS_PATH, {"lastUpdated": today(), "lists": {"NeetCode 150": {"problems": []}}})


def save_neetcode_progress(data: dict) -> None:
    data["lastUpdated"] = today()
    write_json(NEETCODE_PROGRESS_PATH, data)


def validate_neetcode_category(category: str) -> str:
    categories = load_neetcode_categories()["categories"]
    matches = [name for name in categories if name.lower() == category.strip().lower()]
    if not matches:
        raise ValueError(f"Unknown NeetCode category: {category}")
    return matches[0]


def upsert_neetcode_problem(problem: dict) -> None:
    progress = load_neetcode_progress()
    list_name = problem["neetcodeList"]
    progress.setdefault("lists", {}).setdefault(list_name, {"problems": []})
    problems = progress["lists"][list_name].setdefault("problems", [])
    number = normalize_problem_number(problem["number"])

    normalized = {
        "number": number,
        "title": problem["title"],
        "difficulty": problem.get("difficulty", ""),
        "url": problem.get("url", ""),
        "category": validate_neetcode_category(problem["neetcodeCategory"]),
        "status": normalize_neetcode_status(problem.get("neetcodeStatus", "solved")),
    }
    if problem.get("neetcodeOrder") not in (None, ""):
        normalized["order"] = int(problem["neetcodeOrder"])
    if problem.get("directory"):
        normalized["directory"] = problem["directory"]

    for index, existing in enumerate(problems):
        if normalize_problem_number(existing["number"]) == number:
            problems[index] = {**existing, **normalized}
            break
    else:
        problems.append(normalized)

    problems.sort(key=lambda item: (item.get("category", ""), int(item.get("order", 9999)), int(item["number"])))
    save_neetcode_progress(progress)


def neetcode_summary() -> dict:
    config = load_neetcode_categories()
    progress = load_neetcode_progress()
    list_name = config.get("defaultList", "NeetCode 150")
    category_totals = config.get("categories", {})
    problems = progress.get("lists", {}).get(list_name, {}).get("problems", [])

    solved_by_category = Counter()
    tracked_by_category = defaultdict(list)
    for problem in problems:
        category = problem.get("category", "Uncategorized")
        tracked_by_category[category].append(problem)
        if problem.get("status") == "solved":
            solved_by_category[category] += 1

    total = sum(int(value) for value in category_totals.values())
    solved = sum(solved_by_category.values())
    return {
        "list": list_name,
        "total": total,
        "solved": solved,
        "percent": round((solved / total * 100), 1) if total else 0,
        "categoryTotals": category_totals,
        "solvedByCategory": solved_by_category,
        "trackedByCategory": tracked_by_category,
        "lastUpdated": progress.get("lastUpdated", ""),
    }

