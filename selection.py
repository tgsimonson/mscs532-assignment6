"""
selection.py

Implements two algorithms for selecting the kth smallest element
from an unsorted array:

  1. Randomized Quickselect -- expected O(n) time
  2. Median of Medians      -- worst-case O(n) time

Includes empirical benchmarking across three input distributions
and generates a comparison chart.

Usage:
    python selection.py

Outputs:
    selection_comparison.png

Reference:
    Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
    Introduction to algorithms (4th ed.). Random House Publishing Services.
"""

import random
import time
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Shared partition helper
# ---------------------------------------------------------------------------

def _partition(arr, low, high):
    """
    Lomuto partition around arr[high].
    Returns the final index of the pivot.
    Time complexity: O(high - low + 1)
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# Part 1A: Randomized Quickselect
# ---------------------------------------------------------------------------

def randomized_quickselect(arr, k):
    """
    Return the kth smallest element (1-indexed) using Randomized Quickselect.

    Selects a pivot uniformly at random, partitions the array around it,
    and recurses on only one side. Because the pivot is random, no fixed
    input can consistently cause worst-case behavior.

    Time complexity
    ---------------
    Expected: O(n)  -- by linearity of expectation over random pivot choices
    Worst:    O(n²) -- occurs with exponentially small probability

    Space complexity: O(log n) expected recursion depth

    Parameters
    ----------
    arr : list -- input array (modified in place; pass a copy if needed)
    k   : int  -- rank of the desired element (1 = smallest, n = largest)

    Returns
    -------
    The kth smallest element.
    """
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}")
    data = arr[:]
    sys.setrecursionlimit(max(10000, len(data) * 4))
    return _rqs_recursive(data, 0, len(data) - 1, k - 1)


def _rqs_recursive(arr, low, high, k):
    """Recursive helper for Randomized Quickselect (0-indexed k)."""
    if low == high:
        return arr[low]

    # Random pivot
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]

    pivot_idx = _partition(arr, low, high)

    if k == pivot_idx:
        return arr[pivot_idx]
    elif k < pivot_idx:
        return _rqs_recursive(arr, low, pivot_idx - 1, k)
    else:
        return _rqs_recursive(arr, pivot_idx + 1, high, k)


# ---------------------------------------------------------------------------
# Part 1B: Median of Medians (deterministic, worst-case O(n))
# ---------------------------------------------------------------------------

def median_of_medians(arr, k):
    """
    Return the kth smallest element (1-indexed) using the Median of Medians
    algorithm, which guarantees worst-case O(n) time.

    Algorithm (Cormen et al., 2022, Chapter 9):
      1. Divide the array into groups of 5.
      2. Find the median of each group by insertion sort.
      3. Recursively find the median of those medians (the pivot).
      4. Partition around the pivot.
      5. Recurse on only one side.

    The pivot is guaranteed to be between the 30th and 70th percentile of
    the array, ensuring that at least n/4 elements are eliminated at each
    step. This gives the recurrence T(n) <= T(n/5) + T(7n/10) + O(n),
    which solves to T(n) = O(n).

    Time complexity
    ---------------
    Worst case: O(n)  -- guaranteed regardless of input

    Space complexity: O(log n) recursion depth

    Parameters
    ----------
    arr : list -- input array (not modified)
    k   : int  -- rank of the desired element (1 = smallest, n = largest)

    Returns
    -------
    The kth smallest element.
    """
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}")
    sys.setrecursionlimit(max(10000, len(arr) * 4))
    return _mom_select(list(arr), k - 1)


def _mom_select(arr, k):
    """Recursive Median of Medians (0-indexed k)."""
    n = len(arr)

    # Base case: small arrays sorted directly
    if n <= 5:
        return sorted(arr)[k]

    # Step 1: divide into groups of 5 and find each group's median
    groups   = [arr[i:i + 5] for i in range(0, n, 5)]
    medians  = [sorted(g)[len(g) // 2] for g in groups]

    # Step 2: recursively find the median of medians
    pivot = _mom_select(medians, len(medians) // 2)

    # Step 3: partition around the pivot
    low  = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]

    # Step 4: recurse on the appropriate partition
    if k < len(low):
        return _mom_select(low, k)
    elif k < len(low) + len(mid):
        return pivot
    else:
        return _mom_select(high, k - len(low) - len(mid))


# ---------------------------------------------------------------------------
# Input generators
# ---------------------------------------------------------------------------

def random_array(n):
    return [random.randint(0, n * 10) for _ in range(n)]

def sorted_array(n):
    return list(range(n))

def reverse_sorted_array(n):
    return list(range(n, 0, -1))


# ---------------------------------------------------------------------------
# Benchmarking
# ---------------------------------------------------------------------------

def measure_time(select_fn, arr, k):
    """Return elapsed time in milliseconds for one selection call."""
    data = arr[:]
    start = time.perf_counter()
    select_fn(data, k)
    return (time.perf_counter() - start) * 1000


def run_benchmarks():
    sizes = [100, 500, 1000, 2500]

    distributions = {
        "Random":         random_array,
        "Sorted":         sorted_array,
        "Reverse-Sorted": reverse_sorted_array,
    }

    results = {d: {"Randomized": [], "Median of Medians": []} for d in distributions}

    header = (f"{'Distribution':<18} {'n':>5}  "
              f"{'Randomized (ms)':>18}  {'Median of Medians (ms)':>24}")
    print(header)
    print("-" * len(header))

    for dist_name, gen in distributions.items():
        for n in sizes:
            arr = gen(n)
            k   = n // 2   # always select the median

            t_rand = measure_time(randomized_quickselect, arr, k)
            t_mom  = measure_time(median_of_medians,      arr, k)

            results[dist_name]["Randomized"].append(round(t_rand, 3))
            results[dist_name]["Median of Medians"].append(round(t_mom, 3))

            print(f"{dist_name:<18} {n:>5}  {t_rand:>18.3f}  {t_mom:>24.3f}")
        print()

    return sizes, results


# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------

def generate_chart(sizes, results):
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    colors = {"Randomized": "steelblue", "Median of Medians": "tomato"}

    for ax, dist in zip(axes, results):
        x     = range(len(sizes))
        width = 0.35

        ax.bar([i - width / 2 for i in x],
               results[dist]["Randomized"], width,
               label="Randomized Quickselect", color=colors["Randomized"], alpha=0.88)
        ax.bar([i + width / 2 for i in x],
               results[dist]["Median of Medians"], width,
               label="Median of Medians", color=colors["Median of Medians"], alpha=0.88)

        ax.set_title(dist)
        ax.set_xlabel("Input Size")
        ax.set_ylabel("Time (ms)")
        ax.set_xticks(list(x))
        ax.set_xticklabels([str(s) for s in sizes])
        ax.legend(fontsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.suptitle(
        "Randomized Quickselect vs. Median of Medians — Running Time Comparison",
        fontsize=12
    )
    plt.tight_layout()
    plt.savefig("selection_comparison.png", dpi=150, bbox_inches="tight")
    print("Chart saved: selection_comparison.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Correctness checks
    print("Correctness checks:")
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6], 1, 1),
        ([3, 1, 4, 1, 5, 9, 2, 6], 4, 3),
        ([3, 1, 4, 1, 5, 9, 2, 6], 8, 9),
        ([7],                       1, 7),
        ([2, 2, 2, 2],              2, 2),
        (list(range(10, 0, -1)),    5, 5),
    ]

    all_pass = True
    for arr, k, expected in test_cases:
        r = randomized_quickselect(arr[:], k)
        m = median_of_medians(arr[:], k)
        status = "PASS" if r == expected == m else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {status}  k={k} in {arr[:5]}{'...' if len(arr)>5 else ''}  "
              f"-> RQS={r}, MOM={m}, expected={expected}")

    print(f"\nAll checks {'passed' if all_pass else 'FAILED'}.\n")

    sizes, results = run_benchmarks()
    generate_chart(sizes, results)
