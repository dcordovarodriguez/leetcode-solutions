# 5. Longest Palindromic Substring

| Field | Value |
| --- | --- |
| Problem | 5 |
| Difficulty | Medium |
| Language | C++ |
| Completed | 2026-09-26 |
| LeetCode | [https://leetcode.com/problems/longest-palindromic-substring/](https://leetcode.com/problems/longest-palindromic-substring/) |
| NeetCode | NeetCode 150 / 1-D Dynamic Programming / solved / order 150 |

## Approach

Expand outward from every possible center, checking both odd- and even-length palindromes. Track the starting index and length of the longest palindrome found, then return that substring.

## Complexity

- Time: `Time complexity: O(n²)`
- Space: `Space complexity: O(1)`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
