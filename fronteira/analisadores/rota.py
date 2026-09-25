"""Frequência de travessias na rota Brasil <-> Paraguai."""
from datetime import timedelta

from fronteira.analisadores.base import Analisador
from fronteira.modelos import Alerta


class AnalisadorRota(Analisador):
    nome = "Frequência de rota"

    def analisar(self, ctx):
        alertas = []
        if ctx.condutor is None:
            return alertas

        cfg = self.config
        v = ctx.verificacao
        inicio = v.momento - timedelta(days=cfg.janela_rota_dias)
        travessias = ctx.repositorio.travessias_da_pessoa(ctx.condutor.cpf, inicio, v.momento)

        total = len(travessias) + 1  # a travessia de agora também conta
        if total >= cfg.limite_travessias:
            alertas.append(Alerta(
                "ROTA_FREQUENTE",
                f"{total} travessias em {cfg.janela_rota_dias} dias",
                cfg.pontos_rota_frequente,
                self.nome,
            ))

        pares = self._contar_bate_e_volta(travessias)
        if pares >= cfg.limite_bate_volta:
            alertas.append(Alerta(
                "ROTA_BATE_E_VOLTA",
                f"{pares} idas e voltas em menos de 24h",
                cfg.pontos_bate_volta,
                self.nome,
            ))
        return alertas

    def _contar_bate_e_volta(self, travessias):
        """Conta quantas vezes a pessoa foi e voltou em menos de 24 horas."""
        pares = 0
        for anterior, atual in zip(travessias, travessias[1:]):
            horas = (atual.data_hora - anterior.data_hora).total_seconds() / 3600
            if anterior.sentido != atual.sentido and horas <= 24:
                pares += 1
        return pares
