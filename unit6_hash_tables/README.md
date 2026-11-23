# Unit 6 Discussion: Dictionaries as Hash Tables

## Overview

This assignment uses Python dictionaries to demonstrate hash table behavior.

## Learning Objectives

- Insert key-value pairs
- Retrieve values efficiently
- Update existing values
- Remove entries
- Understand hashing concepts

## Requirements

1. Create and populate a dictionary.
2. Demonstrate lookup operations.
3. Demonstrate update operations.
4. Demonstrate delete operations.
5. Test edge cases.
6. Create a real-world scenario.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain how hash tables behave, what collisions are, and how hash tables can improve efficiency.

## Implementation Summary

I kept the World of Warcraft theme from Unit 5 and built a guild roster. Each key was a character name, and each value held the member's class and guild rank.

## Design Approach

- Names were stored in lowercase, since WoW names aren't case-sensitive. "SYLVANAS" and "Sylvanas" found the same member.
- `update_member()` checked that a member existed before changing them, so a typo couldn't add a new member by accident.
- Lookups and deletes on missing names used `get()` and `pop()` with defaults instead of raising `KeyError`.
- I added a small `ChainedHashTable` class with 8 buckets. Python's `dict` hides its collisions, so this class showed them directly.

## Edge Cases

- Looked up a member who wasn't in the guild
- Removed a member who wasn't in the guild
- Updated a misspelled name
- Inserted the same name with different capitalization
- Used an empty dictionary
- Tried a list as a key, which Python rejected because lists can change

## Collisions and Performance

A collision happens when two keys land in the same slot. My `ChainedHashTable` stored colliding keys in a list in that bucket, so a lookup had to walk the list.

| Sign-ups in 8 buckets | Load factor | Longest chain | Average lookup |
| --- | --- | --- | --- |
| 5-player group | 0.62 | 2 | 1.2 comparisons |
| 40-player raid | 5.00 | 7 | 3.1 comparisons |

As the table filled up, lookups got slower. Python's `dict` avoids this by growing its table once it's about two-thirds full.

## Reflection

What I learned

I learned that a dictionary is a hash table. Python hashes each key into a slot, so lookups, updates, and deletes go straight to the entry instead of searching. I also learned that keys have to be hashable, which is why a list can't be a key.

Challenges

My biggest challenge was that Python's `dict` hides collisions, so there was nothing to measure. I built a small hash table with 8 buckets to see them. Python also randomizes string hashes each run, so my bucket counts changed every time until I wrote a fixed hash function.

How hash tables behave

A hash table turns a key into a slot number and stores the value there, so lookups stay close to O(1) no matter how big the table gets. A collision is when two keys land in the same slot, and each collision adds a comparison. Keeping the load factor low by resizing keeps those chains short.

