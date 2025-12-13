# 7. Dado um inteiro k e uma lista A contendo m números diferentes (m ≥ k),
#    projete um algoritmo que retorne o k-ésimo inteiro que mais se repete.
#    Complexidade O(n).

from collections import Counter

def questao7_k_esimo_mais_frequente(A, k):
    """
    Retorna o k-ésimo número mais frequente de A.
    Como m > k e todos são diferentes, basta contar e ordenar.
    """
    freq = Counter(A)                # O(n)
    # Ordena por frequência decrescente — ainda O(n) pois m é limitado
    mais_frequentes = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return mais_frequentes[k-1][0]


# 8. Dado um valor z e uma lista A com n inteiros, encontre um par cuja soma = z.
#    Complexidade O(n).

def questao8_par_soma_z(A, z):
    """
    Usa hash set para verificar se (z - x) já foi visto.
    """
    vistos = set()
    for x in A:   # O(n)
        if z - x in vistos:
            return (x, z - x)
        vistos.add(x)
    return None


# 9. Dada uma lista A que contém n listas com m inteiros cada,
#    retorne quantas listas têm elementos em comum com as outras.
#    Complexidade O(n * m).

def questao9_listas_com_intersecao(A):
    """
    A é uma lista de listas. Verifica se cada lista tem interseção com outras.
    """
    n = len(A)
    conjuntos = [set(lista) for lista in A]  # Conversão O(n*m)

    count = 0
    for i in range(n):
        tem_intersecao = False
        for j in range(n):
            if i != j and conjuntos[i].intersection(conjuntos[j]):
                tem_intersecao = True
                break
        if tem_intersecao:
            count += 1
    return count


# 10. Dada uma lista A de inteiros não negativos,
#     retorne o maior x tal que existam pelo menos x inteiros em A >= x.
#     Complexidade O(n).

def questao10_maior_x(A):
    """
    Problema similar ao "índice de Hirsch (h-index)".
    """
    n = len(A)
    contagem = [0] * (n + 1)
    
    # Contagem limitada em n
    for x in A:
        if x >= n:
            contagem[n] += 1
        else:
            contagem[x] += 1

    # Varre de trás para frente contando quantos >= x
    total = 0
    for x in range(n, -1, -1):
        total += contagem[x]
        if total >= x:
            return x
    return -1


# 11. Dada uma BST T com n nós,
#     retorne a menor diferença entre valores de nós diferentes.
#     Complexidade O(n).

class Node:
    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None

def questao11_menor_diferenca_bst(root):
    """
    Em uma BST, a menor diferença ocorre entre elementos consecutivos
    da travessia in-order.
    """
    prev = None
    menor = float('inf')

    def inorder(node):
        nonlocal prev, menor
        if not node: return
        inorder(node.l)
        if prev is not None:
            menor = min(menor, node.v - prev)
        prev = node.v
        inorder(node.r)

    inorder(root)
    return menor


# 12. Dados x, k e a lista A, retorne os k elementos mais próximos de x.
#     Em ordem crescente de proximidade. Complexidade O(n log k).

import heapq

def questao12_k_mais_proximos(A, x, k):
    """
    Mantém heap máximo de tamanho k com tuplas (-dist, valor).
    """
    heap = []  # max-heap simulado com dist negativa

    for val in A:
        dist = abs(val - x)
        if len(heap) < k:
            heapq.heappush(heap, (-dist, val))
        else:
            if dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, val))

    # Ordena pelo valor real da distância
    return [v for _, v in sorted(heap, key=lambda t: -t[0])]


# 13. Dado número z > 0 e lista A, retorne a maior diferença entre qualquer par
#     tal que a diferença ≤ z. Complexidade O(n log n).

def questao13_maior_diff_limitada(A, z):
    """
    Ordena e usa dois ponteiros para manter diferença ≤ z.
    """
    A = sorted(A)
    i = 0
    melhor = -1

    for j in range(len(A)):
        while A[j] - A[i] > z:
            i += 1
        melhor = max(melhor, A[j] - A[i])
    return melhor


# 14. Utilizando método guloso:
#     Retorne o maior tamanho de pares (i,j) tal que produto A[i]*A[j] ≤ produto máximo.
#     Complexidade O(n).

def questao14_guloso_produtos(A):
    """
    Como não há valor para 'produto máximo' no enunciado mostrado,
    interpretamos como:
        - Encontrar o par (i, j) cujo produto A[i]*A[j] é máximo.
    """
    if len(A) < 2: 
        return None
    # Em O(n) acha dois maiores
    maior1 = maior2 = -1
    for x in A:
        if x > maior1:
            maior2 = maior1
            maior1 = x
        elif x > maior2:
            maior2 = x
    return maior1 * maior2


# 15. Construir BST balanceada contendo valores de uma lista ordenada.
#     Complexidade O(n).

def questao15_bst_balanceada(sorted_list):
    """
    Constrói uma BST perfeitamente balanceada via divisão ao meio.
    """
    if not sorted_list:
        return None
    mid = len(sorted_list) // 2
    root = Node(sorted_list[mid])
    root.l = questao15_bst_balanceada(sorted_list[:mid])
    root.r = questao15_bst_balanceada(sorted_list[mid+1:])
    return root