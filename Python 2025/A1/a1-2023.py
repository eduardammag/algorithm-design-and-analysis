"""2 - Dada uma sequência A ORDENADA contendo n inteiros distintos,
crie um algoritmo capaz de determinar se existe um índice i tal que:
A[i] = i. A complexidade do pior caso deve ser O(log n)!
IDEIA:
A está ordenada → podemos aplicar busca binária.
Se A[mid] > mid então a solução só pode estar à esquerda.
Se A[mid] < mid então só pode estar à direita.
Se A[mid] == mid → achou!
COMPLEXIDADE: O(log n)"""

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
        """
        Atualiza prioridade de uma tarefa:
        Estratégia simples: remover tudo e reempilhar ajustado.
        Ainda é O(n log n), mas é a solução mais clara em Python.
        Se implementássemos heap de índice manual, seria O(log n).
        """
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

Definição da distância:     |A[i] - a|

Complexidade: O(n)

SOLUÇÃO:
1) Encontrar mediana → Quickselect em O(n)
2) Calcular distâncias O(n)
3) Obter os k menores → Quickselect novamente O(n)
4) Retornar elementos

TOTAL: O(n)
"""

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
Cada número pertence ao conjunto:
    {n², n² + 1, n² + 2, ..., n² + n}

Criar algoritmo que encontre o NÚMERO QUE MAIS SE REPETE.

Observação: como existem n números possíveis e n números na entrada,
pode haver empates — basta retornar qualquer um.

Complexidade O(n).

IDEIA:
    - Todos valores estão no intervalo [n² , n² + n]
    - Podemos usar contagem direta (counting) em vetor de tamanho n+1
    - Frequências em O(n)
"""

def questao5(A):
    n = len(A)
    base = n*n
    freq = [0] * (n+1)   # valores n² ... n²+n

    for x in A:
        freq[x - base] += 1

    # índice de maior frequência
    idx = max(range(n+1), key=lambda i: freq[i])
    return base + idx
