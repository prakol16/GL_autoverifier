from __future__ import annotations
from typing import *
from collections import deque
import heapq

T = TypeVar('T')

depth_penalty = 2


class Node(Generic[T]):
    value: T
    parent: Optional[Node[T]]
    children: Optional[List[Node[T]]] = None
    result: Optional[bool] = None
    invalid: bool = False
    is_and: bool
    depth: int

    def __init__(self, value: T, parent: Optional[Node[T]], is_and: bool):
        self.value = value
        self.parent = parent
        self.is_and = is_and
        self.depth = 0 if parent is None else parent.depth + 1

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

    def __init__(self, start: T, expand_and: Callable[[T], List[T]],
                                 expand_or: Callable[[T], List[T]]):
        self.root = Node(start, None, True)
        self.expand_and = expand_and
        self.expand_or = expand_or

    def local_depth_first(self, root: Node, max_iters=40):
        stack: List[Node] = [root]
        extra_stack: List[Node] = []
        iters = 0
        while root.result is None and iters < max_iters and stack:
            node = stack.pop()
            if node.invalid:
                continue
            new_vals = [Node(v, node, not node.is_and) for v in (self.expand_and if node.is_and else self.expand_or)(node.value)]
            node.children = new_vals
            node.update()

            iters += 1
            if node.is_and != root.is_and and len(new_vals) > 1:
                extra_stack.extend(new_vals)
            else:
                stack.extend(new_vals)
        return (stack + extra_stack) if root.result is None else []

    def search(self, debug=False) -> bool:
        # Invariants: contains all nodes whose children is None;
        # A node's result is None if it cannot be determined by the result of children
        # and a value otherwise

        stack = deque([self.root])
        # stack = [self.root]
        while self.root.result is None:
            # node = heapq.heappop(stack)
            node = stack.popleft()
            if node.invalid:
                continue
            stack.extend(self.local_depth_first(node))

            # new_vals = [Node(v, node, not node.is_and) for v in (self.expand_and if node.is_and else self.expand_or)(node.value)]
            # node.children = new_vals
            # stack.extend(new_vals)
            # node.update()
            if debug:
                print(self.root, "\n\n")
        return self.root.result




