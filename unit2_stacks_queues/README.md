# Unit 2 Discussion: Stacks and Queues

## Overview

This assignment explores two fundamental linear data structures:

- Stack (LIFO)
- Queue (FIFO)

## Learning Objectives

- Implement stack operations
- Implement queue operations
- Understand LIFO and FIFO behavior
- Create edge cases

## Requirements

Complete all TODO sections:

1. Implement stack operations.
2. Implement queue operations.
3. Demonstrate LIFO behavior.
4. Demonstrate FIFO behavior.
5. Create and test edge cases.
6. Create a real-world scenario.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain the differences between stacks and queues as this relates to real-world applications.


Implementation Summary
I built on the Unit 1 homelab inventory and imported `Server` with `from unit1\_oop.unit1\_discussion import Server` instead of rewriting it.
Stack: services were pushed as they started (postgres, redis, api, nginx) and popped to shut down in reverse, so nothing stopped before the services that depended on it.
Queue: four servers were provisioned in the order they were requested.
Patch window: a queue held servers waiting for updates, and a stack stopped each server's services in reverse order before restarting them.

Design
The stack used a list and the queue used a `deque`, so every add and remove was O(1). A list-based queue would have needed `pop(0)`, which is O(n).
Removing or peeking on an empty structure raised `IndexError` instead of returning `None`, since `None` could be a stored value.
An optional `max\_size` raised `CapacityError` when full. I didn't use `deque(maxlen=...)` because it silently drops the oldest item.

Edge Cases
Each was caught with try/except and printed a reason instead of crashing: `pop`, `peek`, `dequeue`, and `front` on 
empty structures, adding past `max\_size`, and `max\_size=0`. I also emptied a single-item stack and queue and confirmed `is\_empty()` returned `True`.

Memory and Growth
Both structures used O(n) memory, one reference per item. 
Items were stored by reference, not copied, so adding a `Server` didn't duplicate it. 
The list grew by occasionally reallocating and copying its references; the deque added fixed-size blocks without copying. Neither had a limit unless `max\_size` was set.

Reflection

What I learned

I learned how to use data structures and program with abstract data types (ADTs). 
The Stack and Queue classes define what each operation does, like push, pop, enqueue, and dequeue, while hiding whether a list or a deque stores the data underneath.

Challenges

A challenge I encountered was an `AttributeError` when testing the queue implementation.
I fixed it by reading the traceback, which named the line, the object's type, and the attribute it didn't have.
That showed the code was asking an object for something it didn't have, so I corrected the call to use an attribute or method that object actually had, then reran the tests.

Stacks vs. queues in real-world applications
The difference is which item gets served next.
A stack serves the newest item first, which fits work that has to be unwound in reverse, like undo or shutting down services that depend on each other. 
A queue serves the oldest item first, which fits work where fairness matters, like help desk tickets or provisioning requests. 
Using the wrong one causes real problems, a stack for tickets would let new tickets bury old ones, and a queue for shutdown would stop a database while the app using it was still running.
