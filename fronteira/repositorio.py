"""Guarda os dados do sistema em memória (simula as bases oficiais)."""


def normalizar_placa(placa):
    return placa.replace("-", "").upper()


class RepositorioDados:
    def __init__(self):
        self._pessoas = {}
        self._veiculos = {}
        self._travessias = []
        self._transacoes = []

    def adicionar_pessoa(self, pessoa):
        self._pessoas[pessoa.cpf] = pessoa

    def adicionar_veiculo(self, veiculo):
        self._veiculos[normalizar_placa(veiculo.placa)] = veiculo

    def registrar_travessia(self, travessia):
        self._travessias.append(travessia)

    def registrar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def buscar_pessoa(self, cpf):
        return self._pessoas.get(cpf)

    def buscar_veiculo(self, placa):
        return self._veiculos.get(normalizar_placa(placa))

    def todas_pessoas(self):
        return list(self._pessoas.values())

    def travessias_da_pessoa(self, cpf, inicio, fim):
        itens = [t for t in self._travessias if t.cpf == cpf and inicio <= t.data_hora <= fim]
        itens.sort(key=lambda t: t.data_hora)
        return itens

    def transacoes_da_pessoa(self, cpf, inicio, fim):
        itens = [t for t in self._transacoes if t.cpf == cpf and inicio <= t.data_hora <= fim]
        itens.sort(key=lambda t: t.data_hora)
        return itens
