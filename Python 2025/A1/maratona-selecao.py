"""
===============================================
5 QUESTÕES DE MARATONA – ALGORITMOS DE SELEÇÃO
(Quickselect, Mediana das Medianas)
Todas com enunciado + solução comentada
===============================================
"""

# --------------------------------------------------------------
# QUESTÃO 1 — QUICKSELECT BÁSICO
# --------------------------------------------------------------
"""
Enunciado:
Dado um vetor de inteiros e um valor k (0-indexado), encontre
o k-ésimo menor elemento usando o algoritmo Quickselect.

Entrada de exemplo:
  arr = [9, 1, 5, 3, 7, 2, 8]
  k = 3   (3º menor → resposta = 5)

Saída:
  Retorne o k-ésimo menor elemento.
"""

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


# --------------------------------------------------------------
# QUESTÃO 2 — ENCONTRAR A MEDIANA USANDO QUICKSELECT
# --------------------------------------------------------------
"""
Enunciado:
Dado um vetor de tamanho N (N ímpar), encontre a mediana
utilizando Quickselect.

Exemplo:
  arr = [12, 7, 3, 9, 14]
  mediana = 9
"""

def mediana_quickselect(arr):
    """Mede a mediana usando Quickselect O(n) esperado."""
    n = len(arr)
    k = n // 2                 # índice da mediana
    return quickselect(arr, k)

print("Q2:", mediana_quickselect([12,7,3,9,14]))  # esperado: 9


# --------------------------------------------------------------
# QUESTÃO 3 — MEDIANA DAS MEDIANAS (BFPRT) PARA SELEÇÃO EXATA
# --------------------------------------------------------------
"""
Enunciado:
Implemente o algoritmo Mediana das Medianas (BFPRT),
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
    """Retorna a mediana das medianas (BFPRT)."""
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


# --------------------------------------------------------------
# QUESTÃO 4 — ENCONTRAR O 10% MENOR ELEMENTO (SELEÇÃO PERCENTIL)
# --------------------------------------------------------------
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


# --------------------------------------------------------------
# QUESTÃO 5 — MEDIANA DE DOIS VETORES (SELEÇÃO POR FUSÃO VIRTUAL)
# --------------------------------------------------------------
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


"""
===============================================================
5 QUESTÕES – ALGORITMOS DE SELEÇÃO (COM CONTEXTO)
Enunciados + soluções completas + comentários linha a linha
===============================================================
"""

# --------------------------------------------------------------
# QUESTÃO 6 — K-ÉSIMO MAIOR TEMPO DE RESPOSTA NO SERVIDOR
# --------------------------------------------------------------
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



# --------------------------------------------------------------
# QUESTÃO 7 — SOLDADO MEDIANO (MEDIANA DAS MEDIANAS)
# --------------------------------------------------------------
"""
Contexto:
Uma fila de soldados com alturas aleatórias.
O comandante quer encontrar o soldado que ocupa a posição mediana,
mas precisa ser rápido e robusto (garantia de O(n)).

Tarefa:
Usar Mediana das Medianas (BFPRT) para encontrar a mediana exata.
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



# --------------------------------------------------------------
# QUESTÃO 8 — OS M MENORES PRODUTOS DO MARKETPLACE
# --------------------------------------------------------------
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



# --------------------------------------------------------------
# QUESTÃO 9 — K-ÉSIMO MENOR EM FLUXO (ONLINE SELECTION)
# --------------------------------------------------------------
"""
Contexto:
Recebemos uma sequência contínua de valores (temperaturas).
Precisamos manter o k-ésimo menor valor a cada nova leitura sem guardar tudo.

Tarefa:
Manter duas heaps:
  - max_heap (com os k menores valores)
  - min_heap (com os demais)
O topo da max_heap contém o k-ésimo menor.
"""

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



# --------------------------------------------------------------
# QUESTÃO 10 — ESCOLHA DO PIVÔ IDEAL PARA QUICKSORT
# --------------------------------------------------------------
"""
Contexto:
O QuickSort perdeu desempenho em casos adversos.
Precisamos escolher um pivô robusto usando Mediana das Medianas.

Tarefa:
Criar apenas a função choose_pivot(arr) que retorna um pivô robusto.
"""

def choose_pivot(arr):
    """Retorna pivô robusto usando BFPRT (Mediana das Medianas)."""
    return mediana_das_medianas(arr, 0, len(arr)-1)

# Teste
print("Q10:", choose_pivot([12,5,70,1,40,30,25]))  # pivô aproximado da mediana → 25 ou 30
