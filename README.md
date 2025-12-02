# Super-Dashboard CE — Visão 360° de Produtos

Este projeto consiste em um **Super-Dashboard consolidado** desenvolvido em **Python + Streamlit** que integra dados de Vendas, Estoque e Compras, oferecendo aos gestores uma **visão 360° de cada produto** para identificar riscos, oportunidades e tomar decisões estratégicas de forma integrada.

O projeto também inclui dashboards individuais para análise isolada de vendas, controle de estoque e gestão de compras.

---

## Autor

**Lucas Willian Santos**

---

##  Funcionalidades

### Super-Dashboard (Consolidado) ⭐
- **Integração 360°**: Visão unificada de Estoque, Vendas e Compras por produto
- **Filtros Interativos**: Produto, Categoria, Loja, Período (com atualização em tempo real)
- **Painel de Visão 360°**: Para cada produto, exibe estoque vs vendas vs compras com alertas visuais
- **Indicadores Estratégicos**: Produtos críticos, maior gasto, lucratividade, excesso de estoque
- **Série Temporal**: Receita vs Gasto mensal para planejamento estratégico
- **Comparativo de Fornecedores**: Scatter plot (preço vs prazo) com análise de desempenho
- **Heatmap Integrado**: Relação estoque × vendas × compras para top 15 produtos
- **Recomendações Automáticas**: Alertas de ruptura, oportunidades de custo, produtos lucrativos
- **Download de Dados**: Exportação de produtos críticos, lista consolidada ou segmentada

### Dashboard de Vendas
- Filtros por loja, produto e período
- Gráfico de série temporal (vendas mensais)
- Top 10 produtos mais vendidos
- Cálculo automático de receita
- Download dos dados filtrados
- Importação de CSV/XLSX ou uso de dados de exemplo

### Dashboard de Estoque
- Upload de arquivos CSV/XLSX com dados de estoque
- Filtros por categoria e busca por nome de produto
- Tabela interativa com destaque para produtos críticos
- Indicadores de produtos abaixo do estoque mínimo
- Gráfico comparativo: Estoque Atual vs Estoque Mínimo
- Cálculo do valor total do inventário
- Download dos dados filtrados
- Recomendações rápidas para gestores

### Dashboard de Compras e Fornecedores
- Upload de arquivos CSV/XLSX com dados de compras
- Filtros por fornecedor, produto e período
- **Comparativo entre Fornecedores**: Preço médio vs Prazo médio de entrega (gráfico scatter)
- **Volume de Compras por Mês**: Série temporal com gasto mensal
- **Produtos com Maior Gasto**: Top 15 produtos por investimento acumulado
- Indicadores: total gasto, quantidade comprada, fornecedores únicos, transações
- Recomendações estratégicas para gestores
- Download dos dados filtrados

---

## Tecnologias Utilizadas

- **Python** 3.9+
- **Streamlit** - Framework para criação de dashboards interativos
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Gráficos interativos
- **NumPy** - Operações numéricas
- **Openpyxl** - Leitura de arquivos Excel

---

## Instalação

### 1. Pré-requisitos

Certifique-se de ter o Python 3.9 ou superior instalado em seu sistema.

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install streamlit pandas plotly numpy openpyxl
```

Ou crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
openpyxl>=3.1.0
```

E então execute:

```bash
pip install -r requirements.txt
```

---

## Executando os Dashboards

### ⭐ Super-Dashboard (Recomendado - Visão Consolidada)

```bash
streamlit run app/Super_Dashboard_Streamlit.py
```

### Dashboard de Vendas (Individual)

```bash
streamlit run app/Dashboard_Vendas_Streamlit.py
```

### Dashboard de Estoque (Individual)

```bash
streamlit run app/Dashboard_Estoque_Streamlit.py
```

### Dashboard de Compras e Fornecedores (Individual)

```bash
streamlit run app/Dashboard_Compras_Streamlit.py
```

O navegador abrirá automaticamente em: **http://localhost:8501/**

---

## Arquitetura do Projeto

### Estrutura de Arquivos
```
app/
  ├── Super_Dashboard_Streamlit.py     # Super-Dashboard consolidado (NOVO)
  ├── Dashboard_Vendas_Streamlit.py    # Dashboard individual de Vendas
  ├── Dashboard_Estoque_Streamlit.py   # Dashboard individual de Estoque
  └── Dashboard_Compras_Streamlit.py   # Dashboard individual de Compras
```

### Fluxo de Integração
1. **Super-Dashboard** carrega dados de 3 fontes: Estoque, Vendas e Compras
2. **Consolidação** por produto: relaciona produtos entre datasets
3. **Indicadores Integrados**: calcula métricas que refletem visão 360°
4. **Decisões Estratégicas**: fornece insights baseados em dados consolidados

## Formato dos Dados

### Super-Dashboard (requer 3 fontes)
O dashboard carrega automaticamente os arquivos de cada fonte ou usa dados de exemplo:

#### Dados de Estoque
- `product_id` - ID do produto
- `product_name` - Nome do produto
- `category` - Categoria
- `supplier` - Fornecedor principal
- `quantity` - Quantidade em estoque
- `min_stock` - Estoque mínimo
- `unit_cost` - Custo unitário
- `last_update` - Data da última atualização

#### Dados de Vendas
- `date` - Data da venda
- `store` - Loja/filial
- `product_name` - Nome do produto
- `quantity` - Quantidade vendida
- `unit_price` - Preço unitário

#### Dados de Compras
- `date` - Data da compra
- `supplier` - Fornecedor
- `product_name` - Nome do produto
- `quantity` - Quantidade comprada
- `unit_price` - Preço unitário
- `delivery_days` - Prazo de entrega

### Dashboard de Vendas

O arquivo CSV/XLSX deve conter no mínimo as seguintes colunas:

- `date` - Data da venda
- `store` - Nome da loja
- `product_name` - Nome do produto
- `quantity` - Quantidade vendida
- `unit_price` - Preço unitário

### Dashboard de Estoque

O arquivo CSV/XLSX deve conter no mínimo as seguintes colunas:

- `product_id` - ID do produto
- `product_name` - Nome do produto
- `category` - Categoria do produto
- `supplier` - Fornecedor
- `quantity` - Quantidade em estoque
- `min_stock` - Estoque mínimo recomendado
- `unit_cost` - Custo unitário
- `last_update` - Data da última atualização

### Dashboard de Compras e Fornecedores

O arquivo CSV/XLSX deve conter no mínimo as seguintes colunas:

- `date` - Data da compra
- `supplier` - Nome do fornecedor
- `product_name` - Nome do produto
- `quantity` - Quantidade comprada
- `unit_price` - Preço unitário da compra
- `delivery_days` - Prazo de entrega em dias

---

## Documentação

Para mais detalhes sobre como executar e usar os dashboards, consulte o [Manual de Execução](docs/manual_execucao.md).


