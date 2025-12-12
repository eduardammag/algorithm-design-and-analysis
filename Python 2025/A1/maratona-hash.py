"""
===========================================================
QUESTÃO 1 — Tabela Hash com Encadeamento: Contagem de Colisões
-----------------------------------------------------------
Implemente uma tabela hash de tamanho M utilizando encadeamento.
Ao inserir N chaves, conte quantas colisões ocorreram.

Uma colisão ocorre quando:
 - vamos inserir uma chave num bucket que já contém pelo menos 1 elemento
===========================================================
"""

def hash_insert_chaining_count_collisions(M, keys):
    # Cria a tabela hash: um vetor de listas vazias
    table = [[] for _ in range(M)]

    collisions = 0  # contador de colisões

    for key in keys:
        index = key % M  # função hash simples

        # Se o bucket já não estiver vazio → colisão
        if len(table[index]) > 0:
            collisions += 1

        # Inserção normal no encadeamento
        table[index].append(key)

    return collisions



"""
===========================================================
QUESTÃO 2 — Hash com Endereçamento Aberto: Sondagem Linear
-----------------------------------------------------------
Implementar:
 I X → inserir X
 B X → buscar X
 P   → imprimir tabela

Hash:
 h(key, i) = (key % M + i) % M

Caso a tabela fique cheia → imprimir "FULL".
===========================================================
"""

def hashing_linear_probing(M, operations):
    # Cria uma tabela hash preenchida com None (vazio)
    table = [None] * M

    def insert_linear(x):
        # Tenta inserir a chave x usando sondagem linear
        for i in range(M):
            pos = (x % M + i) % M  # fórmula da sondagem linear
            if table[pos] is None:  # posição livre
                table[pos] = x
                return
        print("FULL")  # tabela cheia sem posição

    def search_linear(x):
        # Busca usando sondagem linear
        for i in range(M):
            pos = (x % M + i) % M
            if table[pos] is None:  # encontrou vazio → não existe
                break
            if table[pos] == x:
                print("FOUND")
                return
        print("NOT FOUND")

    def print_table():
        # Imprime a tabela linha reta
        print(" ".join(str(v) if v is not None else "_" for v in table))

    # Processamento das operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_linear(int(parts[1]))

        elif parts[0] == "B":
            search_linear(int(parts[1]))

        elif parts[0] == "P":
            print_table()



"""
===========================================================
QUESTÃO 3 — Hash com Endereçamento Aberto: Sondagem Quadrática
-----------------------------------------------------------
Operações:
 I X → inserir
 B X → buscar
 R X → remover (usando marcador "DELETED")

Hash:
 h(key, i) = (key % M + i*i) % M
===========================================================
"""

def hashing_quadratic_probing(M, operations):
    # Cria tabela com None para vazio e "DEL" para deletado
    table = [None] * M

    def insert_quad(x):
        # Inserção com sondagem quadrática
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None or table[pos] == "DEL":
                table[pos] = x
                return
        print("FAILED")  # não encontrou posição

    def search_quad(x):
        # Busca com sondagem quadrática
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None:  # posição vazia → não existe
                break
            if table[pos] == x:
                print("FOUND")
                return
        print("NOT FOUND")

    def remove_quad(x):
        # Remoção marcando "DEL"
        for i in range(M):
            pos = (x % M + i*i) % M
            if table[pos] is None:
                break
            if table[pos] == x:
                table[pos] = "DEL"
                return

    # Executa operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_quad(int(parts[1]))

        elif parts[0] == "B":
            search_quad(int(parts[1]))

        elif parts[0] == "R":
            remove_quad(int(parts[1]))



"""
===========================================================
QUESTÃO 4 — Double Hashing: Contagem de Sondas
-----------------------------------------------------------
Inserir várias chaves usando double hashing e contar quantas
sondagens totais foram necessárias.

h1(key) = key mod M
h2(key) = 1 + (key mod (M-1))
h(key,i) = (h1 + i*h2) mod M

Cada tentativa conta como 1 sondagem.
===========================================================
"""

def double_hashing_count_probes(M, keys):
    table = [None] * M
    probes = 0  # contador de sondagens

    for key in keys:
        h1 = key % M
        h2 = 1 + (key % (M - 1))

        for i in range(M):
            pos = (h1 + i * h2) % M
            probes += 1  # conta tentativa

            if table[pos] is None:
                table[pos] = key
                break

    return probes



"""
===========================================================
QUESTÃO 5 — Encadeamento com Remoção e Relatórios
-----------------------------------------------------------
Operações:
 I X → inserir X
 R X → remover X
 B X → buscar X
 L   → imprimir tamanhos dos buckets

Imprimir L como:
 size0 size1 size2 ... size(M-1)
===========================================================
"""

def hashing_chaining_full(M, operations):
    # Cria tabela hash como lista de listas
    table = [[] for _ in range(M)]

    def insert_chain(x):
        index = x % M
        table[index].append(x)

    def remove_chain(x):
        index = x % M
        # Remove apenas uma ocorrência se existir
        if x in table[index]:
            table[index].remove(x)

    def search_chain(x):
        index = x % M
        if x in table[index]:
            print("FOUND")
        else:
            print("NOT FOUND")

    def list_sizes():
        # imprime o tamanho de cada bucket da tabela
        print(" ".join(str(len(bucket)) for bucket in table))

    # Processamento das operações
    for op in operations:
        parts = op.split()

        if parts[0] == "I":
            insert_chain(int(parts[1]))

        elif parts[0] == "R":
            remove_chain(int(parts[1]))

        elif parts[0] == "B":
            search_chain(int(parts[1]))

        elif parts[0] == "L":
            list_sizes()



"""
===========================================================
EXEMPLOS DE USO (TESTE RÁPIDO)
===========================================================
"""

if __name__ == "__main__":
    print("\n--- Q1 ---")
    print(hash_insert_chaining_count_collisions(5, [1, 6, 11, 3, 8]))

    print("\n--- Q2 ---")
    hashing_linear_probing(5, ["I 1", "I 6", "I 11", "B 6", "P"])

    print("\n--- Q3 ---")
    hashing_quadratic_probing(7, ["I 10", "I 3", "I 17", "B 10", "R 10", "B 10"])

    print("\n--- Q4 ---")
    print(double_hashing_count_probes(7, [10, 20, 5, 33, 12]))

    print("\n--- Q5 ---")
    hashing_chaining_full(4, ["I 5", "I 9", "I 13", "B 9", "R 9", "L"])
