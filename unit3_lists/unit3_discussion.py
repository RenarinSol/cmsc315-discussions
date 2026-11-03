"""
==================================================
Unit 3 DISCUSSION: List Operations (Insert, Delete, Search)
==================================================

INSTRUCTIONS:
This assignment focuses on understanding how lists behave when elements
are inserted, removed, and searched. You will analyze how Python lists
shift elements in memory and how different operations impact performance.

----
Application scenario: the homelab inventory from Units 1 and 2.
- The core tests use a list of open ports on a server.
- Real-world scenario: a firewall rule list. Rules are checked top to
  bottom and the first match wins, so their order matters.
"""

import time
from collections import deque

from unit1_oop.unit1_discussion import Server


def insert_at(lst, index, value):
    """
    TODO (Student):
    Insert a value into the list at the specified index.

    Requirements:
    - Use a list operation to insert the value.
    - Add comments explaining what happens to existing elements
      after an insertion occurs.
    - Use comments to explain how insertion performance may vary depending on
      where the insertion occurs.
    """
    # list.insert() clamps bad indexes instead of failing, so insert(100, x)
    # quietly appends. Reject them so a misplaced firewall rule is caught.
    # len(lst) is allowed because it means "insert at the end".
    # bool is excluded because Python treats True as 1.
    if not isinstance(index, int) or isinstance(index, bool):
        return False
    if index < 0 or index > len(lst):
        return False

    # A list is a dynamic array, so every element from index onward shifts
    # one spot right to make room. Their indexes all go up by 1.
    # Front: every element shifts, O(n).
    # Middle: about half shift, still O(n).
    # End: nothing shifts, amortized O(1). The array occasionally resizes
    # and copies, but that's rare enough to average out.
    lst.insert(index, value)
    return True


def delete_at(lst, index):
    """
    TODO (Student):
    Remove and return the value at the specified index.

    Requirements:
    - Validate that the index exists.
    - Return the removed value.
    - Return None if the index is invalid.
    - Add comments explaining why index validation and safe deletion are important.
    """
    # pop() raises IndexError on a bad index, which would crash the program.
    # Checking first lets the function return None and leave the list alone.
    if not isinstance(index, int) or isinstance(index, bool):
        return None

    # Negative indexes are rejected even though Python allows them.
    # search_value() returns -1 when nothing is found, and pop(-1) would
    # delete the last item. In the firewall scenario that's "deny all".
    # This check also covers an empty list, where no index is valid.
    if index < 0 or index >= len(lst):
        return None

    # None is ambiguous if the list could hold None (why Unit 2 raised an
    # error instead). This program never stores None, so it's safe here.

    # Everything after index shifts one spot left to close the gap.
    # O(n) at the front, O(1) at the end.
    return lst.pop(index)


def search_value(lst, value):
    """
    TODO (Student):
    Search for a value within the list.

    Requirements:
    - Return the index if the value is found.
    - Return -1 if the value is not found.
    - Add comments explaining why this is a linear search and why it scans sequentially.
    """
    # Linear search: check each element in order from index 0.
    # The list isn't sorted, so no element can be skipped.
    # Best case O(1), worst case O(n) when the value is last or missing.
    # The loop stops at the first match, same as a firewall rule check.
    # enumerate() returns -1 for a miss instead of list.index()'s ValueError.
    for i, item in enumerate(lst):
        if item == value:
            return i
    return -1


def demonstrate_firewall_rules():
    """
    Real-world scenario: firewall rules for web01.

    Firewalls keep rules in an ordered list and use the first rule that
    matches. That takes inserts at the end, at a set position, and at the
    front, plus search and delete. A stack or queue only works at the ends.
    """
    print("\n=== REAL-WORLD SCENARIO: FIREWALL RULES FOR web01 ===")

    # Unit 1 Server class; add_service() still validates the ports.
    web01 = Server("web01", "10.0.0.10", "Ubuntu 24.04")
    web01.add_service("ssh", 22)
    web01.add_service("nginx", 80)
    web01.add_service("nginx-tls", 443)

    # "deny all" has to stay last to catch anything not allowed above it.
    rules = ["deny all"]

    # Insert each allow rule just above "deny all", pushing it down.
    for svc in web01.services:
        insert_at(rules, len(rules) - 1, f"allow tcp/{svc['port']}")
    print("Rules built from web01's services:")
    for i, rule in enumerate(rules):
        print(f"  {i}: {rule}")

    #  scanning IP has to go at the top, or "allow tcp/22"
    # would match first. Every existing rule shifts down.
    insert_at(rules, 0, "deny from 203.0.113.50")
    print("\nAfter an emergency block at the top:", rules)

    # SSH is moving behind a VPN. Find the rule, then delete it by index.
    pos = search_value(rules, "allow tcp/22")
    removed = delete_at(rules, pos)
    print(f"Found 'allow tcp/22' at index {pos}; removed {removed!r}")
    print("Rules now:", rules)

    # Rule doesn't exist: search returns -1 and delete refuses it.
    pos = search_value(rules, "allow tcp/3389")
    print(f"\nsearch for 'allow tcp/3389' -> {pos}; delete_at({pos}) -> {delete_at(rules, pos)}")
    print(f"'deny all' is still the last rule? {rules[-1] == 'deny all'}")


def run_performance_check(n=50_000):
    """
    Times front vs. end inserts for the comments above.
    Exact times depend on the machine, so compare the ratios.
    """
    print(f"\n=== PERFORMANCE CHECK ({n:,} inserts each) ===")

    # End of a list: nothing shifts.
    data = []
    start = time.perf_counter()
    for i in range(n):
        data.insert(len(data), i)
    end_time = time.perf_counter() - start

    # Front of a list: every element shifts on every insert.
    data = []
    start = time.perf_counter()
    for i in range(n):
        data.insert(0, i)
    front_time = time.perf_counter() - start

    # deque (from Unit 2) is built from linked blocks, so nothing shifts.
    linked = deque()
    start = time.perf_counter()
    for i in range(n):
        linked.appendleft(i)
    deque_time = time.perf_counter() - start

    print(f"list insert at end:    {end_time:.4f} s")
    print(f"list insert at front:  {front_time:.4f} s")
    print(f"deque append at front: {deque_time:.4f} s")
    if end_time > 0:
        print(f"List front inserts were about {front_time / end_time:.0f}x slower than end inserts.")


def main():
    print("=== UNIT 3: LIST OPERATIONS ===")

    # ===============================
    # TODO (Student): INSERTION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Create a list containing several values.
    # 2. Display the original list.
    # 3. Test insertion at:
    #    - the beginning
    #    - the middle
    #    - the end
    # 4. Display the list after each insertion.
    # 5. Use comments to explain each step in the implementation.

    print("\n=== INSERTION TESTS ===")

    # Open ports on a server.
    ports = [22, 80, 443, 3306, 5432]
    print("Original ports:            ", ports)

    # Beginning: all 5 existing values shift right.
    insert_at(ports, 0, 21)
    print("Insert 21 at beginning:    ", ports)

    # Middle: 6 // 2 = 3, so only index 3 onward shifts.
    mid = len(ports) // 2
    insert_at(ports, mid, 8080)
    print(f"Insert 8080 at middle ({mid}): ", ports)

    # End: index len(ports) is the same as append, nothing shifts.
    insert_at(ports, len(ports), 9090)
    print("Insert 9090 at end:        ", ports)

    # ===============================
    # TODO (Student): DELETION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Delete an item from:
    #    - the beginning
    #    - the middle
    #    - the end
    # 2. Display the removed value.
    # 3. Display the updated list after each deletion.
    # 4. Use comments to clearly explain what is happening in the output.

    print("\n=== DELETION TESTS ===")
    print("Starting ports:", ports)

    # Beginning: removes 21, and everything else shifts left one spot.
    removed = delete_at(ports, 0)
    print(f"Removed {removed} from beginning ->", ports)

    # Middle: recalculate since the list got shorter.
    mid = len(ports) // 2
    removed = delete_at(ports, mid)
    print(f"Removed {removed} from middle (index {mid}) ->", ports)

    # End: len - 1 is the last valid index, so nothing shifts.
    removed = delete_at(ports, len(ports) - 1)
    print(f"Removed {removed} from end ->", ports)

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for a value that exists.
    # 2. Search for a value that does not exist.
    # 3. Display the search results with clear explanations.
    # 4. Use comments to explain each step.

    print("\n=== SEARCH TESTS ===")
    print("Searching in:", ports)

    # Existing value: the scan stops at the match.
    target = 3306
    idx = search_value(ports, target)
    print(f"search_value({target}) -> {idx}: found at index {idx} "
          f"after checking {idx + 1} element(s).")

    # Missing value: 443 was removed above, so every element gets checked.
    target = 443
    idx = search_value(ports, target)
    print(f"search_value({target}) -> {idx}: not found after checking "
          f"all {len(ports)} element(s).")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Delete using an invalid index
    # - Search for a missing value
    # - Insert into an empty list
    # - Delete from an empty list
    # - Use comments to explain each edge case.

    print("\n=== EDGE CASES ===")

    # 1. Empty list has no valid index, so delete returns None.
    empty = []
    print("1. Delete from empty list ->", delete_at(empty, 0))

    # 2. Index 0 is both the beginning and the end of an empty list.
    print("2. Insert into empty list ->", insert_at(empty, 0, 22), "| list:", empty)

    # 3. Too high, negative, and wrong type are all rejected.
    sample = [22, 80, 443]
    print("3. Delete index 10 ->", delete_at(sample, 10),
          "| index -1 ->", delete_at(sample, -1),
          "| index '1' ->", delete_at(sample, "1"),
          "| list:", sample)

    # 4. len(lst) is valid for insert (the end) but not for delete.
    print("4. delete_at(len) ->", delete_at(sample, len(sample)),
          "| insert_at(len) ->", insert_at(sample, len(sample), 8443),
          "| list:", sample)

    # 5. list.insert would append this; insert_at rejects it.
    print("5. insert_at(100) on a 4-item list ->", insert_at(sample, 100, 9999),
          "| list:", sample)

    # 6. A failed search (-1) passed to delete removes nothing.
    print("6. delete_at(search_value(sample, 3389)) ->",
          delete_at(sample, search_value(sample, 3389)), "| list:", sample)

    # 7. The loop never runs on an empty list, so it returns -1.
    print("7. Search empty list ->", search_value([], 22))

    # 8. Only the first match is returned.
    dupes = [80, 443, 80, 443]
    print("8. Search 443 in", dupes, "->", search_value(dupes, 443), "(first match)")

    demonstrate_firewall_rules()
    run_performance_check()


if __name__ == "__main__":
    main()
