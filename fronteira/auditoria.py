"""Registro de auditoria: guarda quem foi avaliado e qual foi o resultado."""
import os
from datetime import datetime


class RegistroAuditoria:
    def __init__(self, caminho=None):
        self.caminho = caminho  # arquivo onde gravar (opcional)
        self.entradas = []

    def registrar(self, relatorio):
        v = relatorio.verificacao
        condutor = relatorio.condutor.cpf_mascarado if relatorio.condutor else "nao_identificado"
        codigos = ",".join(a.codigo for a in relatorio.alertas)

        linha = (
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | placa={v.placa} | condutor={condutor} "
            f"| risco={relatorio.nivel.name} | pontos={relatorio.pontuacao} | alertas={codigos}"
        )
        self.entradas.append(linha)

        if not self.caminho:
            return
        pasta = os.path.dirname(self.caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with open(self.caminho, "a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")
