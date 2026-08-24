"""
Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento
Disciplina: Algoritmos e Lógica de Programação

Autor: Thiago Felipe de Oliveira
RA: 293439
Curso: Graduação Tecnológica em Inteligência Artificial e Automação Digital

Ideia geral: simular a inspeção de peças de uma linha de montagem, que hoje
é feita na mão. O programa recebe os dados de cada peça, decide se ela passa
ou não nos critérios de qualidade, guarda as aprovadas em caixas de 10 e no
final mostra um resumo de tudo.
"""

# critérios de aprovação (dei uma olhada no enunciado e coloquei aqui em cima
# pra ser fácil de mudar depois, se precisar)
PESO_MINIMO = 95
PESO_MAXIMO = 105
CORES_ACEITAS = ("azul", "verde")
COMPRIMENTO_MINIMO = 10
COMPRIMENTO_MAXIMO = 20
CAPACIDADE_CAIXA = 10


class Peca:
    """Uma peça que saiu da linha de montagem: id, peso, cor e comprimento."""

    def __init__(self, id_peca, peso, cor, comprimento):
        self.id = id_peca
        self.peso = peso
        self.cor = cor.lower().strip()
        self.comprimento = comprimento
        self.status = None
        self.motivos = []  # só é preenchido se a peça for reprovada
        self.caixa = None

    def avaliar(self):
        # checo os três critérios separadamente porque uma peça pode falhar
        # em mais de um ao mesmo tempo, e eu queria mostrar todos os motivos
        # e não só o primeiro que encontrar
        motivos = []

        if not (PESO_MINIMO <= self.peso <= PESO_MAXIMO):
            motivos.append(
                f"Peso fora do padrão ({self.peso}g; aceito entre "
                f"{PESO_MINIMO}g e {PESO_MAXIMO}g)"
            )

        if self.cor not in CORES_ACEITAS:
            motivos.append(
                f"Cor não aceita ('{self.cor}'; aceitas: {', '.join(CORES_ACEITAS)})"
            )

        if not (COMPRIMENTO_MINIMO <= self.comprimento <= COMPRIMENTO_MAXIMO):
            motivos.append(
                f"Comprimento fora do padrão ({self.comprimento}cm; aceito entre "
                f"{COMPRIMENTO_MINIMO}cm e {COMPRIMENTO_MAXIMO}cm)"
            )

        self.motivos = motivos
        self.status = "Reprovada" if motivos else "Aprovada"
        return self.status

    def __str__(self):
        base = (f"ID {self.id} | Peso: {self.peso}g | Cor: {self.cor} | "
                f"Comprimento: {self.comprimento}cm | Status: {self.status}")
        if self.status == "Reprovada":
            base += f" | Motivo(s): {'; '.join(self.motivos)}"
        if self.caixa:
            base += f" | Caixa: {self.caixa}"
        return base


class Caixa:
    """Caixa onde as peças aprovadas vão sendo guardadas, até 10 por vez."""

    def __init__(self, numero):
        self.numero = numero
        self.pecas = []
        self.fechada = False

    def adicionar(self, peca):
        self.pecas.append(peca)
        peca.caixa = self.numero
        if len(self.pecas) >= CAPACIDADE_CAIXA:
            self.fechada = True

    def __str__(self):
        ids = ", ".join(str(p.id) for p in self.pecas)
        status = "FECHADA" if self.fechada else "EM USO"
        return f"Caixa {self.numero} [{status}] ({len(self.pecas)} peças): {ids}"


class SistemaGestao:
    """Junta tudo: cadastro de peças, avaliação, caixas e relatório final."""

    def __init__(self):
        self.pecas_cadastradas = {}
        self.caixas = [Caixa(1)]
        self.proximo_numero_caixa = 2

    def cadastrar_peca(self, id_peca, peso, cor, comprimento):
        if id_peca in self.pecas_cadastradas:
            raise ValueError(f"Já existe uma peça cadastrada com o ID '{id_peca}'.")

        peca = Peca(id_peca, peso, cor, comprimento)
        peca.avaliar()
        self.pecas_cadastradas[id_peca] = peca

        if peca.status == "Aprovada":
            self._armazenar(peca)

        return peca

    def _armazenar(self, peca):
        # se a caixa atual já tá cheia, abre uma nova antes de guardar
        caixa_atual = self.caixas[-1]
        if caixa_atual.fechada:
            caixa_atual = Caixa(self.proximo_numero_caixa)
            self.proximo_numero_caixa += 1
            self.caixas.append(caixa_atual)
        caixa_atual.adicionar(peca)

    def listar_por_status(self, status):
        return [p for p in self.pecas_cadastradas.values() if p.status == status]

    def listar_caixas_fechadas(self):
        return [c for c in self.caixas if c.fechada]

    def remover_peca(self, id_peca):
        peca = self.pecas_cadastradas.get(id_peca)
        if peca is None:
            raise ValueError(f"Nenhuma peça encontrada com o ID '{id_peca}'.")

        # se a peça já tava numa caixa, tira ela de lá também.
        # e como a caixa perdeu uma peça, ela deixa de estar "cheia"
        # e volta a aceitar peças novas
        if peca.caixa is not None:
            for caixa in self.caixas:
                if caixa.numero == peca.caixa:
                    caixa.pecas = [p for p in caixa.pecas if p.id != id_peca]
                    if len(caixa.pecas) < CAPACIDADE_CAIXA:
                        caixa.fechada = False
                    break

        del self.pecas_cadastradas[id_peca]
        return peca

    def gerar_relatorio(self):
        aprovadas = self.listar_por_status("Aprovada")
        reprovadas = self.listar_por_status("Reprovada")
        caixas_com_pecas = [c for c in self.caixas if c.pecas]

        contagem_motivos = {}
        for peca in reprovadas:
            for motivo in peca.motivos:
                chave = motivo.split(" (")[0]
                contagem_motivos[chave] = contagem_motivos.get(chave, 0) + 1

        return {
            "total_aprovadas": len(aprovadas),
            "total_reprovadas": len(reprovadas),
            "motivos_reprovacao": contagem_motivos,
            "quantidade_caixas_utilizadas": len(caixas_com_pecas),
            "pecas_reprovadas_detalhe": reprovadas,
        }


# ---------- funções auxiliares de leitura, com uma validação simples ----------

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("  >> Valor inválido. Digite um número (ex.: 98.5).")


def ler_texto_nao_vazio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  >> Este campo não pode ficar vazio.")


# ---------- dados de exemplo (só pra facilitar de mostrar no vídeo) ----------

def carregar_pecas_exemplo(sistema):
    """
    Cadastra algumas peças de exemplo assim que o programa abre, pra já ter
    dados prontos pra mostrar nas opções de listar/relatório sem precisar
    digitar tudo na hora da gravação. É só remover a chamada dessa função lá
    no menu_principal() se não quiser mais esse carregamento automático.
    """
    exemplos = [
        ("P001", 98,  "azul",  15),
        ("P002", 100, "verde", 12),
        ("P003", 102, "azul",  18),
        ("P004", 97,  "verde", 14),
        ("P005", 99,  "azul",  16),
        ("P006", 200, "azul",  15),    # reprovada: peso
        ("P007", 100, "preto", 15),    # reprovada: cor
        ("P008", 100, "verde", 50),    # reprovada: comprimento
        ("P009", 150, "amarelo", 30),  # reprovada: vários motivos
        ("P010", 95,  "azul",  10),
        ("P011", 105, "verde", 20),
        ("P012", 96,  "azul",  17),
        ("P013", 101, "verde", 13),
        ("P014", 100, "azul",  15),    # essa fecha a caixa 1 (10 aprovadas)
        ("P015", 98,  "verde", 14),    # essa já entra na caixa 2
    ]
    for id_peca, peso, cor, comprimento in exemplos:
        sistema.cadastrar_peca(id_peca, peso, cor, comprimento)


# ---------- menu (interface em terminal) ----------

def exibir_cabecalho(texto):
    print("\n" + "=" * 55)
    print(texto.center(55))
    print("=" * 55)


def menu_cadastrar(sistema):
    exibir_cabecalho("CADASTRAR NOVA PEÇA")
    id_peca = ler_texto_nao_vazio("ID da peça: ")
    if id_peca in sistema.pecas_cadastradas:
        print(f"  >> Já existe uma peça com o ID '{id_peca}'.")
        return
    peso = ler_float("Peso (g): ")
    cor = ler_texto_nao_vazio("Cor: ")
    comprimento = ler_float("Comprimento (cm): ")

    peca = sistema.cadastrar_peca(id_peca, peso, cor, comprimento)
    print(f"\n  Resultado: {peca}")


def menu_listar(sistema):
    exibir_cabecalho("LISTAR PEÇAS APROVADAS / REPROVADAS")
    print("1. Aprovadas\n2. Reprovadas\n3. Todas")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        pecas = sistema.listar_por_status("Aprovada")
    elif opcao == "2":
        pecas = sistema.listar_por_status("Reprovada")
    else:
        pecas = list(sistema.pecas_cadastradas.values())

    if not pecas:
        print("  Nenhuma peça encontrada para este filtro.")
        return

    for peca in pecas:
        print(f"  - {peca}")


def menu_remover(sistema):
    exibir_cabecalho("REMOVER PEÇA CADASTRADA")
    id_peca = ler_texto_nao_vazio("ID da peça a remover: ")
    try:
        peca = sistema.remover_peca(id_peca)
        print(f"  >> Peça '{peca.id}' removida com sucesso.")
    except ValueError as erro:
        print(f"  >> Erro: {erro}")


def menu_caixas_fechadas(sistema):
    exibir_cabecalho("CAIXAS FECHADAS")
    caixas = sistema.listar_caixas_fechadas()
    if not caixas:
        print("  Nenhuma caixa foi fechada ainda.")
        return
    for caixa in caixas:
        print(f"  - {caixa}")


def menu_relatorio(sistema):
    exibir_cabecalho("RELATÓRIO FINAL")
    r = sistema.gerar_relatorio()

    print(f"Total de peças aprovadas .......... {r['total_aprovadas']}")
    print(f"Total de peças reprovadas .......... {r['total_reprovadas']}")
    print(f"Quantidade de caixas utilizadas .... {r['quantidade_caixas_utilizadas']}")

    if r["motivos_reprovacao"]:
        print("\nMotivos de reprovação:")
        for motivo, qtd in r["motivos_reprovacao"].items():
            print(f"  - {motivo}: {qtd} peça(s)")
    else:
        print("\nNenhuma peça reprovada até o momento.")


def menu_principal():
    sistema = SistemaGestao()
    carregar_pecas_exemplo(sistema)  # remova essa linha se não quiser dados de exemplo

    opcoes = {
        "1": ("Cadastrar nova peça", menu_cadastrar),
        "2": ("Listar peças aprovadas/reprovadas", menu_listar),
        "3": ("Remover peça cadastrada", menu_remover),
        "4": ("Listar caixas fechadas", menu_caixas_fechadas),
        "5": ("Gerar relatório final", menu_relatorio),
        "0": ("Sair", None),
    }

    while True:
        exibir_cabecalho("SISTEMA DE GESTÃO DE PEÇAS - LINHA DE MONTAGEM")
        for chave, (descricao, _) in opcoes.items():
            print(f"  {chave}. {descricao}")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        elif escolha in opcoes:
            try:
                opcoes[escolha][1](sistema)
            except ValueError as erro:
                print(f"  >> Erro: {erro}")
        else:
            print("  >> Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
