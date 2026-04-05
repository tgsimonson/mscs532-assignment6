# Assignment 6: Medians, Order Statistics, and Elementary Data Structures

**Course:** MSCS 532 — Algorithms and Data Structures  
**University of the Cumberlands**

---

## Overview

This repository contains Python implementations and written analysis for two parts:

1. **Selection Algorithms** — Randomized Quickselect and Median of Medians, with empirical comparison
2. **Elementary Data Structures** — Dynamic array, stack, queue, singly linked list, and rooted tree

---

## Files

| File | Description |
|---|---|
| `selection.py` | Randomized Quickselect and Median of Medians with benchmarks |
| `data_structures.py` | Dynamic array, stack, queue, linked list, and rooted tree |
| `selection_comparison.png` | Benchmark chart (auto-generated when you run selection.py) |
| `report.docx` | Full written report (APA 7th edition) |

---

## How to Run

**Requirements:** Python 3.8+, matplotlib

```bash
pip install matplotlib
```

**Run selection algorithm benchmarks:**

```bash
python selection.py
```

Runs correctness checks on both algorithms, benchmarks across three input distributions and four sizes, prints timing results, and saves `selection_comparison.png`.

**Run data structures demo:**

```bash
python data_structures.py
```

Demonstrates all operations for each data structure with printed output.

---

## Part 1: Selection Algorithms

### Randomized Quickselect

Selects the kth smallest element by choosing a random pivot, partitioning around it, and recursing on only the side containing k. Expected time O(n), worst case O(n²) with exponentially small probability.

### Median of Medians

Guarantees worst-case O(n) by constructing a pivot provably between the 30th and 70th percentile of the array. Divides input into groups of five, finds each group's median, and recursively finds the median of those medians as the pivot.

### Key Empirical Findings

- Randomized Quickselect is consistently faster in practice due to lower constant factors.
- Median of Medians carries overhead from grouping, sorting, and list allocation at each level.
- Both confirm O(n) behavior empirically with no degradation on sorted or reverse-sorted inputs.

---

## Part 2: Elementary Data Structures

| Structure | Access | Insert | Delete | Notes |
|---|---|---|---|---|
| Dynamic Array | O(1) | O(n) arbitrary, O(1) amortized end | O(n) arbitrary | Doubles capacity on overflow |
| Stack | O(1) top | O(1) amortized | O(1) amortized | Array-backed, cache-friendly |
| Queue | O(1) front | O(1) amortized | O(1) amortized | Circular buffer avoids shifting |
| Singly Linked List | O(n) | O(1) head/tail | O(n) | No shifting; pointer-based |
| Rooted Tree | O(n) | O(1) at known node | O(n) | Left-child right-sibling representation |

---

## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). Random House Publishing Services. https://reader.yuzu.com/books/9780262367509
