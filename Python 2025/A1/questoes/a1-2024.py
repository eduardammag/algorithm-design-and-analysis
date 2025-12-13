""" 3 - Uma empresa de análise de redes sociais tem uma base com milhões de usuários.
Para cada usuário há: id, número de seguidores e índice de engajamento.
Um 'influenciador emergente' é:
    - está no top 10% em engajamento (por engajamento) e
    - NÃO está no top 10% em número de seguidores.
Dada uma sequência A de n tuplas <id, seguidores, engajamento>, identifique
todos os influenciadores emergentes. O algoritmo deve ser O(n).

Observações e requisitos:
- Precisamos identificar os limiares (thresholds) para top 10% de engajamento
  e para top 10% de seguidores e só depois filtrar os elementos entre eles.
- Para garantir O(n) podemos usar seleção linear (quickselect mediano aleatório)
  para encontrar os k-ésimos maiores/menores em tempo linear esperado; com
  particionamento randomizado temos O(n) esperado; com mediana-das-medianas
  podemos garantir O(n) pior-case (mais complexo).
- Implementação abaixo usa quickselect randomizado (O(n) esperado), simples e
  prática; se for obrigatório O(n) pior caso, substitua por seleção determinística.
"""

import random
import math

def quickselect_on_key(arr, k, key=lambda x: x):
    """
    Retorna o k-ésimo menor elemento segundo key (0-indexed) usando quickselect.
    Implementação recursive randomizada: O(n) expected.
    """
    if not arr:
        raise ValueError("arr vazio")
    if len(arr) == 1:
        return arr[0]
    pivot = key(random.choice(arr))
    menores = [x for x in arr if key(x) < pivot]
    iguais  = [x for x in arr if key(x) == pivot]
    maiores = [x for x in arr if key(x) > pivot]
    if k < len(menores):
        return quickselect_on_key(menores, k, key)
    if k < len(menores) + len(iguais):
        return iguais[0]
    return quickselect_on_key(maiores, k - len(menores) - len(iguais), key)

def find_top_percent_threshold(arr, percent, key=lambda x: x):
    """
    Dado arr, retorna o LIMIAR (valor) tal que os elementos >= limiar
    formam aproximadamente o top 'percent' por key.
    percent: por exemplo 0.10 para top 10%
    Nota: lidamos com arredondamentos usando ceil.
    """
    n = len(arr)
    if n == 0:
        return None
    t = math.ceil(percent * n)  # número de elementos no top
    # queremos o k-ésimo maior → equivalente ao (n - t)-ésimo menor (0-indexed)
    k = n - t
    kth_elem = quickselect_on_key(arr, k, key)
    threshold = key(kth_elem)
    return threshold

def identify_emergent_influencers(data):
    """
    data: lista de tuplas (id, seguidores, engajamento)
    Retorna lista de ids que são emergentes (top10% engajamento e não top10% seguidores).
    Complexidade: O(n) expected com quickselect randomizado.
    """
    n = len(data)
    if n == 0:
        return []

    # 1) calcular thresholds
    eng_threshold = find_top_percent_threshold(data, 0.10, key=lambda t: t[2])
    fol_threshold = find_top_percent_threshold(data, 0.10, key=lambda t: t[1])

    # 2) percorrer e filtrar: emergente => eng >= eng_threshold AND seguidores < fol_threshold
    # Observação: dependendo de empates, definimos regras: usamos >= para engajamento top,
    # e < (estritamente menor) para seguidores (para cumprir 'não está no top 10%').
    emergents = []
    for id_u, seguidores, eng in data:
        if eng >= eng_threshold and seguidores < fol_threshold:
            emergents.append(id_u)

    return emergents

"""
Discussão teórica:
- quickselect_on_key com pivô aleatório dá O(n) tempo esperado, O(n^2) pior caso raro.
- Se for exigido O(n) no pior caso, usar seleção determinística (mediana das medianas).
- A fase de filtragem é O(n), portanto total O(n) expected.
"""

"""
QUESTÃO 4 (5 pontos)
nunciado:
Uma sequência A de tamanho n contém inteiros positivos e negativos.

a) Projete um algoritmo O(n^3) capaz de determinar índices i < j tais que
   a soma A[i] + ... + A[j] é máxima.

b) Otimize a solução produzindo um algoritmo O(n^2).

c) Avalie se é possível produzir um algoritmo O(n). Caso seja possível,
   apresente o algoritmo; caso contrário, prove que é impossível.
"""

# (a) ALGORITMO O(n^3) — força bruta completa
def max_subarray_cubico(A):
    """
    Para cada par (i, j) com i <= j, calcula soma A[i..j] somando elementarmente.
    Complexidade: O(n^3) — três loops aninhados (i, j e somador k).
    Retorna (max_sum, i, j)
    """
    n = len(A)
    best_sum = float("-inf")
    best_pair = (None, None)
    for i in range(n):                        # O(n)
        for j in range(i, n):                 # O(n)
            s = 0
            for k in range(i, j+1):           # O(n)
                s += A[k]
            if s > best_sum:
                best_sum = s
                best_pair = (i, j)
    return best_sum, best_pair[0], best_pair[1]


# (b) ALGORITMO O(n^2) — usando somas prefixadas
def max_subarray_quadratico(A):
    """
    Usa somas prefixadas para calcular soma A[i..j] em O(1):
      prefix[0] = 0
      prefix[t] = A[0] + ... + A[t-1]
    Soma(i,j) = prefix[j+1] - prefix[i]
    Duas loops: i e j -> O(n^2)
    Retorna (max_sum, i, j)
    """
    n = len(A)
    prefix = [0] * (n + 1)
    for t in range(1, n+1):                  # O(n)
        prefix[t] = prefix[t-1] + A[t-1]

    best_sum = float("-inf")
    best_pair = (None, None)
    for i in range(n):                        # O(n)
        for j in range(i, n):                 # O(n)
            s = prefix[j+1] - prefix[i]      # O(1)
            if s > best_sum:
                best_sum = s
                best_pair = (i, j)
    return best_sum, best_pair[0], best_pair[1]


# (c) ALGORITMO O(n) — Kadane
def max_subarray_kadane(A):
    """
    Kadane's algorithm:
    - Mantemos 'current_sum' = max soma subarray TERMINANDO no índice atual
    - Atualizamos global 'best_sum' continuamente.
    - Tempo O(n), espaço O(1).
    Retorna (best_sum, start_index, end_index)
    """
    n = len(A)
    best_sum = A[0]
    current_sum = A[0]
    best_start = best_end = 0
    current_start = 0

    for i in range(1, n):
        x = A[i]
        # Se current_sum + x < x, reiniciamos current_sum em x (início novo subarray)
        if current_sum + x < x:
            current_sum = x
            current_start = i
        else:
            current_sum += x

        # Atualiza melhor global
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = i

    return best_sum, best_start, best_end

"""
Análise e justificativas (parte c):
- É POSSÍVEL obter O(n) para o problema do máximo subarray: o algoritmo de Kadane
  resolve exatamente isso em tempo linear e espaço constante. Logo, O(n) é possível.
- Prova (intuitiva) de corretude de Kadane:
  - current_sum mantém a melhor soma de subarray que termina no índice i.
  - Se a soma até i for negativa, estender por i+1 só pioraria, por isso reiniciamos.
  - Todas as somas ótimas são consideradas e best_sum guarda a melhor encontrada.
"""
