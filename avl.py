from __future__ import annotations


class Node:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1


class AVLTree:
    def __init__(self) -> None:
        self.root: Node | None = None
        self.rotations = 0

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Node | None) -> int:
        if node is None:
            return 0
        return node.height

    def _update(self, node: Node) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance(self, node: Node) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, node: Node) -> Node:
        child = node.left
        if child is None:
            return node
        self.rotations += 1
        node.left = child.right
        child.right = node
        self._update(node)
        self._update(child)
        return child

    def _rotate_left(self, node: Node) -> Node:
        child = node.right
        if child is None:
            return node
        self.rotations += 1
        node.right = child.left
        child.left = node
        self._update(node)
        self._update(child)
        return child

    def _rebalance(self, node: Node) -> Node:
        self._update(node)
        balance = self._balance(node)

        if balance > 1:
            if node.left is not None and self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if node.right is not None and self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key: int) -> bool:
        self.root, inserted = self._insert(self.root, key)
        return inserted

    def _insert(self, node: Node | None, key: int) -> tuple[Node, bool]:
        if node is None:
            return Node(key), True

        if key == node.key:
            return node, False
        if key < node.key:
            node.left, inserted = self._insert(node.left, key)
        else:
            node.right, inserted = self._insert(node.right, key)

        if inserted:
            node = self._rebalance(node)
        return node, inserted

    def search(self, key: int) -> Node | None:
        node = self.root
        while node is not None:
            if key == node.key:
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def in_order(self) -> list[int]:
        keys: list[int] = []

        def visit(node: Node | None) -> None:
            if node is None:
                return
            visit(node.left)
            keys.append(node.key)
            visit(node.right)

        visit(self.root)
        return keys

    def show(self) -> str:
        if self.root is None:
            return "(árvore vazia)"

        lines: list[str] = []

        def visit(node: Node | None, depth: int, side: str) -> None:
            if node is None:
                return
            lines.append(f"{'  ' * depth}{side}: {node.key}")
            visit(node.left, depth + 1, "Esquerda")
            visit(node.right, depth + 1, "Direita")

        visit(self.root, 0, "Raiz")
        return "\n".join(lines)

    def remove(self, key: int) -> bool:
        self.root, removed = self._remove(self.root, key)
        return removed

    def _remove(self, node: Node | None, key: int) -> tuple[Node | None, bool]:
        if node is None:
            return None, False

        if key < node.key:
            node.left, removed = self._remove(node.left, key)
        elif key > node.key:
            node.right, removed = self._remove(node.right, key)
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.right, _ = self._remove(node.right, successor.key)
            removed = True

        if removed:
            node = self._rebalance(node)
        return node, removed
