from avl import AVLTree
from red_black import RedBlackTree


def choose_tree() -> AVLTree | RedBlackTree:
    while True:
        print("Escolha a árvore:")
        print("1 - AVL")
        print("2 - Rubro-Negra")
        choice = input("Opção: ").strip()

        if choice == "1":
            print("\nÁrvore AVL selecionada.\n")
            return AVLTree()
        if choice == "2":
            print("\nÁrvore Rubro-Negra selecionada.\n")
            return RedBlackTree()

        print("Opção inválida. Escolha 1 ou 2.\n")


def read_key() -> int:
    while True:
        value = input("Valor: ").strip()
        try:
            return int(value)
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def run() -> None:
    tree = choose_tree()

    while True:
        print("1 - Inserir elemento")
        print("2 - Buscar elemento")
        print("3 - Remover elemento")
        print("4 - Exibir elementos em ordem crescente")
        print("5 - Mostrar estrutura da árvore")
        print("0 - Sair")
        choice = input("Opção: ").strip()

        if choice == "1":
            key = read_key()
            if tree.insert(key):
                print(f"{key} foi inserido.\n")
            else:
                print(f"{key} já existe na árvore.\n")
        elif choice == "2":
            key = read_key()
            if tree.search(key) is not None:
                print(f"{key} foi encontrado.\n")
            else:
                print(f"{key} não foi encontrado.\n")
        elif choice == "3":
            key = read_key()
            if tree.remove(key):
                print(f"{key} foi removido.\n")
            else:
                print(f"{key} não existe na árvore.\n")
        elif choice == "4":
            keys = tree.in_order()
            if keys:
                print(f"Elementos em ordem crescente: {', '.join(map(str, keys))}\n")
            else:
                print("A árvore está vazia.\n")
        elif choice == "5":
            print(tree.show(), end="\n\n")
        elif choice == "0":
            print("Programa encerrado.")
            return
        else:
            print("Opção inválida. Escolha uma das opções do menu.\n")


if __name__ == "__main__":
    run()
