"""Funções auxiliares pequenas, usadas em vários pontos do sistema."""


def mascarar_cpf(cpf):
    """Esconde os dígitos do meio do CPF. Ex.: 123.456.789-09 -> ***.456.789-**"""
    return "***" + cpf[3:11] + "-**"


def formatar_brl(valor):
    """Ex.: 1500 -> 'R$ 1500,00'"""
    return "R$ " + f"{valor:.2f}".replace(".", ",")
