# Unit 3 Discussion: List Operations

## Overview

This assignment examines insertion, deletion, and searching in Python lists.

## Learning Objectives

- Insert values into a list
- Delete values from a list
- Search for values in a list
- Analyze list behavior and performance

## Requirements

1. Test insertion at the beginning, middle, and end.
2. Test deletion at the beginning, middle, and end.
3. Search for existing and missing values.
4. Demonstrate edge cases.
5. Create a real-world scenario.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. How do list operations impact performance in real-world applications?


Implementation

I continued the homelab inventory from Units 1 and 2. 
The tests use a list of open ports on a server, 
and the real-world scenario is a firewall rule list for web01, built with the Unit 1 Server class.

Design Approach

- insert_at() rejects indexes outside 0 to len(lst). Plain list.insert() quietly appends instead, which could put a firewall rule in the wrong place.

- delete_at() returns None for any invalid index, including negatives. search_value() returns -1 when nothing is found, and pop(-1) would delete the last item.

- search_value() is a linear search that returns the first match.


Edge Cases

- Delete from an empty list
- Insert into an empty list
- Delete with an index that's too high, negative, or not a number
- Insert past the end of the list
- A failed search (-1) passed into a delete
- search an empty list
- search a list with duplicates

Memory and Growth

A Python list is a dynamic array. Adding or removing at the end is fast because nothing moves. 
At the front or middle, every element after that spot has to shift, so it's O(n). 
Search is O(n) because the list isn't sorted. 
In my timing test, front inserts were about 30 to 100 times slower than end inserts.


When a Linked List Outperforms an Array-Based List

A linked list is faster when you insert or delete often at the front, or at a spot you already have a reference to.
It only relinks a couple of pointers, while an array shifts every element after the change.
A deque, which uses linked blocks, was much faster than a list for front inserts in my test. 
The catch is that finding a position in a linked list takes O(n), so arrays are still better for indexing and use less memory.


Real-World Scenario

Firewall rules are kept in an ordered list and checked from the top down, so the first match wins.
Admins insert rules at specific spots, add emergency blocks at the top, and remove old rules, while deny all stays last. Because order matters, a list is the right structure.


Reflection

What I learned

I learned that a Python list is a dynamic array, and that explains its performance. 
Inserting or deleting anywhere except the end shifts every element after that position, 
so where a change happens matters as much as how many items there are. 
I also practiced writing functions that check their input and fail safely instead of crashing.

Challenges

My biggest challenge was a design problem I almost missed. 
Python allows negative indexes, and my search returns -1 when it doesn't find something. 
Passing a failed search into a delete would have quietly removed the last item. 
In my firewall scenario, that's the deny all rule. I fixed it by having delete_at() reject negative indexes, then added an edge case for it.

List operations and performance

A list that only grows at the end, like a log, stays fast at any size.
A list that takes inserts at the front slows down as it grows. 
In my test, front inserts were slower than end inserts. When that happens, a deque or linked list is the better tool.