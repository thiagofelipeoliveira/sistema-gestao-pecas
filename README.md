# Sistema de Gestão de Peças

Trabalho da disciplina de Algoritmos e Lógica de Programação — desafio "Gestão de
Peças, Qualidade e Armazenamento". A ideia é simular a inspeção automática de peças
numa linha de montagem: em vez de alguém conferir cada peça no olho, o programa
aplica as regras de qualidade, guarda o que foi aprovado em caixas e no final mostra
um resumo de tudo.

## O que o programa faz

Menu no terminal com 5 opções:

1. Cadastrar nova peça (id, peso, cor, comprimento)
2. Listar peças aprovadas / reprovadas / todas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório final

## Critérios de aprovação

Pra ser aprovada, a peça precisa atender aos três ao mesmo tempo:

- Peso entre 95g e 105g
- Cor azul ou verde
- Comprimento entre 10cm e 20cm

Se falhar em mais de um critério, o sistema mostra todos os motivos, não só o
primeiro.

## Sobre as caixas

Cada caixa aguenta 10 peças aprovadas. Quando enche, fecha sozinha e abre uma nova.
Se eu remover uma peça de uma caixa que já estava fechada, ela reabre (volta a
aceitar peças até encher de novo) — não fazia sentido deixar ela marcada como
fechada com uma vaga sobrando.

## Estrutura do código

- `Peca`: guarda os dados da peça e tem o método que avalia se ela passa ou não
- `Caixa`: controla quantas peças tem e se já está cheia
- `SistemaGestao`: junta tudo — cadastro, decisão de armazenamento, remoção e relatório
- as funções `menu_*`: cada uma cuida de uma opção do menu

## Como rodar

Precisa de Python 3.8+ instalado.

```bash
python sistema_pecas.py
```

(em algumas máquinas o comando é `python3 sistema_pecas.py`)

Depois é só seguir o menu digitando o número da opção.

## Dados de exemplo

Assim que o programa abre, ele já cadastra automaticamente 15 peças de exemplo
(algumas aprovadas, algumas reprovadas por motivos diferentes), pra já ter
dados prontos nas opções de listar, caixas fechadas e relatório sem precisar
digitar tudo na hora. Isso é feito pela função `carregar_pecas_exemplo()`,
chamada no início do `menu_principal()`. Se quiser rodar o sistema do zero,
sem nenhuma peça pré-cadastrada, é só remover ou comentar essa linha.

## Exemplo de uso

Cadastrando uma peça aprovada:

```
Escolha uma opção: 1

ID da peça: A001
Peso (g): 98.5
Cor: azul
Comprimento (cm): 15

  Resultado: ID A001 | Peso: 98.5g | Cor: azul | Comprimento: 15.0cm | Status: Aprovada | Caixa: 1
```

Cadastrando uma peça reprovada por mais de um motivo:

```
ID da peça: A002
Peso (g): 120
Cor: preto
Comprimento (cm): 25

  Resultado: ID A002 | Peso: 120.0g | Cor: preto | Comprimento: 25.0cm | Status: Reprovada |
  Motivo(s): Peso fora do padrão (120.0g; aceito entre 95g e 105g);
  Cor não aceita ('preto'; aceitas: azul, verde);
  Comprimento fora do padrão (25.0cm; aceito entre 10cm e 20cm)
```

Relatório final:

```
Escolha uma opção: 5

Total de peças aprovadas .......... 1
Total de peças reprovadas .......... 1
Quantidade de caixas utilizadas .... 1

Motivos de reprovação:
  - Peso fora do padrão: 1 peça(s)
  - Cor não aceita: 1 peça(s)
  - Comprimento fora do padrão: 1 peça(s)
```

## Testes que fiz

Rodei um teste com 12 peças aprovadas seguidas pra ver se a caixa fechava certo com
10 e abria a próxima. Testei peça reprovada por cada critério separado e por vários
critérios juntos. E testei remover uma peça de uma caixa já fechada, pra confirmar
que ela reabre.

## Autor

Thiago Felipe de Oliveira
RA: 293439
Curso: Graduação Tecnológica em Inteligência Artificial e Automação Digital
