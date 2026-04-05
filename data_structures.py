"""
data_structures.py

Implements the following elementary data structures from scratch in Python:

  1. DynamicArray  -- array with insertion, deletion, and access
  2. Stack         -- LIFO structure backed by a dynamic array
  3. Queue         -- FIFO structure backed by a dynamic array
  4. SinglyLinkedList -- singly linked list with insert, delete, traversal
  5. RootedTree    -- general rooted tree using linked list node representation

Usage:
    python data_structures.py

Reference:
    Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
    Introduction to algorithms (4th ed.). Random House Publishing Services.
"""


# ---------------------------------------------------------------------------
# 1. Dynamic Array
# ---------------------------------------------------------------------------

class DynamicArray:
    """
    A resizable array supporting insertion, deletion, and O(1) access.

    Internally uses a fixed-size Python list that doubles when capacity
    is exceeded and halves when the array is less than one-quarter full.
    This amortizes the cost of resizing to O(1) per operation.

    Operations
    ----------
    access(index)      : O(1)
    insert_at(i, val)  : O(n) -- shifts elements to make room
    append(val)        : O(1) amortized
    delete_at(i)       : O(n) -- shifts elements to fill gap
    __len__()          : O(1)
    """

    def __init__(self):
        self._capacity = 4
        self._size     = 0
        self._data     = [None] * self._capacity

    def access(self, index):
        """
        Return the element at the given index.
        Time complexity: O(1)
        """
        self._check_index(index)
        return self._data[index]

    def append(self, value):
        """
        Append a value to the end of the array.
        Time complexity: O(1) amortized
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert_at(self, index, value):
        """
        Insert value at the given index, shifting subsequent elements right.
        Time complexity: O(n)
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range.")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete_at(self, index):
        """
        Remove and return the element at the given index, shifting subsequent
        elements left.
        Time complexity: O(n)
        """
        self._check_index(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data     = new_data
        self._capacity = new_capacity

    def _check_index(self, index):
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range.")

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"DynamicArray({[self._data[i] for i in range(self._size)]})"


# ---------------------------------------------------------------------------
# 2. Stack
# ---------------------------------------------------------------------------

class Stack:
    """
    Last-In, First-Out (LIFO) stack backed by a DynamicArray.

    Using an array for the stack is natural because push and pop both
    operate on the same end (the top), giving O(1) amortized time for
    both operations without any pointer overhead.

    Operations
    ----------
    push(value)  : O(1) amortized
    pop()        : O(1) amortized
    peek()       : O(1)
    is_empty()   : O(1)
    """

    def __init__(self):
        self._data = DynamicArray()

    def push(self, value):
        """Push a value onto the top of the stack. Time: O(1) amortized."""
        self._data.append(value)

    def pop(self):
        """
        Remove and return the top element.
        Time: O(1) amortized
        Raises ValueError if the stack is empty.
        """
        if self.is_empty():
            raise ValueError("Stack underflow: cannot pop from an empty stack.")
        return self._data.delete_at(len(self._data) - 1)

    def peek(self):
        """Return the top element without removing it. Time: O(1)."""
        if self.is_empty():
            raise ValueError("Stack is empty.")
        return self._data.access(len(self._data) - 1)

    def is_empty(self):
        """Return True if the stack contains no elements. Time: O(1)."""
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack(top -> {self._data})"


# ---------------------------------------------------------------------------
# 3. Queue
# ---------------------------------------------------------------------------

class Queue:
    """
    First-In, First-Out (FIFO) queue backed by a Python list used as a
    circular buffer to avoid O(n) dequeue cost.

    A naive array queue that always dequeues from index 0 would require
    shifting all remaining elements, giving O(n) dequeue time. The
    circular buffer approach uses head and tail pointers so that both
    enqueue and dequeue are O(1) amortized.

    Operations
    ----------
    enqueue(value)  : O(1) amortized
    dequeue()       : O(1) amortized
    peek()          : O(1)
    is_empty()      : O(1)
    """

    def __init__(self):
        self._capacity = 4
        self._data     = [None] * self._capacity
        self._head     = 0
        self._size     = 0

    def enqueue(self, value):
        """Add a value to the back of the queue. Time: O(1) amortized."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        tail = (self._head + self._size) % self._capacity
        self._data[tail] = value
        self._size += 1

    def dequeue(self):
        """
        Remove and return the front element.
        Time: O(1) amortized
        Raises ValueError if the queue is empty.
        """
        if self.is_empty():
            raise ValueError("Queue underflow: cannot dequeue from an empty queue.")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def peek(self):
        """Return the front element without removing it. Time: O(1)."""
        if self.is_empty():
            raise ValueError("Queue is empty.")
        return self._data[self._head]

    def is_empty(self):
        """Return True if the queue contains no elements. Time: O(1)."""
        return self._size == 0

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data    = new_data
        self._head    = 0
        self._capacity = new_capacity

    def __len__(self):
        return self._size

    def __repr__(self):
        elements = [self._data[(self._head + i) % self._capacity]
                    for i in range(self._size)]
        return f"Queue(front -> {elements})"


# ---------------------------------------------------------------------------
# 4. Singly Linked List
# ---------------------------------------------------------------------------

class _ListNode:
    """A single node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """
    Singly linked list supporting insertion, deletion, and traversal.

    Each node stores data and a pointer to the next node. The list
    maintains head and tail pointers so that both prepend and append
    are O(1).

    Linked lists are preferred over arrays when frequent insertions and
    deletions at arbitrary positions are required, since no shifting is
    needed. The tradeoff is O(n) access time versus O(1) for arrays.

    Operations
    ----------
    prepend(val)       : O(1)
    append(val)        : O(1)
    insert_after(node) : O(1)
    delete(val)        : O(n) -- must find the node first
    search(val)        : O(n)
    traverse()         : O(n)
    __len__()          : O(1)
    """

    def __init__(self):
        self.head  = None
        self.tail  = None
        self._size = 0

    def prepend(self, data):
        """Insert a new node at the front of the list. Time: O(1)."""
        node = _ListNode(data)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def append(self, data):
        """Insert a new node at the end of the list. Time: O(1)."""
        node = _ListNode(data)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def insert_after(self, target_data, new_data):
        """
        Insert new_data immediately after the first node containing
        target_data. Time: O(n) to find the target node.
        Raises ValueError if target_data is not found.
        """
        current = self.head
        while current:
            if current.data == target_data:
                node = _ListNode(new_data)
                node.next = current.next
                current.next = node
                if current == self.tail:
                    self.tail = node
                self._size += 1
                return
            current = current.next
        raise ValueError(f"{target_data} not found in list.")

    def delete(self, data):
        """
        Remove the first node containing data.
        Time: O(n)
        Returns True if deleted, False if not found.
        """
        current  = self.head
        previous = None
        while current:
            if current.data == data:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                if current == self.tail:
                    self.tail = previous
                self._size -= 1
                return True
            previous = current
            current  = current.next
        return False

    def search(self, data):
        """
        Return the first node containing data, or None if not found.
        Time: O(n)
        """
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

    def traverse(self):
        """Yield each element in order from head to tail. Time: O(n)."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        return self._size

    def __repr__(self):
        return " -> ".join(str(x) for x in self.traverse()) + " -> None"


# ---------------------------------------------------------------------------
# 5. Rooted Tree
# ---------------------------------------------------------------------------

class _TreeNode:
    """
    A node in a rooted tree.

    Uses the left-child, right-sibling representation described in
    Cormen et al. (2022): each node stores a pointer to its leftmost
    child and a pointer to its next sibling. This allows a tree of
    arbitrary branching factor to be represented with only two pointers
    per node, using O(n) space total.

    Attributes
    ----------
    data            : any   -- the value stored at this node
    parent          : _TreeNode -- parent node (None for root)
    left_child      : _TreeNode -- first (leftmost) child
    right_sibling   : _TreeNode -- next sibling
    """

    def __init__(self, data):
        self.data          = data
        self.parent        = None
        self.left_child    = None
        self.right_sibling = None


class RootedTree:
    """
    General rooted tree using the left-child, right-sibling representation.

    This structure supports trees of arbitrary branching factor. Adding a
    child to any node is O(1) if the node reference is known. Traversal
    visits every node exactly once in O(n) time.

    Operations
    ----------
    add_child(parent, child_data) : O(1)
    bfs_traversal()               : O(n) -- breadth-first
    dfs_traversal()               : O(n) -- depth-first preorder
    """

    def __init__(self, root_data):
        self.root = _TreeNode(root_data)

    def add_child(self, parent_node, child_data):
        """
        Add a new child node to parent_node.
        The new child becomes the leftmost child of parent_node.
        Time: O(1)
        """
        child = _TreeNode(child_data)
        child.parent = parent_node
        child.right_sibling = parent_node.left_child
        parent_node.left_child = child
        return child

    def bfs_traversal(self):
        """
        Yield nodes in breadth-first (level) order.
        Time: O(n)
        """
        from collections import deque
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            yield node.data
            child = node.left_child
            while child:
                queue.append(child)
                child = child.right_sibling

    def dfs_traversal(self):
        """
        Yield nodes in depth-first preorder.
        Time: O(n)
        """
        yield from self._dfs(self.root)

    def _dfs(self, node):
        if node is None:
            return
        yield node.data
        child = node.left_child
        while child:
            yield from self._dfs(child)
            child = child.right_sibling

    def __repr__(self):
        return f"RootedTree(root={self.root.data})"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo_dynamic_array():
    print("[ DynamicArray ]")
    da = DynamicArray()
    for v in [10, 20, 30, 40]:
        da.append(v)
    print(f"  After appending 10,20,30,40: {da}")
    da.insert_at(1, 15)
    print(f"  After insert_at(1, 15):      {da}")
    deleted = da.delete_at(3)
    print(f"  After delete_at(3) [{deleted}]:   {da}")
    print(f"  access(2) = {da.access(2)}")
    print()


def demo_stack():
    print("[ Stack ]")
    s = Stack()
    for v in [1, 2, 3, 4]:
        s.push(v)
    print(f"  After pushing 1,2,3,4: peek = {s.peek()}, size = {len(s)}")
    print(f"  pop() -> {s.pop()}")
    print(f"  pop() -> {s.pop()}")
    print(f"  peek() -> {s.peek()}, is_empty() -> {s.is_empty()}")
    print()


def demo_queue():
    print("[ Queue ]")
    q = Queue()
    for v in ["a", "b", "c", "d"]:
        q.enqueue(v)
    print(f"  After enqueuing a,b,c,d: peek = {q.peek()}, size = {len(q)}")
    print(f"  dequeue() -> {q.dequeue()}")
    print(f"  dequeue() -> {q.dequeue()}")
    print(f"  peek() -> {q.peek()}, is_empty() -> {q.is_empty()}")
    print()


def demo_linked_list():
    print("[ SinglyLinkedList ]")
    ll = SinglyLinkedList()
    for v in [10, 20, 30, 40]:
        ll.append(v)
    print(f"  After appending 10,20,30,40: {ll}")
    ll.prepend(5)
    print(f"  After prepend(5):            {ll}")
    ll.insert_after(20, 25)
    print(f"  After insert_after(20, 25):  {ll}")
    ll.delete(25)
    print(f"  After delete(25):            {ll}")
    print(f"  search(30): found = {ll.search(30) is not None}")
    print(f"  search(99): found = {ll.search(99) is not None}")
    print()


def demo_rooted_tree():
    print("[ RootedTree ]")
    tree = RootedTree("A")
    b = tree.add_child(tree.root, "B")
    c = tree.add_child(tree.root, "C")
    d = tree.add_child(tree.root, "D")
    tree.add_child(b, "E")
    tree.add_child(b, "F")
    tree.add_child(c, "G")

    print(f"  BFS order: {list(tree.bfs_traversal())}")
    print(f"  DFS order: {list(tree.dfs_traversal())}")
    print()


if __name__ == "__main__":
    print("=" * 55)
    print("  Elementary Data Structures — Demo")
    print("=" * 55)
    print()
    demo_dynamic_array()
    demo_stack()
    demo_queue()
    demo_linked_list()
    demo_rooted_tree()
    print("All demos complete.")
