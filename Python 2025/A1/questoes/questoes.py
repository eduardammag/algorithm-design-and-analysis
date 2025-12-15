################################## a1 2022

""" 2- Dada uma sequência A com n números naturais DISTINTOS,
projetar um algoritmo que verifique se existem 3 números distintos
cuja soma seja igual a x. Complexidade exigida: O(n² log n)
Ideia:
1. Ordenar o array -> O(n log n)
2. Para cada par (i, j), buscar x - (A[i] + A[j]) por busca binária -> O(log n)
Total: n² pares x log n = O(n² log n)"""
def questao2(A, x):
    A = sorted(A)                      # O(n log n)
    n = len(A)

    for i in range(n):
        for j in range(i+1, n):
            alvo = x - (A[i] + A[j])  # valor que falta para completar a soma
            # Busca binária — O(log n)
            lo, hi = 0, n-1
            while lo <= hi:
                mid = (lo+hi)//2
                if A[mid] == alvo and mid != i and mid != j:
                    return True
                if A[mid] < alvo:
                    lo = mid + 1
                else:
                    hi = mid - 1
    return False


""" 3 - Uma sequência A de tamanho n contém inteiros positivos e negativos.
a) Produzir algoritmo O(n³) que encontra i e j, tal que i < j tal que soma(A[i]+...+A[j]) é máxima.
b) Otimizar para O(n²).
c) Avaliar se é possível O(n). (Sim — Kadane)"""
# a) Solução O(n³)
def max_subarray_cubico(A):
    n = len(A)
    melhor = float("-inf")
    for i in range(n):               # O(n)
        for j in range(i, n):        # O(n)
            soma = 0
            for k in range(i, j+1):  # O(n)
                soma += A[k]
            melhor = max(melhor, soma)
    return melhor

# b) Solução O(n²)
def max_subarray_quadratico(A):
    n = len(A)
    melhor = float("-inf")
    for i in range(n):              # O(n)
        soma = 0
        for j in range(i, n):       # O(n)
            soma += A[j]            # soma acumulada
            melhor = max(melhor, soma)
    return melhor

# c) Solução O(n) — Kadane
def max_subarray_kadane(A):
    melhor = atual = A[0]
    for x in A[1:]:
        atual = max(x, atual + x)
        melhor = max(melhor, atual)
    return melhor


""" 4 - Explique como funciona o algoritmo de remoção de um elemento em uma 
tabela hash, considerando as duas estratégias clássicas de tratamento 
de colisões:
(a) ENCADEAMENTO 

Na estratégia de encadeamento, cada posição da tabela hash (bucket)
contém uma LISTA (normalmente uma lista ligada). Para remover:
1. Calcula-se o bucket: b = h(key)
2. Percorre-se a lista bucket[b] comparando cada elemento com key
3. Quando encontrado, remove-se o nó da lista.
    - Remover da lista é operação O(1)
           (se já temos a referência ou o índice).
    - O custo dominante é PERCORRER a lista → O(k),
           onde k é o número de elementos naquele bucket.

VANTAGENS:
      - Remoção é simples: basta retirar da lista.
      - Não prejudica buscas futuras, pois listas independem de tombstones.

COMPLEXIDADE:
      - Melhor caso: O(1)
      - Pior caso: O(n) (quando todas as chaves colidem no mesmo bucket)
      - Caso médio com hash bom: O(α), onde α = n/m (fator de carga)


(b) ENDEREÇAMENTO ABERTO 
Se removemos simplesmente a chave e colocamos None, 
quebramos a cadeia de sondagem e causamos "buracos".  
Isso impede que futuras BUSCAS encontrem elementos corretamente.
Utilizamos uma MARCA ESPECIAL chamada TOMBSTONE.

Função da TOMBSTONE:
- Diz que "havia algo aqui, mas foi removido".
- Mantém a continuidade da sondagem.
- Permite busca correta de elementos posteriores.
- Permite inserir novos elementos nessa posição futuramente.

COMPLEXIDADE:
    - Remoção: O(n) no pior caso (igual à busca por linear probing).
    - No caso médio: O(1) por operação, para fator de carga < 0.7."""


"""5- Dadas sequências A (m elementos) e B (n elementos), m ≥ n,
produzir sequência C contendo os elementos de A REORDENADOS segundo
a ordem dos elementos de B. Os elementos de A que não aparecem em 
B vão para o final em ordem crescente. Exemplo:
A = [5,8,9,3,5,7,1,3,4,9,5,1,8,4]
B = [3,5,7,2]
C = [3,3,3,5,5,5,7,1,1,4,4,8,8,9,9]
Complexidade requerida: O(m log m)"""

def questao5(A, B):
    from collections import Counter
    freq = Counter(A)  # Frequências de A
    C = []
    # Primeiro, adiciona elementos na ordem de B
    for b in B:
        if b in freq:
            C.extend([b]*freq[b])
            del freq[b]
    # Agora adiciona os que sobraram, mas em ordem crescente
    restantes = []
    for val, qt in freq.items():
        restantes.extend([val]*qt)
    C.extend(sorted(restantes))  # O(m log m)
    return C


""" 6 - Dada uma sequência A com n números reais distintos,
encontrar os √n menores números em O(n).
Solução:
- Encontrar o elemento de ordem k = √n via quickselect → O(n)
- Depois, varrer o vetor e coletar todos os ≤ pivot → O(n)"""

import math
import random

def quickselect(A, k):
    # Retorna o k-ésimo menor (0-indexed)
    if len(A) == 1:
        return A[0]

    p = random.choice(A)
    menores  = [x for x in A if x < p]
    iguais   = [x for x in A if x == p]
    maiores  = [x for x in A if x > p]

    if k < len(menores):
        return quickselect(menores, k)
    elif k < len(menores) + len(iguais):
        return p
    else:
        return quickselect(maiores, k - len(menores) - len(iguais))

def questao6(A):
    n = len(A)
    k = int(math.sqrt(n))
    limite = quickselect(A, k-1)  # o k-ésimo menor

    # Coleta dos √n menores
    menores = [x for x in A if x <= limite]

    # Caso venham mais de √n valores iguais ao pivô,
    # mantemos apenas √n elementos.
    return sorted(menores)[:k]


###################################### a1 2023

"""2 - Dada uma sequência A ORDENADA contendo n inteiros distintos,
crie um algoritmo capaz de determinar se existe um índice i tal que:
A[i] = i. A complexidade do pior caso deve ser O(log n)!
IDEIA: A está ordenada → podemos aplicar busca binária.
Se A[mid] > mid então a solução só pode estar à esquerda.
Se A[mid] < mid então só pode estar à direita.
Se A[mid] == mid → achou! COMPLEXIDADE: O(log n)"""

def questao2(A):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2

        if A[mid] == mid:
            return True
        elif A[mid] > mid:
            hi = mid - 1
        else:
            lo = mid + 1

    return False


""" 3 - O sistema precisa gerenciar uma FILA DE TAREFAS, cada uma contendo:
    - referência T
    - prioridade p (quanto MENOR o número, maior a prioridade)
O módulo deve fornecer:
    • add_task(t, p)     → O(log n)
    • next_task()        → O(1)
    • remove_task()      → O(log n)
a) Descrever a estrutura geral:
    USAMOS UM MIN-HEAP (prioridade mínima = tarefa mais urgente)
b) Criar algoritmo para cada operação:
    - add_task: inserir no heap → O(log n)
    - next_task: retornar heap[0] → O(1)
    - remove_task: remover raiz + heapify → O(log n)
c) Novo requisito:
    atualizar a prioridade de uma tarefa
    Solução eficiente: guardar um **mapa TAREFA → ÍNDICE NO HEAP**
    e aplicar “decrease-key” → O(log n)
"""
import heapq
class PriorityQueue:
    def __init__(self):
        self.heap = []                # min-heap
        self.position = {}            # mapeia tarefa → índice

    def add_task(self, task, priority):
        # Inserimos um tuplo (priority, task)
        heapq.heappush(self.heap, (priority, task))
        # O Python não fornece índice diretamente, então reconstruímos:
        self._rebuild_position()

    def next_task(self):
        # Apenas consulta o topo
        if not self.heap: return None
        return self.heap[0][1]

    def remove_task(self):
        # Remove tarefa mais prioritária
        if not self.heap: return None
        priority, task = heapq.heappop(self.heap)
        self._rebuild_position()
        return task

    def update_priority(self, task, new_priority):
        """Atualiza prioridade de uma tarefa:
        Estratégia simples: remover tudo e reempilhar ajustado.
        Ainda é O(n log n). Se implementássemos heap de índice manual, seria O(log n)."""
        for i, (p, t) in enumerate(self.heap):
            if t == task:
                self.heap[i] = (new_priority, task)
                heapq.heapify(self.heap)
                self._rebuild_position()
                return True
        return False

    def _rebuild_position(self):
        """Reconstrói o mapeamento tarefa → índice."""
        self.position = {task: i for i, (p, task) in enumerate(self.heap)}


"""4 - A contém n POSITIVOS INT distintos.
Criar algoritmo que encontre os k números MAIS PRÓXIMOS da mediana a.
Definição da distância: |A[i] - a|. Complexidade: O(n)
SOLUÇÃO:
1) Encontrar mediana → Quickselect em O(n)
2) Calcular distâncias O(n)
3) Obter os k menores → Quickselect novamente O(n)
4) Retornar elementos
TOTAL: O(n)"""

import random

def quickselect_kth(A, k):
    """Quickselect retorna o k-ésimo menor (0-indexed)."""
    if len(A) == 1:
        return A[0]
    p = random.choice(A)
    menores = [x for x in A if x < p]
    iguais = [x for x in A if x == p]
    maiores = [x for x in A if x > p]
    if k < len(menores):
        return quickselect_kth(menores, k)
    elif k < len(menores) + len(iguais):
        return p
    else:
        return quickselect_kth(maiores, k - len(menores) - len(iguais))

def questao4(A, k):
    n = len(A)
    # 1) Encontrar mediana (posição n//2)
    mediana = quickselect_kth(A, n//2)
    # 2) Calcular distâncias
    dist = [(abs(x - mediana), x) for x in A]
    # 3) Quickselect sobre distâncias
    kth_val = quickselect_kth(dist, k-1)[0]
    # 4) Filtrar valores com dist ≤ kth_val
    resposta = [x for (d, x) in dist if d <= kth_val]
    # Caso venham mais de k valores empatados
    return resposta[:k]


"""5 - A contém n inteiros positivos. 
Cada número pertence ao conjunto: {n², n² + 1, n² + 2, ..., n² + n}
Criar algoritmo que encontre o NÚMERO QUE MAIS SE REPETE.
Observação: como existem n números possíveis e n números na entrada,
pode haver empates — basta retornar qualquer um. Complexidade O(n).
IDEIA:
    - Todos valores estão no intervalo [n² , n² + n]
    - Podemos usar contagem direta (counting) em vetor de tamanho n+1
    - Frequências em O(n)"""

def questao5(A):
    n = len(A)
    base = n*n
    freq = [0] * (n+1)   # valores n² ... n²+n
    for x in A:
        freq[x - base] += 1
    # índice de maior frequência
    idx = max(range(n+1), key=lambda i: freq[i])
    return base + idx

############################# a1 2024
"""3 - Uma empresa de análise de redes sociais possui uma base com milhões de usuários.
Cada usuário é representado por uma tupla:
    <id_usuario, seguidores, engajamento>
Um influenciador emergente é aquele que:
- está no top 10% em termos de engajamento
- NÃO está no top 10% em número de seguidores

Projete um algoritmo O(n) que identifique todos os influenciadores emergentes
a partir de uma sequência A com n usuários.
"""
def quickselect(A, k, key):
    """
    Retorna o elemento que estaria na posição k
    se A fosse ordenado segundo a função key.
    Complexidade média: O(n)
    """
    if len(A) == 1:
        return A[0]
    pivot = A[len(A) // 2]
    pivot_value = key(pivot)

    menores = [x for x in A if key(x) < pivot_value]
    iguais   = [x for x in A if key(x) == pivot_value]
    maiores  = [x for x in A if key(x) > pivot_value]
    if k < len(menores):
        return quickselect(menores, k, key)
    elif k < len(menores) + len(iguais):
        return iguais[0]
    else:
        return quickselect(maiores, k - len(menores) - len(iguais), key)


def influenciadores_emergentes(A):
    n = len(A)
    if n == 0:
        return []
    # índice que separa os 10% maiores valores
    k = int(0.9 * n)
    # limiar do top 10% de engajamento
    eng_limite = quickselect(A, k, key=lambda x: x[2])[2]
    # limiar do top 10% de seguidores
    seg_limite = quickselect(A, k, key=lambda x: x[1])[1]
    # varredura final O(n)
    resultado = []
    for (id_u, seguidores, engajamento) in A:
        if engajamento >= eng_limite and seguidores < seg_limite:
            resultado.append((id_u, seguidores, engajamento))
    return resultado

####################3 lista 2024
# 7. Dado um inteiro k e uma lista A contendo m números diferentes (m ≥ k),
#    projete um algoritmo que retorne o k-ésimo inteiro que mais se repete.
#    Complexidade O(n).

from collections import Counter

def questao7_k_esimo_mais_frequente(A, k):
    """Retorna o k-ésimo número mais frequente de A.
    Como m > k e todos são diferentes, basta contar e ordenar."""
    freq = Counter(A)                # O(n)
    # Ordena por frequência decrescente — ainda O(n) pois m é limitado
    mais_frequentes = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return mais_frequentes[k-1][0]


# 8. Dado um valor z e uma lista A com n inteiros, encontre um par cuja soma = z.
#    Complexidade O(n).
def questao8_par_soma_z(A, z):
    """Usa hash set para verificar se (z - x) já foi visto. """
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
    """A é uma lista de listas. Verifica se cada lista tem interseção com outras."""
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
    """Problema similar ao "índice de Hirsch (h-index)"."""
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


# 11. Dada uma BST T com n nós, retorne a menor diferença entre valores de nós diferentes.
# Complexidade O(n).
class Node:
    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None

def questao11_menor_diferenca_bst(root):
    """Em uma BST, a menor diferença ocorre entre elementos consecutivos
    da travessia in-order."""
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
    """Mantém heap máximo de tamanho k com tuplas (-dist, valor)."""
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
    """Ordena e usa dois ponteiros para manter diferença ≤ z."""
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
    """Como não há valor para 'produto máximo' no enunciado mostrado,
    interpretamos como:
        - Encontrar o par (i, j) cujo produto A[i]*A[j] é máximo."""
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
    """Constrói uma BST perfeitamente balanceada via divisão ao meio."""
    if not sorted_list:
        return None
    mid = len(sorted_list) // 2
    root = Node(sorted_list[mid])
    root.l = questao15_bst_balanceada(sorted_list[:mid])
    root.r = questao15_bst_balanceada(sorted_list[mid+1:])
    return root

######################################################### maratona busca
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

############################# maratona hash
""" 1 — Tabela Hash com Encadeamento: Contagem de Colisões
Implemente uma tabela hash de tamanho M utilizando encadeamento.
Ao inserir N chaves, conte quantas colisões ocorreram.
Uma colisão ocorre quando:
 - vamos inserir uma chave num bucket que já contém pelo menos 1 elemento
"""

def hash_insert_chaining_count_collisions(M, keys):
    # Cria a tabela hash: um vetor de listas vazias
    table = [[] for _ in range(M)]

    collisions = 0  # contador de colisões

    for key in keys:
        index = key % M  # função hash simples

        # Se o bucket já não estiver vazio → colisão
        if len(table[index]) > 0:
            collisions += 1

        # Inserção normal no encadeamento
        table[index].append(key)

    return collisions



""" 2 — Hash com Endereçamento Aberto: Sondagem Linear
Implementar:
 I X → inserir X
 B X → buscar X
 P   → imprimir tabela

Hash:
 h(key, i) = (key % M + i) % M
Caso a tabela fique cheia → imprimir "FULL"."""

def hashing_linear_probing(M, operations):
    # Cria uma tabela hash preenchida com None (vazio)
    table = [None] * M

    def insert_linear(x):
        # Tenta inserir a chave x usando sondagem linear
        for i in range(M):
            pos = (x % M + i) % M  # fórmula da sondagem linear
            if table[pos] is None:  # posição livre
                table[pos] = x
                return
        print("FULL")  # tabela cheia sem posição

    def search_linear(x):
        # Busca usando sondagem linear
        for i in range(M):
            pos = (x % M + i) % M
            if table[pos] is None:  # encontrou vazio → não existe
                break
            if table[pos] == x:
                print("FOUND")
                return
        print("NOT FOUND")

    def print_table():
        # Imprime a tabela linha reta
        print(" ".join(str(v) if v is not None else "_" for v in table))

    # Processamento das operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_linear(int(parts[1]))

        elif parts[0] == "B":
            search_linear(int(parts[1]))

        elif parts[0] == "P":
            print_table()



"""3 — Hash com Endereçamento Aberto: Sondagem Quadrática
Operações:
 I X → inserir
 B X → buscar
 R X → remover (usando marcador "DELETED")
Hash:
 h(key, i) = (key % M + i*i) % M
"""

def hashing_quadratic_probing(M, operations):
    # Cria tabela com None para vazio e "DEL" para deletado
    table = [None] * M

    def insert_quad(x):
        # Inserção com sondagem quadrática
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None or table[pos] == "DEL":
                table[pos] = x
                return
        print("FAILED")  # não encontrou posição

    def search_quad(x):
        # Busca com sondagem quadrática
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None:  # posição vazia → não existe
                break
            if table[pos] == x:
                print("FOUND")
                return
        print("NOT FOUND")

    def remove_quad(x):
        # Remoção marcando "DEL"
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None:
                break
            if table[pos] == x:
                table[pos] = "DEL"
                return

    # Executa operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_quad(int(parts[1]))

        elif parts[0] == "B":
            search_quad(int(parts[1]))

        elif parts[0] == "R":
            remove_quad(int(parts[1]))



"""
4 — Double Hashing: Contagem de Sondas
Inserir várias chaves usando double hashing e contar quantas
sondagens totais foram necessárias.

h1(key) = key mod M
h2(key) = 1 + (key mod (M-1))
h(key,i) = (h1 + i*h2) mod M

Cada tentativa conta como 1 sondagem.
"""

def double_hashing_count_probes(M, keys):
    table = [None] * M
    probes = 0  # contador de sondagens

    for key in keys:
        h1 = key % M
        h2 = 1 + (key % (M - 1))

        for i in range(M):
            pos = (h1 + i * h2) % M
            probes += 1  # conta tentativa

            if table[pos] is None:
                table[pos] = key
                break

    return probes



""" 5 — Encadeamento com Remoção e Relatórios
Operações:
 I X → inserir X
 R X → remover X
 B X → buscar X
 L   → imprimir tamanhos dos buckets

Imprimir L como: size0 size1 size2 ... size(M-1)"""

def hashing_chaining_full(M, operations):
    # Cria tabela hash como lista de listas
    table = [[] for _ in range(M)]

    def insert_chain(x):
        index = x % M
        table[index].append(x)

    def remove_chain(x):
        index = x % M
        # Remove apenas uma ocorrência se existir
        if x in table[index]:
            table[index].remove(x)

    def search_chain(x):
        index = x % M
        if x in table[index]:
            print("FOUND")
        else:
            print("NOT FOUND")

    def list_sizes():
        # imprime o tamanho de cada bucket da tabela
        print(" ".join(str(len(bucket)) for bucket in table))

    # Processamento das operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_chain(int(parts[1]))

        elif parts[0] == "R":
            remove_chain(int(parts[1]))

        elif parts[0] == "B":
            search_chain(int(parts[1]))

        elif parts[0] == "L":
            list_sizes()

##########################3 maratona ordenacao

#  1 — Ordenação por Bubble Sort (contando trocas)
""" Enunciado:
Dado um vetor de N inteiros, ordene-o utilizando Bubble Sort,
mas também retorne o número total de trocas realizadas.
Imprima o array ordenado e o total de trocas.

Entrada de exemplo:
[5, 1, 4, 2, 8]

Saída esperada:
Array ordenado: [1, 2, 4, 5, 8]
Trocas: 4"""

def bubble_sort_count(arr):
    n = len(arr)
    trocas = 0
    for i in range(n):
        for j in range(n - 1 - i):
            # Se o elemento atual é maior que o próximo, troque
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                trocas += 1
    return arr, trocas

print(" 1")
a = [5, 1, 4, 2, 8]
ordenado, t = bubble_sort_count(a)
print("Ordenado:", ordenado)
print("Trocas:", t)
print("-" * 60)


#  2 — Insertion Sort com contagem de inserções
"""Enunciado:
Implemente o algoritmo Insertion Sort e conte quantas vezes
um elemento foi movido dentro do array.

Entrada:
[9, 5, 1, 4, 3]

Saída:
Ordenado: [1, 3, 4, 5, 9]
Movimentos: (algum valor)"""

def insertion_sort_moves(arr):
    moves = 0
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1

        # Move elementos maiores que a chave
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            moves += 1
            j -= 1

        # Inserção da chave na posição correta
        arr[j + 1] = chave
    return arr, moves

print(" 2")
b = [9, 5, 1, 4, 3]
ordenado, mv = insertion_sort_moves(b)
print("Ordenado:", ordenado)
print("Movimentos:", mv)
print("-" * 60)


#  3 — MergeSort para contar inversões
""" Enunciado:
Use MergeSort para contar o número de inversões no array.
Uma inversão ocorre quando i < j, mas arr[i] > arr[j].

Entrada:
[2, 4, 1, 3, 5]

Saída:
Inversões: 3"""

def merge_count(arr):
    if len(arr) <= 1:
        return arr, 0

    meio = len(arr) // 2
    esquerda, inv_esq = merge_count(arr[:meio])
    direita, inv_dir = merge_count(arr[meio:])

    i = j = 0
    merged = []
    inversoes = inv_esq + inv_dir

    # Mescla contabilizando inversões
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            merged.append(esquerda[i])
            i += 1
        else:
            merged.append(direita[j])
            j += 1
            inversoes += len(esquerda) - i  # posições restantes da esquerda

    merged.extend(esquerda[i:])
    merged.extend(direita[j:])

    return merged, inversoes

print(" 3")
c = [2, 4, 1, 3, 5]
ordenado, inv = merge_count(c)
print("Ordenado:", ordenado)
print("Inversões:", inv)
print("-" * 60)


#  4 — QuickSort (pivô final) + contar partições
"""Enunciado:
Implemente o QuickSort usando como pivô o último elemento
e conte quantas partições (chamadas da função partition) ocorreram.

Entrada:
[10, 7, 8, 9, 1, 5]

Saída exemplo:
Ordenado: [1, 5, 7, 8, 9, 10]
Partições: (algum valor)"""

particoes = 0

def partition(arr, low, high):
    global particoes
    particoes += 1  # Quantas vezes a função partition é chamada

    pivo = arr[high]
    i = low - 1

    for j in range(low, high):
        # Colocar elementos menores que o pivô à esquerda
        if arr[j] < pivo:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1

def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

print(" 4")
d = [10, 7, 8, 9, 1, 5]
particoes = 0
quicksort(d, 0, len(d) - 1)
print("Ordenado:", d)
print("Partições:", particoes)
print("-" * 60)


#  5 — HeapSort para ordenar notas de alunos
""" Enunciado:
Você recebe as notas de alunos e deve ordená-las usando HeapSort.
Imprima o vetor ordenado de forma crescente.

Entrada:
[70, 50, 90, 30, 100, 60]

Saída:
[30, 50, 60, 70, 90, 100]
"""

def heapify(arr, n, i):
    maior = i
    esq = 2 * i + 1
    dir = 2 * i + 2

    # Verifica se o filho esquerdo é maior que o pai
    if esq < n and arr[esq] > arr[maior]:
        maior = esq

    # Verifica se o filho direito é maior que o maior até agora
    if dir < n and arr[dir] > arr[maior]:
        maior = dir

    # Se o maior não for o pai, troque e continue heapificando
    if maior != i:
        arr[i], arr[maior] = arr[maior], arr[i]
        heapify(arr, n, maior)


def heapsort(arr):
    n = len(arr)

    # Constrói o heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extrai elementos do heap um a um
    for i in range(n - 1, 0, -1):
        # Move o maior elemento para o fim
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

print(" 5")
e = [70, 50, 90, 30, 100, 60]
heapsort(e)
print("Ordenado:", e)
print("-" * 60)


# 6 — MergeSort em tempos de entrega
"""Enunciado:
Uma empresa de logística recebe uma lista com os tempos estimados de
entrega de pedidos (em horas). Para organizar melhor a distribuição,
é necessário ordenar esses tempos em ordem crescente usando MergeSort.
Além disso, deve-se informar quantas chamadas de "merge" ocorreram.

Exemplo:
Entrada: [12, 5, 7, 3, 9]
Saída:
Ordenado: [3, 5, 7, 9, 12]
Merges realizados: X"""

merge_calls = 0

def merge_sort_count(arr):
    global merge_calls
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_count(arr[:mid])
    right = merge_sort_count(arr[mid:])

    merge_calls += 1  # contamos cada operação de merge

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    # Mesclando enquanto ambos têm elementos
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Anexando restos
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(" 1")
tempos = [12, 5, 7, 3, 9]
merge_calls = 0
result = merge_sort_count(tempos)
print("Ordenado:", result)
print("Merges realizados:", merge_calls)
print("-" * 70)


#  7 — QuickSort com pivô mediana de 3 (tempos de corrida)
"""Enunciado:
Em uma maratona, você recebe os tempos finais dos corredores.
Ordene os tempos usando QuickSort escolhendo o pivô pela mediana
dos valores: primeiro, meio e último elemento.

Devolva:
- vetor ordenado
- número de trocas

Entrada:
[312, 280, 294, 300, 310, 275]"""

trocas_quick = 0

def mediana_de_tres(arr, low, high):
    mid = (low + high) // 2
    trio = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    trio.sort(key=lambda x: x[0])
    return trio[1][1]  # retorna índice do valor mediano

def partition_mediana(arr, low, high):
    global trocas_quick
    p = mediana_de_tres(arr, low, high)
    arr[p], arr[high] = arr[high], arr[p]  # coloca pivô no fim
    trocas_quick += 1

    pivo = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivo:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            trocas_quick += 1

    arr[i+1], arr[high] = arr[high], arr[i+1]
    trocas_quick += 1
    return i + 1

def quicksort_mediana(arr, low, high):
    if low < high:
        pi = partition_mediana(arr, low, high)
        quicksort_mediana(arr, low, pi - 1)
        quicksort_mediana(arr, pi + 1, high)

print(" 2")
tempos_corrida = [312, 280, 294, 300, 310, 275]
trocas_quick = 0
quicksort_mediana(tempos_corrida, 0, len(tempos_corrida) - 1)
print("Ordenado:", tempos_corrida)
print("Trocas:", trocas_quick)
print("-" * 70)


#  8 — Counting Sort em notas escolares
"""
Enunciado:
Uma escola deseja ordenar as notas (0 a 100) dos alunos.
Use Counting Sort para ordenar e também exiba o vetor auxiliar
de contagem.

Entrada:
[70, 50, 90, 30, 100, 60, 50, 80]
"""

def counting_sort(arr, max_val=100):
    count = [0] * (max_val + 1)

    # Contando ocorrências
    for val in arr:
        count[val] += 1

    # Construindo array ordenado
    idx = 0
    sorted_arr = []
    for num, c in enumerate(count):
        for _ in range(c):
            sorted_arr.append(num)
            idx += 1

    return sorted_arr, count

print(" 3")
notas = [70, 50, 90, 30, 100, 60, 50, 80]
sorted_notas, count_vec = counting_sort(notas)
print("Ordenado:", sorted_notas)
print("Vetor de contagem:", count_vec)
print("-" * 70)


#  9 — Radix Sort mostrando buckets a cada passo
"""Enunciado:
Você deve ordenar números de protocolo (mesmo número de dígitos)
usando Radix Sort e mostrar os buckets usados em cada dígito.

Entrada:
[329, 457, 657, 839, 436, 720, 355]"""

def radix_sort_verbose(arr):
    max_digits = len(str(max(arr)))
    output = list(arr)

    for d in range(max_digits):
        print(f"== Dígito {d} ==")
        buckets = [[] for _ in range(10)]

        # Distribui nos buckets conforme o dígito atual
        for num in output:
            digit = (num // (10 ** d)) % 10
            buckets[digit].append(num)

        # Mostrando buckets
        for i, b in enumerate(buckets):
            print(f"Bucket {i}: {b}")

        # Junta novamente
        output = [num for bucket in buckets for num in bucket]
        print("Após esse dígito:", output)
        print("-" * 40)

    return output

print(" 4")
protocolos = [329, 457, 657, 839, 436, 720, 355]
final_radix = radix_sort_verbose(protocolos)
print("Ordenado:", final_radix)
print("-" * 70)


#  10 — HeapSort em pesos de produtos
"""Enunciado:
Uma fábrica precisa ordenar os pesos dos produtos de forma crescente.
Use HeapSort e mostre o estado do heap a cada remoção do maior elemento.

Entrada:
[12.4, 5.8, 9.0, 3.1, 15.2, 11.0]"""

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Verificando filhos
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapsort_verbose(arr):
    n = len(arr)

    # Construindo heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    print("Heap inicial:", arr)

    # Extraindo elementos
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        print(f"Após remover o maior (colocado na pos {i}):", arr)
        heapify(arr, i, 0)

    return arr

print(" 5")
pesos = [12.4, 5.8, 9.0, 3.1, 15.2, 11.0]
resultado_heap = heapsort_verbose(pesos)
print("Ordenado:", resultado_heap)
print("-" * 70)


#  11 — Insertion Sort em número de páginas de livros
"""
Enunciado:
Uma biblioteca recebeu uma lista com a quantidade de páginas de novos livros.
Eles querem usar Insertion Sort para ordenar, já que o conjunto é pequeno.

Tarefa:
- Ordenar usando Insertion Sort
- Contar quantos deslocamentos ocorreram
- Imprimir vetor final

Entrada:
[320, 150, 220, 180, 400]
"""

def insertion_sort_pages(arr):
    moves = 0
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        # move elementos maiores que a chave
        while j >= 0 and arr[j] > chave:
            arr[j+1] = arr[j]
            moves += 1
            j -= 1
        arr[j+1] = chave
    return arr, moves

print(" 1")
livros = [320, 150, 220, 180, 400]
ordenado1, mv1 = insertion_sort_pages(livros)
print("Ordenado:", ordenado1)
print("Deslocamentos:", mv1)
print("-" * 70)


#  12 — Bucket Sort em pesos de pacotes
"""
Enunciado:
Um armazém recebe pacotes com pesos entre 0 e 1 kg.
Como a distribuição é uniforme, Bucket Sort é ideal.

Tarefa:
- Implementar Bucket Sort
- Mostrar os buckets após a distribuição

Entrada:
[0.42, 0.32, 0.23, 0.52, 0.12, 0.75, 0.33]
"""

def bucket_sort_verbose(arr):
    n = len(arr)
    buckets = [[] for _ in range(n)]

    # Distribuição dos elementos nos baldes
    for val in arr:
        idx = int(val * n)
        if idx == n:
            idx = n - 1
        buckets[idx].append(val)

    print("Buckets após distribuição:")
    for i, b in enumerate(buckets):
        print(f"Bucket {i}: {b}")

    # Ordenação individual dos buckets
    for b in buckets:
        b.sort()

    # Concatena resultado
    result = []
    for b in buckets:
        result.extend(b)
    return result

print(" 2")
pacotes = [0.42, 0.32, 0.23, 0.52, 0.12, 0.75, 0.33]
ordenado2 = bucket_sort_verbose(pacotes)
print("Ordenado:", ordenado2)
print("-" * 70)


# 13— MergeSort para ordenar vendas mensais
"""
Enunciado:
Uma loja registra vendas diárias durante 30 dias.
Eles querem analisar períodos de baixa demanda, então precisam ordenar
os valores usando MergeSort e saber quantas divisões ocorreram.

Entrada: 30 valores de vendas (exemplo gerado no código).
"""

merge_divisions = 0

def merge_sort_sales(arr):
    global merge_divisions
    if len(arr) <= 1:
        return arr

    merge_divisions += 1  # conta a divisão

    mid = len(arr) // 2
    left = merge_sort_sales(arr[:mid])
    right = merge_sort_sales(arr[mid:])

    return merge_sales(left, right)

def merge_sales(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Exemplo de vendas
import random
vendas = [random.randint(100, 2000) for _ in range(30)]

print(" 3")
merge_divisions = 0
ordenado3 = merge_sort_sales(vendas)
print("Vendas ordenadas:", ordenado3)
print("Divisões realizadas:", merge_divisions)
print("-" * 70)


# 14 — Radix Sort base 16 em códigos hexadecimais
"""
Enunciado:
Códigos de peças industriais possuem 4 dígitos hexadecimais.
Devem ser ordenados com Radix Sort em base 16.

Tarefa:
- Converter códigos para inteiros
- Executar Radix Sort base 16
- Converter de volta para hex

Entrada:
["1A3F", "0F22", "3B10", "1A01", "2CFF"]
"""

def radix_sort_hex(arr):
    # Converte hex para inteiro
    nums = [int(x, 16) for x in arr]

    max_val = max(nums)
    exp = 1

    while max_val // exp > 0:
        buckets = [[] for _ in range(16)]

        for num in nums:
            digit = (num // exp) % 16
            buckets[digit].append(num)

        nums = [num for bucket in buckets for num in bucket]
        exp *= 16

    # Converte de volta para hexadecimal
    return [format(num, "04X") for num in nums]

print(" 4")
codigos = ["1A3F", "0F22", "3B10", "1A01", "2CFF"]
ordenado4 = radix_sort_hex(codigos)
print("Ordenado (hex):", ordenado4)
print("-" * 70)


#  15 — HeapSort em prioridades de suporte
"""
Enunciado:
Chamados de suporte têm prioridades (1 a 100).
Quem tem maior prioridade deve ser atendido primeiro.
Usar HeapSort para transformar em heap máximo e mostrar a fila
sendo esvaziada.

Entrada:
[55, 80, 30, 95, 60, 74]
"""

def heapify(arr, n, i):
    largest = i
    left = 2*i + 1
    right = 2*i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapsort_support(arr):
    n = len(arr)

    # Construindo heap
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    print("Heap inicial:", arr)

    # Extraindo elementos
    saida = []
    for i in range(n-1, -1, -1):
        arr[i], arr[0] = arr[0], arr[i]
        saida.append(arr[i])
        print("Após remover maior:", arr[:i], "| Removido:", arr[i])
        heapify(arr, i, 0)

    return saida  # prioridades em ordem decrescente

print(" 5")
prioridades = [55, 80, 30, 95, 60, 74]
ordenado5 = heapsort_support(prioridades)
print("Chamados em ordem de atendimento:", ordenado5)
print("-" * 70)

##########################3 maratona selecao

# QUESTÃO 1 — QUICKSELECT BÁSICO
"""Enunciado:
Dado um vetor de inteiros e um valor k (0-indexado), encontre
o k-ésimo menor elemento usando o algoritmo Quickselect.

Entrada de exemplo:
arr = [9, 1, 5, 3, 7, 2, 8]
k = 3   (3º menor → resposta = 5)

Saída: Retorne o k-ésimo menor elemento."""

def quickselect(arr, k):
    """Retorna o k-ésimo menor elemento usando Quickselect. O(n) esperado."""

    # Função auxiliar de partição
    def partition(left, right, pivot_index):
        pivot = arr[pivot_index]               # pega o valor do pivô
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]  # coloca pivot no fim
        store = left                           # posição para ordenar menores
        for i in range(left, right):           # percorre o intervalo
            if arr[i] < pivot:                 # se menor que o pivô
                arr[i], arr[store] = arr[store], arr[i]  # troca
                store += 1
        arr[store], arr[right] = arr[right], arr[store]  # coloca pivot no centro
        return store

    left, right = 0, len(arr)-1

    while True:
        pivot_index = (left + right) // 2      # pivô simples: meio
        pos = partition(left, right, pivot_index)

        if pos == k:                           # achou a posição exata
            return arr[pos]
        elif pos < k:
            left = pos + 1                     # busca à direita
        else:
            right = pos - 1                    # busca à esquerda

# Teste simples
print("Q1:", quickselect([9,1,5,3,7,2,8], 3))  # esperado: 5


# QUESTÃO 2 — ENCONTRAR A MEDIANA USANDO QUICKSELECT
"""Enunciado:
Dado um vetor de tamanho N (N ímpar), encontre a mediana
utilizando Quickselect.

Exemplo:
  arr = [12, 7, 3, 9, 14]
  mediana = 9"""

def mediana_quickselect(arr):
    """Mede a mediana usando Quickselect O(n) esperado."""
    n = len(arr)
    k = n // 2                 # índice da mediana
    return quickselect(arr, k)

print("Q2:", mediana_quickselect([12,7,3,9,14]))  # esperado: 9


# QUESTÃO 3 — MEDIANA DAS MEDIANAS PARA SELEÇÃO EXATA
"""
Enunciado:
Implemente o algoritmo Mediana das Medianas,
que garante O(n) no pior caso para encontrar o k-ésimo menor.

Usar grupos de 5 elementos para escolher o pivô robusto.

Exemplo:
  arr = [8,2,6,4,5,1,9,7,3]
  k = 4
  4º menor = 5
"""

def partition_mm(arr, left, right, pivot):
    """Particiona com pivô dado e retorna o índice final do pivô."""
    for i in range(left, right+1):
        if arr[i] == pivot:                    # acha o pivô
            arr[i], arr[right] = arr[right], arr[i]
            break
    store = left
    for i in range(left, right):
        if arr[i] < pivot:                     # move menores
            arr[i], arr[store] = arr[store], arr[i]
            store += 1
    arr[store], arr[right] = arr[right], arr[store]  # coloca pivô
    return store

def mediana_das_medianas(arr, left, right):
    """Retorna a mediana das medianas."""
    n = right - left + 1

    if n <= 5:                                 # caso base: ordena pequeno
        sub = sorted(arr[left:right+1])
        return sub[n // 2]

    medians = []
    i = left
    while i <= right:
        grupo = arr[i : min(i+5, right+1)]     # grupo de 5
        grupo.sort()
        medians.append(grupo[len(grupo)//2])   # adiciona mediana do grupo
        i += 5

    return mediana_das_medianas(medians, 0, len(medians)-1)

def select_bfprt(arr, left, right, k):
    """Seleciona k-ésimo menor (0-indexado) em O(n) pior caso."""
    if left == right:
        return arr[left]

    pivot = mediana_das_medianas(arr, left, right)
    pos = partition_mm(arr, left, right, pivot)

    if pos == k:
        return arr[pos]
    elif pos < k:
        return select_bfprt(arr, pos+1, right, k)
    else:
        return select_bfprt(arr, left, pos-1, k)

# Teste
print("Q3:", select_bfprt([8,2,6,4,5,1,9,7,3], 0, 8, 4))  # esperado: 5


# QUESTÃO 4 — ENCONTRAR O 10% MENOR ELEMENTO (SELEÇÃO PERCENTIL)
"""
Enunciado:
Dado um vetor grande, encontre o elemento que está no percentil p.
(p é dado entre 0 e 100)

Use Quickselect.

Exemplo:
  arr = [10, 40, 90, 20, 50, 60, 30, 80, 70]
  p = 30
  índice = floor(0.30 * 9) = 2
  resposta = 30 (3º menor)
"""

def percentil(arr, p):
    """Retorna o elemento que está no percentil p."""
    idx = int((p/100) * len(arr))      # índice alvo
    idx = min(max(idx,0), len(arr)-1)  # clamp
    return quickselect(arr, idx)

print("Q4:", percentil([10,40,90,20,50,60,30,80,70], 30))  # esperado: 30


# QUESTÃO 5 — MEDIANA DE DOIS VETORES (SELEÇÃO POR FUSÃO VIRTUAL)
"""
Enunciado:
Dado dois vetores A e B NÃO concatená-los explícitamente.
Encontre a mediana da união A ∪ B usando seleção.

Use o princípio do "k-th smallest" usando busca binária + seleção.

Exemplo:
  A = [1,3,5]
  B = [2,4,6]
  união ordenada = [1,2,3,4,5,6]
  mediana = (3 + 4) / 2 = 3.5
"""

def kth_smallest_2arrays(A, B, k):
    """Retorna o k-ésimo menor considerando 0-index (A,B ordenados)."""
    # Garantir que A é o menor vetor
    if len(A) > len(B):
        return kth_smallest_2arrays(B, A, k)

    if not A:                       # se A vazio, retorna direto de B
        return B[k]

    if k == 0:
        return min(A[0], B[0])

    ia = min(len(A)-1, k//2)        # divide proporção do k
    ib = k - ia - 1

    if A[ia] > B[ib]:
        return kth_smallest_2arrays(A, B[ib+1:], k - (ib+1))
    else:
        return kth_smallest_2arrays(A[ia+1:], B, k - (ia+1))

def mediana_2arrays(A, B):
    """Calcula mediana da união de A e B."""
    n = len(A) + len(B)
    if n % 2 == 1:
        return kth_smallest_2arrays(A, B, n//2)
    else:
        m1 = kth_smallest_2arrays(A, B, n//2 - 1)
        m2 = kth_smallest_2arrays(A, B, n//2)
        return (m1 + m2) / 2

# Teste
print("Q5:", mediana_2arrays([1,3,5], [2,4,6]))  # esperado: 3.5


# QUESTÃO 6 — K-ÉSIMO MAIOR TEMPO DE RESPOSTA NO SERVIDOR
"""
Contexto:
Um servidor registra os tempos de resposta (ping) de milhares de jogadores.
Queremos o k-ésimo MAIOR ping, mas ordenar toda a lista seria caro.

Tarefa:
Use Quickselect adaptado para retornar o k-ésimo maior.
"""

def quickselect_kth_largest(arr, k):
    """Retorna o k-ésimo maior valor usando Quickselect. O(n) esperado."""

    # Convertendo k-ésimo maior para índice equivalente do menor
    # exemplo: k=1 maior => índice = n-1
    k_index = len(arr) - k

    # Função auxiliar de partição (mesma do quickselect)
    def partition(left, right, pivot_index):
        pivot = arr[pivot_index]                             # valor do pivô
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]  # põe pivô no fim
        store = left                                         # posição para menores
        for i in range(left, right):
            if arr[i] < pivot:                               # coloca menores antes
                arr[i], arr[store] = arr[store], arr[i]
                store += 1
        arr[store], arr[right] = arr[right], arr[store]      # pivô no lugar final
        return store                                          # índice final do pivô

    left, right = 0, len(arr)-1

    while True:
        pivot_index = (left + right) // 2                    # pivô = meio
        pos = partition(left, right, pivot_index)            # posiciona pivô

        if pos == k_index:                                   # achou o índice alvo
            return arr[pos]
        elif pos < k_index:                                  # procurar à direita
            left = pos + 1
        else:                                                # procurar à esquerda
            right = pos - 1

# Teste
print("Q6:", quickselect_kth_largest([50, 10, 90, 30, 70, 20], 2))  # 2º maior → 70



# QUESTÃO 7 — SOLDADO MEDIANO (MEDIANA DAS MEDIANAS)
"""
Contexto:
Uma fila de soldados com alturas aleatórias.
O comandante quer encontrar o soldado que ocupa a posição mediana,
mas precisa ser rápido e robusto (garantia de O(n)).

Tarefa:
Usar Mediana das Medianas para encontrar a mediana exata.
"""

def partition_mm(arr, left, right, pivot):
    """Particiona usando pivô indicado e retorna a posição final."""
    for i in range(left, right+1):
        if arr[i] == pivot:                         # encontra pivô
            arr[i], arr[right] = arr[right], arr[i] # move pivô p/ fim
            break

    store = left
    for i in range(left, right):
        if arr[i] < pivot:                          # elementos menores
            arr[i], arr[store] = arr[store], arr[i]
            store += 1

    arr[store], arr[right] = arr[right], arr[store] # pivô no lugar
    return store

def mediana_das_medianas(arr, left, right):
    """Escolhe um pivô robusto pelo método BFPRT."""
    n = right - left + 1

    if n <= 5:                                      # caso pequeno
        sub = sorted(arr[left:right+1])
        return sub[n//2]

    medians = []
    i = left

    while i <= right:
        grupo = arr[i : min(i+5, right+1)]          # grupo de até 5
        grupo.sort()
        medians.append(grupo[len(grupo)//2])        # mediana do grupo
        i += 5

    return mediana_das_medianas(medians, 0, len(medians)-1)

def bfprt(arr, left, right, k):
    """Seleciona o k-ésimo menor elemento usando BFPRT."""
    if left == right:
        return arr[left]

    pivot = mediana_das_medianas(arr, left, right)
    pos = partition_mm(arr, left, right, pivot)

    if pos == k:
        return arr[pos]
    elif pos < k:
        return bfprt(arr, pos+1, right, k)
    else:
        return bfprt(arr, left, pos-1, k)

def mediana_bfprt(arr):
    """Retorna a mediana usando BFPRT."""
    n = len(arr)
    k = n // 2
    return bfprt(arr, 0, n-1, k)

# Teste
print("Q7:", mediana_bfprt([170, 180, 175, 160, 165]))  # esperado: 170



# QUESTÃO 8 — OS M MENORES PRODUTOS DO MARKETPLACE
"""
Contexto:
Dada uma lista enorme de preços, queremos encontrar os M menores preços,
mas sem ordenar tudo.

Tarefa:
Use Quickselect para separar o array em duas partes:
  - esquerda: contém os M menores (não necessariamente ordenados)
  - direita: o restante
"""

def m_menores(arr, m):
    """Retorna lista contendo os M menores elementos (desordenados)."""

    if m <= 0:
        return []

    if m >= len(arr):
        return arr.copy()

    # Quickselect até o índice m-1
    quickselect(arr, m-1)            # usa função da questão 1 (já definida acima)

    # Os M menores estão nas posições 0..m-1
    return arr[:m]

# Teste
print("Q8:", m_menores([40,10,50,20,30,5,90], 3))   # esperado: [5,10,20] (ordem interna pode variar)



# QUESTÃO 9 — K-ÉSIMO MENOR EM FLUXO (ONLINE SELECTION)
"""Contexto: Recebemos uma sequência contínua de valores (temperaturas).
Precisamos manter o k-ésimo menor valor a cada nova leitura sem guardar tudo.
Tarefa:
Manter duas heaps:
  - max_heap (com os k menores valores)
  - min_heap (com os demais)
O topo da max_heap contém o k-ésimo menor."""

import heapq

class KthSmallestStream:
    def __init__(self, k):
        self.k = k
        self.max_heap = []       # guardará os k menores (valores negativos para simular max-heap)
        self.min_heap = []       # o restante

    def add(self, value):
        """Insere valor no fluxo mantendo o k-ésimo menor acessível."""

        if len(self.max_heap) < self.k:
            heapq.heappush(self.max_heap, -value)        # insere no max-heap
        else:
            if value < -self.max_heap[0]:                # se é menor que o maior dos k menores
                heapq.heappush(self.max_heap, -value)
                moved = -heapq.heappop(self.max_heap)    # mantém tamanho = k
                heapq.heappush(self.min_heap, moved)
            else:
                heapq.heappush(self.min_heap, value)     # vai direto p/ min-heap

    def kth_smallest(self):
        """Retorna o k-ésimo menor atual."""
        if len(self.max_heap) < self.k:
            return None
        return -self.max_heap[0]

# Teste
stream = KthSmallestStream(3)
for x in [50,20,10,40,30]:
    stream.add(x)
print("Q9:", stream.kth_smallest())   # 3º menor → 30



# QUESTÃO 10 — ESCOLHA DO PIVÔ IDEAL PARA QUICKSORT
"""Contexto:
O QuickSort perdeu desempenho em casos adversos.
Precisamos escolher um pivô robusto usando Mediana das Medianas.

Tarefa:
Criar apenas a função choose_pivot(arr) que retorna um pivô robusto."""

def choose_pivot(arr):
    """Retorna pivô robusto usando BFPRT (Mediana das Medianas)."""
    return mediana_das_medianas(arr, 0, len(arr)-1)

# Teste
print("Q10:", choose_pivot([12,5,70,1,40,30,25]))  # pivô aproximado da mediana → 25 ou 30
