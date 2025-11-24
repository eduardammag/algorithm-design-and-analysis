from graph_list import GraphList
from collections import deque

def bfs(graph: GraphList, v0: int):
    num_vertices = graph.num_vertices
    order = [-1] * num_vertices     # Armazena a ordem em que cada vértice é visitado (inicialmente não visitados)
    parent = [-1] * num_vertices    # Armazena o pai de cada vértice na BFS
    queue = deque()                 # Fila para controle dos vértices a serem visitados
    counter = 0                     # Contador da ordem de visita

    order[v0] = counter             # Marca o vértice inicial como visitado com ordem 0
    counter += 1
    parent[v0] = v0                 # O vértice inicial é pai de si mesmo
    queue.append(v0)                # Enfileira o vértice inicial

    # Processa enquanto houver elementos na fila
    while queue:
        v1 = queue.popleft()        # Remove o primeiro elemento da fila
        for v2, _ in graph.adj_list[v1]:  # Percorre os vizinhos de v1 (ignorando pesos)
            if order[v2] == -1:     # Se o vizinho ainda não foi visitado
                order[v2] = counter # Registra ordem de visita
                parent[v2] = v1     # Define o pai do vizinho
                counter += 1
                queue.append(v2)    # Enfileira o vizinho
    return order, parent            # Retorna ordenação e pais na BFS


def reconstruir_caminho(parent, origem, destino):
    if parent[destino] == -1:       # Se o destino não foi alcançado pela BFS
        return None
    
    caminho = [destino]             # Começa o caminho pelo destino
    while caminho[-1] != origem:    # Retrocede pelos pais até chegar à origem
        caminho.append(parent[caminho[-1]])
    caminho.reverse()               # Inverte para obter caminho origem → destino
    return caminho




