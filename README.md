# 🛒 Cesta na Mão - Pipeline de Dados (ETL)

Este repositório contém os scripts de engenharia de dados (ETL) responsáveis por extrair, higienizar e padronizar o acervo histórico de planilhas (2022-2026) do projeto de extensão **Cesta na Mão** (IFNMG - Campus Januária).

O objetivo principal é transformar dados brutos e manuais coletados em campo em uma base estruturada (JSON/CSV), pronta para ser consumida e importada em um banco de dados relacional (PostgreSQL).

## 📁 Estrutura do Repositório

* `DADOS/`: Pasta base contendo as planilhas originais de coleta, organizadas rigorosamente por ano e mês.
* `constantes.py`: Arquivo de configuração contendo as listas oficiais e validadas de supermercados, postos, produtos e marcas. Utilizado como base de consulta para a correção de erros de digitação via *fuzzy matching*.
* `etl.py`: Script principal do pipeline de Extração, Transformação e Carga. Lê as planilhas, aplica as regras de validação (datas, tratamento de moedas via Regex e correção textual) e consolida o histórico.
* `notebook.ipynb`: Notebook voltado para o *Data Profiling* (perfilamento de dados). Analisa frequências textuais e gera relatórios para auditoria de erros humanos.
* `opendf.ipynb`: Notebook auxiliar para testes, visualização de *dataframes* e conversão secundária.
* `requirements.txt`: Lista de dependências Python necessárias para rodar o projeto.

## 🚀 Como Configurar o Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Natan-ls/Projeto-cesta-basica-.git
   cd Projeto-cesta-basica-
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   # No Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # No Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Instale as dependências:**
   *(O projeto é compatível com gerenciadores modernos como o `uv` ou o `pip` tradicional)*

```bash
pip install -r requirements.txt
```

## 🛠️ Como Utilizar

### Passo 1: Auditoria de Padrões

Antes de processar a base final, principalmente se novas planilhas brutas forem adicionadas à pasta `DADOS/`, é recomendável verificar se há variações severas de nomenclatura.

1. Abra e execute as células do `notebook.ipynb`.
2. O script criará a pasta `analise/` gerando o arquivo `analise_padrao.xlsx`.
3. Verifique as abas do Excel. Caso identifique um produto, marca ou estabelecimento inédito, adicione-o às listas do arquivo `constantes.py`.

### Passo 2: Execução do Pipeline (ETL)

Para higienizar os dados históricos e gerar o arquivo de carga (Seed) para o banco de dados, execute:

```bash
python etl.py
```

O script criará automaticamente a pasta `db/` e salvará o arquivo `historico.json`. Este arquivo conterá todos os preços higienizados, cruzados e validados, prontos para a importação estruturada.
