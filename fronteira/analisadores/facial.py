"""Verificação facial (simulada).

Cada rosto é uma lista de números (embedding). Rostos da mesma pessoa geram
números parecidos, então comparamos a distância entre as duas listas.
"""
import math

from fronteira.analisadores.base import Analisador
from fronteira.modelos import Alerta


class VerificadorFacial:
    def __init__(self, limiar=1.0):
        self.limiar = limiar

    def distancia(self, a, b):
        return math.dist(a, b)

    def confere(self, a, b):
        return self.distancia(a, b) <= self.limiar

    def identificar(self, embedding, pessoas):
        """Devolve a pessoa mais parecida, ou None se ninguém for parecido o bastante."""
        melhor = None
        menor_distancia = None
        for pessoa in pessoas:
            d = self.distancia(embedding, pessoa.embedding_facial)
            if menor_distancia is None or d < menor_distancia:
                melhor, menor_distancia = pessoa, d
        if menor_distancia is not None and menor_distancia <= self.limiar:
            return melhor
        return None


class AnalisadorFacial(Analisador):
    nome = "Verificação facial"

    def __init__(self, verificador, config=None):
        super().__init__(config)
        self.verificador = verificador

    def analisar(self, ctx):
        alertas = []

        if ctx.proprietario is not None:
            confere = self.verificador.confere(
                ctx.verificacao.embedding_capturado, ctx.proprietario.embedding_facial
            )
            if not confere:
                alertas.append(Alerta(
                    "FACE_DIVERGENTE",
                    "Rosto do condutor não confere com o dono do veículo",
                    self.config.pontos_face_divergente,
                    self.nome,
                ))

        if ctx.condutor is None:
            alertas.append(Alerta(
                "CONDUTOR_NAO_IDENTIFICADO",
                "Rosto do condutor não encontrado na base de dados",
                self.config.pontos_condutor_desconhecido,
                self.nome,
            ))
        return alertas
