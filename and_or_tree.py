from __future__ import annotations
from typing import *
from collections import deque

T = TypeVar('T')


def any_none(ls: Iterable[Optional[bool]]) -> Optional[bool]:
    """Returns true if any of inputs are true, and none if any are none"""
    for x in ls:
        if x is None:
            return None
        if x:
            return True
    return False


def all_none(ls: Iterable[Optional[bool]]) -> Optional[bool]:
    """Returns true if all values are true, none if any are none"""
    for x in ls:
        if x is None:
            return None
        if not x:
            return False
    return True


class Node(Generic[T]):
    value: T
    parent: Optional[Node[T]]
    children: Optional[List[Node[T]]] = None
    result: Optional[bool] = None
    invalid: bool = False
    is_and: bool

    def __init__(self, value: T, parent: Optional[Node[T]], is_and: bool):
        self.value = value
        self.parent = parent
        self.is_and = is_and

    def refresh_result(self) -> Optional[T]:
        if self.children is None:
            return None
        unk = False
        for child in self.children:
            v = child.refresh_result()
            if v is None:
                unk = True
            if v is not None and self.is_and != v:
                return v
        return None if unk else self.is_and

    def update(self):
        self.result = self.refresh_result()
        if self.result is not None:
            self.set_invalid()
            if self.parent is not None:
                self.parent.update()

    def set_invalid(self):
        self.invalid = True
        if self.children is not None:
            for child in self.children:
                child.set_invalid()

    def to_string(self, depth=0) -> List[str]:
        res = [f'{" " * depth}{"And" if self.is_and else "Or"} Node {self.value} with '
               f'{"?" if self.children is None else len(self.children)} child(ren);'
               f'invalid {self.invalid}; result {self.result}']
        if self.children is not None:
            for child in self.children:
                res.extend(child.to_string(depth + 1))
        return res

    def __str__(self):
        return "\n".join(self.to_string())


class Tree(Generic[T]):
    root: Node[T]
    expand_and: Callable[[T], List[T]]
    expand_or: Callable[[T], List[T]]

    def __init__(self, start: T, expand_and: Callable[[T], List[T]], expand_or: Callable[[T], List[T]]):
        self.root = Node(start, None, True)
        self.expand_and = expand_and
        self.expand_or = expand_or

    def search(self, debug=False) -> bool:
        # Invariants: contains all nodes whose children is None;
        # A node's result is None if it cannot be determined by the result of children
        # and a value otherwise
        stack = deque([self.root])
        iters = 0
        while self.root.result is None:
            iters += 1
            # if iters > 30:
            #     raise Exception("Took too long")
            node = stack.popleft()
            if node.invalid:
                continue

            new_vals = [Node(v, node, not node.is_and) for v in (self.expand_and if node.is_and else self.expand_or)(node.value)]
            node.children = new_vals
            stack.extend(new_vals)
            node.update()
            if debug:
                print(self.root, "\n\n")
        return self.root.result




