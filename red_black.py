from __future__ import annotations


class Node:
    def __init__(self, key: int, color: str) -> None:
        self.key = key
        self.color = color
        self.left: Node
        self.right: Node
        self.parent: Node


class RedBlackTree:
    def __init__(self) -> None:
        self.nil = Node(0, "black")
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        self.root = self.nil

    def search(self, key: int) -> Node | None:
        node = self.root
        while node is not self.nil:
            if key == node.key:
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def in_order(self) -> list[int]:
        keys: list[int] = []

        def visit(node: Node) -> None:
            if node is self.nil:
                return
            visit(node.left)
            keys.append(node.key)
            visit(node.right)

        visit(self.root)
        return keys

    def show(self) -> str:
        if self.root is self.nil:
            return "(árvore vazia)"

        lines: list[str] = []

        def visit(node: Node, depth: int, side: str) -> None:
            if node is self.nil:
                return
            lines.append(
                f"{'  ' * depth}{side}: {node.key} ({node.color.upper()})"
            )
            visit(node.left, depth + 1, "Esquerda")
            visit(node.right, depth + 1, "Direita")

        visit(self.root, 0, "Raiz")
        return "\n".join(lines)

    def insert(self, key: int) -> bool:
        parent = self.nil
        node = self.root

        while node is not self.nil:
            parent = node
            if key == node.key:
                return False
            if key < node.key:
                node = node.left
            else:
                node = node.right

        added = Node(key, "red")
        added.left = self.nil
        added.right = self.nil
        added.parent = parent

        if parent is self.nil:
            self.root = added
        elif key < parent.key:
            parent.left = added
        else:
            parent.right = added

        self._fix_insert(added)
        return True

    def _rotate_left(self, node: Node) -> None:
        child = node.right
        node.right = child.left
        if child.left is not self.nil:
            child.left.parent = node

        child.parent = node.parent
        if node.parent is self.nil:
            self.root = child
        elif node is node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child

        child.left = node
        node.parent = child

    def _rotate_right(self, node: Node) -> None:
        child = node.left
        node.left = child.right
        if child.right is not self.nil:
            child.right.parent = node

        child.parent = node.parent
        if node.parent is self.nil:
            self.root = child
        elif node is node.parent.right:
            node.parent.right = child
        else:
            node.parent.left = child

        child.right = node
        node.parent = child

    def _fix_insert(self, node: Node) -> None:
        while node.parent.color == "red":
            if node.parent is node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "red":
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == "red":
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self._rotate_left(node.parent.parent)

        self.root.color = "black"

    def remove(self, key: int) -> bool:
        target = self.root
        while target is not self.nil and target.key != key:
            if key < target.key:
                target = target.left
            else:
                target = target.right

        if target is self.nil:
            return False

        moved = target
        old_color = moved.color
        if target.left is self.nil:
            child = target.right
            self._transplant(target, target.right)
        elif target.right is self.nil:
            child = target.left
            self._transplant(target, target.left)
        else:
            moved = self._minimum(target.right)
            old_color = moved.color
            child = moved.right
            if moved.parent is target:
                child.parent = moved
            else:
                self._transplant(moved, moved.right)
                moved.right = target.right
                moved.right.parent = moved

            self._transplant(target, moved)
            moved.left = target.left
            moved.left.parent = moved
            moved.color = target.color

        if old_color == "black":
            self._fix_remove(child)
        return True

    def _minimum(self, node: Node) -> Node:
        while node.left is not self.nil:
            node = node.left
        return node

    def _transplant(self, old: Node, new: Node) -> None:
        if old.parent is self.nil:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new
        new.parent = old.parent

    def _fix_remove(self, node: Node) -> None:
        while node is not self.root and node.color == "black":
            if node is node.parent.left:
                sibling = node.parent.right
                if sibling is self.nil:
                    node = node.parent
                    continue
                if sibling.color == "red":
                    sibling.color = "black"
                    node.parent.color = "red"
                    self._rotate_left(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    node = node.parent
                else:
                    if sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self._rotate_right(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = "black"
                    sibling.right.color = "black"
                    self._rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling is self.nil:
                    node = node.parent
                    continue
                if sibling.color == "red":
                    sibling.color = "black"
                    node.parent.color = "red"
                    self._rotate_right(node.parent)
                    sibling = node.parent.left
                if sibling.right.color == "black" and sibling.left.color == "black":
                    sibling.color = "red"
                    node = node.parent
                else:
                    if sibling.left.color == "black":
                        sibling.right.color = "black"
                        sibling.color = "red"
                        self._rotate_left(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = "black"
                    sibling.left.color = "black"
                    self._rotate_right(node.parent)
                    node = self.root

        node.color = "black"
