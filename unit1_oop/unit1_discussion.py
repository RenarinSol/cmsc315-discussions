"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.

Application scenario: a small homelab inventory. A Device is anything on the
network; a Server is a Device that also runs services on specific ports.
"""


from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.
#
# Replace the pass statement with your implementation.

class Device:
    """Parent class: a generic device on a network."""

    # Class variable: shared by every Device (and every subclass instance)
    network_name = "homelab"

    def __init__(self, hostname: str, ip_address: str):
        # input validation so empty values print a fail
        if not hostname.strip():
            raise ValueError("hostname cannot be empty")
        if not ip_address.strip():
            raise ValueError("ip_address cannot be empty")

        # Instance variables: unique to each object
        self.hostname = hostname
        self.ip_address = ip_address

    def describe(self) -> str:
        """Return a one-line summary of the device."""
        return f"{self.hostname} ({self.ip_address}) on network '{self.network_name}'"

    # Student extension: special method for a developer-friendly representation
    def __repr__(self) -> str:
        return f"{type(self).__name__}(hostname={self.hostname!r}, ip_address={self.ip_address!r})"


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class Server(Device):
    """Child class: a Device that runs network services."""

    # New class variables
    device_type = "server"
    max_services = 10

    def __init__(self, hostname: str, ip_address: str, os_name: str):
        # Reuse the parent's constructor for hostname and ip_address
        super().__init__(hostname, ip_address)

        # New instance variables
        self.os_name = os_name
        # Created inside __init__ so each Server gets its own list
        # (a mutable default argument would be shared across instances)
        self.services = []

    def add_service(self, name: str, port: int) -> None:
        """Register a service. Each service is a dict, so the list holds nested mutable data."""
        if not name.strip():
            raise ValueError("service name cannot be empty")
        if not 1 <= port <= 65535:
            raise ValueError(f"port {port} is outside the valid range 1-65535")
        if any(svc["port"] == port for svc in self.services):
            raise ValueError(f"port {port} is already in use on {self.hostname}")
        if len(self.services) >= self.max_services:
            raise ValueError(f"{self.hostname} already has the maximum of {self.max_services} services")

        self.services.append({"name": name, "port": port})

    def describe(self) -> str:
        """Override: extend the parent's summary with server-specific details."""
        base = super().describe()
        if self.services:
            svc_list = ", ".join(f"{s['name']}:{s['port']}" for s in self.services)
        else:
            svc_list = "none"
        return f"{base} | {self.device_type}, {self.os_name} | services: {svc_list}"

    # Student extension: len(server) returns the number of services
    def __len__(self) -> int:
        return len(self.services)


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")

    web = Server("web01", "10.0.0.10", "Ubuntu 24.04")
    db = Server("db01", "10.0.0.20", "Debian 12")

    # Same class variable, accessed two ways
    print(f"Server.device_type -> {Server.device_type}")
    print(f"web.device_type    -> {web.device_type}")

    # Add an attribute to only one object after creation

    # The IDE warns about this because rack_location isn't defined in the class.
    # That's intentional. todo3 asks for an attribute added after the object exists.
    # noinspection PyUnresolvedReferences
    web.rack_location = "Rack A, U3"

    # Each object's own namespace: only instance variables live here
    print(f"\nweb.__dict__ -> {web.__dict__}")
    print(f"db.__dict__  -> {db.__dict__}")
    print(f"'rack_location' in db.__dict__? {'rack_location' in db.__dict__}")

    # Class namespace: class variables and methods, not instance data
    server_names = [k for k in Server.__dict__ if not k.startswith("__")]
    print(f"\nServer.__dict__ (non-dunder keys) -> {server_names}")
    print(f"'network_name' in Server.__dict__? {'network_name' in Server.__dict__}")
    print(f"But web.network_name still resolves -> {web.network_name}")
    print(f"Lookup order (MRO) -> {[cls.__name__ for cls in Server.__mro__]}")

    # Assigning through an instance creates a NEW instance attribute that shadows
    # the class variable; it does not change the class or other objects
    web.device_type = "vm"
    print(f"\nAfter web.device_type = 'vm':")
    print(f"web.device_type    -> {web.device_type}  (instance attribute)")
    print(f"db.device_type     -> {db.device_type}  (still the class variable)")
    print(f"Server.device_type -> {Server.device_type}")
    print(f"web.__dict__ now   -> {web.__dict__}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")

    original = Server("app01", "10.0.0.30", "Rocky Linux 9")
    original.add_service("nginx", 80)
    original.add_service("ssh", 22)

    # Shallow copy: a new Server object, but its attributes point to the same
    # objects as the original. original.services and shallow.services are one list.
    shallow = copy(original)

    # Deep copy: a new Server object and new copies of everything nested inside it.
    # deep.services is a separate list holding separate dicts.
    deep = deepcopy(original)

    print(f"original.services is shallow.services? {original.services is shallow.services}")
    print(f"original.services is deep.services?    {original.services is deep.services}")

    # Modify the original's nested data in two ways
    original.services[0]["port"] = 8080            # mutate a dict inside the list
    original.services.append({"name": "postgres", "port": 5432})  # mutate the list itself

    # Rebinding a toplevel attribute on the shallow copy doesnt affect the original:
    # it points shallow.hostname at a new string instead of changing a shared object
    shallow.hostname = "app01-copy"

    print("\nAfter modifying original's nested data:")
    print(f"original -> {original.describe()}")
    print(f"shallow  -> {shallow.describe()}")   # sees both changes (shared list)
    print(f"deep     -> {deep.describe()}")      # unchanged (independent list)


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    print("\n--- Parent object ---")
    switch = Device("switch01", "10.0.0.2")
    print(switch.describe())
    print(repr(switch))

    print("\n--- Child object ---")
    nas = Server("nas01", "10.0.0.50", "TrueNAS SCALE")
    print(nas.describe())                 # overridden method, no services yet
    nas.add_service("smb", 445)
    nas.add_service("nfs", 2049)
    print(nas.describe())                 # overridden method calls super().describe()
    print(f"Inherited attribute network_name -> {nas.network_name}")
    print(f"isinstance(nas, Device)? {isinstance(nas, Device)}")
    print(f"Number of services (len) -> {len(nas)}")

    print("\n--- Edge cases ---")
    bad_inputs = [
        ("empty service name", lambda: nas.add_service("", 8000)),
        ("port out of range", lambda: nas.add_service("web", 70000)),
        ("duplicate port", lambda: nas.add_service("samba2", 445)),
        ("empty hostname", lambda: Server("", "10.0.0.99", "Linux")),
        ("whitespace-only IP", lambda: Device("ap01", "   ")),
    ]
    for label, action in bad_inputs:
        try:
            action()
            print(f"{label}: accepted (unexpected)")
        except ValueError as err:
            print(f"{label}: rejected -> {err}")

    # Boundary test: fill a server to exactly max_services, then try one more
    full = Server("full01", "10.0.0.60", "Alpine")
    for i in range(Server.max_services):
        full.add_service(f"svc{i}", 9000 + i)
    print(f"full01 holds {len(full)} services (the limit is {Server.max_services})")
    try:
        full.add_service("one-too-many", 9999)
        print("over limit: accepted (unexpected)")
    except ValueError as err:
        print(f"over limit: rejected -> {err}")

    # Changing the class variable on the parent affects every instance that
    # has not shadowed it, including child-class instances
    Device.network_name = "lab-vlan20"
    print(f"\nAfter Device.network_name = 'lab-vlan20':")
    print(switch.describe())
    print(nas.describe())

    Device.network_name = "homelab"  # reset so the demos start clean

    demonstrate_namespaces()
    demonstrate_copying()


if __name__ == "__main__":
    main()
