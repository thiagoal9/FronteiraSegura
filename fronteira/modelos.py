"""Classes de dados usadas pelo resto do sistema."""
from enum import Enum

from fronteira.utils import mascarar_cpf


class NivelRisco(Enum):
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"


class Sentido(Enum):
    BR_PY = "Brasil → Paraguai"
    PY_BR = "Paraguai → Brasil"


class TipoTransacao(Enum):
    SAQUE = "saque"
    DEPOSITO = "depósito"


class Pessoa:
    def __init__(self, cpf, nome, embedding_facial, antecedentes=None, mandado_prisao=False):
        self.cpf = cpf
        self.nome = nome
        self.embedding_facial = embedding_facial  # "rosto" representado como lista de números
        self.antecedentes = antecedentes or []
        self.mandado_prisao = mandado_prisao

    @property
    def cpf_mascarado(self):
        return mascarar_cpf(self.cpf)


class Veiculo:
    def __init__(self, placa, proprietario_cpf, queixa_roubo=False):
        self.placa = placa
        self.proprietario_cpf = proprietario_cpf
        self.queixa_roubo = queixa_roubo


class PostoFronteira:
    def __init__(self, nome, cidade_brasil, cidade_paraguai):
        self.nome = nome
        self.cidade_brasil = cidade_brasil
        self.cidade_paraguai = cidade_paraguai


class Travessia:
    def __init__(self, cpf, placa, posto, sentido, data_hora):
        self.cpf = cpf
        self.placa = placa
        self.posto = posto
        self.sentido = sentido
        self.data_hora = data_hora


class TransacaoBancaria:
    def __init__(self, cpf, tipo, valor, data_hora):
        self.cpf = cpf
        self.tipo = tipo
        self.valor = valor
        self.data_hora = data_hora


class Verificacao:
    """Dados capturados pelo posto na hora da abordagem."""

    def __init__(self, placa, embedding_capturado, posto, sentido, momento):
        self.placa = placa
        self.embedding_capturado = embedding_capturado
        self.posto = posto
        self.sentido = sentido
        self.momento = momento


class Alerta:
    def __init__(self, codigo, descricao, pontos, origem):
        self.codigo = codigo
        self.descricao = descricao
        self.pontos = pontos
        self.origem = origem


class RelatorioRisco:
    def __init__(self, verificacao, alertas, pontuacao, nivel, recomendacao, condutor=None):
        self.verificacao = verificacao
        self.alertas = alertas
        self.pontuacao = pontuacao
        self.nivel = nivel
        self.recomendacao = recomendacao
        self.condutor = condutor

    def texto(self):
        v = self.verificacao
        if self.condutor:
            condutor = f"{self.condutor.nome} (CPF {self.condutor.cpf_mascarado})"
        else:
            condutor = "não identificado"

        linhas = [
            f"Placa {v.placa} | {v.posto.nome} | {v.sentido.value}",
            f"Condutor: {condutor}",
            f"Risco: {self.nivel.value} ({self.pontuacao}/100)",
        ]
        if self.alertas:
            linhas.append("Alertas:")
            for a in self.alertas:
                linhas.append(f"  +{a.pontos} {a.codigo}: {a.descricao}")
        else:
            linhas.append("Alertas: nenhum")
        linhas.append(f"Recomendação: {self.recomendacao}")
        return "\n".join(linhas)
