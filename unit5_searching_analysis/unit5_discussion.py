"""
=====================================================
UNIT 5 DISCUSSION: SEARCH ALGORITHMS (LINEAR vs BINARY)
=====================================================

INSTRUCTIONS:
In this assignment, you will implement and analyze two
fundamental search algorithms: linear search and binary search.

You will demonstrate your understanding by modifying the
provided code, running experiments on different dataset sizes,
and clearly explaining your results through code comments
and program output.

----
Application scenario: World of Warcraft.
- Binary search: the game's item database, sorted by item ID.
- Linear search: a character's bags, where items sit in whatever slot
  they landed in, so there's no order to take advantage of.
"""

import time


def linear_search(lst, target, stats=None):
    """
    TODO (Student):
    Implement a linear search algorithm.

    Requirements:
    - Search the list from beginning to end.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining why linear search
      has O(n) time complexity.
    """
    # Check each element in order until one matches.
    # Nothing about the list tells us where the target is, so in the worst
    # case (last item, or missing) every element gets checked. The work
    # grows in step with the list size, which is O(n).
    # It also works on unsorted data, since it never relies on order.
    for i, item in enumerate(lst):
        if stats is not None:
            stats["comparisons"] += 1
        if item == target:
            return i
    return -1


def binary_search(lst, target, stats=None):
    """
    TODO (Student):
    Implement a binary search algorithm.

    Requirements:
    - Assume the list is already sorted.
    - Repeatedly reduce the search space by half.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining how each iteration
      reduces the search space.
    """
    # Comparing a string to an int raises TypeError, so a target of the
    # wrong type is treated as not found instead of crashing.
    if lst and type(target) is not type(lst[0]):
        return -1

    # low and high mark the part of the list that could still hold the target.
    low, high = 0, len(lst) - 1

    while low <= high:
        mid = (low + high) // 2
        if stats is not None:
            stats["comparisons"] += 1

        if lst[mid] == target:
            return mid
        # The list is sorted, so if the middle is too small, everything to
        # its left is too small as well. Drop the left half.
        if lst[mid] < target:
            low = mid + 1
        # Otherwise the middle is too big, so drop the right half.
        else:
            high = mid - 1
        # Each pass cuts the remaining range in half: 200,000 items become
        # 100,000, then 50,000, and so on. That takes about log2(n) passes.

    # low passed high, so the range is empty and the target isn't there.
    return -1


def count_comparisons(search, lst, target):
    """Run a search and return (index, comparisons it took)."""
    stats = {"comparisons": 0}
    index = search(lst, target, stats)
    return index, stats["comparisons"]


# A few real items, sorted by item ID the way the game's database is.
ITEM_DB = [
    (6948, "Hearthstone"),
    (17182, "Sulfuras, Hand of Ragnaros"),
    (19019, "Thunderfury, Blessed Blade of the Windseeker"),
    (22691, "Corrupted Ashbringer"),
    (32837, "Warglaive of Azzinoth"),
    (34334, "Thori'dal, the Stars' Fury"),
    (46017, "Val'anyr, Hammer of Ancient Kings"),
    (49623, "Shadowmourne"),
    (71086, "Dragonwrath, Tarecgosa's Rest"),
]
ITEM_IDS = [item_id for item_id, _ in ITEM_DB]


def demonstrate_wow_scenario():
    """
    Real-world scenario: finding items in World of Warcraft.

    The item database is sorted by ID, so a lookup by ID can use binary
    search. Bags and lookups by name have no usable order, so they need
    linear search.
    """
    print("\n=== REAL-WORLD SCENARIO: WORLD OF WARCRAFT ===")

    # Linking an item in chat sends its ID. The client finds the item
    # by ID in a sorted database, which is a binary search problem.
    item_id = 49623
    index, steps = count_comparisons(binary_search, ITEM_IDS, item_id)
    print(f"Chat link for item {item_id}: {ITEM_DB[index][1]} "
          f"({steps} comparisons, binary search)")

    # Bags aren't sorted. Loot goes into the first open slot, and items
    # move around constantly, so linear search is the only option.
    bags = ["Runecloth", "Major Healing Potion", "Elixir of the Mongoose",
            "Heavy Runecloth Bandage", "Felcloth", "Hearthstone",
            "Flask of Supreme Power", "Arcanite Bar"]
    slot, steps = count_comparisons(linear_search, bags, "Hearthstone")
    print(f"Hearthstone found in bag slot {slot} ({steps} comparisons, "
          f"linear search)")

    # Sorting the bags first would cost O(n log n), more than one scan.
    # With items changing every few seconds, the sort would also be out of
    # date right away, so it never pays off.

    # The database is sorted by ID, not name, so a name lookup can't use
    # binary search. It falls back to checking every entry.
    names = [name for _, name in ITEM_DB]
    index, steps = count_comparisons(linear_search, names, "Shadowmourne")
    print(f"Search by name for Shadowmourne: item {ITEM_DB[index][0]} "
          f"({steps} comparisons, linear search)")

    # Running binary search on the unsorted bags gives a wrong answer.
    # The Hearthstone is there, but binary search drops the half it's in.
    print(f"Binary search on unsorted bags for Hearthstone: "
          f"{binary_search(bags, 'Hearthstone')} (wrong, it's in slot {slot})")


def main():
    print("=== UNIT 5: SEARCH ALGORITHMS ===")

    # ===============================
    # TODO (Student): SMALL DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a small sorted dataset.
    # 2. Test both linear search and binary search.
    # 3. Search for:
    #    - a value that exists
    #    - a value that does not exist
    # 4. Use comments to clearly explain the results.

    print("\n=== SMALL DATASET TEST ===")
    print(f"Item IDs (sorted): {ITEM_IDS}")

    # 46017 (Val'anyr) is near the end, so linear search walks almost the
    # whole list while binary search jumps there from the middle.
    # 50000 isn't a real entry, so both searches return -1.
    for target in [46017, 50000]:
        lin_index, lin_steps = count_comparisons(linear_search, ITEM_IDS, target)
        bin_index, bin_steps = count_comparisons(binary_search, ITEM_IDS, target)
        print(f"Search {target}: linear -> {lin_index} in {lin_steps} comparisons, "
              f"binary -> {bin_index} in {bin_steps} comparisons")

    # On 9 items the gap is small. Either search is fast at this size.

    # ===============================
    # TODO (Student): LARGE DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a much larger sorted dataset.
    # 2. Test both search algorithms.
    # 3. Compare the results.
    # 4. Use comments to explain why binary search becomes more
    #    efficient as datasets grow larger.

    print("\n=== LARGE DATASET TEST ===")

    # WoW has over 200,000 item IDs. This stands in for the full database.
    size = 200_000
    big_db = list(range(1, size + 1))
    print(f"Dataset: {size:,} sorted item IDs")

    # Near the end is the worst case for linear search. Missing is too.
    for target in [180_000, 250_000]:
        lin_index, lin_steps = count_comparisons(linear_search, big_db, target)
        bin_index, bin_steps = count_comparisons(binary_search, big_db, target)
        print(f"Search {target:,}: linear {lin_steps:,} comparisons, "
              f"binary {bin_steps} comparisons (index {bin_index})")

    # Timing 200 lookups spread across the list backs up the counts.
    targets = list(range(1, size, size // 200))
    start = time.perf_counter()
    for t in targets:
        linear_search(big_db, t)
    lin_time = time.perf_counter() - start
    start = time.perf_counter()
    for t in targets:
        binary_search(big_db, t)
    bin_time = time.perf_counter() - start
    print(f"200 lookups: linear {lin_time:.3f} s, binary {bin_time:.5f} s")

    # Linear search grows with n: 10x more items means 10x more checks.
    # Binary search grows with log2(n): 10x more items adds only about
    # 3 checks, since each comparison throws away half the list.
    for n in [1_000, 1_000_000, 1_000_000_000]:
        print(f"  {n:>13,} items: linear worst case {n:,}, "
              f"binary worst case {n.bit_length()}")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Single-element list
    # - Value not present
    # - Value at the first position
    # - Value at the last position
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")

    # 1. Empty list: linear search's loop never runs, and binary search
    #    starts with high = -1, so its loop never runs either.
    print(f"1. Empty list: linear {linear_search([], 6948)}, "
          f"binary {binary_search([], 6948)}")

    # 2. One item: low, high, and mid all point at index 0.
    print(f"2. Single item [6948]: linear {linear_search([6948], 6948)}, "
          f"binary {binary_search([6948], 6948)}")

    # 3. First and last positions: the best case for linear search is the
    #    first item, and the last item is its worst. Binary search handles
    #    both ends in about the same number of steps.
    first, last = ITEM_IDS[0], ITEM_IDS[-1]
    _, lin_first = count_comparisons(linear_search, ITEM_IDS, first)
    _, lin_last = count_comparisons(linear_search, ITEM_IDS, last)
    _, bin_first = count_comparisons(binary_search, ITEM_IDS, first)
    _, bin_last = count_comparisons(binary_search, ITEM_IDS, last)
    print(f"3. First item {first}: linear {lin_first}, binary {bin_first} "
          f"comparisons. Last item {last}: linear {lin_last}, "
          f"binary {bin_last} comparisons")

    # 4. Missing values just below the smallest ID and just above the
    #    largest. Both searches return -1 without going out of range.
    print(f"4. Below range (1): binary {binary_search(ITEM_IDS, 1)}. "
          f"Above range (999999): binary {binary_search(ITEM_IDS, 999999)}")

    # 5. Wrong type: "19019" is a string, not an int. Linear search uses
    #    == and returns -1. Binary search uses <, which would raise
    #    TypeError, so it checks the type first.
    print(f"5. Target '19019' as a string: "
          f"linear {linear_search(ITEM_IDS, '19019')}, "
          f"binary {binary_search(ITEM_IDS, '19019')}")

    # 6. Duplicates: binary search returns a match, but not always the
    #    first one. Linear search always returns the first.
    dupes = [100, 200, 200, 200, 300]
    print(f"6. Search 200 in {dupes}: linear {linear_search(dupes, 200)}, "
          f"binary {binary_search(dupes, 200)}")

    demonstrate_wow_scenario()


if __name__ == "__main__":
    main()
