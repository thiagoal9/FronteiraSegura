"""Gera dados fictícios e os cenários de demonstração.

Nada aqui é real: nomes, CPFs, placas, rostos e valores são inventados.
"""
import random
from datetime import datetime, timedelta

from fronteira.modelos import (
    Pessoa,
    PostoFronteira,
    Sentido,
    TipoTransacao,
    TransacaoBancaria,
    Travessia,
    Veiculo,
    Verificacao,
)
from fronteira.repositorio import RepositorioDados

MOMENTO_DEMO = datetime(2026, 9, 24, 14, 0)

POSTO_FOZ = PostoFronteira("Ponte da Amizade", "Foz do Iguaçu (PR)", "Ciudad del Este")
POSTO_PONTA_PORA = PostoFronteira("Posto Ponta Porã", "Ponta Porã (MS)", "Pedro Juan Caballero")

NOMES = ["Carlos", "Ana", "João", "Mariana", "Pedro", "Luiza", "Rafael", "Beatriz"]
SOBRENOMES = ["Almeida", "Souza", "Oliveira", "Santos", "Lima", "Pereira", "Costa", "Ribeiro"]


class CenarioDemo:
    def __init__(self, titulo, descricao, verificacao):
        self.titulo = titulo
        self.descricao = descricao
        self.verificacao = verificacao


class GeradorDados:
    def __init__(self, semente=42):
        self.rng = random.Random(semente)  # com a mesma semente, os dados saem sempre iguais

    def cpf(self):
        d = "".join(str(self.rng.randint(0, 9)) for _ in range(11))
        return f"{d[0:3]}.{d[3:6]}.{d[6:9]}-{d[9:11]}"

    def placa(self):
        letras = "".join(self.rng.choice("ABCDEFGHIJ") for _ in range(3))
        return f"{letras}{self.rng.randint(0, 9)}{self.rng.choice('ABCDEFGHIJ')}{self.rng.randint(10, 99)}"

    def nome(self):
        return self.rng.choice(NOMES) + " " + self.rng.choice(SOBRENOMES)

    def embedding(self):
        """Um rosto novo: 5 números aleatórios."""
        return [self.rng.uniform(0, 10) for _ in range(5)]

    def captura_de(self, embedding):
        """Uma nova foto da mesma pessoa: os mesmos números com uma pequena variação."""
        return [x + self.rng.uniform(-0.1, 0.1) for x in embedding]

    def nova_pessoa(self, nome=None, antecedentes=None, mandado=False):
        return Pessoa(self.cpf(), nome or self.nome(), self.embedding(), antecedentes, mandado)

    def historico_bancario(self, repo, cpf, ate, quantidade=10):
        """Movimentações pequenas e normais nos últimos meses."""
        for _ in range(quantidade):
            dias = self.rng.uniform(5, 180)
            tipo = self.rng.choice(list(TipoTransacao))
            valor = round(self.rng.uniform(100, 3000), 2)
            repo.registrar_transacao(TransacaoBancaria(cpf, tipo, valor, ate - timedelta(days=dias)))

    def registrar_viagens(self, repo, pessoa, placa, posto, agora, viagens):
        """Cada viagem é um par (dias_atras, sentido)."""
        for dias_atras, sentido in viagens:
            data = agora - timedelta(days=dias_atras)
            repo.registrar_travessia(Travessia(pessoa.cpf, placa, posto, sentido, data))

    def popular_base(self, repo, quantidade=20):
        """Pessoas aleatórias na base, para o reconhecimento facial ter que escolher."""
        for _ in range(quantidade):
            repo.adicionar_pessoa(self.nova_pessoa())

    def _cadastrar(self, repo, pessoa, queixa_roubo=False):
        """Coloca a pessoa na base e cadastra um veículo no nome dela. Devolve a placa."""
        placa = self.placa()
        repo.adicionar_pessoa(pessoa)
        repo.adicionar_veiculo(Veiculo(placa, pessoa.cpf, queixa_roubo))
        return placa

    def montar_cenarios(self):
        repo = RepositorioDados()
        self.popular_base(repo)
        agora = MOMENTO_DEMO
        cenarios = []

        # 1: viajante ocasional (risco BAIXO)
        p1 = self.nova_pessoa("Carlos Almeida")
        placa1 = self._cadastrar(repo, p1)
        self.historico_bancario(repo, p1.cpf, agora)
        self.registrar_viagens(repo, p1, placa1, POSTO_FOZ, agora,
                                [(20, Sentido.BR_PY), (18, Sentido.PY_BR)])
        v1 = Verificacao(placa1, self.captura_de(p1.embedding_facial), POSTO_FOZ, Sentido.BR_PY, agora)
        cenarios.append(CenarioDemo(
            "Viajante ocasional",
            "O dono está dirigindo, viaja pouco e a movimentação bancária é normal.", v1))

        # 2: viaja muito, com idas e voltas no mesmo dia (risco MÉDIO)
        p2 = self.nova_pessoa("Mariana Souza")
        placa2 = self._cadastrar(repo, p2)
        self.historico_bancario(repo, p2.cpf, agora)
        self.registrar_viagens(repo, p2, placa2, POSTO_PONTA_PORA, agora, [
            (25, Sentido.BR_PY), (24.7, Sentido.PY_BR),
            (15, Sentido.BR_PY), (14.6, Sentido.PY_BR),
            (5, Sentido.BR_PY), (4.6, Sentido.PY_BR),
            (2, Sentido.BR_PY),
        ])
        v2 = Verificacao(placa2, self.captura_de(p2.embedding_facial), POSTO_PONTA_PORA, Sentido.PY_BR, agora)
        cenarios.append(CenarioDemo(
            "Viajante frequente (bate-e-volta)",
            "Muitas travessias em 30 dias, com idas e voltas no mesmo dia.", v2))

        # 3: saques altos antes da viagem (risco MÉDIO)
        p3 = self.nova_pessoa("Rafael Lima")
        placa3 = self._cadastrar(repo, p3)
        self.historico_bancario(repo, p3.cpf, agora)
        for horas_atras, valor in [(60, 42000.0), (48, 44500.0), (30, 47000.0)]:
            data = agora - timedelta(hours=horas_atras)
            repo.registrar_transacao(TransacaoBancaria(p3.cpf, TipoTransacao.SAQUE, valor, data))
        v3 = Verificacao(placa3, self.captura_de(p3.embedding_facial), POSTO_FOZ, Sentido.BR_PY, agora)
        cenarios.append(CenarioDemo(
            "Saques altos antes da viagem",
            "Três saques logo abaixo do limite de comunicação nas 72h anteriores.", v3))

        # 4: outra pessoa dirigindo, com mandado (risco ALTO)
        dono4 = self.nova_pessoa("Beatriz Costa")
        placa4 = self._cadastrar(repo, dono4)
        motorista4 = self.nova_pessoa("Diego Rocha", mandado=True)
        repo.adicionar_pessoa(motorista4)
        v4 = Verificacao(placa4, self.captura_de(motorista4.embedding_facial), POSTO_FOZ, Sentido.BR_PY, agora)
        cenarios.append(CenarioDemo(
            "Condutor diferente do dono, com mandado",
            "O rosto não é o do dono do carro. A pessoa é identificada na base e tem mandado.", v4))

        # 5: veículo roubado e condutor desconhecido (risco ALTO)
        dono5 = self.nova_pessoa("Patrícia Dias")
        placa5 = self._cadastrar(repo, dono5, queixa_roubo=True)
        v5 = Verificacao(placa5, self.captura_de(self.embedding()), POSTO_PONTA_PORA, Sentido.BR_PY, agora)
        cenarios.append(CenarioDemo(
            "Veículo roubado, condutor desconhecido",
            "A placa tem queixa de roubo e o rosto não está na base.", v5))

        # 6: placa não cadastrada (risco MÉDIO)
        p6 = self.nova_pessoa("Tiago Ferreira")
        repo.adicionar_pessoa(p6)
        v6 = Verificacao(self.placa(), self.captura_de(p6.embedding_facial), POSTO_FOZ, Sentido.PY_BR, agora)
        cenarios.append(CenarioDemo(
            "Placa não cadastrada",
            "Nenhum dono para a placa. O condutor é identificado só pelo rosto.", v6))

        return repo, cenarios
