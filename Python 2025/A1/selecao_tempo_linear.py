# =============================================================
# PARTITION PADRÃO (pivô = último elemento)
# Complexidade: O(r - l)
# =============================================================
def partition(v, l, r):
    pivot = v[r]               # pivô é o último elemento
    j = l                      # j aponta para a região de valores menores
    for i in range(l, r):      # percorre tudo exceto o pivô
        if v[i] <= pivot:
            # troca manual (sem swap)
            temp = v[i]
            v[i] = v[j]
            v[j] = temp
            j += 1
    # posiciona pivô na posição final
    temp = v[j]
    v[j] = v[r]
    v[r] = temp
    return j


# =============================================================
# PARTITION COM PIVÔ EXTERNO (USADO EM selectMOM)
# Complexidade: O(r - p)
# =============================================================
def partition_with_pivot(v, p, r, pivot_value):
    # Encontrar a posição do pivô
    pivot_index = p
    while pivot_index <= r and v[pivot_index] != pivot_value:
        pivot_index += 1

    # Move pivô para o fim
    temp = v[pivot_index]
    v[pivot_index] = v[r]
    v[r] = temp

    # Particiona exatamente como partition normal
    pivot = v[r]
    j = p
    for i in range(p, r):
        if v[i] <= pivot:
            temp = v[i]
            v[i] = v[j]
            v[j] = temp
            j += 1

    # Coloca pivô na posição final
    temp = v[j]
    v[j] = v[r]
    v[r] = temp
    return j


# =============================================================
# QUICKSORT (para uso interno em medianOf)
# Complexidade: médio O(n log n) / pior O(n²)
# =============================================================
def quicksort(v, l, r):
    if l < r:
        j = partition(v, l, r)
        quicksort(v, l, j - 1)
        quicksort(v, j + 1, r)


# =============================================================
# medianOf — ordena até 5 elementos e retorna a mediana
# Complexidade: O(1) porque n ≤ 5
# =============================================================
def medianOf(v):
    """
    v é uma lista de tamanho de 1 a 5
    retorna o elemento central após ordenar
    """
    arr = v[:]                   # copia para não mexer no original
    quicksort(arr, 0, len(arr) - 1)
    return arr[len(arr) // 2]    # mediana


# =============================================================
# QUICKSELECT (k-ésimo menor — versão igual ao C)
# Complexidade: Médio O(n)
#               Pior O(n²)
# =============================================================
def quickselect(v, l, r, x):
    """
    Retorna o x-ésimo menor elemento no intervalo v[l:r].
    x é 1-indexado (igual ao C).
    """
    if x > 0 and x <= r - l + 1:
        j = partition(v, l, r)

        # Posição do pivô após partição
        if j - l == x - 1:
            return v[j]

        # k está no lado esquerdo
        if j - l > x - 1:
            return quickselect(v, l, j - 1, x)

        # k está no lado direito (ajustar índice)
        return quickselect(v, j + 1, r, x - (j - l + 1))

    return -1


# =============================================================
# SELECT MOM — "Mediana das Medianas"
# Complexidade: O(n) no pior caso (determinístico)
# =============================================================
def selectMOM(v, p, r, k):
    """
    Retorna o k-ésimo menor elemento em v[p:r].
    Usa algoritmo de seleção linear determinístico.
    k é 1-indexado.
    """
    n = r - p + 1
    if k <= 0 or k > n:
        return -1

    # Lista para armazenar medianas dos grupos de 5
    median = []
    pos = p

    # Divide em grupos de 5 e coleta as medianas
    while pos <= r:
        size = r - pos + 1
        group = v[pos : pos + 5]   # pega até 5 elementos
        median.append(medianOf(group))
        pos += 5

    # Se só temos uma mediana, ela é o pivô
    if len(median) == 1:
        mom = median[0]
    else:
        # Recursivamente calcula a mediana das medianas
        mid = len(median) // 2
        mom = selectMOM(median, 0, len(median) - 1, mid + 1)

    # Particiona usando a mediana das medianas como pivô
    j = partition_with_pivot(v, p, r, mom)

    # Achou o k-ésimo menor
    if j - p == k - 1:
        return v[j]

    # Está no lado esquerdo
    if j - p > k - 1:
        return selectMOM(v, p, j - 1, k)

    # Está no lado direito (ajusta índice)
    return selectMOM(v, j + 1, r, k - (j - p + 1))
