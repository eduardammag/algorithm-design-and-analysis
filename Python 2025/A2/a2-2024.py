""" 1) Uma organização ambiental desenvolveu um sistema para monitoramento de florestas cuja comunicação é
baseada em uma rede de sensores sem fio. Um sensor A consegue enviar uma mensagem para um sensor B diretamente
se a distância entre eles for menor ou igual ao raio de transmissão s.r em metros.
Dado um conjunto de sensores S, em que cada elemento possui uma localização (s.x, s.y) 
e um raio de transmissão s.r em metros, projete um algoritmo capaz de calcular a rota 
para transmitir uma mensagem entre si e sf através dos sensores da rede, 
de forma que percorra a menor distância possível em metros.
O algoritmo deve retornar uma sequência de sensores representando o caminho completo 
que a mensagem irá percorrer:
— primeiro, os sensores utilizados para enviar a requisição de si até sf;
— em seguida, os sensores utilizados para enviar a resposta de sf até si.
Caso não seja possível estabelecer a comunicação, o algoritmo deve indicar isso.
Analise a complexidade do algoritmo proposto."""

import math
import heapq

def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Constrói o grafo baseado nas capacidades dos sensores
# sensores[i] = (x, y, r)
# Um sensor i pode se conectar a j se a distância entre eles
# for <= ao raio de ambos.
def construir_grafo(sensores):
    n = len(sensores)  # (vértices)
    adj = [[] for _ in range(n)]

    # Avalia todos os pares ordenados (i, j)
    for i in range(n):
        x1, y1, r1 = sensores[i]   
        for j in range(n):
            if i == j:
                continue
            x2, y2, r2 = sensores[j]  
            d = distancia((x1, y1), (x2, y2))
            # Criamos aresta i → j *somente se* o raio de i é suficiente
            # para cobrir a distância até j.
            if d <= r1:
                # Adiciona aresta saindo de i para j, com peso = distância
                adj[i].append((j, d))

    return adj


# Implementação clássica do Dijkstra com min-heap (heapq)
# Retorna o caminho mínimo entre 'start' e 'end'
def dijkstra(adj, start, end):
    n = len(adj)
    dist = [float('inf')] * n                # distâncias mínimas
    parent = [-1] * n                        # para reconstruir caminho
    dist[start] = 0                          # distância do início é 0
    pq = [(0, start)]                        # heap (distância, vértice)
    while pq:
        d, u = heapq.heappop(pq)             # pega vértice de menor distância atual
        if d > dist[u]:                     
            continue
        if u == end:                         # se chegou ao destino, pode parar
            break
        # relaxamento das arestas
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    # se não alcança o destino
    if dist[end] == float('inf'):
        return None
    # reconstrói o caminho em ordem reversa
    path = []
    cur = end
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()                           # inverte para ordem correta
    return path


def rota_completa(sensores, si, sf):
    adj = construir_grafo(sensores)          # constrói o grafo
    ida = dijkstra(adj, si, sf)              # caminho de ida
    volta = dijkstra(adj, sf, si)            # caminho de volta
    if ida is None or volta is None:         # se qualquer lado for impossível
        return None
    return ida + volta[1:]                  # remove duplicação do vértice central (sf)


# ANÁLISE DE COMPLEXIDADE
# rota_completa():
#   - Chama construir_grafo → O(n^2)
#   - Chama dijkstra duas vezes → 2 * O(E log V)
#   - Como o grafo pode ter até E = O(n^2) arestas no pior caso,
#     então: Θ(n² log n)

""" 2) Considere um grafo G = (V, E) conexo e não-dirigido. Dizemos que uma aresta e ∈ E é uma ponte se
sua remoção produzir um grafo G' não-conexo.

a) Se existir uma aresta e = (vi, vj) que não é uma ponte podemos afirmar 
   que existe um ciclo em G que contém os vértices vi e vj. Por quê?

Seja G = (V, E) um grafo conexo e não-dirigido, e seja e = (vi, vj) ∈ E uma aresta que NÃO é ponte.
Por definição, uma aresta não é ponte quando sua remoção NÃO desconecta o grafo.
Portanto, ao removermos e, obtemos G' = (V, E \ {e}), que permanece conexo.
Se G' é conexo, então ainda existe pelo menos um caminho entre vi e vj em G' — isto é,
um caminho que não utiliza a aresta e que foi removida. Podemos representar esse caminho como:

        P = vi → u1 → u2 → ... → uk → vj

Nenhuma das arestas desse caminho é e, já que estamos trabalhando no grafo G' (sem e).
Agora, quando voltamos a considerar a aresta e = (vi, vj) no grafo original G,
o caminho P junto da aresta e formam um ciclo simples:
        vi → u1 → ... → uk → vj --e--> vi

Esse ciclo inclui tanto vi quanto vj.
Portanto:
- Se e NÃO é ponte, sua remoção não separa vi de vj.
- Logo, existe um caminho alternativo entre vi e vj que não usa e.
- E esse caminho, combinado com e, forma necessariamente um ciclo passando por vi e vj.

b) Projete um algoritmo que receba uma aresta e = (vi, vj) e determine se a mesma é uma ponte. """

# Uma aresta é ponte se, ao removê-la, o número de componentes conexas do grafo aumenta — ou seja, 
# ela é essencial para conectar partes do grafo.

def eh_ponte(adj, u, v):
    n = len(adj)                       # quantidade de vértices
    visited = [False] * n              # marca se vértice já foi visitado
    tin = [-1] * n                     # tempo de descoberta do vértice
    low = [-1] * n                     # menor tempo alcançável via ancestrais ou back-edges
    timer = [0]                        # contador mutável usado dentro da DFS
    is_bridge = [False]                # será marcado como True se (u, v) for ponte

    # DFS para calcular tin[x] e low[x]
    # parent: pai no DFS (para não contar aresta de retorno
    # como aresta de árvore)
    def dfs(x, parent):
        visited[x] = True
        tin[x] = low[x] = timer[0]     # tanto tin quanto low começam iguais
        timer[0] += 1                  # incrementa tempo global

        # percorre todos os vizinhos de x
        for y in adj[x]:

            # ignora a aresta que volta para o pai
            if y == parent:
                continue

            if not visited[y]:
                # seguimos na árvore DFS
                dfs(y, x)

                # atualiza low[x] baseado no filho y
                low[x] = min(low[x], low[y])

                # condição clássica de ponte:
                # se low[y] > tin[x], então a aresta (x, y) é ponte
                if low[y] > tin[x]:

                    # verifica se justamente a aresta testada é (u, v)
                    if (x == u and y == v) or (x == v and y == u):
                        is_bridge[0] = True

            else:
                # caso de aresta de retorno (back-edge)
                # atualiza low[x] usando tin[y]
                low[x] = min(low[x], tin[y])

    # Chamamos a DFS a partir do vértice 0 (assume-se grafo conectado,
    # ou ao menos que a aresta buscada está no mesmo componente)
    dfs(0, -1)

    return is_bridge[0]

# ANÁLISE DE COMPLEXIDADE
# Seja V = número de vértices e E = número de arestas.
# - A DFS percorre cada vértice uma única vez → O(V)
# - Cada aresta (u, v) é examinada no máximo duas vezes (ida/volta) → O(E)
# - Todas as operações dentro da DFS são O(1)
# Portanto, o tempo total é: Θ(V + E)
# O uso de tin[] e low[] não altera a ordem de complexidade,
# pois são apenas acessos O(1) durante o DFS.

""" 3) Uma empresa está projetando a infraestrutura de comunicação para sua nova planta industrial.
A planta possui diversos prédios que precisam ser conectados através de fibra óptica.
Para cada par de prédios existe um custo para instalação e uma largura de banda máxima.
A engenharia já definiu o conjunto mínimo de conexões necessárias para interligar 
todos os prédios minimizando custo total (i.e., uma Árvore Geradora Mínima).
A equipe de TI deseja tornar o projeto tolerante a falhas inserindo redundâncias — 
ou seja, para cada par de prédios deve existir mais de um caminho na rede.
Dada a topologia completa da planta (com custos e larguras de banda possíveis), 
o conjunto de conexões já escolhido, e um requisito mínimo de velocidade W, 
projete um algoritmo que decide se é possível tornar a rede tolerante a falhas garantindo redundância para todas as conexões. 
O algoritmo deve retornar a lista de conexões redundantes com banda ≥ W, ou indicar se é impossível. Analise a complexidade.
"""
from collections import deque

# BFS MODIFICADO:
# Encontra caminho entre u e v sem usar a aresta proibida (ban_u, ban_v), e usando apenas arestas com banda >= W.
def bfs_alternativo(adj, u, v, W, ban_u, ban_v):
    fila = deque([u])
    visit = {u}

    # Queremos encontrar caminho alternativo U → V, mas sem poder usar a aresta da MST (ban_u, ban_v)
    while fila:
        x = fila.popleft()

        if x == v:
            return True   # caminho alternativo encontrado

        for y, peso, banda in adj[x]:

            # NÃO usar a aresta (ban_u, ban_v) nem (ban_v, ban_u)
            if (x == ban_u and y == ban_v) or (x == ban_v and y == ban_u):
                continue

            # Respeitar banda mínima
            if banda < W:
                continue

            if y not in visit:
                visit.add(y)
                fila.append(y)

    return False


# ALGORITMO PRINCIPAL
# mst_edges: lista de arestas da MST já fornecida
# adj: grafo completo com custo e banda
# W: banda mínima
# Retorna lista de arestas externas que geram redundância OU None se impossível

def encontrar_redundancias(adj, mst_edges, W):
    redundantes = []

    # Para cada aresta da MST precisamos encontrar um segundo caminho
    for u, v in mst_edges:

        # Tentar encontrar caminho alternativo
        ok = bfs_alternativo(adj, u, v, W, ban_u=u, ban_v=v)

        if not ok:
            return None   # impossível garantir redundância

        # Agora precisamos registrar QUAL aresta externa foi usada.
        # Para isso, procuramos uma aresta externa (a,b) que permita banda >= W e que forme ciclo com (u,v).
        # Vamos procurar QUALQUER aresta externa com banda >= W que conecte dois nós do caminho u→v sem passar pela própria (u,v).
        for a in range(len(adj)):
            for b, peso, banda in adj[a]:

                # Ignorar aresta da própria MST
                if (a, b) in mst_edges or (b, a) in mst_edges:
                    continue
                # Banda mínima
                if banda < W:
                    continue
                # Se esta aresta permite caminho alternativo, serve como redundância
                if bfs_alternativo(adj, u, v, W, ban_u=u, ban_v=v):
                    redundantes.append((a, b))
                    break
            else:
                continue
            break

    return redundantes


""" 4) Considere o problema de agendamento de tarefas: dado o conjunto de tarefas T = {t1, …, tn} com n elementos, cada uma com:
    - tempo de início tk.start
    - tempo de término tk.end
    - valor tk.value
Encontre o subconjunto de tarefas S ⊆ T que possa ser alocado sem sobreposição temporal, maximizando: Σ(t_i.value)

(a) Desenvolva um algoritmo auxiliar que receba uma tarefa e retorne a tarefa compatível anterior (que termine antes da
    atual começar) com o maior tempo de término possível.
(b) Projete o algoritmo que encontra a solução ótima usando o algoritmo auxiliar.
(c) Indique a técnica de projeto utilizada.
(d) Analise a complexidade e justifique.
Este é o clássico problema “Weighted Interval Scheduling”.
"""
class Tarefa:
    def __init__(self, start, end, value):
        self.start = start
        self.end = end
        self.value = value

    def __repr__(self):
        return f"(start={self.start}, end={self.end}, value={self.value})"

#  (a) ALGORITMO AUXILIAR – BUSCA BINÁRIA MANUAL
# Dado tasks ordenado por tempo de término e um índice i, encontrar o maior j < i tal que:
#  tasks[j].end <= tasks[i].start
# Retorna o índice j, ou -1 se não existir tarefa compatível.

def busca_tarefa_compatível(tasks, i):
    """ Busca binária manual para encontrar a tarefa compatível que termina
    mais tarde mas ainda antes da tarefa i começar. """
    inicio = 0
    fim = i - 1
    resposta = -1  # caso nenhuma seja compatível

    target = tasks[i].start  # início da tarefa atual

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if tasks[meio].end <= target:
            # tarefa compatível; tentar achar outra com término mais próximo
            resposta = meio
            inicio = meio + 1
        else:
            # tarefa termina depois do início da atual → incompatível
            fim = meio - 1
    return resposta


#  (b) ALGORITMO ÓTIMO – DP (Weighted Interval Scheduling)
def agendamento_otimo(tasks):
    """ Retorna:
        - valor máximo
        - conjunto ótimo de tarefas"""

    # 1. Ordenação por tempo de término
    tasks = sorted(tasks, key=lambda t: t.end)
    n = len(tasks)

    # 2. Calculando p(i) – para cada tarefa, sua última compatível
    p = [0]*n
    for i in range(n):
        p[i] = busca_tarefa_compatível(tasks, i)

    # 3. DP clássica
    dp = [0]*n
    dp[0] = tasks[0].value

    for i in range(1, n):
        incluir = tasks[i].value
        if p[i] != -1:
            incluir += dp[p[i]]
        dp[i] = max(dp[i-1], incluir)

    # 4. Reconstrução da solução
    sol = []
    i = n - 1

    while i >= 0:
        incluir = tasks[i].value + (dp[p[i]] if p[i] != -1 else 0)

        # Se incluir é melhor que excluir
        if incluir >= (dp[i-1] if i > 0 else 0):
            sol.append(tasks[i])
            i = p[i]
        else:
            i -= 1

    sol.reverse()
    return dp[-1], sol

#  (c) Técnica utilizada é programação dinâmica combinada com busca binária.
#  (d) Complexidade: Ordenação: O(n log n) + Cálculo de p(i) com busca binária: O(n log n) + DP: O(n)
# Total:  O(n log n)
