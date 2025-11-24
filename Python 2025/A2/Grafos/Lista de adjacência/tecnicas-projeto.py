""" 1) Agendamento de tarefas: Dado o conjunto de tarefas T = {t1,t2,..,tn} com n elementos, cada uma com um tempo
de início start[tk] e um tempo de término end[tk], encontre o maior subconjunto de tarefas que pode ser alocado 
sem sobreposição temporal."""

# Algoritmo de Agendamento de Tarefas sem Sobreposição
# Estratégia: Greedy (gulosa) — selecionar sempre a tarefa que termina primeiro.

def agendar_tarefas(tarefas):
    """ Recebe uma lista de tarefas, onde cada tarefa é uma tupla: (inicio, fim, nome)
    Ex.: (1, 4, "t1")
    Retorna o maior subconjunto possível de tarefas sem sobreposição."""

    # ORDENAR AS TAREFAS PELO TEMPO DE TÉRMINO
    tarefas_ordenadas = sorted(tarefas, key=lambda t: t[1])

    # Conjunto/Lista de tarefas selecionadas
    selecionadas = []

    # INSERIR A PRIMEIRA TAREFA DA LISTA
    # Como está ordenado pelo fim, a primeira é sempre válida para iniciar a construção da solução ótima.
    primeira = tarefas_ordenadas[0]
    selecionadas.append(primeira)

    # Guardamos a última tarefa aceita, pois precisamos verificar conflitos
    ultima_tarefa = primeira

    # PERCORRER TODAS AS OUTRAS TAREFAS
    for tarefa in tarefas_ordenadas[1:]:
        inicio_atual = tarefa[0]
        fim_ultima   = ultima_tarefa[1]

        # Se o início da tarefa atual for >= ao fim da última aceita:
        # significa que NÃO há sobreposição → podemos alocar.
        if inicio_atual >= fim_ultima:
            selecionadas.append(tarefa)
            ultima_tarefa = tarefa  # Atualiza a última tarefa aceita
    return selecionadas

# COMPLEXIDADE
# Ordenação das tarefas: O(n log n)
# Varredura linear para selecionar tarefas: O(n)
# Complexidade total: θ(n log n)

"""O método guloso funciona quando um problema possui escolhas locais ótimas e subestrutura ótima.
A escolha local ótima significa que podemos decidir a melhor opção naquele instante. 
A subestrutura ótima garante que, depois de feita essa escolha, o restante do problema continua tendo uma solução ótima interna,
permitindo que o processo seja repetido até o fim. 

Para provar que essa estratégia realmente gera a solução ótima global, usamos o argumento de troca (swap argument).
Ele compara uma solução gulosa (G) com qualquer solução ótima (S) e mostra que, se houver diferença, 
podemos substituir em (S) a tarefa escolhida por (G) sem perder validade nem qualidade. 
Repetindo essa troca sempre que necessário, concluímos que existe uma solução ótima idêntica à gulosa, 
provando que a escolha gulosa é correta.
"""

""" 2) Mochila fracionária com método guloso."""

def mochila_fracionaria(itens, pesos, valores, capacidade):
    """
    itens   : lista com IDs ou nomes dos itens
    pesos   : lista com pesos de cada item
    valores : lista com valores de cada item
    capacidade : capacidade total da mochila
    Retorna um vetor M indicando a fração de cada item escolhida.
    """
    n = len(itens)

    # 1) Calcular razao valor/peso de cada item
    # Criamos uma lista de tuplas: (razao, peso, valor, indice)
    lista = []
    for i in range(n):
        razao = valores[i] / pesos[i]
        lista.append((razao, pesos[i], valores[i], i))

    # 2) Ordenar pela razao valor/peso (do maior para o menor)
    lista.sort(reverse=True, key=lambda x: x[0])

    M = [0] * n # Vetor resultado (frações)
    C = capacidade  # capacidade restante

    # 3) Preencher a mochila de forma gulosa
    for razao, peso, valor, idx in lista:
        if C == 0:
            break

        # Se ainda cabe o item inteiro
        if peso <= C:
            M[idx] = 1        # pega o item todo
            C -= peso
        else:
            # so cabe uma fracao do item
            M[idx] = C / peso
            C = 0            # mochila ficou cheia
    return M

# Complexidade:
#   Ordenação: O(n log n)
#   Varredura: O(n)
#   Total: theta(n log n)

"""A prova de otimalidade segue diretamente da estrutura do problema: como itens podem ser fracionados,
nunca é desvantajoso substituir parte de um item com menor valor/peso por outro com valor/peso maior. 
Usando o argumento guloso, podemos mostrar que qualquer solução ótima que não siga essa ordem pode ser transformada, 
por trocas de frações, em outra solução de mesmo peso e valor maior — até coincidir com a solução gulosa. 
Isso garante que escolher sempre o item com maior razão valor/peso leva à solução globalmente ótima.
"""

"""3) Contagem de inversões: dado uma sequência com n números, calcule o número de inversões necessário para torná-la ordenada.
Exemplo: considere a sequência a seguir:  A ={3,7,2,9,5}. O número total de inversões é 4:  (7,2),(3,2),(9,5),(7,5)"""

# Contagem de Inversoes usando o metodo baseado no Merge Sort
# Uma inversao ocorre quando um elemento A[i] > A[j] e i < j. 
# O metodo eficiente divide a lista, conta inversoes na metade esquerda, na metade direita, e depois conta as inversoes
# que acontecem entre as duas metades no momento da combinacao.
# A combinacao (Merge) permite detectar rapidamente quantos elementos da direita "passam na frente" de elementos da esquerda.
# Esse metodo tem complexidade O(n log n).

def count_inversions(A):
    """Retorna uma tupla: (numero_de_inversoes, lista_ordenada)"""
    # Caso base: lista com 1 elemento nao tem inversoes
    if len(A) <= 1:
        return 0, A[:]  # retorna copia da lista para evitar efeitos colaterais

    # 1) Dividir a lista ao meio
    meio = len(A) // 2
    esquerda = A[:meio]
    direita = A[meio:]

    # 2) Contar inversoes recursivamente nas duas metades
    inv_esq, esquerda_ordenada = count_inversions(esquerda)
    inv_dir, direita_ordenada = count_inversions(direita)

    # 3) Contar inversoes ao combinar (merge) as duas metades
    inv_combine, lista_ordenada = merge_and_count(esquerda_ordenada, direita_ordenada)

    # Soma total de inversoes
    total = inv_esq + inv_dir + inv_combine
    return total, lista_ordenada


def merge_and_count(L, R):
    """
    Faz o merge das listas L e R (ambas ordenadas) e conta as inversoes
    entre elementos das duas listas.
    Uma inversao e detectada quando R[j] < L[i], pois significa
    que o elemento de R deveria aparecer antes do elemento de L.
    """

    i = 0  # ponteiro para L
    j = 0  # ponteiro para R
    merged = []
    inversoes = 0

    # Enquanto houver elementos em ambas as listas
    while i < len(L) and j < len(R):
        # Se L[i] <= R[j], entao nao ha inversao aqui
        if L[i] <= R[j]:
            merged.append(L[i])
            i += 1
        else:
            # R[j] < L[i] => todos os elementos restantes em L
            # a partir de i formam inversao com R[j]
            merged.append(R[j])
            inversoes += len(L) - i
            j += 1

    # Coloca os elementos restantes (sem gerar novas inversoes)
    merged.extend(L[i:])
    merged.extend(R[j:])

    return inversoes, merged

# COMPLEXIDADE
# A divisao recursiva gera arvore de altura log n
# A combinacao (merge) em cada nivel custa O(n)
# Total: O(n log n)

"""4) Pares mais próximos: dado uma sequência com n pontos em um plano, encontre o par com a menor distância euclidiana"""
# Metodo: Dividir e Conquistar (Divide and Conquer)
# Complexidade: O(n log n)
# Ideia geral:
# - Ordenamos os pontos inicialmente pelo eixo x.
# - Dividimos em duas metades.
# - Encontramos o par mais proximo na metade esquerda e direita.
# - Seja delta = distancia minima encontrada ate agora.
# - Combinamos os resultados verificando apenas os pontos que
#   estao a uma distancia <= delta da linha divisoria.
# - Por uma propriedade geometrica, basta comparar um ponto
#   com no maximo 6 ou 7 pontos seguintes na faixa.

import math
# Funcao para calcular distancia entre dois pontos (x1,y1), (x2,y2)
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Funcao principal que inicia o processo
def closest_pairs(P):
    # Ordena os pontos pelo eixo X (passo inicial fundamental)
    P_ordenado = sorted(P, key=lambda x: x[0])
    return closest_pairs_rec(P_ordenado)

# Funcao recursiva do algoritmo
def closest_pairs_rec(P):
    n = len(P)

    # Caso base: listas muito pequenas podem ser resolvidas diretamente
    if n <= 3:
        return brute_force(P)

    # 1) Dividir a lista de pontos
    meio = n // 2
    Pl = P[:meio]   # metade esquerda
    Pr = P[meio:]   # metade direita

    # 2) Resolver recursivamente
    parL, deltaL = closest_pairs_rec(Pl)
    parR, deltaR = closest_pairs_rec(Pr)

    # 3) Melhor distancia entre esquerda e direita
    delta = min(deltaL, deltaR)
    melhor_par = parL if delta == deltaL else parR

    # 4) Combinar os resultados:
    # Criar faixa (strip) com pontos proximos da linha divisoria
    x_div = P[meio][0]
    strip = [p for p in P if abs(p[0] - x_div) <= delta]

    # Ordenar a faixa pelo eixo y
    strip.sort(key=lambda x: x[1])

    # 5) Comparar cada ponto com ate 7 seguintes (propriedade geometrica)
    for i in range(len(strip)):
        for j in range(i+1, min(i+7, len(strip))):
            d = dist(strip[i], strip[j])
            if d < delta:
                delta = d
                melhor_par = (strip[i], strip[j])

    # 6) Retorna o melhor par e delta
    return melhor_par, delta


# Metodo força bruta para poucas comparacoes
def brute_force(P):
    melhor = None
    delta = float("inf")

    for i in range(len(P)):
        for j in range(i+1, len(P)):
            d = dist(P[i], P[j])
            if d < delta:
                delta = d
                melhor = (P[i], P[j])

    return melhor, delta

# COMPLEXIDADE
# - Dividimos os pontos em duas metades -> log n niveis
# - Cada nivel faz um merge/combinação O(n)
# - Comparação na faixa (strip): no maximo 7 vizinhos por ponto
# Complexidade total: theta(n log n)

""" 5) Problema (fibonacci): dado um inteiro n≥1 encontre 𝐹n"""
# Problema de Fibonacci – Programacao Dinamica
# Implementacao TOP-DOWN (memoization) e BOTTOM-UP (iterativa)
# Complexidade de ambas: O(n)

# SOLUCAO TOP-DOWN (com memoization)
# Ideia:
#   - Criamos um vetor F onde F[n] guarda o resultado do subproblema.
#   - Se F[n] == -1, significa que ainda nao foi calculado.
#   - Se ja calculou, retornamos o valor imediatamente (evita recursao repetida).
#   - A recursao com memoizacao garante que cada subproblema e resolvido apenas 1 vez.

def fib_topdown_aux(n, F):
    """Funcao auxiliar recursiva com memoization."""
    # Se ainda nao calculamos F[n], resolvemos agora
    if F[n] == -1:
        F[n] = fib_topdown_aux(n - 1, F) + fib_topdown_aux(n - 2, F)
    return F[n]

def fib_topdown(n):
    """Funcao principal do metodo top-down."""
    # Caso base
    if n <= 2:
        return 1

    # Cria um vetor F[1..n]
    F = [-1] * (n + 1)
    F[1] = 1
    F[2] = 1

    # Inicializamos todos os outros valores com -1 (indica nao calculado)
    for i in range(3, n + 1):
        F[i] = -1

    # Chama a funcao recursiva auxiliar
    return fib_topdown_aux(n, F)


# SOLUCAO BOTTOM-UP (iterativa)
# Ideia:
#   - Resolve os subproblemas crescentes: F[1], F[2], F[3], ..., F[n]
#   - Cada termo depende apenas dos dois anteriores.
#   - Armazena tudo em um vetor e retorna F[n] ao final.

def fib_bottomup(n):
    """Implementacao iterativa bottom-up."""
    if n <= 2:
        return 1

    # Vetor F[1..n]
    F = [0] * (n + 1)
    F[1] = 1
    F[2] = 1

    # Preenche o vetor de forma crescente
    for i in range(3, n + 1):
        F[i] = F[i - 1] + F[i - 2]

    return F[n]

# COMPLEXIDADE
# TOP-DOWN:
#   - Cada subproblema (F[k]) e resolvido uma unica vez.
#   - Consultas seguintes usam memoizacao.
#   - Complexidade total: O(n)
#
# BOTTOM-UP:
#   - Computa F[1], F[2], ..., F[n] de forma direta.
#   - Cada iteracao custa O(1).
#   - Complexidade total: O(n)
#
# Ambas tem a mesma complexidade, mas:
#   - Top-down e recursiva e inicia do problema maior.
#   - Bottom-up e iterativa e resolve do menor para o maior.




"""6) Problema Mochila 0/1: Dado um conjunto de itens com pesos w[i] e valores v[i], escolher o subconjunto de itens 
que maximize o valor total, respeitando a capacidade maxima W."""

# ---------------------- SOLUCAO TOP-DOWN ---------------------

def mochila_topdown(n, v, w, W):
    """
    n = quantidade de itens
    v = lista de valores (indexados de 1 a n)
    w = lista de pesos  (indexados de 1 a n)
    W = capacidade maxima da mochila
    """

    # Criacao da matriz M: (n+1) x (W+1)
    # M[j][i] representa: melhor valor usando itens 1..j com capacidade i
    M = [[-1 for _ in range(W + 1)] for _ in range(n + 1)]

    # Inicializa linha j=0 (0 itens → valor = 0)
    for i in range(W + 1):
        M[0][i] = 0

    # Inicializa coluna i=0 (capacidade 0 → valor = 0)
    for j in range(1, n + 1):
        M[j][0] = 0

    # ----------------------
    # Funcao recursiva
    # ----------------------
    def mochila_aux(i, cap):
        # Se já calculado → retorna
        if M[i][cap] != -1:
            return M[i][cap]

        # Se o peso do item é maior que a capacidade → nao usar
        if w[i] > cap:
            M[i][cap] = mochila_aux(i - 1, cap)
        else:
            # Caso contrário: opção de usar ou não usar o item i
            usando = v[i] + mochila_aux(i - 1, cap - w[i])
            nao_usando = mochila_aux(i - 1, cap)
            M[i][cap] = max(usando, nao_usando)

        return M[i][cap]

    # Retorna o resultado final
    return mochila_aux(n, W)



# ---------------------- SOLUCAO BOTTOM-UP --------------------

def mochila_bottomup(n, v, w, W):
    """
    n = quantidade de itens
    v = lista de valores (indexados de 1 a n)
    w = lista de pesos  (indexados de 1 a n)
    W = capacidade maxima da mochila
    """

    # Criacao da matriz M: (n+1) x (W+1)
    M = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Preenche a tabela do menor subproblema para o maior
    for j in range(1, n + 1):
        for cap in range(1, W + 1):

            # Se nao cabe, copia o valor de cima
            if w[j] > cap:
                M[j][cap] = M[j - 1][cap]
            else:
                # Caso contrário: escolher o melhor entre usar ou nao usar
                usando = v[j] + M[j - 1][cap - w[j]]
                nao_usando = M[j - 1][cap]
                M[j][cap] = max(usando, nao_usando)

    # Melhor valor usando n itens e capacidade W
    return M[n][W]

# ---------------------- COMPLEXIDADE -------------------------

# Tanto a abordagem Top-Down (com memoizacao) quanto a Bottom-Up apresentam a MESMA complexidade de tempo e espaço.
# Explicacao:
# - A matriz M possui dimensoes (n+1) x (W+1)
# - Cada entrada M[j][i] eh preenchida apenas UMA vez.
# Portanto:
#   Complexidade de tempo:  Theta(n * W)
#   Complexidade de memoria: Theta(n * W)
# A diferenca eh apenas o fluxo de execucao:
# - Top-Down calcula apenas os subproblemas necessarios (via recursao).
# - Bottom-Up calcula todos os subproblemas de forma iterativa.
# Mesmo assim, no pior caso, ambas as abordagens custam Theta(n * W).
