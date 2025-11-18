# Manual de Execução — Dashboards de Vendas e Estoque

Este manual fornece instruções detalhadas para executar e utilizar os dashboards de análise de vendas e controle de estoque.

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Instalação](#2-instalação)
3. [Executando os Dashboards](#3-executando-os-dashboards)
4. [Dashboard de Vendas](#4-dashboard-de-vendas)
5. [Dashboard de Estoque](#5-dashboard-de-estoque)

---

## 1. Pré-requisitos

Antes de começar, certifique-se de ter:

- **Python 3.9 ou superior** instalado
- **Pip** atualizado

### Verificando a instalação do Python

```bash
python --version
# ou
python3 --version
```

---

## 2. Instalação

### Passo 1: Criar ambiente virtual (recomendado)

Criar um ambiente virtual isola as dependências do projeto:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 2: Instalar dependências

```bash
pip install streamlit pandas plotly numpy openpyxl
```

Ou, se você criou um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Passo 3: Verificar instalação

```bash
streamlit --version
```

---

## 3. Executando os Dashboards

### Dashboard de Vendas

```bash
streamlit run app/Dashboard_Vendas_Streamlit.py
```

### Dashboard de Estoque

```bash
streamlit run app/Dashboard_Estoque_Streamlit.py
```

### O que acontece?

1. O Streamlit iniciará o servidor local
2. Seu navegador padrão abrirá automaticamente
3. O dashboard estará disponível em: **http://localhost:8501/**

---

## 4. Dashboard de Vendas

### 4.1 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Clique na checkbox "Usar dados de exemplo"
   - Dados serão gerados automaticamente

2. **Carregar seu próprio arquivo**
   - Clique em "Browse files" ou arraste um arquivo CSV/XLSX
   - O arquivo deve conter as colunas: `date`, `store`, `product_name`, `quantity`, `unit_price`

### 4.2 Aplicando Filtros

Na barra lateral, você pode:

- **Selecionar lojas**: Escolha uma ou mais lojas para análise
- **Selecionar produtos**: Filtre por produtos específicos (opcional)
- **Definir período**: Selecione o intervalo de datas desejado

### 4.3 Visualizando Resultados

O dashboard exibe:

- **KPIs principais**: Receita total, quantidade vendida, produtos diferentes
- **Gráfico de série temporal**: Vendas mensais ao longo do tempo
- **Top 10 produtos**: Produtos mais vendidos por quantidade
- **Receita por loja**: Detalhamento da receita por estabelecimento

### 4.4 Exportando Dados

Clique no botão **"Baixar dados filtrados (CSV)"** para exportar os dados filtrados.

---

## 5. Dashboard de Estoque

### 5.1 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Dados de estoque serão gerados automaticamente

2. **Carregar seu próprio arquivo**
   - Faça upload de um arquivo CSV/XLSX
   - O arquivo deve conter as colunas: `product_id`, `product_name`, `category`, `supplier`, `quantity`, `min_stock`, `unit_cost`, `last_update`

### 5.2 Aplicando Filtros

Na barra lateral, você pode:

- **Filtrar por categoria**: Selecione uma categoria específica ou "Todas"
- **Buscar produto**: Digite parte do nome do produto para busca rápida
- **Mostrar apenas alertas**: Marque para ver somente produtos abaixo do estoque mínimo

### 5.3 Visualizando Resultados

O dashboard exibe:

- **KPIs principais**: 
  - Total de unidades em estoque
  - SKUs cadastrados
  - Produtos abaixo do mínimo (alertas)
  - Valor total do estoque

- **Tabela interativa**: 
  - Lista completa de produtos
  - Linhas em vermelho destacam produtos críticos
  - Informações detalhadas de cada item

- **Gráfico comparativo**: 
  - Estoque atual vs Estoque mínimo
  - Produtos mais críticos destacados em vermelho

- **Recomendações**: 
  - Lista de produtos com prioridade de reposição

### 5.4 Exportando Dados

Clique no botão **"Baixar dados filtrados (CSV)"** para exportar os dados filtrados.

---
