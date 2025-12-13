# Com encadeamento
# Nó da lista duplamente encadeada usada em cada bucket
class HTNode:
    def __init__(self, key, value):
        self.key = key          
        self.value = value      
        self.next = None        
        self.previous = None    

class HashTable:
    def __init__(self, size):
        self.size = size                     # tamanho da tabela (O(1))
        self.table = [None] * size           # vetor de buckets (O(size))

def hash_int(key, size):
    return key % size # O(1)

def hash_str(value: str, size: int) -> int:
    h = 0
    for ch in value:                     # O(n), onde n = tamanho da string
        h = (h * 256 + ord(ch)) % size
    return h

# Insere novo nó ou atualiza valor existente
# Complexidade: #   - Melhor caso: O(1), #   - Pior caso:  O(n_bucket)
def insert_or_update(ht: HashTable, key, value):
    h = hash_int(key, ht.size)         # O(1)
    node = ht.table[h]                 # primeiro da lista (O(1))

    # procura chave no bucket — O(n_bucket)
    while node is not None and node.key != key:
        node = node.next

    if node is None:
        # insere novo nó no início da lista — O(1)
        new_node = HTNode(key, value)
        first = ht.table[h]

        new_node.next = first
        new_node.previous = None

        if first is not None:
            first.previous = new_node

        ht.table[h] = new_node
    else:
        # chave encontrada → apenas atualizar valor — O(1)
        node.value = value


# SEARCH
# Retorna o nó da chave ou None
#
# Complexidade:
#   - Melhor caso: O(1)
#   - Pior caso:  O(n_bucket)
def search(ht: HashTable, key):
    h = hash_int(key, ht.size)       # O(1)
    node = ht.table[h]

    # percorre lista encadeada — O(n_bucket)
    while node is not None and node.key != key:
        node = node.next

    return node


# REMOVE
# Remove um nó correspondente à chave
#
# Complexidade:
#   - Busca: O(n_bucket)
#   - Remoção: O(1)
def remove(ht: HashTable, key):
    h = hash_int(key, ht.size)      # O(1)
    node = ht.table[h]

    # busca nó — O(n_bucket)
    while node is not None and node.key != key:
        node = node.next

    if node is None:
        return False  # chave não existe

    # Ajusta ponteiro do próximo — O(1)
    if node.next is not None:
        node.next.previous = node.previous

    # Ajusta ponteiro do anterior — O(1)
    if node.previous is not None:
        node.previous.next = node.next
    else:
        # nó era cabeça da lista
        ht.table[h] = node.next

    return True
