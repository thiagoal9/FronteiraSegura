# Relatório do Projeto

## 1. Título

**FronteiraSegura: sistema de análise de risco para rodovias de fronteira Brasil–Paraguai**

## 2. Descrição

Sistema em Python que apoia agentes de fiscalização nos postos de fronteira. Quando um veículo é abordado, o sistema recebe a placa e o rosto capturado do condutor e faz quatro verificações:

1. **Rosto:** o rosto do condutor é o mesmo do dono registrado do veículo? Se não for, quem é?
2. **Histórico criminal:** o condutor tem mandado de prisão ou antecedentes? O veículo tem queixa de roubo?
3. **Rota:** o condutor faz a rota Brasil–Paraguai (ou Paraguai–Brasil) com muita frequência?
4. **Banco:** houve saque ou depósito muito alto nas horas antes da viagem?

Cada problema encontrado vira um **alerta com pontos**. A soma define o risco (BAIXO, MÉDIO ou ALTO), e o sistema mostra o motivo de cada alerta. A decisão final é sempre do agente.

Nesta versão inicial os dados são fictícios e o reconhecimento facial é simulado: cada rosto é uma lista de 5 números, e rostos da mesma pessoa têm números parecidos.

## 3. Justificativa

As fronteiras com o Paraguai são uma rota importante para contrabando, descaminho, tráfico de drogas e armas. O agente tem pouco tempo por abordagem, e as informações costumam ficar em sistemas separados. Reunir tudo em uma avaliação só ajuda a priorizar os casos mais suspeitos e a explicar cada decisão.

Um sistema assim usa dados sensíveis, e isso foi considerado:

- **Biometria** é dado pessoal sensível (LGPD, Lei 13.709/2018).
- **Dados bancários** são protegidos pelo sigilo bancário (Lei Complementar 105/2001). Na prática, o acesso dependeria de ordem judicial ou de comunicações formais, como as feitas ao COAF.
- **Erros são possíveis:** por isso o sistema apenas recomenda, mostra o motivo de cada alerta e deixa a decisão para o agente.
- **Privacidade e rastreabilidade:** o CPF é sempre mostrado e gravado mascarado, e cada avaliação fica registrada em um log de auditoria.

Por isso o projeto usa somente dados fictícios.

## 4. Funcionalidades

- Comparar o rosto do condutor com o do dono do veículo
- Identificar o condutor na base quando o rosto não é do dono
- Consultar mandado de prisão, antecedentes e queixa de roubo do veículo
- Contar as travessias dos últimos 30 dias e detectar idas e voltas em menos de 24h
- Detectar saque ou depósito alto nas 72 horas antes da viagem
- Detectar fracionamento: vários valores logo abaixo do limite de comunicação ao banco
- Avisar quando a placa não tem dono cadastrado
- Calcular a pontuação (máximo 100) e classificar o risco
- Gravar um log de auditoria com CPF mascarado
- Gerar dados e cenários fictícios para demonstração

### Pontos de cada alerta (configuráveis em `config.py`)

| Alerta | Pontos |
|---|---|
| Rosto diferente do dono do veículo | 30 |
| Condutor não identificado na base | 20 |
| Placa não cadastrada | 50 |
| Mandado de prisão | 60 |
| Veículo com queixa de roubo | 60 |
| Antecedentes | 20 |
| 6 ou mais travessias em 30 dias | 25 |
| 2 ou mais idas e voltas em menos de 24h | 15 |
| Saque ou depósito de R$ 10.000 ou mais | 30 |
| 3 ou mais valores entre R$ 40.000 e R$ 50.000 (fracionamento) | 25 |

Classificação: menos de 30 pontos é **BAIXO**, de 30 a 59 é **MÉDIO**, 60 ou mais é **ALTO**. Os valores são ilustrativos.

### Resultado da demonstração

| Cenário | Pontos | Nível |
|---|---|---|
| Viajante ocasional | 0 | BAIXO |
| Viajante frequente (bate-e-volta) | 40 | MÉDIO |
| Saques altos antes da viagem | 55 | MÉDIO |
| Condutor diferente do dono, com mandado | 90 | ALTO |
| Veículo roubado, condutor desconhecido | 100 | ALTO |
| Placa não cadastrada | 50 | MÉDIO |

## 5. Temas abordados

- Programação orientada a objetos: classes, herança, classe abstrata e polimorfismo
- Listas, dicionários, laços de repetição e condicionais
- Datas e intervalos de tempo
- Reconhecimento facial (conceito): rosto representado por números e comparado por distância
- Modelagem com diagrama de classes (UML)
- Testes automatizados
- Ética, privacidade e legislação (LGPD e sigilo bancário)

## 6. Tecnologias

- Python 3
- Git e GitHub
- pytest (testes)
- Graphviz e Mermaid (diagrama de classes)

## 7. Bibliotecas

Biblioteca padrão do Python:

| Módulo | Uso |
|---|---|
| `enum` | Níveis de risco, sentido da travessia e tipo de transação |
| `abc` | Classe abstrata `Analisador` |
| `datetime` | Datas e janelas de tempo |
| `math` | Distância entre dois rostos (`math.dist`) |
| `random` | Geração de dados fictícios |
| `os` | Criar a pasta do log de auditoria |

Externa: **pytest**, somente para os testes.

## 8. Distribuição das tarefas

> Preencha com os nomes da equipe.

| Tarefa | Arquivos | Responsável |
|---|---|---|
| Diagrama de classes | `docs/diagrama_classes.*` | |
| Classes de dados | `modelos.py`, `utils.py` | |
| Verificação facial | `analisadores/facial.py` | |
| Histórico criminal | `analisadores/criminal.py` | |
| Frequência de rota | `analisadores/rota.py` | |
| Análise bancária | `analisadores/bancario.py` | |
| Motor de risco e configuração | `motor_risco.py`, `config.py`, `analisadores/base.py` | |
| Dados, repositório e auditoria | `repositorio.py`, `gerador_dados.py`, `auditoria.py` | |
| Demonstração e testes | `main.py`, `tests/` | |
| Relatório e repositório no GitHub | `docs/RELATORIO.md`, `README.md` | |

## 9. Limitações e próximos passos

- O reconhecimento facial é simulado. O próximo passo é usar fotos reais com uma biblioteca de reconhecimento facial.
- Os dados são fictícios e os pesos são ilustrativos. Precisariam ser calibrados com dados reais.
- Os dados ficam só na memória e somem quando o programa termina. Um banco de dados resolveria isso.
- Ler a placa automaticamente por imagem e criar um painel para os agentes.

## 10. Como executar

```bash
python3 -m fronteira
```
