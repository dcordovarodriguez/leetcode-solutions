#!/usr/bin/env python3
"""Print a terminal summary of NeetCode roadmap progress."""

from __future__ import annotations

from neetcode_utils import neetcode_summary


def main() -> int:
    summary = neetcode_summary()
    title = f"{summary['list']} Progress"
    print(title)
    print("-" * len(title))
    for category, total in summary["categoryTotals"].items():
        solved = summary["solvedByCategory"][category]
        print(f"{category:<24} {solved:>3} / {int(total):<3}")
    print()
    print(f"Total: {summary['solved']} / {summary['total']}")
    print(f"Progress: {summary['percent']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

