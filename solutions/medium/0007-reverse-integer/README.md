# 7. Reverse Integer

| Field | Value |
| --- | --- |
| Problem | 7 |
| Difficulty | Medium |
| Language | C++ |
| Completed | 2026-10-14 |
| LeetCode | [https://leetcode.com/problems/reverse-integer/](https://leetcode.com/problems/reverse-integer/) |
| NeetCode | No |

## Approach

I get the last digit one at a time and append it to the reverslse. Before I multiply by 10 and adding the next digit, I check whether that would exceed the 32 bit integer range, and return 0 if it does.

## Complexity

- Time: `0(log |x|)`
- Space: `O(1)`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
