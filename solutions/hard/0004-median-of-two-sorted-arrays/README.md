# 4. Median of Two Sorted Arrays

| Field | Value |
| --- | --- |
| Problem | 4 |
| Difficulty | Hard |
| Language | Python |
| Completed | 2026-08-26 |
| LeetCode | [https://leetcode.com/problems/median-of-two-sorted-arrays/submissions/2121346414/](https://leetcode.com/problems/median-of-two-sorted-arrays/submissions/2121346414/) |
| NeetCode | NeetCode 150 / Binary Search / solved |

## Approach

Use binary search on the smaller sorted array to find a partition where all values on the left side are less than or equal to all values on the right side. Once the correct partition is found, compute the median from the boundary values without merging the arrays.

## Complexity

- Time: `0(log(min(m, n)))`
- Space: `0(1)`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
