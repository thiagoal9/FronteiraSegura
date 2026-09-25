"""Movimentação bancária nas horas antes da travessia."""
from datetime import timedelta

from fronteira.analisadores.base import Analisador
from fronteira.modelos import Alerta, TipoTransacao
from fronteira.utils import formatar_brl


class AnalisadorBancario(Analisador):
    nome = "Análise bancária"

    def analisar(self, ctx):
        if ctx.condutor is None:
            return []

        cfg = self.config
        v = ctx.verificacao
        inicio = v.momento - timedelta(hours=cfg.janela_banco_horas)
        transacoes = ctx.repositorio.transacoes_da_pessoa(ctx.condutor.cpf, inicio, v.momento)

        alertas = []
        for tipo in TipoTransacao:
            valores = [t.valor for t in transacoes if t.tipo == tipo]
            for alerta in (self._valor_atipico(tipo, valores), self._fracionamento(tipo, valores)):
                if alerta is not None:
                    alertas.append(alerta)
        return alertas

    def _valor_atipico(self, tipo, valores):
        """Algum valor é alto demais?"""
        cfg = self.config
        if not valores or max(valores) < cfg.limite_valor:
            return None
        return Alerta(
            f"{tipo.name}_ATIPICO",
            f"{tipo.value.capitalize()} de {formatar_brl(max(valores))} "
            f"nas {cfg.janela_banco_horas}h antes da travessia",
            cfg.pontos_valor_atipico,
            self.nome,
        )

    def _fracionamento(self, tipo, valores):
        """Vários valores logo abaixo do limite de comunicação ao banco central?"""
        cfg = self.config
        minimo = cfg.limite_comunicacao * 0.8
        suspeitos = sum(1 for valor in valores if minimo <= valor < cfg.limite_comunicacao)
        if suspeitos < cfg.minimo_fracionadas:
            return None
        return Alerta(
            f"FRACIONAMENTO_{tipo.name}",
            f"{suspeitos} {tipo.value}s logo abaixo do limite de {formatar_brl(cfg.limite_comunicacao)}",
            cfg.pontos_fracionamento,
            self.nome,
        )
