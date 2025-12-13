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
