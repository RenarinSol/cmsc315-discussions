# Unit 5 Discussion: Search Algorithms

## Overview

This assignment compares linear search and binary search.

## Learning Objectives

- Implement linear search
- Implement binary search
- Compare performance
- Analyze algorithm efficiency

## Requirements

1. Test both algorithms on a small dataset.
2. Test both algorithms on a large dataset.
3. Demonstrate edge cases.
4. Analyze performance.
5. Create a real-world search scenario.


## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain when to use linear versus binary search, including tradeoffs in real-world scenarios.

## Implementation Summary

I used a World of Warcraft theme. The small dataset was nine real items sorted by item ID, like Thunderfury (19019) and Shadowmourne (49623). The large dataset stood in for the game's full item database with 200,000 sorted IDs.

## Design Approach

- `linear_search()` checked each item in order and returned the first match, or -1.
- `binary_search()` kept a `low` and `high` range and cut it in half each pass until it found the target or the range was empty.
- Both functions took an optional `stats` dictionary that counted comparisons, so the output showed how much work each search did.
- `binary_search()` returned -1 for a target of the wrong type, since comparing a string to an int raises `TypeError`.

## Results

| Search | Linear | Binary |
| --- | --- | --- |
| 46017 in 9 items | 7 comparisons | 2 comparisons |
| 180,000 in 200,000 items | 180,000 comparisons | 16 comparisons |
| Missing ID in 200,000 items | 200,000 comparisons | 18 comparisons |

In my run, 200 lookups took about 0.56 seconds with linear search and less than a millisecond with binary search.

## Edge Cases

- Searched an empty list and a single-item list
- Searched for the first and last items
- Searched for IDs below and above the range
- Searched for an ID passed as a string
- Searched a list with duplicates, where binary search returned a match but not the first one

## Real-World Scenario

Linking an item in chat sends its ID, and the game finds it in a sorted database, so binary search fit. Bags were the opposite: loot goes into the first open slot and items move constantly, so finding a Hearthstone took a linear search. Searching the item database by name also needed linear search, because the data was sorted by ID, not name. When I ran binary search on the unsorted bags, it returned -1 even though the Hearthstone was there.

## When Binary Search Can't Be Used

Binary search only works when the data is sorted by the same key being searched and any position can be reached directly. It doesn't work on unsorted data, on data sorted by a different field, or on a linked list, where reaching the middle means walking every node before it. It also doesn't pay off when data changes so often that it would need re-sorting before every search.

## Reflection

What I learned

I learned that binary search gets its speed from order. Each comparison rules out half of what's left, so 200,000 items took only 18 comparisons, while linear search needed all 200,000. Counting comparisons showed that more clearly than timing alone.

Challenges

My biggest challenge was the edge cases around the loop bounds. Binary search has to stop when `low` passes `high`, and an off-by-one mistake there either skips the last item or loops forever. Testing the first item, the last item, and values just outside the range confirmed the bounds were right. I also found that binary search crashed on a string target, so I added a type check.

Linear vs. binary search

Binary search is the better choice when data is sorted and searched often, like WoW's item database. Linear search still makes sense for small or constantly changing data, like bag slots, where sorting would cost more than a single scan.

## How to Run

In IntelliJ, right-click `unit5_discussion.py` and select Run, or run `python -m unit5_searching_analysis.unit5_discussion` from the project root.
