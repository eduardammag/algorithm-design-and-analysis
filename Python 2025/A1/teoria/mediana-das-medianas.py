# PARTITION COM PIVÔ EXTERNO (usado no algoritmo SelectMOM)
# Complexidade: O(r - p)

# PARTITION PADRÃO
def partition(v, l, r):
    """Particiona o vetor v no intervalo [l, r] escolhendo o último elemento como pivô.
    Ao final da execução:
    - Todos os elementos em v[l : j] são menores ou iguais ao pivô
    - v[j] contém o pivô em sua posição final correta
    - Todos os elementos em v[j+1 : r] são maiores que o pivô
    v : Vetor de elementos comparáveis.
    l : Índice inicial do intervalo a ser particionado (inclusive).
    r : Índice final do intervalo a ser particionado (inclusive).
    j : Índice final do pivô após a partição.
    Complexidade: O(r - l). Percorre cada elemento do intervalo exatamente uma vez."""
    pivot = v[r]
    # j marca a fronteira entre:
    # - v[l : j-1] -> elementos <= pivô
    # - v[j : i-1] -> elementos > pivô (região ainda desorganizada)
    j = l
    # Percorre o vetor do início do intervalo até antes do pivô
    for i in range(l, r):
        # Se o elemento atual é menor ou igual ao pivô,
        # ele deve pertencer à região da esquerda
        if v[i] <= pivot:
            # Troca v[i] com v[j], expandindo a região <= pivô
            v[i], v[j] = v[j], v[i]
            j += 1  # Avança a fronteira dos elementos menores
    # Após o laço:
    # - v[l : j-1] contém todos os elementos <= pivô
    # - v[j : r-1] contém elementos > pivô
    # Agora colocamos o pivô exatamente entre essas duas regiões
    v[j], v[r] = v[r], v[j]
    return j


def partition_with_pivot(v, p, r, pivot_value):
    """
    Particiona o vetor v no intervalo [p, r] utilizando um pivô
    cujo valor é fornecido externamente (pivot_value).

    O algoritmo primeiro localiza uma ocorrência do valor do pivô
    dentro do intervalo, move esse pivô para o final e então aplica
    o particionamento padrão (Lomuto).

    Ao final:
    - v[p : j] contém elementos <= pivô
    - v[j] contém o pivô em sua posição final correta
    - v[j+1 : r] contém elementos > pivô

    Parâmetros:
    ----------
    v : list
        Vetor de elementos comparáveis. A operação é feita in-place.
    p : int
        Índice inicial do intervalo (inclusive).
    r : int
        Índice final do intervalo (inclusive).
    pivot_value : any
        Valor do pivô escolhido externamente (ex.: mediana das medianas).

    Retorno:
    -------
    j : int
        Índice final do pivô após a partição.

    Complexidade:
    -------------
    Tempo: O(r - p)
    Espaço: O(1)
    """

    # 1) Localiza uma ocorrência do valor do pivô no intervalo
    pivot_index = p
    while pivot_index <= r and v[pivot_index] != pivot_value:
        pivot_index += 1

    # 2) Move o pivô para o final do intervalo
    #    (pré-requisito do esquema de Lomuto)
    v[pivot_index], v[r] = v[r], v[pivot_index]

    # 3) Particionamento padrão (Lomuto)
    pivot = v[r]   # pivô agora está no final
    j = p          # fronteira dos elementos <= pivô

    for i in range(p, r):
        # Se o elemento pertence à região esquerda
        if v[i] <= pivot:
            v[i], v[j] = v[j], v[i]
            j += 1

    # 4) Coloca o pivô entre as duas regiões
    v[j], v[r] = v[r], v[j]

    return j


# QUICKSORT (uso interno para ordenar pequenos vetores)
# Complexidade: médio O(n log n) / pior O(n²)
def quicksort(v, l, r):
    """
    Ordena o vetor v no intervalo [l, r] usando QuickSort.

    Esta implementação é usada apenas internamente para vetores
    muito pequenos (até 5 elementos), o que evita o pior caso
    na prática.

    Parâmetros:
    ----------
    v : list
        Vetor a ser ordenado (in-place).
    l : int
        Índice inicial do intervalo.
    r : int
        Índice final do intervalo.
    """
    if l < r:
        j = partition(v, l, r)
        quicksort(v, l, j - 1)
        quicksort(v, j + 1, r)


# medianOf — retorna a mediana de até 5 elementos
# Complexidade: O(1), pois n ≤ 5
def medianOf(v):
    """
    Retorna a mediana de um vetor de tamanho entre 1 e 5.

    O vetor original não é modificado. A função cria uma cópia,
    ordena os elementos e retorna o valor central.

    Parâmetros:
    ----------
    v : list
        Lista de tamanho 1 ≤ |v| ≤ 5.

    Retorno:
    -------
    mediana : any
        O elemento mediano após a ordenação.
    """
    arr = v[:]  # cópia defensiva para não alterar o vetor original
    quicksort(arr, 0, len(arr) - 1)
    return arr[len(arr) // 2]


# SELECT MOM — Seleção determinística (Mediana das Medianas)
# Complexidade: O(n) no pior caso
def selectMOM(v, p, r, k):
    """
    Retorna o k-ésimo menor elemento do vetor v no intervalo [p, r],
    utilizando o algoritmo determinístico Median of Medians (MOM).

    O algoritmo garante tempo linear O(n) no pior caso ao escolher
    um pivô "bom" (mediana das medianas).

    Parâmetros:
    ----------
    v : list
        Vetor de elementos comparáveis.
        O vetor é modificado in-place durante a execução.
    p : int
        Índice inicial do intervalo (inclusive).
    r : int
        Índice final do intervalo (inclusive).
    k : int
        Ordem estatística desejada (1-indexado).
        Ex.: k = 1 retorna o menor elemento.

    Retorno:
    -------
    elemento : any
        O k-ésimo menor elemento do intervalo.

    Retorna -1 se k estiver fora do intervalo válido.
    """

    n = r - p + 1

    # Verificação de validade de k
    if k <= 0 or k > n:
        return -1

    # 1) Divide o vetor em grupos de 5 elementos
    #    e coleta as medianas de cada grupo
    medians = []
    pos = p

    while pos <= r:
        group = v[pos : min(pos + 5, r + 1)]
        medians.append(medianOf(group))
        pos += 5

    # 2) Encontra a mediana das medianas (pivô)
    if len(medians) == 1:
        mom = medians[0]
    else:
        mid = len(medians) // 2
        mom = selectMOM(medians, 0, len(medians) - 1, mid + 1)

    # 3) Particiona o vetor usando o pivô determinístico
    j = partition_with_pivot(v, p, r, mom)

    # 4) Decide em qual lado está o k-ésimo menor
    if j - p == k - 1:
        return v[j]

    if j - p > k - 1:
        return selectMOM(v, p, j - 1, k)

    return selectMOM(v, j + 1, r, k - (j - p + 1))
