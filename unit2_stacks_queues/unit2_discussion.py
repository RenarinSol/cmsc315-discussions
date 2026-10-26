"""
===========================================================
UNIT 2 DISCUSSION: STACKS AND QUEUES (PYTHON)
===========================================================

OVERVIEW:
This assignment introduces two fundamental data structures:
the Stack (LIFO) and the Queue (FIFO).

You will complete, modify, and extend the starter code while
explaining key concepts through comments and improved output.

----
Application scenario: the homelab inventory from Unit 1.
- Queue: servers waiting to be provisioned are built in the order they
  were requested (first requested, first built).
- Stack: a server's services are pushed as they start, so popping shuts
  them down in reverse order (the last service started stops first).
"""

from collections import deque

from unit1_oop.unit1_discussion import Server

class CapacityError(Exception):
    """Raised when push/enqueue is called on a structure that is full."""


def _check_max_size(max_size):
    """Shared validation: max_size must be None or a positive whole number."""
    if max_size is not None and max_size < 1:
        raise ValueError(f"max_size must be at least 1 (got {max_size})")


class Stack:
    def __init__(self, max_size=None):
        # TODO (Student): Create the internal data structure for the stack.
        # Hint: A Python list can be used to store stack values.

        # A list works because all stack activity happens at the end of the list.
        # append() and pop() at the end are O(1) amortized. nothing has to shift.
        _check_max_size(max_size)
        self._items = []
        # Optional capacity limit. None means the stack can
        # keep growing until the computer runs out of memory.
        self.max_size = max_size

    def push(self, value):
        # TODO (Student): Add value to the stack.
        # Add a short comment explaining why this operation supports LIFO behavior.

        #  every new value goes on top (the end of the list), so the most
        # recently pushed value is always the next one pop() removes.
        if self.max_size is not None and len(self._items) >= self.max_size:
            raise CapacityError(f"stack is full ({self.max_size} items); cannot push {value!r}")
        self._items.append(value)

    def pop(self):
        # TODO (Student): Remove and return the most recently added value.
        # Improve or explain empty-stack handling.
        # What should happen if the stack is empty?

        # Empty stack: raise IndexError instead of returning None. Returning None
        # would be ambiguous, because None could be a value someone pushed. Raising
        # also matches what python's own list.pop() does on an empty list.
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        # TODO (Student): Return the top value without removing it.
        # Add a comment explaining what peek does.

        # peek returns the top value (the one pop() would return next) but leaves
        # it in place, so the stack is unchanged. Same empty handling as pop().
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        # TODO (Student): Return True if the stack has no values.
        return len(self._items) == 0

    # len(stack) returns the number of items
    def __len__(self):
        return len(self._items)

    # Readable view, listed from bottom to top
    def __repr__(self):
        return f"Stack(bottom -> top: {self._items})"


class Queue:
    def __init__(self, max_size=None):
        # TODO (Student): Create the internal data structure for the queue.
        # Hint: collections.deque is useful for efficient queue operations.

        # deque removes from the front in O(1). A list would need pop(0), which
        # is O(n) because every remaining item has to shift left by one.
        _check_max_size(max_size)
        self._items = deque()
        # Optional capacity limit. deque(maxlen=...) is not
        # used for this: a full deque with maxlen discards an item from
        # the other end, which would quietly drop the oldest request. Raising an
        # error makes the caller deal with the full queue instead.
        self.max_size = max_size

    def enqueue(self, value):
        # TODO (Student): Add value to the back of the queue.
        # Add a short comment explaining why this operation supports FIFO behavior.

        # FIFO: new values join at the back, and dequeue() removes from the front,
        # so values leave in the same order they arrived.
        if self.max_size is not None and len(self._items) >= self.max_size:
            raise CapacityError(f"queue is full ({self.max_size} items); cannot enqueue {value!r}")
        self._items.append(value)

    def dequeue(self):
        # TODO (Student): Remove and return the value from the front of the queue.
        # Explain or improve empty-queue handling.

        # Empty queue: raise IndexError for the same reasons as Stack.pop().
        # deque.popleft() would raise on its own, but its message ("pop from an
        # empty deque") describes the internals instead of the queue.
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def front(self):
        # TODO (Student): Return the front value without removing it.
        # Add a comment explaining what front returns.

        # front returns the oldest value still waiting (the one dequeue() would
        # return next) without removing it.
        if self.is_empty():
            raise IndexError("front of an empty queue")
        return self._items[0]

    def is_empty(self):
        # TODO (Student): Return True if the queue has no values.
        return len(self._items) == 0

    # len(queue) returns the number of items
    def __len__(self):
        return len(self._items)

    # Readable view, listed from front to back
    def __repr__(self):
        return f"Queue(front -> back: {list(self._items)})"


def expect_error(label, action):
    """Run an operation that should fail, and print the error instead of crashing."""
    try:
        result = action()
        print(f"  {label}: returned {result!r} (unexpected)")
    except (IndexError, CapacityError, ValueError) as err:
        print(f"  {label}: rejected with {type(err).__name__} -> {err}")


def demonstrate_patch_window():
    """
    Real-world scenario that uses both structures together: a maintenance window.

    - A Queue holds the servers waiting to be patched. Patching in request order
      is predictable, and no server gets skipped while newer requests jump ahead.
    - For each server, a Stack holds its running services. Services stop in
      reverse start order (pop), get pushed onto a second stack, and then popping
      that second stack restarts them in the original order.
    """
    print("\n=== REAL-WORLD SCENARIO: PATCH WINDOW ===")

    db01 = Server("db01", "10.0.0.20", "Debian 12")
    db01.add_service("postgres", 5432)
    db01.add_service("pgbouncer", 6432)

    web01 = Server("web01", "10.0.0.10", "Ubuntu 24.04")
    web01.add_service("php-fpm", 9000)
    web01.add_service("nginx", 80)

    patch_queue = Queue()
    patch_queue.enqueue(db01)
    patch_queue.enqueue(web01)
    print(f"Queued for patching: db01, then web01 (size {len(patch_queue)})")

    # The queue stores a reference to each Server, not a copy (the same idea as
    # the Unit 1 shallow copy). A change made after enqueueing shows up in the queue.
    db01.add_service("backup-agent", 9102)
    print("Added backup-agent to db01 after it was queued.")
    print(f"patch_queue.front() is db01? {patch_queue.front() is db01} -> "
          f"queued db01 now has {len(patch_queue.front())} services")

    while not patch_queue.is_empty():
        server = patch_queue.dequeue()
        print(f"\nPatching {server.hostname} (next in line: "
              f"{patch_queue.front().hostname if not patch_queue.is_empty() else 'nobody'})")

        # server.services is in start order, so push each one as "running"
        running = Stack()
        for svc in server.services:
            running.push(svc["name"])

        # Stop in reverse start order. Each stopped service goes onto a second
        # stack, which reverses the order again for the restart.
        stopped = Stack()
        while not running.is_empty():
            name = running.pop()
            stopped.push(name)
            print(f"  stop    {name}")

        print(f"  apply   updates to {server.os_name}")

        while not stopped.is_empty():
            print(f"  start   {stopped.pop()}")

    print(f"\nPatch queue empty? {patch_queue.is_empty()}")


def main():
    print("=== UNIT 2: STACKS AND QUEUES ===")

    # ===============================
    # TODO (Student): STACK DEMO
    # ===============================
    # Requirements:
    # 1. Create a Stack object.
    # 2. Add at least 4 values to the stack.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate LIFO behavior.
    # 5. Show what happens when pop() is used on an empty stack.
    #
    # Edge Cases:
    # 6. Show what happens when peek() is used on an empty stack.
    # 7. Create a stack with only one item, remove it,
    #    and verify the stack is empty afterward.

    print("\n=== STACK DEMO ===")
    print("Scenario: app01 starts its services in dependency order. Each started")
    print("service is pushed onto a stack, so shutdown can pop them in reverse.")

    # 1. Create a Stack object.
    running = Stack()
    app01 = Server("app01", "10.0.0.30", "Rocky Linux 9")

    # 2. Add at least 4 values. The database starts first because the API needs
    #    it, and nginx starts last because it forwards traffic to the API.
    for name, port in [("postgres", 5432), ("redis", 6379), ("api", 8000), ("nginx", 80)]:
        app01.add_service(name, port)  # Unit 1 method, with its port validation
        running.push(name)
        print(f"  push({name!r}) -> started {name}; top of stack is now {running.peek()!r}")

    print(f"  {running}, size {len(running)}")
    print(f"  peek() -> {running.peek()!r} (looked at the top only; size is still {len(running)})")

    # 4. Demonstrate LIFO: pop until empty. The last service started is the first
    #    one stopped, so nothing is still running when something it depends on stops.
    print("\n  Shutting down app01 by popping until the stack is empty:")
    while not running.is_empty():
        print(f"  pop() -> stopped {running.pop()!r}")
    print(f"  Stop order was the reverse of start order. is_empty() -> {running.is_empty()}")

    print("\n  Stack edge cases:")
    # 5. pop() on an empty stack
    expect_error("pop() on an empty stack", running.pop)

    # 6. peek() on an empty stack
    expect_error("peek() on an empty stack", running.peek)

    # 7. Single-item stack: remove the only item, then confirm it's empty
    single = Stack()
    single.push("ssh")
    print(f"  Single-item stack {single}, is_empty() -> {single.is_empty()}")
    removed = single.pop()
    print(f"  pop() -> {removed!r}, is_empty() -> {single.is_empty()}")

    # Capacity limit (boundary condition / "stack overflow")
    capped = Stack(max_size=2)
    capped.push("ssh")
    capped.push("ntp")
    print(f"  Capped stack at its limit: {capped}")
    expect_error("push() past max_size=2", lambda: capped.push("dns"))
    expect_error("Stack(max_size=0)", lambda: Stack(max_size=0))

    # ===============================
    # TODO (Student): QUEUE DEMO
    # ===============================
    # Requirements:
    # 1. Create a Queue object.
    # 2. Add at least 4 values to the queue.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate FIFO behavior.
    # 5. Show what happens when dequeue() is used on an empty queue.
    #
    # Edge Cases:
    # 6. Show what happens when front() is used on an empty queue.
    # 7. Create a queue with only one item, remove it,
    #    and verify the queue is empty afterward.

    print("\n=== QUEUE DEMO ===")
    print("Scenario: new servers are requested for the homelab and provisioned")
    print("(imaged and brought online) in the order the requests came in.")

    # 1. Create a Queue object.
    provisioning = Queue()

    # 2. Add at least 4 values. Each value is a Unit 1 Server object, which shows
    #    the queue works with any kind of data, not just strings or numbers.
    requests = [
        Server("web02", "10.0.0.11", "Ubuntu 24.04"),
        Server("db02", "10.0.0.21", "Debian 12"),
        Server("nas01", "10.0.0.50", "TrueNAS SCALE"),
        Server("mon01", "10.0.0.70", "Alpine"),
    ]
    for server in requests:
        provisioning.enqueue(server)
        print(f"  enqueue({server.hostname}) -> joined the back; "
              f"front is still {provisioning.front().hostname}, size {len(provisioning)}")

    print(f"  front() -> {provisioning.front().hostname} (next to be provisioned; nothing removed)")

    # 4. Demonstrate FIFO: dequeue until empty. Servers come out in request order.
    print("\n  Provisioning servers by dequeuing until the queue is empty:")
    while not provisioning.is_empty():
        server = provisioning.dequeue()
        print(f"  dequeue() -> provisioning {server.hostname} ({server.os_name})")
    print(f"  Build order matched request order. is_empty() -> {provisioning.is_empty()}")

    print("\n  Queue edge cases:")
    # 5. dequeue() on an empty queue
    expect_error("dequeue() on an empty queue", provisioning.dequeue)

    # 6. front() on an empty queue
    expect_error("front() on an empty queue", provisioning.front)

    # 7. Single-item queue: remove the only item, then confirm it's empty
    single_q = Queue()
    single_q.enqueue(Server("spare01", "10.0.0.90", "Proxmox VE"))
    print(f"  Single-item queue {single_q}, is_empty() -> {single_q.is_empty()}")
    removed = single_q.dequeue()
    print(f"  dequeue() -> {removed.hostname}, is_empty() -> {single_q.is_empty()}")

    # Capacity limit (boundary condition / full queue)
    capped_q = Queue(max_size=2)
    capped_q.enqueue("ticket-1")
    capped_q.enqueue("ticket-2")
    print(f"  Capped queue at its limit: {capped_q}")
    expect_error("enqueue() past max_size=2", lambda: capped_q.enqueue("ticket-3"))
    print(f"  Oldest item was kept, not dropped: front() -> {capped_q.front()!r}")

    demonstrate_patch_window()


if __name__ == "__main__":
    main()
