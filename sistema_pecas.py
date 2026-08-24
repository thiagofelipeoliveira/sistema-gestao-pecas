"""
Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento
-------------------------------------------------------------------------
Sistema em Python para controle de produção e qualidade de peças fabricadas
em uma linha de montagem industrial.

Autor: (preencha com seu nome)
Disciplina: Algoritmos e Lógica de Programação
"""

# ============================================================
# CONSTANTES - critérios de qualidade e regras de negócio
# ============================================================
PESO_MINIMO = 95       # gramas
PESO_MAXIMO = 105      # gramas
CORES_ACEITAS = ("azul", "verde")
COMPRIMENTO_MINIMO = 10   # cm
COMPRIMENTO_MAXIMO = 20   # cm
CAPACIDADE_CAIXA = 10      # peças por caixa


# ============================================================
# CLASSES DO DOMÍNIO
# ============================================================
class Peca:
    """Representa uma peça produzida na linha de montagem."""

    def __init__(self, id_peca, peso, cor, comprimento):
        self.id = id_peca
        self.peso = peso
        self.cor = cor.lower().strip()
        self.comprimento = comprimento
        self.status = None      # "Aprovada" ou "Reprovada"
        self.motivos = []       # lista de motivos de reprovação (se houver)
        self.caixa = None       # número da caixa em que foi armazenada

    def avaliar(self):
        """Aplica as regras de qualidade e define status/motivos da peça."""
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
    """Representa uma caixa de armazenamento de peças aprovadas."""

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
    """Sistema central: cadastro, avaliação, armazenamento e relatórios."""

    def __init__(self):
        self.pecas_cadastradas = {}   # id -> Peca (todas, aprovadas e reprovadas)
        self.caixas = [Caixa(1)]      # começa com a caixa 1 aberta
        self.proximo_numero_caixa = 2

    # -------------------- Cadastro --------------------
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
        """Coloca a peça aprovada na caixa atual; abre nova caixa se necessário."""
        caixa_atual = self.caixas[-1]
        if caixa_atual.fechada:
            caixa_atual = Caixa(self.proximo_numero_caixa)
            self.proximo_numero_caixa += 1
            self.caixas.append(caixa_atual)
        caixa_atual.adicionar(peca)

    # -------------------- Consultas --------------------
    def listar_por_status(self, status):
        return [p for p in self.pecas_cadastradas.values() if p.status == status]

    def listar_caixas_fechadas(self):
        return [c for c in self.caixas if c.fechada]

    # -------------------- Remoção --------------------
    def remover_peca(self, id_peca):
        peca = self.pecas_cadastradas.get(id_peca)
        if peca is None:
            raise ValueError(f"Nenhuma peça encontrada com o ID '{id_peca}'.")

        # Se a peça está armazenada em uma caixa, remove de lá também.
        if peca.caixa is not None:
            for caixa in self.caixas:
                if caixa.numero == peca.caixa:
                    caixa.pecas = [p for p in caixa.pecas if p.id != id_peca]
                    # Uma caixa que perde uma peça deixa de estar cheia,
                    # então ela volta a poder receber novas peças.
                    if len(caixa.pecas) < CAPACIDADE_CAIXA:
                        caixa.fechada = False
                    break

        del self.pecas_cadastradas[id_peca]
        return peca

    # -------------------- Relatório --------------------
    def gerar_relatorio(self):
        aprovadas = self.listar_por_status("Aprovada")
        reprovadas = self.listar_por_status("Reprovada")
        caixas_com_pecas = [c for c in self.caixas if c.pecas]

        # Contabiliza motivos de reprovação agrupados
        contagem_motivos = {}
        for peca in reprovadas:
            for motivo in peca.motivos:
                chave = motivo.split(" (")[0]  # agrupa por tipo de motivo
                contagem_motivos[chave] = contagem_motivos.get(chave, 0) + 1

        relatorio = {
            "total_aprovadas": len(aprovadas),
            "total_reprovadas": len(reprovadas),
            "motivos_reprovacao": contagem_motivos,
            "quantidade_caixas_utilizadas": len(caixas_com_pecas),
            "pecas_reprovadas_detalhe": reprovadas,
        }
        return relatorio


# ============================================================
# FUNÇÕES AUXILIARES DE ENTRADA (com validação)
# ============================================================
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


# ============================================================
# INTERFACE DE MENU (CLI)
# ============================================================
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
