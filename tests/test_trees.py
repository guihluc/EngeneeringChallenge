import itertools
import math
import random
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
        if node.left is not tree.nil:
            assert node.left.parent is node
        if node.right is not tree.nil:
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


TREES = (
    (AVLTree, check_avl),
    (RedBlackTree, check_red_black),
)


def kids(tree, key):
    node = tree.search(key)
    empty = getattr(tree, "nil", None)
    return (node.left is not empty) + (node.right is not empty)


def height(tree, node):
    if node is getattr(tree, "nil", None):
        return 0
    return 1 + max(height(tree, node.left), height(tree, node.right))


def fill(tree, check, keys):
    for key in keys:
        assert tree.insert(key)
        check(tree)


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
                self.assertEqual(tree.in_order(), [])
                self.assertEqual(tree.show(), "(árvore vazia)")
                self.assertTrue(tree.insert(10))
                self.assertTrue(tree.insert(5))
                self.assertTrue(tree.insert(15))
                self.assertFalse(tree.insert(10))
                self.assertIsNotNone(tree.search(5))
                self.assertIsNone(tree.search(7))
                self.assertFalse(tree.remove(7))
                self.assertEqual(check(tree), [5, 10, 15])
                self.assertEqual(tree.in_order(), [5, 10, 15])
                view = tree.show()
                self.assertIn("Raiz: 10", view)
                self.assertIn("  Esquerda: 5", view)
                self.assertIn("  Direita: 15", view)
                if tree_type is RedBlackTree:
                    self.assertIn("(BLACK)", view)
                    self.assertIn("(RED)", view)
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


class ScenarioTests(unittest.TestCase):
    def test_ascending_insertion(self):
        keys = list(range(1, 101))
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                self.assertEqual(tree.in_order(), keys)

    def test_descending_insertion(self):
        keys = list(range(100, 0, -1))
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                self.assertEqual(tree.in_order(), sorted(keys))

    def test_unordered_insertion(self):
        keys = random.Random(7).sample(range(1000), 200)
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                self.assertEqual(tree.in_order(), sorted(keys))

    def test_search_existing_and_missing(self):
        keys = list(range(0, 100, 2))
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                for key in keys:
                    self.assertEqual(tree.search(key).key, key)
                for key in (-5, 1, 51, 99, 100, 500):
                    self.assertIsNone(tree.search(key))

    def test_remove_by_number_of_children(self):
        full = [10, 5, 15, 3, 7, 12, 20]
        cases = (
            (full, 3, 0),
            (full, 20, 0),
            (full, 5, 2),
            (full, 10, 2),
            ([10, 5, 15, 3], 5, 1),
            ([10, 5, 15, 12], 15, 1),
            ([10, 5], 10, 1),
            ([10], 10, 0),
        )
        for tree_type, check in TREES:
            for keys, key, count in cases:
                with self.subTest(tree=tree_type.__name__, key=key, kids=count):
                    tree = tree_type()
                    fill(tree, check, keys)
                    self.assertEqual(kids(tree, key), count)
                    self.assertTrue(tree.remove(key))
                    self.assertIsNone(tree.search(key))
                    expected = sorted(k for k in keys if k != key)
                    self.assertEqual(check(tree), expected)
                    self.assertEqual(tree.in_order(), expected)

    def test_remove_missing(self):
        keys = [10, 5, 15, 3, 7]
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                self.assertFalse(tree.remove(99))
                self.assertFalse(tree.remove(-1))
                self.assertEqual(check(tree), sorted(keys))
                self.assertTrue(tree.remove(7))
                self.assertFalse(tree.remove(7))
                self.assertEqual(check(tree), [3, 5, 10, 15])

    def test_empty_tree(self):
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                self.assertIsNone(tree.search(1))
                self.assertFalse(tree.remove(1))
                self.assertEqual(tree.in_order(), [])
                self.assertEqual(tree.show(), "(árvore vazia)")
                self.assertEqual(check(tree), [])

    def test_single_element(self):
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                self.assertTrue(tree.insert(1))
                self.assertFalse(tree.insert(1))
                self.assertEqual(tree.search(1).key, 1)
                self.assertIsNone(tree.search(2))
                self.assertFalse(tree.remove(2))
                self.assertEqual(check(tree), [1])
                self.assertIn("Raiz: 1", tree.show())
                self.assertTrue(tree.remove(1))
                self.assertEqual(check(tree), [])
                self.assertTrue(tree.insert(2))
                self.assertEqual(check(tree), [2])

    def test_balance_after_insertions_and_removals(self):
        rnd = random.Random(3)
        keys = rnd.sample(range(1000), 300)
        removed = rnd.sample(keys, 150)
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                fill(tree, check, keys)
                left = set(keys)
                for key in removed:
                    self.assertTrue(tree.remove(key))
                    left.remove(key)
                    self.assertEqual(check(tree), sorted(left))

    def test_height_stays_small(self):
        n = 1000
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                for key in range(1, n + 1):
                    tree.insert(key)
                check(tree)
                self.assertLessEqual(height(tree, tree.root), 2 * math.log2(n + 1))

    def test_same_operations_on_both_trees(self):
        rnd = random.Random(5)
        ops = [(rnd.choice("ir"), rnd.randrange(60)) for _ in range(600)]
        for tree_type, check in TREES:
            with self.subTest(tree=tree_type.__name__):
                tree = tree_type()
                model = set()
                for op, key in ops:
                    if op == "i":
                        self.assertEqual(tree.insert(key), key not in model)
                        model.add(key)
                    else:
                        self.assertEqual(tree.remove(key), key in model)
                        model.discard(key)
                    self.assertEqual(check(tree), sorted(model))
                self.assertEqual(tree.in_order(), sorted(model))


class MainProgramTests(unittest.TestCase):
    def test_choose_tree(self):
        with patch("builtins.input", side_effect=["opção inválida", "1"]):
            self.assertIsInstance(choose_tree(), AVLTree)

        with patch("builtins.input", side_effect=["2"]):
            self.assertIsInstance(choose_tree(), RedBlackTree)

    def test_run_operations(self):
        choices = ["1", "1", "8", "2", "8", "4", "5", "3", "8", "0"]
        output = StringIO()
        with patch("builtins.input", side_effect=choices), redirect_stdout(output):
            run()

        self.assertIn("Árvore AVL selecionada.", output.getvalue())
        self.assertIn("8 foi inserido.", output.getvalue())
        self.assertIn("8 foi encontrado.", output.getvalue())
        self.assertIn("Elementos em ordem crescente: 8", output.getvalue())
        self.assertIn("Raiz: 8", output.getvalue())
        self.assertIn("8 foi removido.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
