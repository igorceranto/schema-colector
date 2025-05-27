# Schema Collector

Ferramenta para coletar objetos de um schema Oracle e organizá-los em arquivos SQL.

## Requisitos

- Python 3.7+
- Oracle Client
- Acesso ao banco de dados Oracle

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_DSN=seu_host:porta/servico
DB_SCHEMA=seu_schema
```

## Uso

Execute o script principal:
```bash
python schema_collector.py
```

Os objetos serão coletados e organizados na pasta `schema_objects` com a seguinte estrutura:
```
schema_objects/
├── TABLES/
├── VIEWS/
├── PROCEDURES/
├── FUNCTIONS/
├── PACKAGES/
├── TRIGGERS/
└── SEQUENCES/
```

Cada objeto será salvo em um arquivo `.sql` separado dentro de sua respectiva pasta.

## Funcionalidades

- Coleta de tabelas
- Coleta de views
- Coleta de procedures
- Coleta de functions
- Coleta de packages
- Coleta de triggers
- Coleta de sequences

## Logs

O script gera logs detalhados sobre o processo de coleta, incluindo:
- Conexão com o banco de dados
- Coleta de cada objeto
- Erros que possam ocorrer durante o processo 