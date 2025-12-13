#Árvore binária
class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.leftNode = None
        self.rightNode = None
        self.parentNode = None

    # GETTERS
    def get_key(self): return self.key
    def get_data(self): return self.data
    def get_left(self): return self.leftNode
    def get_right(self): return self.rightNode
    def get_parent(self): return self.parentNode

    # SETTERS
    def set_left(self, node):
        self._leftNode = node
        if node is not None:
            node.parentNode = self  # ajusta o pai automaticamente

    def set_right(self, node):
        self._rightNode = node
        if node is not None:
            node.parentNode = self

    def set_parent(self, node): self.parentNode = node


def altura_no(node):
    """Complexidade: O(n)"""
    if node is None:
        return -1
    left_h = altura_no(node.get_left())
    right_h = altura_no(node.get_right())
    return max(left_h, right_h) + 1


# DFS — Depth First Search, todos O(n)
def print_inorder(node):
    """DFS In-order: esquerda → raiz → direita.  | Complexidade: O(n)"""
    if node is None:
        return
    print_inorder(node.get_left())
    print(node.get_key(), end=" ")
    print_inorder(node.get_right())


def print_preorder(node):
    """DFS Pre-order: raiz → esquerda → direita. | Complexidade: O(n)"""
    if node is None:
        return
    print(node.get_key(), end=" ")
    print_preorder(node.get_left())
    print_preorder(node.get_right())


def print_postorder(node):
    """DFS Post-order: esquerda → direita → raiz | Complexidade: O(n)"""
    if node is None:
        return
    print_postorder(node.get_left())
    print_postorder(node.get_right())
    print(node.get_key(), end=" ")

# BFS com fila 
from collections import deque

def print_bfs_queue(root):
    """Complexidade: O(n)"""
    if root is None:
        return
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.get_key(), end=" ")

        left = node.get_left()
        right = node.get_right()

        if left:
            q.append(left)
        if right:
            q.append(right)


# Árvore binária de busca (BST), todos O(h)
# Balanceada: h = log n/ Degenerada: h = n


# Busca binária recursiva
def binary_tree_search_recursive(node, key):
    if node is None or node.get_key() == key:
        return node
    if node.get_key() > key:
        return binary_tree_search_recursive(node.get_left(), key)
    else:
        return binary_tree_search_recursive(node.get_right(), key)


# Busca binária iterativa
def binary_tree_search_iterative(node, key):
    while node is not None and node.get_key() != key:
        if node.get_key() > key:
            node = node.get_left()
        else:
            node = node.get_right()
    return node


# Busca do menor elemento
def binary_tree_search_min(node):
    """ Menor valor = nó mais à esquerda. """
    if node is None:
        return None
    while node.get_left() is not None:
        node = node.get_left()
    return node


# Busca do maior elemento
def binary_tree_search_max(node):
    """Maior valor = nó mais à direita."""
    if node is None:
        return None
    while node.get_right() is not None:
        node = node.get_right()
    return node


# Sucessor em ordem (in-order successor)

def binary_tree_search_successor(node):
    """Retorna o sucessor em ordem.  Complexidade: O(h)"""

    # Se o nó for None, não há sucessor
    if node is None:
        return None

    # Caso 1: se existe subárvore direita, o sucessor é o mínimo dela
    if node.get_right() is not None:
        return binary_tree_search_min(node.get_right())

    # Caso 2: caso não exista subárvore direita, sobe pela árvore
    parent = node.get_parent()           # pega o pai
    # sobe enquanto o nó for filho direito do pai
    while parent is not None and node == parent.get_right():
        node = parent                    # sobe um nível
        parent = parent.get_parent()     # sobe outro nível

    # quando o loop parar, parent será o sucessor (ou None)
    return parent


# Predecessor em ordem (in-order predecessor)

def binary_tree_search_predecessor(node):
    """Retorna o predecessor em ordem. Complexidade: O(h)"""

    # Se o nó for None, não há predecessor
    if node is None:
        return None

    # Caso 1: se há subárvore esquerda, o predecessor é o máximo dela
    if node.get_left() is not None:
        return binary_tree_search_max(node.get_left())

    # Caso 2: senão, sobe até achar um pai onde o nó seja filho direito
    parent = node.get_parent()
    while parent is not None and node == parent.get_left():
        node = parent                   # sobe um nível
        parent = parent.get_parent()    # sobe outro nível

    return parent


# Inserção em BST

def binary_tree_insert(root, key):
    """Insere key na BST recursivamente. Complexidade: O(h)"""

    # Se a raiz é None, cria um novo nó
    if root is None:
        return Node(key, None)   # pode adaptar para aceitar 'data'

    # Se a chave é menor que a do nó atual, vai para a esquerda
    if key < root.get_key():
        root.set_left(binary_tree_insert(root.get_left(), key))

    # Caso contrário, insere na direita
    else:
        root.set_right(binary_tree_insert(root.get_right(), key))

    # Retorna o nó atual para reconstruir os ponteiros corretamente
    return root


# Remoção em BST

def binary_tree_delete(root, key):
    """Remove um valor da árvore e retorna a nova raiz. Complexidade: O(h)"""

    # Se a árvore estiver vazia, nada a remover
    if root is None:
        return root

    # Se a chave é menor, remoção está na esquerda
    if key < root.get_key():
        root.set_left(binary_tree_delete(root.get_left(), key))

    # Se a chave é maior, remoção está na direita
    elif key > root.get_key():
        root.set_right(binary_tree_delete(root.get_right(), key))

    else:
        # Achou o nó: delega para delete_node
        root = binary_tree_delete_node(root)

    # Retorna a raiz atualizada
    return root


# Função auxiliar que remove um único nó da BST

def binary_tree_delete_node(root):
    """
    Remove um nó considerando todos os casos:
    - Sem filhos
    - 1 filho (esquerda ou direita)
    - 2 filhos (substitui pelo sucessor)
    Complexidade: O(h)
    """

    # Caso 1: nó sem filhos
    if root.get_left() is None and root.get_right() is None:
        return None  # o GC do Python cuida do objeto

    # Caso 2: nó tem apenas filho direito
    if root.get_left() is None:
        return root.get_right()

    # Caso 3: nó tem apenas filho esquerdo
    if root.get_right() is None:
        return root.get_left()

    # Caso 4: nó com dois filhos
    # Encontra o sucessor (menor da subárvore direita)
    successor = binary_tree_search_min(root.get_right())

    # Copia a chave do sucessor para o nó atual
    root.set_key(successor.get_key())

    # Remove o sucessor duplicado da subárvore direita
    root.set_right(binary_tree_delete(root.get_right(), successor.get_key()))

    return root
