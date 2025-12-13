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


# QUICKSELECT (k-ésimo menor), Complexidade: Médio O(n)/ Pior O(n²)
def quickselect(v, l, r, x):
    """Retorna o x-ésimo menor elemento do vetor v no intervalo [l, r].
    O algoritmo utiliza a mesma ideia do QuickSort, mas recursiona
    apenas no lado que contém o elemento de interesse, obtendo
    complexidade média O(n).
    v : Vetor de elementos comparáveis (números, por exemplo).
    l : Índice inicial do intervalo considerado (inclusive).
    r : Índice final do intervalo considerado (inclusive).
    x : Ordem estatística desejada (1-indexado).
        Exemplo: x = 1 retorna o menor elemento do intervalo. """

    # Verifica se x está dentro do número de elementos do intervalo [l, r]
    if x > 0 and x <= r - l + 1:
        j = partition(v, l, r)
        # Número de elementos à esquerda do pivô
        # (quantos elementos são estritamente menores ou iguais ao pivô)
        pos_pivo = j - l
        # Caso 1: o pivô é exatamente o x-ésimo menor elemento
        if pos_pivo == x - 1:
            return v[j]
        # Caso 2: o x-ésimo menor elemento está no subvetor esquerdo
        # Mantém x, pois a ordem estatística não muda
        if pos_pivo > x - 1:
            return quickselect(v, l, j - 1, x)
        # Caso 3: o x-ésimo menor elemento está no subvetor direito
        # Ajusta x descontando:
        # - os elementos à esquerda do pivô
        # - o próprio pivô
        return quickselect(v, j + 1, r, x - (pos_pivo + 1))
    return -1

# A complexidade depende da escolha do pivô.
# Se conseguirmos escolher sempre a mediana da sequência em O(n), 
# garantimos que Quickselect também será O(n)







