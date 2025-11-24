# 1)Dada uma sequência A ordenada com n números distintos, projete um algoritmo
# que encontre os k elementos mais próximos do valor contido em uma posição x.
# O algoritmo deve rodar em O(k). A proximidade entre Ai e Aj é |Ai – Aj|.

# Ideia da solução:
# A sequência está ordenada, então basta iniciar dois ponteiros:
# - um à esquerda de x
# - um à direita de x
# e ir escolhendo sempre o mais próximo de A[x].
# Como fazemos k escolhas, a complexidade é O(k).

def k_mais_proximos(A, x, k):
    """
    Encontra os k elementos mais próximos de A[x] usando dois ponteiros.
    Complexidade: O(k).
    """
    n = len(A)
    alvo = A[x]

    # Ponteiros para os lados
    i = x - 1   # esquerda
    j = x + 1   # direita

    resultado = []

    # Repetimos K vezes
    for _ in range(k):
        # Escolhe o mais próximo enquanto ambos ponteiros são válidos
        if i >= 0 and j < n:
            if abs(A[i] - alvo) <= abs(A[j] - alvo):
                resultado.append(A[i])
                i -= 1
            else:
                resultado.append(A[j])
                j += 1

        # Se só a esquerda existe
        elif i >= 0:
            resultado.append(A[i])
            i -= 1

        # Se só a direita existe
        elif j < n:
            resultado.append(A[j])
            j += 1

        # Se nenhum existe
        else:
            break
    return resultado


# 2) Um mergulhador precisa explorar X metros de um túnel subaquático. 
# Seu tanque cheio permite mergulhar Y metros. Há pontos de abastecimento
# ao longo do túnel (ordenados). Deseja-se minimizar o número de paradas ou indicar impossibilidade.

# Solução: Estratégia gulosa clássica: sempre ir até o mais distante ponto possível
# que ainda esteja dentro do alcance Y desde a última parada.
# Complexidade: O(n).

def min_paradas(X, Y, pontos):
    """ Retorna a lista de paradas necessárias ou None se impossível."""
    pontos = sorted(pontos)
    pontos.append(X)   # Consideramos o final como destino
    paradas = []
    pos_atual = 0       # início do túnel
    i = 0
    n = len(pontos)
    while pos_atual + Y < X:
        # Encontrar o ponto mais distante possível a partir de pos_atual
        melhor = pos_atual
        while i < n and pontos[i] <= pos_atual + Y:
            melhor = pontos[i]
            i += 1

        if melhor == pos_atual:
            # Ninguém alcançável → impossível
            return None

        if melhor != X:  # se não estamos no fim, registrar parada
            paradas.append(melhor)

        pos_atual = melhor
    return paradas


# 3) Dado um grafo G não-dirigido, projete um algoritmo que determine se é
# possível remover exatamente K arestas para que o grafo resultante não
# contenha ciclos. Se possível, indicar quais arestas remover.

def remover_k_arestas(n, arestas, K):
    """Remove K arestas que fazem parte de ciclos usando DFS.
    Retorna lista de arestas removidas ou None se impossível."""
    # Construir lista de adjacências
    adj = [[] for _ in range(n)]
    for u, v in arestas:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n
    parent = [-1] * n
    ciclo_arestas = []   # aqui guardamos as arestas que geram ciclo

    def dfs(u):
        visited[u] = True

        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v)

            # Se já foi visitado e não é o pai, achamos um ciclo.
            elif v != parent[u]:
                # Para evitar duplicações, guardamos a aresta padronizada
                if (v, u) not in ciclo_arestas and (u, v) not in ciclo_arestas:
                    ciclo_arestas.append((u, v))

    # Rodamos DFS do grafo inteiro (pode não ser conectado)
    for i in range(n):
        if not visited[i]:
            dfs(i)

    # Verificar se há arestas de ciclo suficientes
    if len(ciclo_arestas) >= K:
        return ciclo_arestas[:K]  # removemos as primeiras K
    else:
        return None

""" 4) a) Defina classes P, NP, NP-Difícil e NP-Completo."""
# P: Problemas decidíveis por um algoritmo determinístico em tempo polinomial.
# NP: Problemas para os quais a verificação de uma solução pode ser feita
# em tempo polinomial.
# NP-Difícil: Todo problema em NP pode ser reduzido a ele em tempo polinomial.
# NP-Completo: Problemas que são simultaneamente NP e NP-Difícil.

"""b) Explique a importância de determinar se P = NP."""
# Se P = NP: Todos os problemas com verificação eficiente também teriam solução eficiente.
# Isso revolucionaria criptografia, otimização, IA, operações, etc.
# Se P ≠ NP: Alguns problemas realmente não têm solução eficiente conhecida.
# Isso justificaria a dificuldade prática de problemas NP-completos.
