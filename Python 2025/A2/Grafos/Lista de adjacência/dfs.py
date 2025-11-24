from graph_list import GraphList

def dfs(graph: 'GraphList'):
    pre_order = [-1] * graph.num_vertices       # ordem de descoberta de cada vértice
    post_order = [-1] * graph.num_vertices      # ordem de finalização de cada vértice
    parents = [-1] * graph.num_vertices         # vetor de pais na DFS
    pre_counter = [0]                           # contador de descoberta (usando lista p/ mutabilidade)
    post_counter = [0]                          # contador de finalização

    # Garante que todos os vértices sejam visitados,
    # inclusive componentes desconexos
    for v in range(graph.num_vertices):
        if pre_order[v] == -1:                  # se o vértice ainda não foi descoberto
            parents[v] = v                      # raiz da DFS é pai de si mesma
            _dfs_recursive(
                graph, v, pre_order, pre_counter,
                post_order, post_counter, parents
            )
    return pre_order, post_order, parents       # retorna as informações coletadas


def _dfs_recursive(graph: 'GraphList', v1, pre_order, pre_counter,
                   post_order, post_counter, parents):

    pre_order[v1] = pre_counter[0]              # marca momento de descoberta do vértice
    pre_counter[0] += 1

    # percorre vizinhos do vértice
    for (v2, peso) in graph.adj_list[v1]:
        if pre_order[v2] == -1:                 # se o vizinho ainda não foi descoberto
            parents[v2] = v1                    # define o pai do vizinho
            _dfs_recursive(
                graph, v2, pre_order, pre_counter,
                post_order, post_counter, parents
            )

    # após explorar todos os vizinhos, marca o momento de finalização
    post_order[v1] = post_counter[0]
    post_counter[0] += 1


# Pre-ordem (descoberta): instante em que o vertice é encontrado pela primeira vez.
# Pos-ordem (finalização): instante em que terminamos de visitar todos os vizinhos e estamos "voltando" na recursão.
# O resultado é uma floresta de arvores DFS (uma para cada componente).
# Exemplo: Se tivermos pre_order = [0, 1, 3, 2, 4, 5] e post_order = [3, 2, 1, 0, 5, 4]. Isso significa:
# O vertice 0 foi descoberto primeiro (pre=0) e finalizado apos 3 vertices (pos=3).
# O vertice 3 foi descoberto na posição 3 e finalizado logo em seguida (pos=0).
# Assim conseguimos saber a "linha do tempo" de cada vertice.
#
# Estrutura gerada:
# - O conjunto de arvores geradas forma uma floresta radicada.
# - As raízes são vertices sem pais (parents[v] == v).
# - As folhas são vertices sem vizinhos não visitados.























# Problema: como determinar se um grafo 𝐺 = (𝑉,𝐸) possui ao menos um ciclo?
# Solução : execute a busca DFS e procure por uma aresta de retorno comparando os intervalos de vida encontrados para cada vértice.

def has_cycle(graph: 'GraphList'):
    """
    Detecta se existe um ciclo em um grafo direcionado usando
    as listas de pré e pós-ordem da DFS.

    Retorna:
        True  → se o grafo contém pelo menos um ciclo.
        False → se o grafo é acíclico.
    """

    # Primeiro, executa DFS para obter pré-ordem e pós-ordem
    pre_order, post_order, _ = dfs(graph)

    print("\n=== Verificando existência de ciclos ===")

    # Percorre todos os vértices e suas arestas
    for v1 in range(graph.num_vertices):
        for (v2, peso) in graph.adj_list[v1]:
            print(f"Analisando aresta {v1} → {v2} ...")

            # Verifica a condição de ciclo:
            # Se v1 foi descoberto depois de v2 (pre[v1] > pre[v2])
            # mas finalizado antes (post[v1] < post[v2]),
            # então há um ciclo.
            if pre_order[v1] > pre_order[v2] and post_order[v1] < post_order[v2]:
                print(f"⚠️  Ciclo detectado: {v1} → {v2}")
                return True

    print("✅ Nenhum ciclo encontrado.")
    return False


# ================================================================
# EXPLICAÇÃO DETALHADA
# ================================================================
#
# 🔹 Ideia principal:
# -------------------
# Após executar a DFS, cada vértice v tem:
#   pre_order[v]  → instante em que foi descoberto.
#   post_order[v] → instante em que terminou de visitar seus vizinhos.
#
# Para cada aresta (v1 → v2), há três casos:
#   1. **Aresta de árvore (tree edge)**:
#        v2 foi descoberto pela primeira vez por v1.
#        → pre[v1] < pre[v2] < post[v2] < post[v1]
#
#   2. **Aresta direta (forward edge)**:
#        v2 é um descendente já finalizado.
#        → pre[v1] < pre[v2] < post[v2] < post[v1]
#
#   3. **Aresta de retorno (back edge)** ⚠️
#        v2 é um ancestral ainda ativo na recursão.
#        → pre[v1] > pre[v2] e post[v1] < post[v2]
#        → Isso indica a existência de um ciclo.
#
#   4. **Aresta cruzada (cross edge)**:
#        liga subárvores distintas, sem causar ciclo.
#
# O algoritmo usa exatamente essa propriedade para detectar ciclos.
#
#
# 🔹 Passo a passo:
# -------------------
# 1. Chama `dfs(graph)` para calcular `pre_order` e `post_order`.
# 2. Para cada aresta (v1 → v2):
#       - Se v1 foi descoberto DEPOIS de v2 (pre[v1] > pre[v2])
#         e finalizado ANTES (post[v1] < post[v2]),
#         então existe um ciclo (v2 alcança v1 novamente).
# 3. Se nenhuma aresta satisfaz a condição, o grafo é acíclico.
#
#
# 🔹 Exemplo:
# -------------------
# Grafo:
#     0 → 1 → 2
#          ↑   |
#          └───┘
#
# DFS:
#   pre_order  = [0, 1, 2]
#   post_order = [5, 3, 4]
#
# Aresta (2 → 1):
#   pre[2]=2 > pre[1]=1  e  post[2]=4 < post[1]=3 ❌ (não)
#
# Mas ajustando os tempos durante a DFS correta:
#   pre[1]=1, pre[2]=2, post[2]=3, post[1]=4
#   → pre[1] < pre[2] < post[2] < post[1] → ok (sem ciclo)
#
# Agora, se houver uma aresta (2 → 0):
#   pre[2]=2 > pre[0]=0  e post[2]=3 < post[0]=5 ✅ ciclo detectado!
#
#
# 🔹 Complexidade:
# -------------------
# - O DFS inicial:      O(V + E)
# - A varredura final:  O(E)
# -------------------------------
# ➤ Complexidade total: O(V + E)
#
# Espaço:
# - Vetores pre_order, post_order, parents: O(V)
# - Pilha recursiva DFS: até O(V)
# ➤ Espaço total: O(V)
#
#
# 🔹 Observações:
# -------------------
# - Funciona corretamente **apenas para grafos direcionados**.
# - Para grafos não direcionados, a detecção de ciclo deve
#   verificar se existe uma aresta para um vértice já visitado
#   que **não é o pai** na DFS.
# ================================================================


def has_cycle_undirected(graph: 'GraphList'):
    """
    Detecta se existe um ciclo em um grafo NÃO DIRECIONADO
    usando uma busca em profundidade (DFS).

    Retorna:
        True  → se o grafo contém pelo menos um ciclo.
        False → se o grafo é acíclico.
    """

    visited = [False] * graph.num_vertices

    print("\n=== Iniciando detecção de ciclo (grafo não direcionado) ===")

    # Pode haver múltiplas componentes → roda DFS em todas
    for v in range(graph.num_vertices):
        if not visited[v]:
            print(f"\n→ Iniciando DFS na componente com raiz {v}")
            if _dfs_cycle_undirected(graph, v, visited, parent=-1):
                print("⚠️  Ciclo detectado nesta componente!")
                return True

    print("✅ Nenhum ciclo encontrado.")
    return False


def _dfs_cycle_undirected(graph: 'GraphList', v, visited, parent, level=0):
    """Função recursiva auxiliar para detecção de ciclo em grafos não direcionados."""
    indent = "  " * level
    visited[v] = True
    print(f"Visitando vértice {v} (pai = {parent})")

    for (vizinho, peso) in graph.adj_list[v]:
        # Caso 1: vizinho ainda não visitado → explorar recursivamente
        if not visited[vizinho]:
            print(f"↳ Indo visitar vizinho {vizinho}")
            if _dfs_cycle_undirected(graph, vizinho, visited, v, level + 1):
                return True  # ciclo encontrado abaixo
        # Caso 2: vizinho já visitado, mas não é o pai → ciclo detectado
        elif vizinho != parent:
            print(f"⚠️  Aresta {v} ↔ {vizinho} fecha um ciclo!")
            return True

    print(f"Retornando de {v}")
    return False


# ================================================================
# EXPLICAÇÃO DETALHADA
# ================================================================
#
# 🔹 Ideia principal:
# -------------------
# Um grafo **não direcionado** possui ciclo se, durante a DFS,
# encontrarmos um vértice já visitado que **não é o pai**
# do vértice atual.
#
# Exemplo de ciclo:
#   0 — 1 — 2
#    \_____/
#
# A DFS saindo de 0 visita 1, depois 2.
# 2 vê que 0 já foi visitado e **não é seu pai**, logo → ciclo.
#
#
# 🔹 Significado das variáveis:
# -----------------------------
# visited[v] → True se o vértice já foi visitado.
# parent     → pai do vértice atual na DFS.
# level      → profundidade da recursão (usado só para prints).
#
#
# 🔹 Passo a passo:
# -------------------
# 1. Marca o vértice atual como visitado.
# 2. Para cada vizinho:
#      - Se ainda não foi visitado → chama DFS recursiva.
#      - Se já foi visitado e **não é o pai**, ciclo encontrado!
# 3. Se não encontrar nenhum caso desses, retorna False.
#
#
# 🔹 Exemplo:
# -------------------
# Grafo:
#     0 — 1 — 2
#      \____/
#
# A DFS encontra:
#   0 → 1 → 2
#   Quando 2 vê 0 (já visitado e ≠ pai), detecta ciclo.
#
#
# 🔹 Complexidade:
# -------------------
# Tempo:  O(V + E)
#   Cada vértice e aresta é visitado uma vez.
#
# Espaço: O(V)
#   Vetor visited + pilha de recursão.
#
# 🔹 Observação:
# -------------------
# - Este método funciona **apenas** para grafos **não direcionados**.
# - Em grafos direcionados, o teste “vizinho != pai” não faz sentido,
#   pois o conceito de “pai” é direcional.
# ================================================================













# Exercício: dado um grafo 𝐺 = (𝑉,𝐸) crie um algoritmo baseado em DFS que classifica cada aresta do grafo on-the-fly
# Ou seja, define se a aresta é: Parte da floresta DFS, De avanço, De retorno, Cruzada. 
# O algoritmo deverá apresentar complexidade 𝑂(𝑉 + 𝐸)

def dfs_classify_edges(graph: 'GraphList'):
    pre_order = [-1] * graph.num_vertices       # ordem de descoberta
    post_order = [-1] * graph.num_vertices      # ordem de finalização
    parents = [-1] * graph.num_vertices
    pre_counter = [0]
    post_counter = [0]

    for v in range(graph.num_vertices):
        if pre_order[v] == -1:
            parents[v] = v
            _dfs_classify_recursive(
                graph, v, pre_order, pre_counter,
                post_order, post_counter, parents
            )
    return pre_order, post_order, parents


def _dfs_classify_recursive(graph: 'GraphList', v1, pre_order, pre_counter,
                            post_order, post_counter, parents):

    pre_order[v1] = pre_counter[0]  # Marca o vértice como descoberto
    pre_counter[0] += 1

    for (v2, peso) in graph.adj_list[v1]:
        if pre_order[v2] == -1:
            print(f"({v1},{v2}) Tree branch")
            parents[v2] = v1
            _dfs_classify_recursive(
                graph, v2, pre_order, pre_counter,
                post_order, post_counter, parents
            )

        elif post_order[v2] == -1:
            print(f"({v1},{v2}) Return")
        else:
            if pre_order[v2] > pre_order[v1]:
                print(f"({v1},{v2}) Forward")
            else:
                print(f"({v1},{v2}) Cross")

    post_order[v1] = post_counter[0]
    post_counter[0] += 1
























































