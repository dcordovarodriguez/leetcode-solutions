# 3. Longest Substring Without Repeating Characters

| Field | Value |
| --- | --- |
| Problem | 3 |
| Difficulty | Medium |
| Language | Python |
| Completed | 2026-08-26 |
| LeetCode | [https://leetcode.com/problems/longest-substring-without-repeating-characters/](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |
| NeetCode | NeetCode 150 / Sliding Window / solved |

## Approach

Use a sliding window and a set to track characters in the current substring. Expand the right side of the window, and when a duplicate appears, move the left side forward while removing characters until the substring is unique again. Track the maximum window length.

## Complexity

- Time: `O(n)`
- Space: `0(min(n, charset))`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
