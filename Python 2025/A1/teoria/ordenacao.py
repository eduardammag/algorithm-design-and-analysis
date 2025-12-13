# Bubble Sort Otimizado
def bubble_sort(v):
    n = len(v)
    for j in range(n - 1):                 # Cada passagem completa no vetor
        swapped = False                    # Flag para detectar se houve troca
        for i in range(n - 1):             # Compara cada par adjacente
            if v[i] > v[i + 1]:            # Se estiver fora de ordem
                temp = v[i]                
                v[i] = v[i + 1]
                v[i + 1] = temp
                swapped = True
        if not swapped:                    # Se nenhuma troca ocorreu, vetor já ordenado
            break


# Selection Sort
def selection_sort(v):
    n = len(v)
    for i in range(n - 1):                 # Posição atual onde o menor deve ir
        min_index = i                      # Assume que o mínimo está em i
        for j in range(i + 1, n):          # Procura o menor no restante
            if v[j] < v[min_index]:
                min_index = j
        temp = v[i]
        v[i] = v[min_index]
        v[min_index] = temp


# Insertion Sort
def insertion_sort(v):
    n = len(v)
    for i in range(1, n):                  # Começa do segundo elemento
        current_value = v[i]               # Valor a ser inserido
        j = i - 1
        # Move todos para a direita até achar a posição correta
        while j >= 0 and v[j] > current_value:
            v[j + 1] = v[j]                # Desloca para a direita
            j -= 1
        v[j + 1] = current_value           # Insere o valor


# Função merge para o Merge Sort
def merge(v, startA, startB, endB):
    # Cria vetor temporário com o tamanho exato
    r = [0] * (endB - startA)

    a_index = startA     # Ponteiro do primeiro subvetor
    b_index = startB     # Ponteiro do segundo subvetor
    r_index = 0

    # Intercala até esvaziar algum subvetor
    while a_index < startB and b_index < endB:
        if v[a_index] <= v[b_index]:
            r[r_index] = v[a_index]
            a_index += 1
        else:
            r[r_index] = v[b_index]
            b_index += 1
        r_index += 1

    # Copia o restante da primeira metade
    while a_index < startB:
        r[r_index] = v[a_index]
        a_index += 1
        r_index += 1

    # Copia o restante da segunda metade
    while b_index < endB:
        r[r_index] = v[b_index]
        b_index += 1
        r_index += 1

    # Copia tudo de volta para o vetor original
    for i in range(startA, endB):
        v[i] = r[i - startA]


# Merge Sort
def merge_sort(v, start, end):
    if start < end - 1:               # Existe mais de 1 elemento
        mid = (start + end) // 2      # Divide em duas metades
        merge_sort(v, start, mid)     # Ordena primeira metade
        merge_sort(v, mid, end)       # Ordena segunda metade
        merge(v, start, mid, end)     # Intercala


# Partition do QuickSort
def partition(v, p, r):
    pivot = v[r]                      # Pivô escolhido 
    j = p                             # Marca a região ≤ pivô

    for i in range(p, r):
        if v[i] <= pivot:             # Se pertence à região dos menores
            # troca v[i] e v[j]
            temp = v[i]
            v[i] = v[j]
            v[j] = temp
            j += 1

    # Coloca o pivô na posição final correta
    temp = v[j]
    v[j] = v[r]
    v[r] = temp
    return j


# QuickSort recursivo padrão
def quicksort(v, p, r):
    if p < r:
        j = partition(v, p, r)
        quicksort(v, p, j - 1)
        quicksort(v, j + 1, r)


# QuickSort com tail recursion optimization
def quicksort_optimized(v, p, r):
    while p < r:
        j = partition(v, p, r)
        # Escolhe o menor lado para recursão — otimiza a pilha
        if (j - p) < (r - j):
            quicksort_optimized(v, p, j - 1)
            p = j + 1
        else:
            quicksort_optimized(v, j + 1, r)
            r = j - 1


# Heapify
def heapify(v, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Verifica se left é maior que o atual
    if left < n and v[left] > v[largest]:
        largest = left

    # Verifica se right é maior que o atual
    if right < n and v[right] > v[largest]:
        largest = right

    # Se o maior NÃO era o pai, ajusta a árvore
    if largest != i:
        temp = v[i]
        v[i] = v[largest]
        v[largest] = temp
        heapify(v, n, largest)        # Continua ajustando


# Build Heap
def build_heap(v):
    n = len(v)
    # Começa do último nó que possui filhos até a raiz
    for i in range(n // 2 - 1, -1, -1):
        heapify(v, n, i)


# Heap Sort
def heap_sort(v):
    n = len(v)
    build_heap(v)
    # Extrai um por um do heap
    for i in range(n - 1, 0, -1):
        # Move o maior (v[0]) para o final
        temp = v[0]
        v[0] = v[i]
        v[i] = temp
        heapify(v, i, 0)              # Ajusta o heap reduzido


# COUNTING SORT 
def counting_sort(v, k):
    n = len(v)
    fs = [0] * (k + 1) # fs[k+1]
    temp = [0] * n      # temp[n]

    # Inicializa frequências
    for j in range(k + 1):
        fs[j] = 0

    # Conta ocorrências com deslocamento +1
    for i in range(n):
        fs[v[i] + 1] += 1

    # Soma prefixada
    for j in range(1, k + 1):
        fs[j] += fs[j - 1]

    # Distribuição estável
    for i in range(n):
        j = v[i]
        temp[fs[j]] = v[i]
        fs[j] += 1

    # Copia para o vetor original
    for i in range(n):
        v[i] = temp[i]


# RADIX SORT (LSD)
def radix_sort(v, W, K):
    """
    v = lista onde cada elemento é uma lista de bytes ou string indexável
    W = número de posições (tamanho fixo)
    K = valor máximo possível por caractere (ex: 255)
    """
    n = len(v)
    fp = [0] * (K + 1)     # Vetor de frequências
    aux = [None] * n       # Vetor auxiliar

    for w in range(W - 1, -1, -1):  # do último caractere até o primeiro

        # Zera frequências
        for j in range(K + 1):
            fp[j] = 0

        # Conta ocorrências com deslocamento +1
        for i in range(n):
            fp[v[i][w] + 1] += 1

        # Prefix sum
        for j in range(1, K + 1):
            fp[j] += fp[j - 1]

        # Distribuição estável
        for i in range(n):
            j = v[i][w]
            aux[fp[j]] = v[i]
            fp[j] += 1

        # Copia de volta
        for i in range(n):
            v[i] = aux[i]


# INSERTION SORT (para uso no Bucket Sort)
def insertion_sort(v):
    n = len(v)
    for i in range(1, n):
        current_value = v[i]
        j = i - 1
        while j >= 0 and v[j] > current_value:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = current_value


# BUCKET SORT
def bucket_sort(v):
    """
    bucketSort(float v[], int n)
    - Assume floats no intervalo [0,1)
    - Usa n buckets
    - Cada bucket é ordenado com insertion sort
    """
    n = len(v)

    # Cria lista de buckets (equivalente a vector<float> b[n])
    b = [[] for _ in range(n)]

    # Distribui os elementos nos buckets
    for i in range(n):
        idx = int(n * v[i])    # Calcula índice do bucket igual ao C
        b[idx].append(v[i])

    # Ordena cada bucket usando insertion sort
    for i in range(n):
        insertion_sort(b[i])

    # Junta tudo de volta no vetor
    index = 0
    for i in range(n):
        for j in range(len(b[i])):
            v[index] = b[i][j]
            index += 1


"""
 COMPLEXIDADES DOS ALGORITMOS — RESUMO GERAL

1) BUBBLE SORT (OTIMIZADO)
• Tempo (pior caso):     O(n²)
• Tempo (melhor caso):   O(n)  — detecta quando não há trocas
• Tempo (médio):         O(n²)
• Espaço:                O(1)
• Estável:               SIM
Bubble sort compara pares adjacentes e realiza trocas quando necessário.
A versão otimizada para cedo quando nenhuma troca ocorre em uma iteração.


2) SELECTION SORT
• Tempo (pior caso):     O(n²)
• Tempo (melhor caso):   O(n²)
• Tempo (médio):         O(n²)
• Espaço:                O(1)
• Estável:               NÃO
Seleciona repetidamente o menor elemento e o coloca na frente.
Mesmo se o vetor estiver ordenado, percorre tudo para encontrar o mínimo.


3) INSERTION SORT
• Tempo (pior caso):     O(n²)
• Tempo (melhor caso):   O(n)  — vetor já ordenado
• Tempo (médio):         O(n²)
• Espaço:                O(1)
• Estável:               SIM
Insere cada elemento na posição correta entre os anteriores.


4) MERGE SORT
• Tempo (pior caso):     O(n log n)
• Tempo (melhor caso):   O(n log n)
• Tempo (médio):         O(n log n)
• Espaço:                O(n)  — precisa de vetor auxiliar
• Estável:               SIM
Divide o vetor em duas metades, ordena recursivamente e intercala.
É eficiente e previsível.


5) QUICK SORT (versão básica e versão otimizada por cauda)
• Tempo (pior caso):     O(n²) — pivô ruim (ex: vetor já ordenado)
• Tempo (melhor caso):   O(n log n)
• Tempo (médio):         O(n log n)
• Espaço (pilha recursão):
    - pior caso:         O(n)
    - melhor/médio:      O(log n)
• Estável:               NÃO
Usa divisão em torno de um pivô. A versão otimizada sempre recursa no lado
menor, reduzindo o consumo da pilha (tail recursion optimization).


6) HEAP SORT
• Tempo (pior caso):     O(n log n)
• Tempo (melhor caso):   O(n log n)
• Tempo (médio):         O(n log n)
• Espaço:                O(1)
• Estável:               NÃO
Constrói um heap máximo e repete extraindo o maior elemento.


7) COUNTING SORT
• Tempo:                 O(n + k)
• Espaço:                O(n + k)
• Estável:               SIM
Funciona apenas para inteiros pequenos (faixa limitada). Usa contagem
de frequências e prefix sums para distribuir ordenadamente.


8) RADIX SORT (LSD para bytes/strings)
• Tempo:                 O(W * (n + K))
  onde:
     W = número de dígitos/caracteres
     K = faixa de valores (ex: 255)
• Espaço:                O(n + K)
• Estável:               SIM
Aplica counting sort em cada posição (da menos significativa para a mais).


9) BUCKET SORT (para floats em [0,1))
• Tempo (médio):         O(n)      — distribuição uniforme
• Tempo (pior caso):     O(n²)     — todos no mesmo bucket
• Espaço:                O(n)
• Estável:               SIM (usando insertion sort)
Distribui elementos em n baldes, ordena cada balde individualmente
(geralmente com insertion sort) e concatena os resultados.


10) SELEÇÃO LINEAR (QUICKSELECT) — citado no início
• Tempo (pior caso):     O(n²)
• Tempo (médio):         O(n)
• Espaço:                O(1)
Algoritmo semelhante ao quicksort, mas apenas recursa no lado que contém
o k-ésimo menor elemento.


11) MEDIANA DAS MEDIANAS (SELECT EXATO) — citado no início
• Tempo (pior caso):     O(n)
• Espaço:                O(1) ou O(log n) dependendo da forma
Escolhe o pivô de forma determinística garantindo tempo linear no pior caso.


12) BUSCA BINÁRIA (citada no início da conversa)
• Tempo:                 O(log n)
• Espaço:                O(1)
Busca em vetor ordenado dividindo ao meio repetidamente.


13) ÁRVORE BINÁRIA DE BUSCA (citada no início da conversa)
• Busca/Inserção/Remoção:
    - melhor/médio:      O(log n)
    - pior caso:         O(n)  — se ficar degenerada
• Espaço:                O(n)
Estrutura que mantém os elementos com ordem relativa,
mas depende do balanceamento.


14) TABELA HASH — ENCADEAMENTO (citada no início)
• Busca/Inserção/Remoção:
    - médio caso:        O(1)
    - pior caso:         O(n)
• Espaço:                O(n)
Usa listas ligadas ou vetores para armazenar colisões.


15) TABELA HASH — ENDEREÇAMENTO ABERTO (citada no início)
• Busca/Inserção/Remoção:
    - médio caso:        O(1)
    - pior caso:         O(n)
• Espaço:                O(n)
Resolve colisões sondando posições alternativas no próprio vetor.


RESUMO FINAL
- Algoritmos O(n log n): merge sort, quicksort (médio), heap sort.
- Algoritmos quadráticos: bubble, selection, insertion (exceto melhores casos).
- Algoritmos lineares: counting sort, radix sort, bucket sort (médio),
  quickselect (médio), mediana das medianas (pior caso).
="""
