"""Base comum a todos os analisadores de risco."""
from fronteira.config import ConfigRisco


class ContextoAnalise:
    """Tudo que um analisador precisa saber sobre a abordagem.

    O "condutor" é a pessoa identificada pelo rosto capturado
    (pode ser o dono do veículo, outra pessoa da base, ou None).
    """

    def __init__(self, verificacao, veiculo, proprietario, condutor, repositorio):
        self.verificacao = verificacao
        self.veiculo = veiculo
        self.proprietario = proprietario
        self.condutor = condutor
        self.repositorio = repositorio


class Analisador:
    """Toda regra nova é uma subclasse que sobrescreve analisar()."""

    nome = "Analisador"

    def __init__(self, config=None):
        self.config = config or ConfigRisco()

    def analisar(self, ctx):
        return []
