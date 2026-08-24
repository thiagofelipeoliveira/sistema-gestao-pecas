# Sistema de Gestão de Peças — Automação Digital

Protótipo em Python desenvolvido para o desafio **"Gestão de Peças, Qualidade e Armazenamento"**,
da disciplina de Algoritmos e Lógica de Programação.

O sistema simula, em uma linha de montagem industrial, a inspeção automática de peças,
substituindo a conferência manual por regras lógicas de aprovação/reprovação, o
armazenamento em caixas de capacidade limitada e a geração de relatórios consolidados.

## Funcionalidades

O programa é um **menu interativo em terminal** com 5 opções principais:

| Opção | Função |
|---|---|
| 1 | Cadastrar nova peça (id, peso, cor, comprimento) |
| 2 | Listar peças aprovadas / reprovadas / todas |
| 3 | Remover peça cadastrada pelo ID |
| 4 | Listar caixas fechadas |
| 5 | Gerar relatório final consolidado |
| 0 | Sair |

### Regras de qualidade aplicadas automaticamente

Uma peça é **aprovada** somente se atender simultaneamente aos três critérios abaixo;
caso contrário, é **reprovada** e o(s) motivo(s) específico(s) são registrados:

- Peso entre **95g e 105g**
- Cor **azul** ou **verde**
- Comprimento entre **10cm e 20cm**

### Armazenamento em caixas

- Cada caixa comporta no máximo **10 peças aprovadas**.
- Ao atingir a capacidade máxima, a caixa é **fechada automaticamente** e uma nova é aberta.
- Se uma peça for removida de uma caixa que já estava fechada, a caixa **reabre**
  (volta a aceitar novas peças até completar 10 novamente), simulando o reaproveitamento
  de espaço físico.

## Estrutura do código

- **`Peca`**: representa cada peça e contém a lógica de avaliação (`avaliar()`).
- **`Caixa`**: representa uma caixa de armazenamento e controla seu preenchimento.
- **`SistemaGestao`**: classe central que orquestra cadastro, avaliação, armazenamento,
  remoção e geração de relatórios.
- **Funções de menu**: camada de interface (CLI) que interage com o usuário e chama os
  métodos da classe `SistemaGestao`.

## Como rodar o programa

**Pré-requisito:** Python 3.8 ou superior instalado ([python.org](https://python.org)).

1. Baixe/clone o repositório.
2. Abra um terminal na pasta do projeto.
3. Execute:

```bash
python sistema_pecas.py
```

(em alguns sistemas o comando é `python3 sistema_pecas.py`)

4. Siga as instruções do menu, digitando o número da opção desejada e pressionando Enter.

## Exemplo de entrada e saída

**Cadastrando uma peça aprovada:**

```
Escolha uma opção: 1

=======================================================
                  CADASTRAR NOVA PEÇA
=======================================================
ID da peça: A001
Peso (g): 98.5
Cor: azul
Comprimento (cm): 15

  Resultado: ID A001 | Peso: 98.5g | Cor: azul | Comprimento: 15.0cm | Status: Aprovada | Caixa: 1
```

**Cadastrando uma peça reprovada (múltiplos motivos):**

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

**Relatório final:**

```
Escolha uma opção: 5

=======================================================
                    RELATÓRIO FINAL
=======================================================
Total de peças aprovadas .......... 1
Total de peças reprovadas .......... 1
Quantidade de caixas utilizadas .... 1

Motivos de reprovação:
  - Peso fora do padrão: 1 peça(s)
  - Cor não aceita: 1 peça(s)
  - Comprimento fora do padrão: 1 peça(s)
```

## Testes realizados

O sistema foi validado com um cenário de 12 peças aprovadas seguidas (para confirmar o
fechamento automático da caixa ao atingir 10 unidades e a abertura da caixa seguinte),
peças reprovadas por peso, cor, comprimento e por múltiplos motivos simultâneos, e a
remoção de uma peça de uma caixa já fechada (confirmando a reabertura da caixa).

## Autor

**Thiago Felipe de Oliveira**
RA: 293439
Curso: Graduação Tecnológica em Inteligência Artificial e Automação Digital
