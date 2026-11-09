"""
=========================================================
UNIT 4 DISCUSSION: BINARY SEARCH TREES (BST)
=========================================================

INSTRUCTIONS:
This assignment focuses on understanding and implementing a
Binary Search Tree (BST).

You will complete and modify the provided code while explaining
key concepts in your own words using comments and output.

----
Application scenario: the homelab inventory from Units 1-3.
- The core tests store VLAN IDs.
- Real-world scenario: an IP address lookup table for the lab's servers.
  DHCP hands out addresses in order (.10, .11, .12...), which is the
  worst insertion order for a BST, so the same IPs are also loaded in a
  balanced order to compare tree shape and search cost.
"""

import sys
from ipaddress import IPv4Address

from unit1_oop.unit1_discussion import Server


class Node:
    def __init__(self, value):
        # TODO (Student):
        # Store the node's value and initialize references
        # to the left and right child nodes.

        # A new node is always a leaf, so both children start empty.
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        # TODO (Student):
        # Initialize an empty Binary Search Tree.

        # An empty tree is just a missing root.
        self.root = None
        # Count of stored values. insert() compares it before and after
        # to tell whether a new node was actually added.
        self.size = 0

    def insert(self, value):
        """
        TODO (Student):
        Insert a value into the BST.

        Requirements:
        - Use the recursive helper method.
        - Add comments explaining why insertion depends on
          whether a value is smaller or larger than the
          current node.
        """
        # Every value must be comparable with the values already in the tree.
        # None can't be compared, and mixing types (an int and a string)
        # raises TypeError, so both are rejected here.
        if value is None:
            return False
        if self.root is not None and type(value) is not type(self.root.value):
            return False

        # Insertion has to follow the same rule search uses: smaller values
        # go left, larger values go right. Placing each value by comparison
        # is what lets search skip half of a balanced tree at every step.
        before = self.size
        self.root = self._insert_recursive(self.root, value)

        # True if a node was added, False for a duplicate.
        return self.size > before

    def _insert_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST insertion.

        Requirements:
        - Create a new node when a position is found.
        - Insert smaller values into the left subtree.
        - Insert larger values into the right subtree.
        - Return the updated node reference.
        """
        # Reached an empty spot, so the new value belongs here.
        if node is None:
            self.size += 1
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        # Equal values are ignored. A lookup table only needs each key once.

        # Returning the node lets each parent re-link to its child on the
        # way back up. Without the return, the new node would never attach.
        return node

    def search(self, value):
        """
        TODO (Student):
        Search for a value in the BST.

        Requirements:
        - Return True if found.
        - Return False if not found.
        - Add comments explaining why BST search is often
          more efficient than linear search.
        """
        # Linear search may check every item, O(n). A BST search makes one
        # comparison per level and drops the whole other subtree each time.
        # In a balanced tree that's about log2(n) checks: around 20 for a
        # million values. A lopsided tree loses that advantage.
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST search.
        """
        # Fell off the tree, so the value isn't stored.
        if node is None:
            return False
        if value == node.value:
            return True
        # Only one side can hold the value, so the other side is skipped.
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def inorder(self):
        """
        TODO (Student):
        Return a list containing the values from an
        in-order traversal.
        """
        values = []
        self._inorder_recursive(self.root, values)
        return values

    def _inorder_recursive(self, node, values):
        """
        TODO (Student):
        Implement in-order traversal.

        Requirements:
        - Visit the left subtree.
        - Visit the current node.
        - Visit the right subtree.
        - Add comments explaining why this traversal
          produces sorted output in a BST.
        """
        if node is None:
            return
        # Everything in the left subtree is smaller than this node and
        # everything on the right is larger. Left, node, right therefore
        # lists the values from smallest to largest at every level.
        self._inorder_recursive(node.left, values)
        values.append(node.value)
        self._inorder_recursive(node.right, values)

    # Extra methods added to show tree shape and search cost.

    def search_path(self, value):
        """Return the nodes visited while searching, to show the skipped subtrees."""
        path = []
        node = self.root
        while node is not None:
            path.append(node.value)
            if value == node.value:
                break
            node = node.left if value < node.value else node.right
        return path

    def height(self) -> int:
        """Number of levels. This is the most comparisons a search can take."""
        return self._height(self.root)

    def _height(self, node) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def display(self, fmt=str):
        """Print the tree sideways: right subtree on top, root on the left."""
        if self.root is None:
            print("    (empty tree)")
            return
        self._display(self.root, 0, fmt)

    def _display(self, node, depth, fmt):
        if node is None:
            return
        self._display(node.right, depth + 1, fmt)
        print("    " + "      " * depth + fmt(node.value))
        self._display(node.left, depth + 1, fmt)


def insert_balanced(tree, sorted_values):
    """
    Insert sorted values median first, then each half the same way.
    Each median becomes the root of its subtree, so the tree stays as
    short as possible no matter how the values arrived.
    """
    if not sorted_values:
        return
    mid = len(sorted_values) // 2
    tree.insert(sorted_values[mid])
    insert_balanced(tree, sorted_values[:mid])
    insert_balanced(tree, sorted_values[mid + 1:])


def demonstrate_ip_lookup():
    """
    Real-world scenario: an IP address lookup table for the homelab.

    Tools like DHCP servers and IPAM software keep addresses sorted so they
    can find a lease, list the subnet in order, or spot the next free IP.
    IPv4Address objects compare numerically, so they work as BST keys.
    """
    print("\n=== REAL-WORLD SCENARIO: IP ADDRESS LOOKUP ===")

    # Unit 1 Server objects supply the addresses. DHCP leased them in
    # order, so they arrive sorted.
    servers = [Server(f"host{i:02d}", f"10.0.0.{i}", "Ubuntu 24.04")
               for i in range(10, 17)]
    leased_order = [IPv4Address(s.ip_address) for s in servers]

    # Sorted input sends every new value to the right of the last one.
    # The tree becomes a single chain, which is a linked list in practice.
    dhcp_tree = BST()
    for ip in leased_order:
        dhcp_tree.insert(ip)
    print("Inserted in DHCP lease order (.10 through .16):")
    dhcp_tree.display()

    # Same seven addresses, median first.
    balanced_tree = BST()
    insert_balanced(balanced_tree, leased_order)
    print("\nSame addresses inserted median first:")
    balanced_tree.display()

    # Both trees hold the same values, so in-order output is identical.
    same = dhcp_tree.inorder() == balanced_tree.inorder()
    print(f"\nBoth trees list the same sorted IPs in-order? {same}")

    # Searching for the last address shows the cost of each shape.
    target = IPv4Address("10.0.0.16")
    for label, tree in [("DHCP order", dhcp_tree), ("Balanced", balanced_tree)]:
        path = [str(ip) for ip in tree.search_path(target)]
        print(f"{label:<11} height {tree.height()}, search for {target} "
              f"checked {len(path)} node(s): {' -> '.join(path)}")

    # A lookup for an address that was never leased.
    missing = IPv4Address("10.0.0.200")
    print(f"Is {missing} leased? {balanced_tree.search(missing)}")


def demonstrate_scaling(n=500):
    """
    Shows how the gap grows with size, and the recursion limit a
    lopsided tree can hit in Python.
    """
    print(f"\n=== INSERTION ORDER AT SCALE ({n} values) ===")

    sequential = BST()
    for i in range(n):
        sequential.insert(i)

    balanced = BST()
    insert_balanced(balanced, list(range(n)))

    print(f"Sequential order: height {sequential.height()} "
          f"(worst-case search checks {sequential.height()} nodes)")
    print(f"Median first:     height {balanced.height()} "
          f"(worst-case search checks {balanced.height()} nodes)")

    # Each level of the tree is one recursive call. Python stops recursion
    # at about 1,000 calls, so a chain longer than that crashes insert().
    limit = sys.getrecursionlimit()
    chain = BST()
    try:
        for i in range(limit + 100):
            chain.insert(i)
        print("Inserted past the recursion limit (unexpected)")
    except RecursionError:
        print(f"Sequential inserts failed with RecursionError at size {chain.size} "
              f"(Python's recursion limit is {limit}). A balanced tree of "
              f"{limit + 100} values would only be about "
              f"{(limit + 100).bit_length()} levels deep.")


def main():
    print("=== UNIT 4: BINARY SEARCH TREES ===")

    # ===============================
    # TODO (Student): BUILD A TREE
    # ===============================
    #
    # Requirements:
    # 1. Create a BST object.
    # 2. Insert at least 7 values.
    # 3. Include values that go into both left
    #    and right subtrees.
    # 4. Display the values inserted.
    # 5. Use comments to explain why a BST is efficient at reducing search space for each step.

    print("\n=== TREE CONSTRUCTION ===")

    # VLAN IDs in the homelab. 50 goes first and becomes the root.
    vlans = BST()
    insert_order = [50, 30, 70, 20, 40, 60, 80, 10, 90]

    for vlan in insert_order:
        vlans.insert(vlan)
        # The path shows where each value landed. Each step down cuts the
        # remaining search space: one comparison rules out a whole subtree.
        path = vlans.search_path(vlan)
        if len(path) == 1:
            side = "root"
        elif vlan < path[-2]:
            side = "left child"
        else:
            side = "right child"
        print(f"insert({vlan}) -> path {' -> '.join(map(str, path))} ({side})")

    # 20, 30, 40 and 10 ended up in the left subtree; 60, 70, 80, 90 in the right.
    print(f"\nInserted {vlans.size} VLANs in this order: {insert_order}")
    print("Tree shape (sideways, root on the left):")
    vlans.display()
    print(f"Height: {vlans.height()} levels for {vlans.size} values")

    # ===============================
    # TODO (Student): IN-ORDER TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Perform an in-order traversal.
    # 2. Display the traversal results.
    # 3. Use comments to explain why the traversal produces
    #    sorted output in a BST.

    print("\n=== IN-ORDER TRAVERSAL ===")

    # Left subtree, then the node, then the right subtree. Since the left
    # side always holds smaller values, the output comes out sorted even
    # though the values were inserted out of order.
    result = vlans.inorder()
    print(f"In-order result: {result}")
    print(f"Matches sorted(insert_order)? {result == sorted(insert_order)}")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for at least two values that exist.
    # 2. Search for at least two values that do not exist.
    # 3. Use comments to clearly explain the results.

    print("\n=== SEARCH TESTS ===")

    # 40 and 90 exist. 25 falls between 20 and 30, and 100 is past the
    # largest value, so neither is stored. Each search follows one path
    # down, so it checks at most height() nodes, not all 9.
    for target in [40, 90, 25, 100]:
        found = vlans.search(target)
        path = " -> ".join(map(str, vlans.search_path(target)))
        result = "found" if found else "not found"
        print(f"search({target}) -> {found}: {result} after checking {path}")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least one edge case.
    #
    # Example ideas:
    # - Traverse an empty tree
    # - Search an empty tree
    # - Insert duplicate values
    # - Create a tree with only one node
    #
    # Use comments to explain what happens and why.

    print("\n=== EDGE CASES ===")

    # 1. Empty tree: the root is None, so traversal returns an empty list
    #    and search returns False right away.
    empty = BST()
    print(f"1. Empty tree: inorder() -> {empty.inorder()}, search(10) -> "
          f"{empty.search(10)}, height -> {empty.height()}")

    # 2. One node: the root is also a leaf, so the tree has height 1.
    single = BST()
    single.insert(99)
    print(f"2. Single node: inorder() -> {single.inorder()}, "
          f"search(99) -> {single.search(99)}, height -> {single.height()}")

    # 3. Duplicate: 40 is already stored, so insert returns False and the
    #    size stays the same.
    print(f"3. insert(40) again -> {vlans.insert(40)}, size still {vlans.size}")

    # 4. Invalid input: None can't be compared, and a string can't be
    #    compared with the int keys. Both are rejected instead of crashing.
    print(f"4. insert(None) -> {vlans.insert(None)}, "
          f"insert('60') -> {vlans.insert('60')}, size still {vlans.size}")

    # 5. Boundary values: the smallest and largest keys are the leftmost
    #    and rightmost nodes, at the ends of the in-order list.
    ordered = vlans.inorder()
    print(f"5. Minimum {ordered[0]} and maximum {ordered[-1]} found: "
          f"{vlans.search(ordered[0])}, {vlans.search(ordered[-1])}")

    demonstrate_ip_lookup()
    demonstrate_scaling()


if __name__ == "__main__":
    main()
