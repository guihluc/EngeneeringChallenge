import itertools
from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from avl import AVLTree
from main import choose_tree, run
from red_black import RedBlackTree


def check_avl(tree: AVLTree) -> list[int]:
    def visit(node, low, high):
        if node is None:
            return 0, []

        if low is not None:
            assert low < node.key
        if high is not None:
            assert node.key < high

        left_height, left_keys = visit(node.left, low, node.key)
        right_height, right_keys = visit(node.right, node.key, high)
        height = 1 + max(left_height, right_height)

        assert abs(left_height - right_height) <= 1
        assert node.height == height
        return height, left_keys + [node.key] + right_keys

    return visit(tree.root, None, None)[1]


def check_red_black(tree: RedBlackTree) -> list[int]:
    assert tree.root.color == "black"
    if tree.root is not tree.nil:
        assert tree.root.parent is tree.nil

    def visit(node, low, high):
        if node is tree.nil:
            return 1, []

        if low is not None:
            assert low < node.key
        if high is not None:
            assert node.key < high
        assert node.left.parent is node
        assert node.right.parent is node

        if node.color == "red":
            assert node.left.color == "black"
            assert node.right.color == "black"

        left_height, left_keys = visit(node.left, low, node.key)
        right_height, right_keys = visit(node.right, node.key, high)
        assert left_height == right_height
        return (
            left_height + (node.color == "black"),
            left_keys + [node.key] + right_keys,
        )

    return visit(tree.root, None, None)[1]


class TreeOperationsTests(unittest.TestCase):
    def test_insert_search_and_remove(self):
        for tree_type, check in (
            (AVLTree, check_avl),
            (RedBlackTree, check_red_black),
        ):
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                self.assertFalse(tree.remove(10))
                self.assertIsNone(tree.search(10))
                self.assertTrue(tree.insert(10))
                self.assertTrue(tree.insert(5))
                self.assertTrue(tree.insert(15))
                self.assertFalse(tree.insert(10))
                self.assertIsNotNone(tree.search(5))
                self.assertIsNone(tree.search(7))
                self.assertFalse(tree.remove(7))
                self.assertEqual(check(tree), [5, 10, 15])
                self.assertTrue(tree.remove(10))
                self.assertIsNone(tree.search(10))
                self.assertEqual(check(tree), [5, 15])
                self.assertTrue(tree.remove(5))
                self.assertTrue(tree.remove(15))
                self.assertEqual(check(tree), [])

    def test_all_small_insertion_orders_and_removals(self):
        values = [1, 2, 3, 4, 5]
        for order in itertools.permutations(values):
            for tree_type, check in (
                (AVLTree, check_avl),
                (RedBlackTree, check_red_black),
            ):
                with self.subTest(tree=tree_type.__name__, order=order):
                    tree = tree_type()
                    for key in order:
                        self.assertTrue(tree.insert(key))
                        self.assertEqual(
                            check(tree), sorted(order[: order.index(key) + 1])
                        )

                    for key in reversed(order):
                        self.assertTrue(tree.remove(key))
                        self.assertNotIn(key, check(tree))

                    self.assertEqual(check(tree), [])

    def test_negative_and_zero_keys(self):
        for tree_type, check in (
            (AVLTree, check_avl),
            (RedBlackTree, check_red_black),
        ):
            tree = tree_type()
            for key in (0, -4, 9, -1):
                self.assertTrue(tree.insert(key))
            self.assertEqual(check(tree), [-4, -1, 0, 9])
            self.assertIsNotNone(tree.search(0))
            self.assertTrue(tree.remove(0))
            self.assertEqual(check(tree), [-4, -1, 9])


class MainProgramTests(unittest.TestCase):
    def test_choose_tree(self):
        with patch("builtins.input", side_effect=["opção inválida", "1"]):
            self.assertIsInstance(choose_tree(), AVLTree)

        with patch("builtins.input", side_effect=["2"]):
            self.assertIsInstance(choose_tree(), RedBlackTree)

    def test_run_operations(self):
        choices = ["1", "1", "8", "2", "8", "3", "8", "0"]
        output = StringIO()
        with patch("builtins.input", side_effect=choices), redirect_stdout(output):
            run()

        self.assertIn("Árvore AVL selecionada.", output.getvalue())
        self.assertIn("8 foi inserido.", output.getvalue())
        self.assertIn("8 foi encontrado.", output.getvalue())
        self.assertIn("8 foi removido.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
