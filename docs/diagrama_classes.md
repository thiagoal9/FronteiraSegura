# Diagrama de Classes

Versão em imagem: [`diagrama_classes.png`](diagrama_classes.png) (também em [SVG](diagrama_classes.svg); fonte Graphviz em [`diagrama_classes.dot`](diagrama_classes.dot)).

A versão abaixo em Mermaid é renderizada automaticamente pelo GitHub.

```mermaid
classDiagram
    direction TB

    class Analisador {
        <<abstract>>
        +str nome
        +ConfigRisco config
        +analisar(ctx) list~Alerta~
    }
    class AnalisadorFacial {
        +VerificadorFacial verificador
        +analisar(ctx) list~Alerta~
    }
    class AnalisadorCriminal {
        +analisar(ctx) list~Alerta~
    }
    class AnalisadorRota {
        +analisar(ctx) list~Alerta~
        -_contar_bate_e_volta(seq) int
    }
    class AnalisadorBancario {
        +analisar(ctx) list~Alerta~
        -_valor_atipico(...) Alerta
        -_fracionamento(...) Alerta
    }
    class VerificadorFacial {
        +float limiar
        +distancia(a, b) float
        +confere(a, b) bool
        +identificar(emb, pessoas) Pessoa
    }
    class ContextoAnalise {
        +Verificacao verificacao
        +Veiculo veiculo
        +Pessoa proprietario
        +Pessoa condutor
        +RepositorioDados repositorio
    }
    class ConfigRisco {
        +float limiar_facial
        +int limite_travessias
        +int janela_banco_horas
        +int limite_valor
    }
    class MotorRisco {
        +RepositorioDados repositorio
        +ConfigRisco config
        +VerificadorFacial verificador
        +list~Analisador~ analisadores
        +RegistroAuditoria auditoria
        +avaliar(verificacao) RelatorioRisco
    }
    class RepositorioDados {
        +adicionar_pessoa(p)
        +adicionar_veiculo(v)
        +registrar_travessia(t)
        +registrar_transacao(t)
        +buscar_pessoa(cpf) Pessoa
        +buscar_veiculo(placa) Veiculo
        +travessias_da_pessoa(cpf, ini, fim)
        +transacoes_da_pessoa(cpf, ini, fim)
    }
    class RegistroAuditoria {
        +str caminho
        +registrar(relatorio)
    }
    class GeradorDados {
        +nova_pessoa() Pessoa
        +embedding() list~float~
        +captura_de(emb) list~float~
        +montar_cenarios() tuple
    }
    class CenarioDemo {
        +str titulo
        +str descricao
        +Verificacao verificacao
    }
    class Pessoa {
        +str cpf
        +str nome
        +list~float~ embedding_facial
        +list~str~ antecedentes
        +bool mandado_prisao
    }
    class Veiculo {
        +str placa
        +str proprietario_cpf
        +bool queixa_roubo
    }
    class PostoFronteira {
        +str nome
        +str cidade_brasil
        +str cidade_paraguai
    }
    class Travessia {
        +str cpf
        +str placa
        +PostoFronteira posto
        +Sentido sentido
        +datetime data_hora
    }
    class TransacaoBancaria {
        +str cpf
        +TipoTransacao tipo
        +float valor
        +datetime data_hora
    }
    class Verificacao {
        +str placa
        +list~float~ embedding_capturado
        +PostoFronteira posto
        +Sentido sentido
        +datetime momento
    }
    class Alerta {
        +str codigo
        +str descricao
        +int pontos
        +str origem
    }
    class RelatorioRisco {
        +Verificacao verificacao
        +list~Alerta~ alertas
        +int pontuacao
        +NivelRisco nivel
        +str recomendacao
        +Pessoa condutor
        +texto() str
    }
    class NivelRisco {
        <<enumeration>>
        BAIXO
        MEDIO
        ALTO
    }
    class Sentido {
        <<enumeration>>
        BR_PY
        PY_BR
    }
    class TipoTransacao {
        <<enumeration>>
        SAQUE
        DEPOSITO
    }

    Analisador <|-- AnalisadorFacial
    Analisador <|-- AnalisadorCriminal
    Analisador <|-- AnalisadorRota
    Analisador <|-- AnalisadorBancario

    MotorRisco o-- "1..*" Analisador
    RepositorioDados o-- Pessoa
    RepositorioDados o-- Veiculo
    RepositorioDados o-- Travessia
    RepositorioDados o-- TransacaoBancaria
    RelatorioRisco *-- "0..*" Alerta

    Veiculo --> Pessoa : proprietário
    Travessia --> PostoFronteira
    Travessia --> Sentido
    TransacaoBancaria --> TipoTransacao
    Verificacao --> PostoFronteira
    Verificacao --> Sentido
    RelatorioRisco --> NivelRisco
    RelatorioRisco --> Verificacao
    RelatorioRisco --> Pessoa : condutor
    ContextoAnalise --> Verificacao
    ContextoAnalise --> Veiculo
    ContextoAnalise --> Pessoa
    ContextoAnalise --> RepositorioDados
    AnalisadorFacial --> VerificadorFacial
    MotorRisco --> VerificadorFacial
    MotorRisco --> RepositorioDados
    Analisador --> ConfigRisco
    CenarioDemo --> Verificacao

    MotorRisco ..> RelatorioRisco : cria
    MotorRisco ..> ContextoAnalise : cria
    MotorRisco ..> RegistroAuditoria : usa
    Analisador ..> ContextoAnalise : usa
    Analisador ..> Alerta : cria
    RegistroAuditoria ..> RelatorioRisco : usa
    GeradorDados ..> RepositorioDados : popula
    GeradorDados ..> CenarioDemo : cria
```

## Decisões de projeto

- **Herança e polimorfismo:** `Analisador` é uma classe abstrata; cada regra de negócio é uma subclasse. O `MotorRisco` percorre a lista de analisadores sem saber qual é qual, então adicionar uma regra nova não exige alterar o motor.
- **Composição:** `RelatorioRisco` é composto por `Alerta`s, que não fazem sentido fora dele.
- **Agregação:** `RepositorioDados` guarda pessoas, veículos, travessias e transações, que existem independentemente dele.
- **Configuração centralizada:** `ConfigRisco` concentra pesos e limites (princípio de responsabilidade única).
