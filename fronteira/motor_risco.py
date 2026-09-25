"""Motor de risco: roda todos os analisadores e calcula a pontuação final."""
from fronteira.analisadores import (
    AnalisadorBancario,
    AnalisadorCriminal,
    AnalisadorFacial,
    AnalisadorRota,
    ContextoAnalise,
    VerificadorFacial,
)
from fronteira.config import ConfigRisco
from fronteira.modelos import Alerta, NivelRisco, RelatorioRisco

RECOMENDACOES = {
    NivelRisco.BAIXO: "Liberar a passagem.",
    NivelRisco.MEDIO: "Encaminhar para inspeção documental e entrevista com o condutor.",
    NivelRisco.ALTO: "Encaminhar para inspeção completa e acionar o supervisor. A decisão final é do agente.",
}


class MotorRisco:
    def __init__(self, repositorio, config=None, auditoria=None):
        self.repositorio = repositorio
        self.config = config or ConfigRisco()
        self.verificador = VerificadorFacial(self.config.limiar_facial)
        self.auditoria = auditoria
        # Para criar uma regra nova, basta criar um analisador e colocar nesta lista
        self.analisadores = [
            AnalisadorFacial(self.verificador, self.config),
            AnalisadorCriminal(self.config),
            AnalisadorRota(self.config),
            AnalisadorBancario(self.config),
        ]

    def avaliar(self, verificacao):
        veiculo = self.repositorio.buscar_veiculo(verificacao.placa)
        proprietario = self.repositorio.buscar_pessoa(veiculo.proprietario_cpf) if veiculo else None
        condutor = self._identificar_condutor(verificacao, proprietario)

        ctx = ContextoAnalise(verificacao, veiculo, proprietario, condutor, self.repositorio)

        alertas = []
        if veiculo is None or proprietario is None:
            alertas.append(Alerta(
                "PLACA_NAO_CADASTRADA",
                f"Placa {verificacao.placa} sem proprietário cadastrado",
                self.config.pontos_placa_nao_cadastrada,
                "Motor de risco",
            ))
        for analisador in self.analisadores:
            alertas.extend(analisador.analisar(ctx))

        pontuacao = min(sum(a.pontos for a in alertas), 100)
        nivel = self._classificar(pontuacao)

        relatorio = RelatorioRisco(verificacao, alertas, pontuacao, nivel, RECOMENDACOES[nivel], condutor)
        if self.auditoria is not None:
            self.auditoria.registrar(relatorio)
        return relatorio

    def _identificar_condutor(self, verificacao, proprietario):
        """Quem está dirigindo? Primeiro testa o dono; se não for, procura na base."""
        rosto = verificacao.embedding_capturado
        if proprietario is not None and self.verificador.confere(rosto, proprietario.embedding_facial):
            return proprietario
        return self.verificador.identificar(rosto, self.repositorio.todas_pessoas())

    def _classificar(self, pontuacao):
        if pontuacao >= self.config.nivel_alto:
            return NivelRisco.ALTO
        if pontuacao >= self.config.nivel_medio:
            return NivelRisco.MEDIO
        return NivelRisco.BAIXO
