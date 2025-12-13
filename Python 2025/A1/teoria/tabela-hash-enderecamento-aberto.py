class DANode:
    """
    Nó da tabela hash.
    key       : chave (ou None para posição nunca usada)
    value     : valor armazenado
    recycled  : indica que já foi ocupado antes e depois removido
    """
    def __init__(self, key=None, value=None, recycled=False):
        self.key = key
        self.value = value
        self.recycled = recycled

    def __repr__(self):
        return f"DANode(key={self.key}, value={self.value}, recycled={self.recycled})"


class DirectHashTable:
    """
    Tabela hash com probing linear e redimensionamento automático.
    """

    # CONSTRUTOR
    def __init__(self, size=8, load_factor_max=0.7):
        """
        size            : tamanho inicial da tabela
        load_factor_max : fator de carga que ativa o resize

        Complexidade: O(n) — inicializa a tabela
        """
        self.m_size = size
        self.m_table = [DANode() for _ in range(size)]
        self.count_elements = 0
        self.load_factor_max = load_factor_max

    # HASH UNIFICADA PARA INTEIROS E STRINGS
    def hash_key(self, key):
        """
        Converte key (int ou string) em hash indexável.
        Complexidade: O(1) amortizado em Python.
        """
        if isinstance(key, int):
            return key % self.m_size
        else:
            # hash() de Python + normalização
            return abs(hash(key)) % self.m_size

    # FUNÇÃO INTERNA: RESIZE
    def _resize(self):
        """
        Dobra o tamanho da tabela e reinsere todos os elementos.
        Complexidade: O(n)
        """
        old_table = self.m_table
        self.m_size *= 2
        self.m_table = [DANode() for _ in range(self.m_size)]
        self.count_elements = 0

        # Reinsere apenas os nós válidos
        for node in old_table:
            if node.key is not None and not node.recycled:
                self.insert_or_update(node.key, node.value)

    # INSERT OR UPDATE
    def insert_or_update(self, key, value):
        """
        Insere ou atualiza uma chave.

        Complexidade média: O(1)
        Pior caso: O(n)
        """
        # Resize automático
        if self.count_elements / self.m_size > self.load_factor_max:
            self._resize()

        h = self.hash_key(key)
        first_recycled = None

        for _ in range(self.m_size):
            node = self.m_table[h]

            # Posição nunca usada → inserir aqui
            if node.key is None and not node.recycled:
                # Se encontramos um slot reciclado antes, usamos ele
                if first_recycled is not None:
                    slot = first_recycled
                else:
                    slot = node
                slot.key = key
                slot.value = value
                slot.recycled = False
                self.count_elements += 1
                return True

            # Achou slot reciclado → guardar para possível reuso
            if node.recycled and first_recycled is None:
                first_recycled = node

            # Se chave encontrada → atualizar
            if node.key == key:
                node.value = value
                return True

            h = (h + 1) % self.m_size

        return False  # Tabela cheia (teoricamente impossível com resize)

    # SEARCH
    def search(self, key):
        """
        Retorna DANode ou None.

        Complexidade média: O(1)
        Pior caso: O(n)
        """
        h = self.hash_key(key)

        for _ in range(self.m_size):
            node = self.m_table[h]

            if node.key is None and not node.recycled:
                return None  # chave não existe

            if node.key == key:
                return node

            h = (h + 1) % self.m_size

        return None

    # REMOVE
    def remove(self, key):
        """
        Remove logicamente a chave (marcando recycled=True).
        Complexidade média: O(1)
        Pior caso: O(n)
        """
        node = self.search(key)
        if node is None:
            return False

        node.key = None
        node.value = None
        node.recycled = True
        self.count_elements -= 1
        return True

    # IMPRESSÃO ELEGANTE DOS BUCKETS
    def print_table(self):
        """
        Mostra a tabela em formato amigável.
        Complexidade: O(n)
        """
        print("\n==== HASH TABLE ====")
        for i, node in enumerate(self.m_table):
            if node.key is None and not node.recycled:
                status = "EMPTY"
            elif node.recycled:
                status = "RECYCLED"
            else:
                status = f"({node.key}:{node.value})"

            print(f"[{i:02d}] → {status}")
        print("====================\n")


# RESUMO EM TÓPICOS — TABELAS HASH COM ENDEREÇAMENTO ABERTO
# - A busca por uma chave depende da sequência de sondagem hash(key, i) gerada pela função de espalhamento.
#
# - Existem M! possíveis sequências de sondagem para uma tabela de tamanho M.
#
# - A sondagem linear é o método mais simples para gerar a sequência: hash(key, i) = (hash'(key) + i) % M
#
# - É fácil de implementar, mas sofre com o problema de "agrupamento primário":
#   chaves que colidem tendem a formar blocos contínuos, dificultando o acesso.
#
# - Em endereçamento aberto, qualquer posição da tabela pode ser usada para
#   qualquer chave. A posição hash inicial deixa de ser única para a busca:
#   ela passa a ser apenas a primeira posição mais provável onde a chave pode estar.
#
# - Diferente de hashing com listas encadeadas, chaves com o mesmo hash não
#   ficam isoladas em estruturas independentes — isso causa influência mútua:
#   muitas chaves com mesmo hash aumentam colisões para outras chaves.
#
# - Agrupamentos (clusters) criam longas sequências de sondagem, aumentando
#   o tempo de busca e inserção.
#
# - O ideal é que a função de espalhamento produza distribuição uniforme:
#   cada chave deve ter igual probabilidade de gerar qualquer sequência possível.
#
# SONAGEM QUADRÁTICA
# - Outro método comum: hash(key, i) = hash'(key) + c1*i + c2*i²  (mod M)
# - A primeira posição ainda determina toda a sequência.
# - Produz apenas M sequências distintas dentre as M! possíveis.
# - Espalha melhor que a sondagem linear, mas produz agrupamento secundário:
#   chaves com o mesmo hash seguem exatamente a mesma sequência.
#
# HASH DUPLO (DOUBLE HASHING)
# - Definido por:
#       hash(key, i) = (hash1(key) + i * hash2(key)) % M
#
# - Considerado um dos melhores métodos:
#   – Mesmo que chaves colidam em hash1, hash2 gera deslocamentos diferentes.
#   – Gera até M² sequências distintas.
#   – Minimiza agrupamentos primários e secundários.
#
# CUSTO DE OPERAÇÕES
# - Número médio de sondagens para inserir em endereçamento aberto:
#       α_i = 1 / (1 - α)
#   onde α = fator de carga (elementos ocupados / M)
#
# - Exemplo: se α = 0.75 (gatilho típico de resize):
#       1 / (1 - 0.75) = 4 sondagens esperadas.
#
# OBSERVAÇÕES SOBRE A IMPLEMENTAÇÃO
# - Usa menos memória que hashing com listas encadeadas,
#   pois não precisa de ponteiros para nós individuais.
#
# - O espaço economizado pode ser utilizado para aumentar o tamanho M,
#   reduzindo colisões.
#
# - Evita alocação dinâmica por nó — toda tabela é um único bloco contínuo.
#
# - Pode ser submetida a Resize & Rehash, aumentando capacidade e
#   redistribuindo elementos para manter bom desempenho.
#
