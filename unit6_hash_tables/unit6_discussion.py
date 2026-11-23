"""
====================================================
UNIT 6 DISCUSSION: Python Dictionaries as Hash Tables
====================================================

INSTRUCTIONS:
In this activity, you will work with Python dictionaries
to simulate the behavior of a hash table.

You will modify the provided starter code to demonstrate
common operations and explain key concepts.

Follow all TODO prompts in the code and ensure your output
clearly communicates what your program is doing at each step.

----------------------------------------------------
Application scenario: a World of Warcraft guild roster.
- Keys are character names, values are each member's class and rank.
- Names are case-insensitive in WoW, so keys are stored in lowercase.
- A small hash table of my own (ChainedHashTable) shows the collisions
  and load factor that Python's dict handles behind the scenes.
"""


def key_for(name):
    """Normalize a character name so "Thrall" and "thrall" are one key."""
    return name.strip().lower()


def show_roster(roster):
    """Print each member on its own line."""
    if not roster:
        print("  (roster is empty)")
        return
    for name, info in roster.items():
        print(f"  {name:<10} {info['class']:<13} {info['rank']}")


def update_member(roster, name, field, value):
    """Change a field only if the member exists. Returns True if updated."""
    key = key_for(name)
    # roster[key] = ... would quietly add a new member for a typo'd name,
    # so check first.
    if key not in roster:
        return False
    roster[key][field] = value
    return True

def try_insert(table, key, value):
    """Try to add a key and report whether Python accepted it."""
    # The key's type isn't known here, so IntelliJ doesn't flag a list
    # passed in. Python still checks it when the line runs.
    try:
        table[key] = value
        return "accepted"
    except TypeError as err:
        return f"rejected with TypeError ({err})"

class ChainedHashTable:
    """
    A small hash table with separate chaining, to make collisions visible.
    Each bucket is a list. Keys that hash to the same bucket share a list,
    and a lookup has to walk that list comparing keys.
    """

    def __init__(self, num_buckets):
        self.buckets = [[] for _ in range(num_buckets)]
        self.count = 0

    def _index(self, key):
        # Python randomizes string hashes each run, so this uses a fixed
        # polynomial hash to keep the output the same every time.
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % 1_000_003
        return h % len(self.buckets)

    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.count += 1

    def get(self, key):
        """Return (value, comparisons). Value is None if the key is missing."""
        bucket = self.buckets[self._index(key)]
        for i, (k, v) in enumerate(bucket, start=1):
            if k == key:
                return v, i
        return None, len(bucket)

    def load_factor(self):
        # Average entries per bucket. Higher means longer chains.
        return self.count / len(self.buckets)

    def longest_chain(self):
        return max(len(b) for b in self.buckets)


def demonstrate_collisions():
    """
    Real-world scenario: raid sign-ups stored in a fixed-size hash table.
    The same 8 buckets are used for a small group and for a large raid
    to show how collisions slow lookups as the table fills up.
    """
    print("\n=== REAL-WORLD SCENARIO: COLLISIONS IN RAID SIGN-UPS ===")

    small_group = ["thrall", "jaina", "anduin", "sylvanas", "uther"]
    raid = small_group + [f"raider{i:02d}" for i in range(1, 36)]

    for label, names in [("5-player group", small_group), ("40-player raid", raid)]:
        table = ChainedHashTable(num_buckets=8)
        for name in names:
            table.put(name, "signed up")

        # Average comparisons across every lookup in the table.
        total = sum(table.get(name)[1] for name in names)
        avg = total / len(names)
        print(f"{label}: load factor {table.load_factor():.2f}, "
              f"longest chain {table.longest_chain()}, "
              f"average lookup {avg:.1f} comparisons")

    # With 8 buckets and 40 names, each chain holds about 5 entries, so a
    # lookup walks a short list instead of jumping straight to the value.
    # Python's dict avoids this by growing its table once it's about 2/3
    # full, which keeps lookups close to O(1).

    # A key that collides but isn't stored still costs a full chain walk.
    table = ChainedHashTable(num_buckets=8)
    for name in raid:
        table.put(name, "signed up")
    value, steps = table.get("illidan")
    print(f"Lookup for 'illidan' (not signed up): {value}, "
          f"checked {steps} entries in its bucket")


def main():
    print("=== UNIT 6: DICTIONARIES AS HASH TABLES ===")

    # ===============================
    # TODO (Student): CREATE A HASH TABLE
    # ===============================
    #
    # Requirements:
    # 1. Create an empty dictionary.
    # 2. Add at least 5 key-value pairs.
    # 3. Add comments explaining how a dictionary
    #    behaves like a hash table.
    # 4. Display the contents of the dictionary.


    print("\n=== INSERT OPERATIONS ===")

    # A dict is a hash table. Python runs each key through hash(), turns
    # the result into a slot number, and stores the value in that slot.
    # Finding it later repeats the same math, so no other entries are checked.
    roster = {}
    members = [
        ("Thrall", "Shaman", "Guild Master"),
        ("Jaina", "Mage", "Officer"),
        ("Anduin", "Priest", "Raider"),
        ("Sylvanas", "Hunter", "Raider"),
        ("Valeera", "Rogue", "Member"),
        ("Illidan", "Demon Hunter", "Initiate"),
    ]
    for name, wow_class, rank in members:
        # Keys are lowercase so lookups don't depend on how a name is typed.
        roster[key_for(name)] = {"class": wow_class, "rank": rank}

    print(f"Added {len(roster)} members:")
    show_roster(roster)

    # ===============================
    # TODO (Student): LOOKUP OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Retrieve at least two existing keys.
    # 2. Clearly display the lookup results.
    # 3. Add meaningful comments to explain how the lookup works.

    print("\n=== LOOKUP OPERATIONS ===")

    # roster[key] hashes the key, goes straight to its slot, and confirms
    # the stored key matches. That's O(1) on average, whether the guild
    # has 6 members or 1,000.
    for name in ["Jaina", "SYLVANAS"]:
        info = roster[key_for(name)]
        print(f"Lookup '{name}': {info['class']}, rank {info['rank']}")

    # "SYLVANAS" still worked because the key was lowercased first.

    # ===============================
    # TODO (Student): UPDATE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Update the value associated with an existing key.
    # 2. Display the dictionary before and after the update.
    # 3. Use comments to explain what happens when an existing key is assigned
    #    a new value.

    print("\n=== UPDATE OPERATIONS ===")

    print("Before Illidan's promotion:")
    show_roster(roster)

    # The key already exists, so the dict finds the same slot and replaces
    # the value. No new entry is created, and the size stays the same.
    update_member(roster, "Illidan", "rank", "Raider")

    print("After promoting Illidan to Raider:")
    show_roster(roster)
    print(f"Roster size is still {len(roster)}")

    # ===============================
    # TODO (Student): DELETE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Delete at least one key-value pair.
    # 2. Display the dictionary before and after deletion.
    # 3. Use comments to explain what happens when a key is removed.

    print("\n=== DELETE OPERATIONS ===")

    print("Before Valeera leaves the guild:")
    show_roster(roster)

    # del hashes the key, finds its slot, and removes the entry. The other
    # members stay in their own slots, so nothing has to shift like it
    # would in a list.
    del roster[key_for("Valeera")]

    print("After Valeera left:")
    show_roster(roster)
    print(f"'valeera' still in roster? {'valeera' in roster}")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Lookup a missing key
    # - Delete a missing key safely
    # - Update a missing key
    # - Use an empty dictionary
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASES ===")

    # 1. Missing key: roster["arthas"] would raise KeyError. get() returns
    #    a default instead.
    print(f"1. Lookup 'Arthas': {roster.get(key_for('Arthas'), 'not in guild')}")

    # 2. Deleting a missing key: del would raise KeyError. pop() with a
    #    default removes the key if it's there and does nothing otherwise.
    print(f"2. Remove 'Arthas': {roster.pop(key_for('Arthas'), None)} "
          f"(size still {len(roster)})")

    # 3. Updating a missing key: roster["arthsa"] = ... would add a new
    #    member from a typo. update_member() checks first.
    print(f"3. Update rank for typo 'Arthsa': "
          f"{update_member(roster, 'Arthsa', 'rank', 'Officer')} "
          f"(size still {len(roster)})")

    # 4. Duplicate name with different casing: "THRALL" maps to the same key
    #    as "Thrall", so it replaces the existing entry instead of adding one.
    roster[key_for("THRALL")] = {"class": "Shaman", "rank": "Guild Master"}
    print(f"4. Insert 'THRALL' again: size still {len(roster)}")

    # 5. Empty dictionary: lookups and deletes are safe with get() and pop().
    empty = {}
    print(f"5. Empty roster: get -> {empty.get('jaina')}, "
          f"pop -> {empty.pop('jaina', None)}, size {len(empty)}")

    # 6. Unhashable key: a list can change after it's stored, so its hash
    #    could change too. Python refuses it as a key. A tuple can't
    #    change, so the same names work as a tuple key.
    parties = {}
    print(f"6. List as a key: {try_insert(parties, ['thrall', 'jaina'], 'party')}. "
          f"Tuple as a key: {try_insert(parties, ('thrall', 'jaina'), 'party')}")

    demonstrate_collisions()


if __name__ == "__main__":
    main()
