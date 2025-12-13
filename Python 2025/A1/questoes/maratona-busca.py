"""QUESTÃO 1 — Busca Binária: Contagem de Ocorrências
Dado um vetor ordenado de N inteiros e um valor K,
calcular quantas vezes K aparece no vetor, usando somente
operações de busca binária (O(log N)).

Saída: quantidade de ocorrências de K.
"""

def binary_search_left(arr, x):
    """Encontra a primeira posição >= x"""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def binary_search_right(arr, x):
    """Encontra a primeira posição > x"""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def count_occurrences(arr, k):
    left = binary_search_left(arr, k)
    right = binary_search_right(arr, k)
    return max(0, right - left)


"""QUESTÃO 2 — Primeiro Elemento Maior que X
Dado um vetor ordenado e um valor X,
retornar o menor índice i tal que arr[i] > X.
Se não existir, retornar -1.

Obrigatório: resolver com busca binária.
"""

def first_greater(arr, x):
    lo, hi = 0, len(arr)
    ans = -1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] > x:
            ans = mid
            hi = mid
        else:
            lo = mid + 1
    return ans


"""
QUESTÃO 3 — Construção de BST e Impressão In-Order
Dada uma sequência de inteiros, construir a Árvore Binária
de Busca (BST) e imprimir os elementos em ordem crescente
(in-order).
"""

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def bst_insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    else:
        root.right = bst_insert(root.right, key)
    return root

def bst_inorder(root):
    if root:
        yield from bst_inorder(root.left)
        yield root.key
        yield from bst_inorder(root.right)


"""
QUESTÃO 4 — Altura da BST
Dada uma sequência de inteiros, construir a BST e calcular
sua altura. Altura:
 - árvore vazia → 0
 - apenas raiz → 1
"""

def bst_height(root):
    if root is None:
        return 0
    return 1 + max(bst_height(root.left), bst_height(root.right))


"""
QUESTÃO 5 — BST com Inserção, Busca e Remoção (geral)
Processar Q operações:

 I X  -> inserir X
 R X  -> remover X
 B X  -> buscar X e imprimir "FOUND" ou "NOT FOUND"

A remoção deve tratar os 3 casos:
 1. nó folha
 2. nó com 1 filho
 3. nó com 2 filhos (usar sucessor)

"""

def bst_search(root, key):
    while root:
        if key == root.key:
            return True
        elif key < root.key:
            root = root.left
        else:
            root = root.right
    return False

def bst_min_node(root):
    while root.left:
        root = root.left
    return root

def bst_remove(root, key):
    if root is None:
        return None

    if key < root.key:
        root.left = bst_remove(root.left, key)

    elif key > root.key:
        root.right = bst_remove(root.right, key)

    else:
        # Caso 1: nó folha
        if root.left is None and root.right is None:
            return None
        
        # Caso 2: 1 filho
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        
        # Caso 3: 2 filhos — usa sucessor
        succ = bst_min_node(root.right)
        root.key = succ.key
        root.right = bst_remove(root.right, succ.key)

    return root
