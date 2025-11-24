# 1) PROGRAMAÇÃO DINÂMICA – MOCHILA 0/1 (Knapsack)
# Você recebe N itens, cada um com peso e valor. Sua mochila suporta um peso W.
# Encontre o maior valor possível carregando alguns itens (não pode fracionar).
# Ideia: DP clássico: dp[i][w] = melhor valor usando itens até i com capacidade w.

def knapsack_reconstrucao(weights, values, W):
    n = len(weights)

    # DP completa para reconstrução
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Preenche a tabela dp
    for i in range(1, n + 1):
        for w in range(W + 1):
            # não pegar item
            dp[i][w] = dp[i - 1][w]

            # pegar item, se couber
            if weights[i - 1] <= w:
                valor_com_item = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                dp[i][w] = max(dp[i][w], valor_com_item)

    # --- RECONSTRUÇÃO DOS ITENS ---
    escolhidos = []
    w = W

    # Começamos de dp[n][W] e voltamos para dp[0][0]
    for i in range(n, 0, -1):

        # Se dp[i][w] != dp[i-1][w], significa que o item i-1 FOI escolhido
        if dp[i][w] != dp[i - 1][w]:
            escolhidos.append(i - 1)
            w -= weights[i - 1]  # reduz a capacidade para continuar rastreando

    # A reconstrução fica invertida (do último item para o primeiro)
    escolhidos.reverse()
    return dp[n][W], escolhidos



# 2) PROGRAMAÇÃO DINÂMICA – MAIOR SUBSEQUÊNCIA CRESCENTE (LIS)
# #   Dada uma lista, encontre o tamanho da maior subsequência estritamente crescente.
# Ideia: dp[i] = melhor LIS terminando na posição i.

def LIS(arr):
    n = len(arr)
    dp = [1] * n  # LIS mínima é 1 para todo elemento

    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# 3) PROGRAMAÇÃO DINÂMICA – TROCO MÍNIMO (Coin Change)
# Dadas moedas e um valor-alvo, determine o menor número de moedas necessárias
#   para formar esse valor. Caso seja impossível, retorne -1.
# Ideia: dp[a] = menor número de moedas para formar valor 'a'.

def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # zero moedas para fazer zero

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# 4) GULOSO – SELEÇÃO DE ATIVIDADES
# Dada uma lista de atividades com horários de início e fim, encontre o maior
#   número de atividades que podem ser realizadas sem sobreposição.
# Ideia: Sempre pegue a atividade que termina primeiro.

def activity_selection(activities):
    activities.sort(key=lambda x: x[1])  # ordenar pelo tempo de término
    count = 0
    last_end = -1

    for start, end in activities:
        if start >= last_end:
            count += 1
            last_end = end

    return count


# 5) GULOSO – TROCO (versão gulosa)
# Para sistemas de moeda canônica (ex: moedas de 1,5,10,25), o método guloso
#   sempre funciona. Retorne a quantidade total de moedas usadas.
# Ideia: Pegue sempre a maior moeda possível primeiro.

def greedy_coin_change(coins, amount):
    coins.sort(reverse=True)
    count = 0

    for coin in coins:
        if amount == 0:
            break
        use = amount // coin
        count += use
        amount -= use * coin

    return count


# 6) DIVIDIR E CONQUISTAR – MERGE SORT
# Ordene uma lista usando o algoritmo Merge Sort (O(n log n)).
# Ideia: Divide a lista em duas, ordena as partes e intercala.

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Intercala as duas metades
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# 7) DIVIDIR E CONQUISTAR – EXPONENCIAÇÃO RÁPIDA (Fast Power)
# Calcule a^b em tempo O(log b).
#
# Ideia:
#   a^b = (a^(b/2))^2     se b é par
#   a^b = a * (a^(b/2))^2 se b é ímpar

def fast_pow(a, b):
    if b == 0:
        return 1

    half = fast_pow(a, b // 2)

    if b % 2 == 0:
        return half * half
    else:
        return a * half * half


# 8) PROGRAMAÇÃO DINÂMICA – CAMINHO MÍNIMO EM MATRIZ
# #   Dada uma matriz de custos, encontre o custo mínimo para ir de (0,0)
#   até (n-1,m-1), movendo apenas para direita ou para baixo.
#
# Ideia:
#   dp[i][j] = custo mínimo para chegar naquela célula.

def min_path_sum(grid):
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = grid[0][0]

    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                continue

            top = dp[i - 1][j] if i > 0 else float('inf')
            left = dp[i][j - 1] if j > 0 else float('inf')

            dp[i][j] = grid[i][j] + min(top, left)

    return dp[-1][-1]


# 9) GULOSO – COBRIR PONTOS COM INTERVALOS DE TAMANHO FIXO
# #   Dado um conjunto de pontos em uma reta e um intervalo de tamanho L,
#   determine o menor número de intervalos necessários para cobrir todos eles.
# Ideia: Ordenar e sempre iniciar o intervalo no ponto mais à esquerda não coberto.

def cover_points(points, L):
    points.sort()
    count = 0
    i = 0

    while i < len(points):
        start = points[i]
        end = start + L

        count += 1
        i += 1

        while i < len(points) and points[i] <= end:
            i += 1

    return count


# 10) PROGRAMAÇÃO DINÂMICA – SUBARRAY COM MAIOR SOMA (Kadane)
# Encontre a maior soma de uma subsequência CONTÍNUA na lista.
# Ideia: Kadane: soma corrente reinicia quando ficar negativa.

def max_subarray(arr):
    melhor = atual = arr[0]

    for x in arr[1:]:
        atual = max(x, atual + x)
        melhor = max(melhor, atual)

    return melhor
