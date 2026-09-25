# FronteiraSegura

Sistema em Python que apoia a fiscalização em **rodovias de fronteira Brasil–Paraguai**. Ao abordar um veículo, ele cruza o rosto do condutor, o histórico criminal, a frequência de travessias e a movimentação bancária, e devolve uma **pontuação de risco** (BAIXO, MÉDIO ou ALTO) com o motivo de cada alerta.

> Versão inicial de um projeto acadêmico. Todos os dados são **fictícios** e o reconhecimento facial é **simulado**.

## Como executar

Precisa do Python 3 instalado. Dentro da pasta do projeto:

```bash
python3 -m fronteira
```

Para rodar os testes:

```bash
pip install pytest
pytest
```

## Estrutura

```
fronteira-segura/
├── fronteira/
│   ├── modelos.py        # classes: Pessoa, Veiculo, Travessia, Alerta...
│   ├── config.py         # pontos e limites (é só mudar os valores)
│   ├── repositorio.py    # base de dados em memória
│   ├── motor_risco.py    # roda os analisadores e calcula o risco
│   ├── auditoria.py      # log de auditoria (CPF mascarado)
│   ├── gerador_dados.py  # dados fictícios e cenários de demonstração
│   ├── utils.py          # funções auxiliares
│   ├── main.py           # demonstração
│   └── analisadores/
│       ├── base.py       # classe base Analisador
│       ├── facial.py     # o rosto é do dono do veículo?
│       ├── criminal.py   # mandado, antecedentes, veículo roubado
│       ├── rota.py       # frequência de travessias
│       └── bancario.py   # saques e depósitos antes da viagem
├── tests/
├── docs/                 # relatório e diagrama de classes
├── logs/
└── README.md
```
