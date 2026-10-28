# 10. Regular Expression Matching

| Field | Value |
| --- | --- |
| Problem | 10 |
| Difficulty | Hard |
| Language | C++ |
| Completed | 2026-10-28 |
| LeetCode | [https://leetcode.com/problems/regular-expression-matching/](https://leetcode.com/problems/regular-expression-matching/) |
| NeetCode | No |

## Approach

use a 2d dynamic programming table where dp[i][j] represents whether the first i characters of the string match teh first j characters of the pattern. then handle normal characters and '.' with a direct previous-state match. and handle '*' by skipping the pattern or usign it to consume another matching character.

## Complexity

- Time: `0(m * n)`
- Space: `0(m * n)`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
