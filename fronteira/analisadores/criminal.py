"""Consulta de histórico criminal (simulada)."""
from fronteira.analisadores.base import Analisador
from fronteira.modelos import Alerta


class AnalisadorCriminal(Analisador):
    nome = "Consulta criminal"

    def analisar(self, ctx):
        alertas = []

        if ctx.veiculo is not None and ctx.veiculo.queixa_roubo:
            alertas.append(Alerta(
                "VEICULO_ROUBADO",
                f"Veículo {ctx.veiculo.placa} com queixa de roubo/furto",
                self.config.pontos_veiculo_roubado,
                self.nome,
            ))

        if ctx.condutor is None:
            return alertas  # sem condutor identificado, não dá para consultar antecedentes

        if ctx.condutor.mandado_prisao:
            alertas.append(Alerta(
                "MANDADO_PRISAO",
                "Condutor com mandado de prisão em aberto",
                self.config.pontos_mandado,
                self.nome,
            ))

        if ctx.condutor.antecedentes:
            alertas.append(Alerta(
                "ANTECEDENTES",
                "Antecedentes: " + ", ".join(ctx.condutor.antecedentes),
                self.config.pontos_antecedentes,
                self.nome,
            ))
        return alertas
