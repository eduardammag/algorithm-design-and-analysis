class EdgeNode:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.next = None   # próxima aresta ligada ao vértice u

    def other_vertex(self, x):
        return self.v if x == self.u else self.u


# Problema: dado um grafo 𝐺 = (𝑉,𝐸), representando uma rede com capacidade nas arestas e vértices de
# origem e destino, encontre o fluxo máximo respeitando a capacidade das arestas. 

#  O fluxo será máximo caso a intensidade do  mesmo seja a maior possível no grafo 𝐺.
from collections import deque
import math

def find_next_augmenting_path(v0, vf, parent, parent_edge, edges, num_vertices):
    """
    v0: vértice de origem
    vf: vértice de destino
    parent: array para armazenar o pai de cada vértice
    parent_edge: array para armazenar a aresta usada no caminho
    edges: lista de listas com objetos EdgeNode
    num_vertices: quantidade total de vértices
    """

    visited = [False] * num_vertices
    queue = deque()

    # BFS
    visited[v0] = True
    queue.append(v0)

    while queue:
        v = queue.popleft()
        if v == vf:
            break

        edge = edges[v]

        while edge is not None:
            residual = edge.capacity - edge.flow
            v2 = edge.other_vertex(v)

            if residual > 0 and not visited[v2]:
                visited[v2] = True
                parent[v2] = v
                parent_edge[v2] = edge
                queue.append(v2)

            edge = edge.next

    # Se não chegou ao destino, não existe caminho aumentante
    if not visited[vf]:
        return 0

    # Calcula delta (a capacidade mínima ao longo do caminho encontrado)
    delta = math.inf
    v2 = vf
    while v2 != v0:
        edge = parent_edge[v2]
        delta = min(delta, edge.capacity - edge.flow)
        v2 = parent[v2]

    return delta
