# LeetCode Solutions

![LeetCode solved](https://img.shields.io/badge/LeetCode%20solved-2-blue)
![Easy](https://img.shields.io/badge/Easy-1-brightgreen)
![Medium](https://img.shields.io/badge/Medium-1-yellow)
![Hard](https://img.shields.io/badge/Hard-0-red)
![NeetCode](https://img.shields.io/badge/NeetCode-2%2F150-purple)

This repository tracks my LeetCode practice and NeetCode roadmap progress in one portfolio-ready system.

Solutions are added with a local script and committed through my own GitHub CLI authentication. This avoids granting a third-party browser extension broad access to my GitHub repositories while keeping the repo useful as a professional portfolio record.

Last updated: 2026-08-26

## LeetCode Progress

| Difficulty | Solved |
| --- | ---: |
| Easy | 1 |
| Medium | 1 |
| Hard | 0 |
| **Total** | **2** |

### Languages Used

- Python

### Topics Practiced

- Arrays
- Hash Maps
- Two Pointers
- Sliding Window
- Linked Lists
- Trees
- Graphs
- Dynamic Programming
- Binary Search
- Backtracking

### Completed Problems

| # | Problem | Difficulty | Language | Solution |
| ---: | --- | --- | --- | --- |
| 1 | Two Sum | Easy | Python | [View Solution](solutions/easy/0001-two-sum) |
| 2 | Add Two Numbers | Medium | Python | [View Solution](solutions/medium/0002-add-two-numbers) |

## NeetCode Progress

**NeetCode 150: 2 / 150 - 1.3%**

| Category | Solved | Total | Progress |
| --- | ---: | ---: | --- |
| Arrays & Hashing | 1 | 9 | `#-----------` |
| Two Pointers | 0 | 5 | `------------` |
| Sliding Window | 0 | 6 | `------------` |
| Stack | 0 | 7 | `------------` |
| Binary Search | 0 | 7 | `------------` |
| Linked List | 1 | 11 | `#-----------` |
| Trees | 0 | 15 | `------------` |
| Tries | 0 | 3 | `------------` |
| Heap / Priority Queue | 0 | 7 | `------------` |
| Backtracking | 0 | 9 | `------------` |
| Graphs | 0 | 13 | `------------` |
| Advanced Graphs | 0 | 6 | `------------` |
| 1-D Dynamic Programming | 0 | 12 | `------------` |
| 2-D Dynamic Programming | 0 | 11 | `------------` |
| Greedy | 0 | 8 | `------------` |
| Intervals | 0 | 6 | `------------` |
| Math & Geometry | 0 | 8 | `------------` |
| Bit Manipulation | 0 | 7 | `------------` |

### Tracked NeetCode Problems

| # | Problem | Category | Status | Solution |
| ---: | --- | --- | --- | --- |
| 1 | Two Sum | Arrays & Hashing | solved | [View Solution](solutions/easy/0001-two-sum) |
| 2 | Add Two Numbers | Linked List | solved | [View Solution](solutions/medium/0002-add-two-numbers) |

## Adding a Solution

Run:

```bash
python3 scripts/add_solution.py
```

Or, if you prefer npm:

```bash
npm run leetcode:add
```

The script creates the correct problem directory, copies your solution file, generates the per-problem README, updates LeetCode and optional NeetCode metadata, updates this main README, stages only the relevant files, commits, and pushes to GitHub.

To update NeetCode roadmap progress without adding a completed solution, run:

```bash
npm run neetcode:update
```

To print a terminal progress summary, run:

```bash
npm run neetcode:status
```

Per-problem notes include the problem number, title, difficulty, LeetCode URL, language, completion date, approach, time complexity, and space complexity. Full LeetCode problem statements are intentionally not copied into this repository.
