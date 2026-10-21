# Amazon Engineering Challenge – Árvores Balanceadas (AVL e Rubro-Negra)

Trabalho da Unidade II da disciplina IMD0039 – Estruturas de Dados Básicas II.

**Autor:** [Luis Guilherme Lucas Barreto] – [20250030776]

## Contexto

Na Black Friday, o sistema de catálogo da Amazon precisa inserir, buscar e remover produtos com rapidez, mesmo com muitos acessos. Como Tech Lead, o desafio é implementar e comparar duas árvores balanceadas, a **AVL** e a **Rubro-Negra**, e recomendar qual usar.

Os algoritmos de balanceamento foram feitos manualmente, sem bibliotecas prontas de árvores.

## Funcionalidades

Nas duas árvores:

- Inserção
- Busca
- Remoção
- Percurso em ordem (valores em ordem crescente)
- Impressão da estrutura da árvore (a Rubro-Negra mostra a cor de cada nó)
- Altura da árvore e contagem de rotações (e de recolorimentos na Rubro-Negra)

O programa principal permite escolher em tempo de execução qual árvore usar.

## Estrutura do projeto

| Arquivo | Descrição |
|---|---|
| `avl.py` | Árvore AVL |
| `red_black.py` | Árvore Rubro-Negra |
| `main.py` | Programa com menu para escolher a árvore e executar as operações |
| `compare.py` | Comparação entre as duas árvores com os mesmos dados |
| `tests/test_trees.py` | Testes automatizados |

## Como executar

**Dependências:** apenas Python 3 (testado com Python 3.15). Não é preciso instalar nenhum pacote e não há etapa de compilação, pois o Python é interpretado.

Programa principal:

```
py main.py
```

Comparação entre as árvores:

```
py compare.py
```

Testes:

```
py -m unittest discover -s tests -v
```

Em Linux ou macOS, use `python3` no lugar de `py`.

## Exemplo de uso

```
Escolha a árvore:
1 - AVL
2 - Rubro-Negra
```

Depois da escolha, o menu oferece:

| Opção | Ação |
|---|---|
| 1 | Inserir um valor |
| 2 | Buscar um valor |
| 3 | Remover um valor |
| 4 | Mostrar os elementos em ordem crescente |
| 5 | Mostrar a estrutura da árvore |
| 0 | Sair |

Exemplo de estrutura (opção 5) após inserir 10, 20 e 30 na Rubro-Negra:

```
Raiz: 20 (BLACK)
  Esquerda: 10 (RED)
  Direita: 30 (RED)
```

Na AVL, a mesma sequência produz a mesma forma, sem as cores.

## Decisões de projeto

- **Inserção de valor duplicado:** não é permitida. A árvore não muda, `insert` devolve `False` e o menu avisa o usuário.
- **Busca de valor inexistente:** `search` devolve `None` e o menu informa que o valor não foi encontrado.
- **Remoção de valor inexistente:** a árvore não muda, `remove` devolve `False` e o menu informa que o valor não existe.
- **Árvore vazia:** busca e remoção funcionam sem erro, o percurso devolve lista vazia e a estrutura mostra `(árvore vazia)`.
- **Remoção de nó com dois filhos:** o nó é substituído pelo seu sucessor em ordem (o menor valor da subárvore direita).

## Como os algoritmos funcionam

### AVL

Cada nó guarda sua altura. O fator de balanceamento é a altura da subárvore esquerda menos a da direita, e deve ficar entre -1 e 1.

Depois de cada inserção ou remoção, os nós do caminho são reavaliados de baixo para cima. Se o fator sair do intervalo, há quatro casos:

| Caso | Correção |
|---|---|
| Esquerda-Esquerda | Rotação simples à direita |
| Direita-Direita | Rotação simples à esquerda |
| Esquerda-Direita | Rotação à esquerda no filho, depois à direita |
| Direita-Esquerda | Rotação à direita no filho, depois à esquerda |

### Rubro-Negra

Cada nó é vermelho ou preto. As regras são:

1. A raiz é preta.
2. Nó vermelho não tem filho vermelho.
3. Todo caminho de um nó até suas folhas tem o mesmo número de nós pretos.

A implementação usa um nó sentinela (`nil`) preto no lugar dos filhos vazios.

**Inserção:** o novo nó entra vermelho. Se o pai também for vermelho, olha-se a cor do tio:

- Tio vermelho: recolore pai, tio e avô, e a verificação sobe para o avô.
- Tio preto: faz uma ou duas rotações (conforme o nó seja filho do mesmo lado ou de lado oposto) e recolore.

**Remoção:** quando se remove um nó preto, a árvore fica com um "preto a menos" em um caminho. A correção olha o irmão do nó:

- Irmão vermelho: rotação para transformar em um dos casos seguintes.
- Irmão preto com filhos pretos: recolore o irmão de vermelho e sobe.
- Irmão preto com algum filho vermelho: uma ou duas rotações com recoloração resolvem.

## Testes

Os testes ficam em `tests/test_trees.py` e rodam nas duas árvores. Depois de cada inserção ou remoção eles verificam as propriedades de balanceamento (fator de balanceamento e alturas na AVL; cores e altura negra na Rubro-Negra) e a ordem dos elementos.

| Cenário exigido | Como foi testado |
|---|---|
| Inserção crescente, decrescente e desordenada | 100 chaves crescentes, 100 decrescentes e 200 aleatórias (semente fixa) |
| Busca de elementos existentes e inexistentes | Todas as chaves inseridas e várias ausentes |
| Remoção de nós com diferentes filhos | Folha, nó com 1 filho, nó com 2 filhos, raiz e último elemento |
| Remoção de elemento inexistente | Em árvore com elementos e em remoção repetida |
| Árvore vazia e com um elemento | Testes dedicados |
| Verificação das propriedades de balanceamento | Checagem após cada operação, inclusive em 300 inserções e 150 remoções |
| Mesmos dados e operações nas duas árvores | 600 operações idênticas, comparadas com um `set` de referência |
| Altura limitada | 1000 chaves crescentes têm altura menor que 2·log₂(n+1) |

Também há testes do menu e da comparação.

## Análise comparativa

`py compare.py` insere 1000 chaves e depois remove 500 sorteadas, usando exatamente os mesmos dados e as mesmas remoções nas duas árvores.

```
Dados       | Árvore      | Altura | Rotações | Altura pós-rem. | Rotações pós-rem | Recolor.
------------+-------------+--------+----------+-----------------+------------------+---------
Crescente   | AVL         |     10 |      990 |              10 |               96 |        -
Crescente   | Rubro-Negra |     17 |      983 |              10 |              102 |     1590
------------+-------------+--------+----------+-----------------+------------------+---------
Decrescente | AVL         |     10 |      990 |              10 |               62 |        -
Decrescente | Rubro-Negra |     17 |      983 |              10 |               73 |     1590
------------+-------------+--------+----------+-----------------+------------------+---------
Aleatório   | AVL         |     12 |      692 |              11 |              180 |        -
Aleatório   | Rubro-Negra |     12 |      598 |              12 |              191 |      659
```

- **Altura:** logo após as inserções, "Altura" é o número de níveis do caminho mais longo. A coluna "Rotações" conta as rotações feitas nas inserções.
- **Altura pós-rem. e Rotações pós-rem:** o mesmo, medido depois das 500 remoções (só as rotações das remoções).
- **Recolor.:** recolorimentos da Rubro-Negra (casos em que a correção sobe na árvore). A AVL não usa cores.

### Observações

- **Estratégia de balanceamento:** a AVL é rígida (diferença de altura de no máximo 1). A Rubro-Negra é mais flexível (o caminho mais longo é no máximo o dobro do mais curto).
- **Altura final:** a AVL fica mais baixa em dados ordenados (10 contra 17). Em dados aleatórios as duas ficam próximas (12 e 12 após inserir).
- **Rotações e ajustes:** os números de rotações são parecidos. A Rubro-Negra rotaciona menos nas inserções aleatórias (598 contra 692) e usa recolorimentos para compensar. Nas remoções, a AVL fez menos rotações nos três conjuntos de dados.
- Os valores vêm de uma única execução com semente fixa e dependem desta implementação.

### Vantagens, limitações e aplicações

| | AVL | Rubro-Negra |
|---|---|---|
| Vantagens | Árvore mais baixa, buscas mais rápidas | Reorganiza menos na inserção e na remoção |
| Limitações | Mais rotações em atualizações frequentes, guarda altura em cada nó | Árvore até cerca de 2 vezes mais alta, regras de remoção mais complexas |
| Aplicações | Sistemas com muita leitura e poucas alterações (catálogos, índices) | Sistemas com muitas inserções e remoções (mapas e conjuntos de bibliotecas padrão, agendadores) |

### Recomendação

Para o catálogo da Amazon na Black Friday, recomendo a **AVL** se o fluxo for dominado por consultas, como buscar produtos e preços, pois ela mantém a árvore mais baixa e a busca mais rápida, como mostram as alturas medidas. Se houver muitas atualizações de estoque, com inserções e remoções constantes, a **Rubro-Negra** passa a ser uma boa escolha porque exige menos reorganização estrutural por operação. Como em um catálogo as consultas costumam superar muito as alterações, a recomendação final é a AVL.

## Observação

Não foram usadas bibliotecas prontas de árvores; apenas módulos padrão do Python (`random`, `unittest` e similares) em testes e comparação.
