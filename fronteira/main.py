"""Demonstração: avalia 6 abordagens fictícias e mostra o risco de cada uma."""
from fronteira.auditoria import RegistroAuditoria
from fronteira.gerador_dados import GeradorDados
from fronteira.motor_risco import MotorRisco


def main():
    repo, cenarios = GeradorDados().montar_cenarios()

    auditoria = RegistroAuditoria("logs/auditoria.log")
    motor = MotorRisco(repo, auditoria=auditoria)

    contagem = {"BAIXO": 0, "MÉDIO": 0, "ALTO": 0}
    for numero, cenario in enumerate(cenarios, start=1):
        relatorio = motor.avaliar(cenario.verificacao)
        contagem[relatorio.nivel.value] += 1

        print(f"=== Cenário {numero}: {cenario.titulo} ===")
        print(cenario.descricao)
        print(relatorio.texto())
        print()

    print(f"Resumo: BAIXO {contagem['BAIXO']} | MÉDIO {contagem['MÉDIO']} | ALTO {contagem['ALTO']}")
    print("Log de auditoria gravado em logs/auditoria.log")


if __name__ == "__main__":
    main()
