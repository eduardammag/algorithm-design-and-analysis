import heapq
from graph_list import GraphList

def dijkstra(graph: GraphList, v0: int):
    num_vertices = graph.num_vertices
    parent = [-1] * num_vertices                # Armazena o pai de cada vértice no caminho mínimo
    distance = [float('inf')] * num_vertices   # Armazena a menor distância conhecida até cada vértice
    checked = [False] * num_vertices           # Marca se o vértice já teve suas arestas relaxadas

    # Inicializa o vértice inicial
    parent[v0] = v0                             # O pai do vértice inicial é ele mesmo
    distance[v0] = 0                            # Distância do início até ele mesmo é zero

    # Fila de prioridade (min-heap) para extrair sempre o vértice com menor distância atual
    heap = []
    heapq.heappush(heap, (0, v0))               # Insere tupla (distância, vértice)

    while heap:
        dist_v1, v1 = heapq.heappop(heap)       # Remove o vértice com menor distância estimada

        # Se o vértice já foi completamente processado, ignora
        if checked[v1]:
            continue

        # Se ainda tem distância infinita, não há mais caminhos acessíveis
        if distance[v1] == float('inf'):
            break

        # Relaxa todas as arestas que saem de v1
        for v2, peso in graph.adj_list[v1]:
            if not checked[v2]:
                custo = peso                     # Peso da aresta (v1 -> v2)
                # Verifica se encontrou um caminho melhor para v2
                if distance[v1] + custo < distance[v2]:
                    distance[v2] = distance[v1] + custo
                    parent[v2] = v1
                    heapq.heappush(heap, (distance[v2], v2))  # Atualiza heap com nova distância

        checked[v1] = True                       # Marca vértice como processado

    return parent, distance                      # Retorna pais e distâncias finais
