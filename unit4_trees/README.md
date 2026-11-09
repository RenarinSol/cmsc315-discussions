# Unit 4 Discussion: Binary Search Trees

## Overview

This assignment introduces Binary Search Trees (BSTs) and recursive tree operations.

## Learning Objectives

- Build a BST
- Insert values recursively
- Search recursively
- Perform in-order traversal
- Understand BST organization

## Requirements

1. Build a BST.
2. Insert multiple values.
3. Demonstrate in-order traversal.
4. Test searching.
5. Demonstrate edge cases.
6. Create a real-world BST example.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain BST behavior and compare to how ordering works to create efficiency as compared to other data structures.

## Implementation Summary

I continued the homelab inventory from Units 1–3. The core tests stored nine VLAN IDs, and the real-world scenario was an IP address lookup table built from Unit 1 `Server` objects.

## Design Approach

- `insert()` used the recursive helper and returned `True` or `False`, so the caller could tell whether a value was added.
- Duplicates were ignored, since a lookup table only needs each key once.
- `insert()` rejected `None` and values of a different type than the root, because Python can't compare them.
- `search()` and `inorder()` followed the starter's recursive design.
- I added `search_path()`, `height()`, and `display()` to show which nodes a search checked and what shape the tree had.
- I added `insert_balanced()`, which inserted the median first and then each half, to build the shortest possible tree from sorted data.

## Edge Cases

- Traversed and searched an empty tree
- Built a tree with only one node
- Inserted a duplicate value
- Inserted `None` and a string into a tree of integers
- Searched for the smallest and largest values
- Inserted sorted values past Python's recursion limit

## How Trees Improve Performance

Each comparison in a BST drops a whole subtree. A balanced tree finds any value in about log2(n) steps. My VLAN tree held 9 values in 4 levels, and a balanced tree of 500 values was only 9 levels deep. A list has to check items one by one, and in-order traversal returns the values already sorted.

## Why BSTs Can Become Inefficient

A BST's shape depends on insertion order. Sorted input sends every value to the right, so the tree becomes a chain and search drops to O(n), the same as a linked list. When I inserted 500 values in order, the tree was 500 levels tall. In Python, a chain that deep also broke recursive insert, which failed with `RecursionError` at about 1,000 values. Self-balancing trees, like AVL and red-black trees, fix this by reshaping themselves after inserts.

## Real-World Use

DHCP servers and IP address management tools keep addresses sorted to find a lease, list a subnet in order, or spot the next free IP. DHCP also hands out addresses in order, which is the worst case for a plain BST. In my test, the DHCP-order tree was 7 levels tall, and the same seven addresses inserted median first made a tree 3 levels tall.

## Reflection

What I learned

I learned how a BST keeps data ordered with one rule: smaller values go left and larger values go right. I also got more practice with recursion, since insert, search, and traversal all call themselves on a smaller subtree.

Challenges

My biggest challenge was seeing how much insertion order mattered. My first IP tree used addresses in DHCP order and looked fine, but it was really a chain. Printing the tree sideways and its height showed the problem, so I added a median-first insert to compare. Testing sequential inserts at a larger scale also hit Python's recursion limit, which showed that a lopsided tree can crash, not just slow down.

BST behavior and efficiency

A balanced BST finds a value in about log2(n) steps because each comparison skips half of what's left. A list checks items one at a time. A hash table is faster for exact lookups but doesn't keep anything in order. A BST does both, but only while it stays balanced.
