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
├── SEQUENCES/
└── INDEXES/
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
- Coleta de índices

## Logs

O script gera logs detalhados sobre o processo de coleta, incluindo:
- Conexão com o banco de dados
- Coleta de cada objeto
- Erros que possam ocorrer durante o processo

## Estrutura do Projeto

```
schema-colector/
├── schema_collector.py      # Script principal
├── config.py               # Configurações do projeto
├── db_connection.py        # Gerenciamento de conexão com o banco
├── collectors/            # Módulos de coleta específicos
│   ├── table_collector.py
│   ├── view_collector.py
│   ├── procedure_collector.py
│   ├── function_collector.py
│   ├── package_collector.py
│   ├── trigger_collector.py
│   ├── sequence_collector.py
│   └── index_collector.py
├── utils/                 # Utilitários
│   ├── file_utils.py
│   └── logging_utils.py
└── schema_objects/        # Pasta onde os objetos são salvos
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 