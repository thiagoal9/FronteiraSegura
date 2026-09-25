"""Pontos e limites do sistema. Mude os valores aqui para ajustar o comportamento."""


class ConfigRisco:
    # Reconhecimento facial
    limiar_facial = 1.0
    pontos_face_divergente = 30
    pontos_condutor_desconhecido = 20

    # Cadastro do veículo
    pontos_placa_nao_cadastrada = 50

    # Histórico criminal
    pontos_mandado = 60
    pontos_veiculo_roubado = 60
    pontos_antecedentes = 20

    # Frequência da rota Brasil <-> Paraguai
    janela_rota_dias = 30
    limite_travessias = 6
    pontos_rota_frequente = 25
    limite_bate_volta = 2
    pontos_bate_volta = 15

    # Movimentação bancária
    janela_banco_horas = 72
    limite_valor = 10000
    pontos_valor_atipico = 30
    limite_comunicacao = 50000
    minimo_fracionadas = 3
    pontos_fracionamento = 25

    # Classificação final
    nivel_medio = 30
    nivel_alto = 60
