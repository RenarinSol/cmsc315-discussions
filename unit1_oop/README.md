# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

This assignment explores object-oriented programming (OOP) concepts in Python, including inheritance, namespaces, and object copying.

## Learning Objectives

- Create parent and child classes
- Use inheritance to extend functionality
- Understand class and instance namespaces
- Demonstrate shallow and deep copying
- Apply object-oriented design principles

## Requirements

Complete all TODO sections in the source code:

1. Create a parent class.
2. Create a child class using inheritance.
3. Demonstrate class and instance namespaces.
4. Demonstrate shallow and deep copying.
5. Create and test objects in `main()`.
6. Add a student-created extension.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Compare OOP to procedural programming.
4. Discuss the benefits of maintainability and reusability and apply this managing overhead, practical application development, and future use.

## Implementation Summary

I built a small homelab inventory program to demonstrate basic OOP concepts. I chose a homelab because it maps naturally to inheritance: every device on a network has a hostname and an IP address, but servers have extra details, like an operating system and the services they run.

## Class Design

**Device (parent class)**

- Class variable: `network_name`. Every device shares it.
- Instance variables: `hostname` and `ip_address`. Each device gets its own.
- The constructor rejects an empty hostname or IP address.
- `describe()` returns a one-line summary of the device.

**Server (child class)**

- Inherits from `Device`.
- Adds two class variables, `device_type` and `max_services`, and two instance variables, `os_name` and `services`.
- Uses `super().__init__()` so `Device` sets up the hostname and IP. This kept me from rewriting the parent's setup code.
- `services` starts as a new empty list inside `__init__`, so each server gets its own list instead of sharing one.
- Adds a new method, `add_service()`, which stores each service as a dictionary with a name and port.
- Overrides `describe()`. It calls the parent's version first, then adds the OS and services.

## Namespaces

I created two servers, `web01` and `db01`. The output showed:

- Reading `device_type` through the `Server` class and through `web01` both returned "server." `web01` doesn't have its own copy, so Python found it on the class.
- I added `rack_location` to only `web01`. It showed up in `web01.__dict__` but not in `db01.__dict__`.
- Each object's `__dict__` only held its own instance variables. Class variables were not there because they live on the class.
- `network_name` was not in `Server.__dict__` because it is defined on `Device`. `web01.network_name` still worked because Python searches the object, then `Server`, then `Device`.
- When I set `web01.device_type = "vm"`, it created a new instance variable on `web01` only. `db01` and the `Server` class still showed "server." This is called shadowing.

## Shallow vs. Deep Copy

I created a server named `app01` with two services (nginx on port 80 and ssh on port 22), then made a shallow copy and a deep copy. After that, I changed nginx's port to 8080 on the original and added a postgres service.

- The original showed both changes.
- The shallow copy also showed both changes. A shallow copy is a new object, but it still shares the same inner list as the original.
- The deep copy still showed nginx on port 80 and only two services, because a deep copy makes its own copies of every nested list and dictionary.
- I used the `is` operator to prove it: the shallow copy shared the original's exact list (`True`) and the deep copy did not (`False`).
- Changing the shallow copy's hostname did not affect the original. That replaces the value instead of changing a shared object.

## Student Extension

None of the TODOs asked for these, but I added:

- Validation in `add_service()` that rejects an empty name, a port outside 1–65535, a port already in use, and more than 10 services.
- `__repr__`, which gives a readable developer view like `Device(hostname='switch01', ip_address='10.0.0.2')`.
- `__len__`, so `len(server)` returns how many services it runs.

## Edge Cases

Each of these raises a `ValueError`. I caught them with try/except, so the program prints why the input was rejected instead of crashing.

- Empty service name
- Port 70000 (outside the valid range)
- Port 445 used twice on the same server
- Empty hostname, or an IP address that is only spaces
- An 11th service on a server that already has 10

A server with no services is also handled: `describe()` prints "services: none" instead of an empty list.

## Memory and Growth

`services` is a Python list, so it grows as services are added, and adding one is fast. Checking for a duplicate port means looking through the whole list. That's fine with a limit of 10, but with thousands of services a dictionary keyed by port would be faster. Class variables are stored once on the class, so making more servers doesn't copy them. A deep copy uses more memory than a shallow copy because it duplicates every service.

## Real-World Use

This design matches how an IT asset inventory could work. Every asset shares a base record (hostname, IP address), and each type of asset adds its own details. A new asset type, like a printer, would just be a new subclass, without changing the existing code. The port check also mirrors a real problem: two services can't use the same port on one machine.

## Reflection

I learned OOP in Java in my last class, so implementing the same concepts in Python was fun. Inheritance, overriding, and class versus instance variables carried over, but Python needs less 'ceremony'. I can just WRITE.

My biggest challenge was Java habits; I haven’t written Python in a while, and stray semicolons kept creeping in. The other was shallow versus deep copying. A shallow copy is a new object that still shares nested data, like lists, with the original, while a deep copy duplicates everything. Seeing the shallow copy change when I modified the original made it click.

OOP organizes a program around objects and their interactions, while procedural programming is a sequence of steps. When brainstorming, I start procedurally, breaking the problem into steps, then look at which objects each step involves and how they interact.

Encapsulation makes code maintainable. Each class owns its data and behavior, so changes stay contained. The Open/Closed Principle from SOLID says code should be open for extension but closed for modification. Subclassing lets me add features without touching working code, which keeps overhead and risk down as an application grows (Like Ctrl Z, if it breaks undo it).

## How to Run

Right-click `unit1_discussion.py` in IntelliJ and select Run, or run `python3 unit1_discussion.py` in a terminal.