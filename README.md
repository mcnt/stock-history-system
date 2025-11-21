# Sistema de Histórico de Ações

## Visão Geral
O Sistema de Histórico de Ações é uma aplicação em Python projetada para coletar, armazenar e visualizar dados históricos de preços de ações da NASDAQ. Este sistema serve como base para futuras ferramentas de análise financeira.

## Funcionalidades
- Coleta automática de dados da NASDAQ para qualquer ticker de ação especificado.
- Banco de dados SQLite para armazenamento estruturado de ativos e preços.
- Interface web para visualização de preços históricos em formato de gráfico e tabela.
- Atualização periódica dos dados (configurável).
- Suporte a múltiplos ativos simultâneos.

## Estrutura do Projeto
```
stock-history-system
├── src/
│   ├── collector/          # Módulo de coleta de dados
│   │   ├── __init__.py
│   │   └── nasdaq_scraper.py  # Implementação do coletor
│   │
│   ├── db/                 # Módulo de banco de dados
│   │   ├── __init__.py
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   └── init_db.py      # Inicialização do banco
│   │
│   ├── web/                # Módulo web
│   │   ├── __init__.py
│   │   ├── app.py          # Aplicação Flask
│   │   └── templates/      # Templates HTML
│   │       └── index.html  # Interface do usuário
│   │
├── tests/                  # Testes unitários
├── .gitignore
├── requirements.txt        # Dependências do projeto
├── .env.example            # Exemplo de variáveis de ambiente
├── run_collector.py        # Script para executar o coletor
├── run_server.py           # Script para iniciar o servidor web
└── README.md               # Documentação do projeto
```
## Estrutura do Banco de Dados

### Tabela: assets
- id: INTEGER (PK)
- ticker: TEXT (UNIQUE)

### Tabela: prices
- id: INTEGER (PK)
- asset_id: INTEGER (FK para assets.id)
- date: DATE
- open_price: FLOAT
- high_price: FLOAT
- low_price: FLOAT
- close_price: FLOAT
- volume: INTEGER

## Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

## Instalação
1. Clone o repositório:
   ```bash
   git clone <url-do-repositório>
   cd stock-history-system
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env conforme necessário
   ```

## Dados de Exemplo

Para popular o banco de dados com dados de exemplo, execute:

```bash
python seed_database.py
```

## Como Usar
### Coletando Dados
Para iniciar a coleta de dados de um ativo específico:
```bash
# Coletar dados do ticker AAPL
python run_collector.py AAPL

# Coletar dados uma única vez
python run_collector.py AAPL --once

# Especificar intervalo de coleta (em segundos)
python run_collector.py AAPL --interval 3600  # A cada hora
```

### Iniciando o Servidor Web
Para iniciar a aplicação web:
```bash
python run_server.py
```

Acesse `http://localhost:5000` no seu navegador para visualizar a interface.

### Acessando os Dados via API
- `GET /api/prices/<ticker>`: Retorna os preços históricos de um ativo
- `POST /api/collect/<ticker>`: Força a coleta de dados para um ativo

## Configuração
O arquivo `.env` suporta as seguintes variáveis:
- `DATABASE_URL`: URL de conexão com o banco de dados (padrão: SQLite local)
- `DEBUG`: Ativa modo de depuração (True/False)
- `COLLECTOR_INTERVAL`: Intervalo padrão de coleta em segundos

## Solução de Problemas
- **Erro de conexão**: Verifique sua conexão com a internet
- **Dados não encontrados**: Verifique se o ticker está correto e se a ação está listada na NASDAQ
- **Erros de banco de dados**: Tente remover o arquivo `stock_history.db` para forçar a recriação do banco

## Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.