# 1. Two Sum

| Field | Value |
| --- | --- |
| Problem | 1 |
| Difficulty | Easy |
| Language | Python |
| Completed | 2026-08-26 |
| LeetCode | [https://leetcode.com/problems/two-sum/description/](https://leetcode.com/problems/two-sum/description/) |
| NeetCode | NeetCode 150 / Arrays & Hashing / solved |

## Approach

Use a hash map to store each number and its index as I iterate through the array. For each number, calculate the complement needed to reach the target. If that complement is already in the map, return the two indices; otherwise, store the current number and continue.

## Complexity

- Time: `O(n)`
- Space: `0(n)`

## Notes

This README intentionally summarizes the approach without copying the full LeetCode problem statement.
