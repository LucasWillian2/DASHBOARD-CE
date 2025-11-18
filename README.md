# Dashboard de Análise de Vendas e Estoque — Streamlit

Este projeto consiste em **Dashboards interativos** desenvolvidos em **Python + Streamlit** para análise de vendas e controle de estoque, permitindo que gestores visualizem tendências, produtos estratégicos, comportamento de demanda e níveis de inventário.

---

## Autor

**Lucas Willian Santos**

---

##  Funcionalidades

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

### Dashboard de Vendas

```bash
streamlit run app/Dashboard_Vendas_Streamlit.py
```

### Dashboard de Estoque

```bash
streamlit run app/Dashboard_Estoque_Streamlit.py
```

O navegador abrirá automaticamente em: **http://localhost:8501/**

---

## Formato dos Dados

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

---

## Documentação

Para mais detalhes sobre como executar e usar os dashboards, consulte o [Manual de Execução](docs/manual_execucao.md).


