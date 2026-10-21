import random

from avl import AVLTree
from red_black import RedBlackTree


def datasets(n):
    rnd = random.Random(42)
    return {
        "Crescente": list(range(1, n + 1)),
        "Decrescente": list(range(n, 0, -1)),
        "Aleatório": rnd.sample(range(n * 10), n),
    }


def run(tree, keys, removes):
    for k in keys:
        tree.insert(k)
    h_ins = tree.height()
    r_ins = tree.rotations
    for k in removes:
        tree.remove(k)
    return h_ins, r_ins, tree.height(), tree.rotations


def compare(n=1000):
    rows = []
    for name, keys in datasets(n).items():
        removes = random.Random(1).sample(keys, n // 2)
        for label, tree in (("AVL", AVLTree()), ("Rubro-Negra", RedBlackTree())):
            h_ins, r_ins, h_rem, r_tot = run(tree, keys, removes)
            recolors = getattr(tree, "recolors", "-")
            rows.append((name, label, h_ins, r_ins, h_rem, r_tot - r_ins, recolors))
    return rows


def main():
    n = 1000
    print(f"Comparação com {n} elementos (depois remove {n // 2})\n")
    head = ("Dados", "Árvore", "Altura", "Rotações", "Altura pós-rem.", "Rotações pós-rem", "Recolor.")
    rows = [tuple(str(c) for c in r) for r in compare(n)]
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(head)]

    def line(cells):
        parts = []
        for i, c in enumerate(cells):
            parts.append(c.ljust(widths[i]) if i < 2 else c.rjust(widths[i]))
        return " | ".join(parts)

    print(line(head))
    print("-+-".join("-" * w for w in widths))
    for i, r in enumerate(rows):
        if i > 0 and i % 2 == 0:
            print("-+-".join("-" * w for w in widths))
        print(line(r))


if __name__ == "__main__":
    main()
