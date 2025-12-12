"""
===========================================================
 QUESTÃO 1
===========================================================
Determine uma função f(n) tal que o código abaixo tem T(n)=O(f(n)).
A função pow(b,e) calcula b^e. Explicar como f(n) foi encontrada.

Código analisado:

void f(int n){
    int i = 0;
    while(pow(i,2) <= n) {
        int x = 0;
        while(x < i) {
            ++x;
        }
        ++i;
    }
}

ANÁLISE:
- O laço externo executa enquanto i^2 <= n  ⇒  i ≤ √n
- Portanto, o laço externo roda √n vezes.
- O laço interno roda i vezes a cada iteração.
Total = soma(i de 1 até √n) = O((√n)^2 / 2) = O(n)

Resposta: f(n) = n
"""

def questao1(n):
    # Apenas simulação — lógica idêntica ao código C.
    i = 0
    while i*i <= n:
        x = 0
        while x < i:
            x += 1
        i += 1
    return i  # irrelevante, já que a questão era de análise


"""
===========================================================
 QUESTÃO 2
===========================================================
Dada uma sequência A com n números naturais DISTINTOS,
projetar um algoritmo que verifique se existem 3 números distintos
cuja soma seja igual a x.

Complexidade exigida: O(n² log n)

Ideia:
1. Ordenar o array -> O(n log n)
2. Para cada par (i, j), buscar x - (A[i] + A[j]) por busca binária -> O(log n)
Total: n² pares × log n = O(n² log n)
"""

def questao2(A, x):
    A = sorted(A)                      # O(n log n)
    n = len(A)

    for i in range(n):
        for j in range(i+1, n):
            alvo = x - (A[i] + A[j])  # valor que falta para completar a soma
            # Busca binária — O(log n)
            lo, hi = 0, n-1
            while lo <= hi:
                mid = (lo+hi)//2
                if A[mid] == alvo and mid != i and mid != j:
                    return True
                if A[mid] < alvo:
                    lo = mid + 1
                else:
                    hi = mid - 1
    return False


"""
===========================================================
 QUESTÃO 3
===========================================================
Uma sequência A de tamanho n contém inteiros positivos e negativos.

a) Produzir algoritmo O(n³) que encontra i < j tal que soma(A[i]..A[j]) é máxima.
b) Otimizar para O(n²).
c) Avaliar se é possível O(n). (Sim — Kadane)

"""

# a) Solução O(n³)
def max_subarray_cubico(A):
    n = len(A)
    melhor = float("-inf")
    for i in range(n):               # O(n)
        for j in range(i, n):        # O(n)
            soma = 0
            for k in range(i, j+1):  # O(n)
                soma += A[k]
            melhor = max(melhor, soma)
    return melhor


# b) Solução O(n²)
def max_subarray_quadratico(A):
    n = len(A)
    melhor = float("-inf")
    for i in range(n):              # O(n)
        soma = 0
        for j in range(i, n):       # O(n)
            soma += A[j]            # soma acumulada
            melhor = max(melhor, soma)
    return melhor


# c) Solução O(n) — Kadane
def max_subarray_kadane(A):
    melhor = atual = A[0]
    for x in A[1:]:
        atual = max(x, atual + x)
        melhor = max(melhor, atual)
    return melhor


"""
===========================================================
 QUESTÃO 4 (VERSÃO AMPLIADA E TEÓRICA)
===========================================================

Explique como funciona o algoritmo de remoção de um elemento em uma 
tabela hash, considerando as duas estratégias clássicas de tratamento 
de colisões:

(a) ENCADEAMENTO (chaining)
(b) ENDEREÇAMENTO ABERTO (open addressing)

A seguir apresentamos uma explicação teórica detalhada, seguida das 
implementações comentadas linha a linha.
"""

############################################################
# 4A — TABELA HASH COM ENCADEAMENTO (CHAINING)
############################################################
"""
TEORIA — COMO FUNCIONA A REMOÇÃO NO ENCADEAMENTO:

• Na estratégia de encadeamento, cada posição da tabela hash (bucket)
  contém uma LISTA (normalmente uma lista ligada).

• Para inserir:
      h(key) define em qual lista a chave irá.
      A chave é colocada no final da lista.

• Para remover:
      1. Calcula-se o bucket: b = h(key)
      2. Percorre-se a lista bucket[b] comparando cada elemento com key
      3. Quando encontrado, remove-se o nó da lista.
         - Remover da lista é operação O(1)
           (se já temos a referência ou o índice).
         - O custo dominante é PERCORRER a lista → O(k),
           onde k é o número de elementos naquele bucket.

• VANTAGENS:
      - Remoção é simples: basta retirar da lista.
      - Não prejudica buscas futuras, pois listas independem de tombstones.

• COMPLEXIDADE:
      - Melhor caso: O(1)
      - Pior caso: O(n) (quando todas as chaves colidem no mesmo bucket)
      - Caso médio com hash bom: O(α), onde α = n/m (fator de carga)

Abaixo implementamos essa estrutura:
"""

class HashEncadeamento:
    def __init__(self, m=10):
        # Criar uma tabela com m listas vazias
        self.m = m
        self.tab = [[] for _ in range(m)]

    def h(self, key):
        # Função hash simples: key mod m
        return key % self.m

    def insert(self, key):
        # Inserção: apenas adiciona no bucket indicado
        self.tab[self.h(key)].append(key)

    def remove(self, key):
        # Remoção: percorre o bucket para encontrar e remover a chave
        bucket = self.tab[self.h(key)]
        for i, val in enumerate(bucket):
            if val == key:
                # Remoção direta da lista
                del bucket[i]
                return True
        return False


############################################################
# 4B — TABELA HASH COM ENDEREÇAMENTO ABERTO (OPEN ADDRESSING)
############################################################
"""
TEORIA — COMO FUNCIONA A REMOÇÃO NO ENDEREÇAMENTO ABERTO:

• Aqui NÃO usamos listas. Cada chave é armazenada diretamente em uma 
  posição da tabela, e colisões são resolvidas através de re-sondagem
  (linear, quadrática, hashing duplo etc.).

• Problema: Se removemos simplesmente a chave e colocamos None, 
  quebramos a cadeia de sondagem e causamos "buracos".  
  Isso impede que futuras BUSCAS encontrem elementos corretamente.

Exemplo:
    Inserções com hash linear probing:
       key1 → posição 5
       key2 → colidiu → vai para 6
       key3 → colidiu → vai para 7

    Tabela:
       ... 5:key1, 6:key2, 7:key3 ...

    Se removermos key2 colocando None na posição 6:
       posição 6 agora está vazia → a busca por key3 PÁRA em 6
       e erroneamente diz que key3 não existe.

• SOLUÇÃO:
  Utilizamos uma MARCA ESPECIAL chamada TOMBSTONE (ex.: "<del>").

• Função da TOMBSTONE:
      - Diz que "havia algo aqui, mas foi removido".
      - Mantém a continuidade da sondagem.
      - Permite busca correta de elementos posteriores.
      - Permite inserir novos elementos nessa posição futuramente.

• COMPLEXIDADE:
      - Remoção: O(n) no pior caso (igual à busca por linear probing).
      - No caso médio: O(1) por operação, para fator de carga < 0.7.

A seguir, a implementação detalhada:
"""

class HashAberto:
    DELETED = "<del>"  # Tombstone padrão

    def __init__(self, m=10):
        # Tabela inicial com m posições vazias
        self.m = m
        self.tab = [None] * m

    def h(self, key, i=0):
        # Hash com sondagem linear: h(k,i) = (k + i) mod m
        return (key + i) % self.m

    def insert(self, key):
        # Insere procurando primeira posição livre ou marcada como deletada
        for i in range(self.m):
            pos = self.h(key, i)
            if self.tab[pos] in (None, self.DELETED):
                self.tab[pos] = key
                return
        raise Exception("Tabela cheia — impossível inserir")

    def remove(self, key):
        # Para remover, busca-se pela chave exatamente como uma busca normal
        for i in range(self.m):
            pos = self.h(key, i)

            # Se achou a chave → substitui por tombstone
            if self.tab[pos] == key:
                self.tab[pos] = self.DELETED
                return True

            # Se encontrou None, significa que a chave nunca esteve adiante
            if self.tab[pos] is None:
                return False

        # Caso percorra toda a tabela e não encontre
        return False

"""
===========================================================
 QUESTÃO 5
===========================================================
Dadas sequências A (m elementos) e B (n elementos), m ≥ n,
produzir sequência C contendo os elementos de A
REORDENADOS segundo a ordem dos elementos de B.

Os elementos de A que não aparecem em B vão para o final em ordem crescente.

Exemplo:
A = [5,8,9,3,5,7,1,3,4,9,5,1,8,4]
B = [3,5,7,2]
C = [3,3,3,5,5,5,7,1,1,4,4,8,8,9,9]

Complexidade requerida: O(m log m)
"""

def questao5(A, B):
    from collections import Counter

    freq = Counter(A)  # Frequências de A
    C = []

    # Primeiro, adiciona elementos na ordem de B
    for b in B:
        if b in freq:
            C.extend([b]*freq[b])
            del freq[b]

    # Agora adiciona os que sobraram, mas em ordem crescente
    restantes = []
    for val, qt in freq.items():
        restantes.extend([val]*qt)

    C.extend(sorted(restantes))  # O(m log m)

    return C


"""
===========================================================
 QUESTÃO 6
===========================================================
Dada uma sequência A com n números reais distintos,
encontrar os √n menores números em O(n).

Solução:
- Encontrar o elemento de ordem k = √n via quickselect → O(n)
- Depois, varrer o vetor e coletar todos os ≤ pivot → O(n)
"""

import math
import random

def quickselect(A, k):
    # Retorna o k-ésimo menor (0-indexed)
    if len(A) == 1:
        return A[0]

    p = random.choice(A)
    menores  = [x for x in A if x < p]
    iguais   = [x for x in A if x == p]
    maiores  = [x for x in A if x > p]

    if k < len(menores):
        return quickselect(menores, k)
    elif k < len(menores) + len(iguais):
        return p
    else:
        return quickselect(maiores, k - len(menores) - len(iguais))

def questao6(A):
    n = len(A)
    k = int(math.sqrt(n))
    limite = quickselect(A, k-1)  # o k-ésimo menor

    # Coleta dos √n menores
    menores = [x for x in A if x <= limite]

    # Caso venham mais de √n valores iguais ao pivô,
    # mantemos apenas √n elementos.
    return sorted(menores)[:k]
