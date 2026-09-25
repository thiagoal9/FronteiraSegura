"""Testes simples do sistema. Para rodar: pytest"""
from datetime import timedelta

from fronteira.analisadores import (
    AnalisadorBancario,
    AnalisadorCriminal,
    AnalisadorRota,
    ContextoAnalise,
    VerificadorFacial,
)
from fronteira.auditoria import RegistroAuditoria
from fronteira.gerador_dados import MOMENTO_DEMO, POSTO_FOZ, GeradorDados
from fronteira.modelos import NivelRisco, Sentido, TipoTransacao, TransacaoBancaria, Verificacao
from fronteira.motor_risco import MotorRisco
from fronteira.repositorio import RepositorioDados
from fronteira.utils import mascarar_cpf


def montar_contexto(pessoa=None, roubado=False):
    """Cria uma abordagem em que o dono do veículo é quem está dirigindo."""
    gerador = GeradorDados(semente=7)
    repo = RepositorioDados()
    pessoa = pessoa or gerador.nova_pessoa("Teste Silva")
    placa = gerador._cadastrar(repo, pessoa, queixa_roubo=roubado)
    verificacao = Verificacao(
        placa, gerador.captura_de(pessoa.embedding_facial), POSTO_FOZ, Sentido.BR_PY, MOMENTO_DEMO
    )
    veiculo = repo.buscar_veiculo(placa)
    return ContextoAnalise(verificacao, veiculo, pessoa, pessoa, repo), gerador


def codigos(alertas):
    return [a.codigo for a in alertas]


def test_mascarar_cpf():
    assert mascarar_cpf("123.456.789-09") == "***.456.789-**"


def test_mesma_pessoa_confere_e_pessoas_diferentes_nao():
    gerador = GeradorDados()
    verificador = VerificadorFacial()
    rosto = gerador.embedding()
    assert verificador.confere(rosto, gerador.captura_de(rosto))
    assert not verificador.confere(rosto, gerador.embedding())


def test_identificar_pessoa_pelo_rosto():
    gerador = GeradorDados()
    pessoas = [gerador.nova_pessoa() for _ in range(10)]
    achada = VerificadorFacial().identificar(gerador.captura_de(pessoas[3].embedding_facial), pessoas)
    assert achada is pessoas[3]


def test_mandado_e_veiculo_roubado():
    gerador = GeradorDados()
    pessoa = gerador.nova_pessoa("Fulano", mandado=True)
    ctx, _ = montar_contexto(pessoa, roubado=True)
    assert codigos(AnalisadorCriminal().analisar(ctx)) == ["VEICULO_ROUBADO", "MANDADO_PRISAO"]


def test_rota_frequente():
    ctx, gerador = montar_contexto()
    gerador.registrar_viagens(
        ctx.repositorio, ctx.condutor, ctx.verificacao.placa, POSTO_FOZ, MOMENTO_DEMO,
        [(d, Sentido.BR_PY) for d in (25, 20, 15, 10, 5)],
    )
    assert "ROTA_FREQUENTE" in codigos(AnalisadorRota().analisar(ctx))


def test_poucas_viagens_nao_geram_alerta():
    ctx, gerador = montar_contexto()
    gerador.registrar_viagens(
        ctx.repositorio, ctx.condutor, ctx.verificacao.placa, POSTO_FOZ, MOMENTO_DEMO,
        [(10, Sentido.BR_PY), (8, Sentido.PY_BR)],
    )
    assert AnalisadorRota().analisar(ctx) == []


def test_saque_alto_e_fracionamento():
    ctx, _ = montar_contexto()
    for horas, valor in [(50, 41000.0), (30, 44000.0), (10, 48000.0)]:
        data = MOMENTO_DEMO - timedelta(hours=horas)
        ctx.repositorio.registrar_transacao(
            TransacaoBancaria(ctx.condutor.cpf, TipoTransacao.SAQUE, valor, data)
        )
    resultado = codigos(AnalisadorBancario().analisar(ctx))
    assert "SAQUE_ATIPICO" in resultado
    assert "FRACIONAMENTO_SAQUE" in resultado


def test_saque_pequeno_nao_gera_alerta():
    ctx, _ = montar_contexto()
    data = MOMENTO_DEMO - timedelta(hours=5)
    ctx.repositorio.registrar_transacao(
        TransacaoBancaria(ctx.condutor.cpf, TipoTransacao.SAQUE, 400.0, data)
    )
    assert AnalisadorBancario().analisar(ctx) == []


def test_niveis_dos_cenarios_de_demonstracao():
    repo, cenarios = GeradorDados().montar_cenarios()
    motor = MotorRisco(repo)
    niveis = [motor.avaliar(c.verificacao).nivel for c in cenarios]
    assert niveis == [
        NivelRisco.BAIXO, NivelRisco.MEDIO, NivelRisco.MEDIO,
        NivelRisco.ALTO, NivelRisco.ALTO, NivelRisco.MEDIO,
    ]


def test_pontuacao_maxima_e_100():
    repo, cenarios = GeradorDados().montar_cenarios()
    relatorio = MotorRisco(repo).avaliar(cenarios[4].verificacao)
    assert relatorio.pontuacao == 100


def test_auditoria_nao_grava_cpf_completo(tmp_path):
    arquivo = tmp_path / "auditoria.log"
    repo, cenarios = GeradorDados().montar_cenarios()
    motor = MotorRisco(repo, auditoria=RegistroAuditoria(str(arquivo)))
    relatorio = motor.avaliar(cenarios[0].verificacao)
    conteudo = arquivo.read_text(encoding="utf-8")
    assert "***." in conteudo
    assert relatorio.condutor.cpf not in conteudo
