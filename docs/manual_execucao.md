# Manual de Execução — Super-Dashboard e Dashboards Individuais

Este manual fornece instruções detalhadas para executar e utilizar o Super-Dashboard consolidado e os dashboards individuais de análise de vendas, controle de estoque e compras com fornecedores.

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Instalação](#2-instalação)
3. [Executando os Dashboards](#3-executando-os-dashboards)
4. [Super-Dashboard (Consolidado)](#4-super-dashboard-consolidado)
5. [Dashboard de Vendas](#5-dashboard-de-vendas)
6. [Dashboard de Estoque](#6-dashboard-de-estoque)
7. [Dashboard de Compras e Fornecedores](#7-dashboard-de-compras-e-fornecedores)

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

### ⭐ Super-Dashboard (Recomendado - Visão Consolidada 360°)

```bash
streamlit run app/Super_Dashboard_Streamlit.py
```

### Dashboard de Vendas (Análise Individual)

```bash
streamlit run app/Dashboard_Vendas_Streamlit.py
```

### Dashboard de Estoque (Análise Individual)

```bash
streamlit run app/Dashboard_Estoque_Streamlit.py
```

### Dashboard de Compras e Fornecedores (Análise Individual)

```bash
streamlit run app/Dashboard_Compras_Streamlit.py
```

### O que acontece?

1. O Streamlit iniciará o servidor local
2. Seu navegador padrão abrirá automaticamente
3. O dashboard estará disponível em: **http://localhost:8501/**

---

## 4. Super-Dashboard (Consolidado)

### 4.1 Objetivo

Fornecer **visão 360° integrada** de Estoque, Vendas e Compras, permitindo aos gestores:
- Analisar cada produto sob múltiplas perspectivas (inventário, demanda, reposição)
- Identificar riscos (ruptura, excesso) e oportunidades (custo, lucratividade)
- Tomar decisões estratégicas baseadas em dados consolidados
- Correlacionar informações (ex: produto em risco + histórico de compras)

### 4.2 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Dados sintéticos reproduzíveis de Estoque, Vendas e Compras
   - Ideal para entender a interface e funcionalidades

2. **Carregar seus próprios arquivos**
   - **Estoque** (CSV/XLSX): `product_id, product_name, category, supplier, quantity, min_stock, unit_cost, last_update`
   - **Vendas** (CSV/XLSX): `date, store, product_name, quantity, unit_price`
   - **Compras** (CSV/XLSX): `date, supplier, product_name, quantity, unit_price, delivery_days`

### 4.3 Aplicando Filtros

Na barra lateral, você pode filtrar por:

- **Produto(s)**: Selecione um ou mais produtos para análise
- **Categoria(s)**: Filtre por categoria de produtos
- **Loja(s)**: Escolha lojas específicas (para vendas)
- **Período**: Defina intervalo de datas (data início — data fim)

Todos os indicadores, gráficos e alertas atualizam automaticamente.

### 4.4 Visualizando Resultados

#### 📊 Indicadores Estratégicos (KPIs)
- **Receita Total**: Soma de todas as vendas no período
- **Valor Estoque**: Quantidade × Custo unitário para cada produto
- **Gasto em Compras**: Total investido em reposição
- **Produtos Críticos**: Quantidade abaixo do estoque mínimo
- **Excesso Estoque**: Produtos com estoque > 3× mínimo
- **Produtos**: Total de itens analisados

#### 👁️ Painel de Visão 360° do Produto
Selecione um produto para ver:

- **ESTOQUE**:
  - Quantidade atual vs Mínimo recomendado
  - Status (🔴 CRÍTICO ou 🟢 OK)

- **VENDAS**:
  - Quantidade vendida no período
  - Receita total gerada

- **COMPRAS**:
  - Quantidade comprada (reposição)
  - Gasto total em compras
  - Prazo médio de entrega

- **Alertas Personalizados**:
  - ⚠️ RISCO DE RUPTURA (abaixo do mínimo)
  - ⛔ EXCESSO DE ESTOQUE (muito acima do mínimo)
  - ✅ LUCRATIVO (margem positiva)

#### 📈 Análises Consolidadas (Abas)

**1️⃣ Produtos Críticos**
- Lista de todos os produtos abaixo do estoque mínimo
- Ordenados por quantidade (menor primeiro = mais crítico)
- Recomendação: Prioritize reposição destes itens
- Download: Exportar lista em CSV para compras

**2️⃣ Série Temporal**
- Gráfico: Receita (Vendas) vs Gasto (Compras) por mês
- Identifique períodos de maior/menor atividade
- Planeje compras baseado em sazonalidade
- Analise correlação entre venda e reposição

**3️⃣ Comparativo de Fornecedores**
- Scatter plot: Preço médio (eixo Y) vs Prazo médio (eixo X)
- Tamanho da bolha = Volume comprado
- Cor = Gasto total (vermelho=caro, verde=barato)
- **Busque fornecedores no canto inferior esquerdo** (barato + rápido)
- Tabela detalhada com ranking de fornecedores

**4️⃣ Heatmap Estoque-Vendas-Compras**
- Mapa de calor dos top 15 produtos
- Linhas: Métrica (Estoque atual | Vendido | Comprado)
- Colunas: Produtos (ordenados por receita)
- Cores: Intensidade de valor (mais claro = menos, mais escuro = mais)
- Identifique padrões (ex: produto vendido muito mas reposto pouco)

#### 💡 Recomendações Estratégicas
O dashboard exibe 3 recomendações automáticas:

1. **Ruptura Iminente**: Se houver produtos críticos, alerta para priorizar reposição
2. **Otimização de Custos**: Identifica fornecedor com melhor preço (sugestão: concentrar compras)
3. **Oportunidades de Venda**: Produto mais lucrativo (sugestão: promover ou manter estoque)

### 4.5 Decisões Apoiadas

Com base no Super-Dashboard, gestores podem:

a) **Identificar Riscos de Ruptura**: Veja produtos críticos com histórico de vendas alto
   → Decisão: Aumentar frequência/volume de compras para estes produtos

b) **Otimizar Reposição**: Compare vendas acumuladas com compras recebidas
   → Decisão: Ajustar quantidade/frequência de pedidos para reduzir excesso ou ruptura

c) **Avaliar Fornecedores**: Scatter plot mostra melhor custo-benefício (preço + prazo)
   → Decisão: Consolidar compras em fornecedor mais eficiente

d) **Planejar Promoções**: Identifique produtos lucrativos e com estoque em excesso
   → Decisão: Promover produtos para reduzir estoque e aumentar receita

e) **Reduzir Custos**: Compare margem de lucro por produto
   → Decisão: Renegociar preços com fornecedor de produtos com baixa margem

### 4.6 Exportando Dados

- **Produtos Críticos**: Botão "Baixar Lista de Críticos (CSV)" → Use para priorizar compras
- **Dados Completos**: Checkbox "Mostrar tabela completa" → Botão "Baixar Dados Consolidados (CSV)" → Para análises aprofundadas

---

## 5. Dashboard de Vendas

### 5.1 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Clique na checkbox "Usar dados de exemplo"
   - Dados serão gerados automaticamente

2. **Carregar seu próprio arquivo**
   - Clique em "Browse files" ou arraste um arquivo CSV/XLSX
   - O arquivo deve conter as colunas: `date`, `store`, `product_name`, `quantity`, `unit_price`

### 5.2 Aplicando Filtros

Na barra lateral, você pode:

- **Selecionar lojas**: Escolha uma ou mais lojas para análise
- **Selecionar produtos**: Filtre por produtos específicos (opcional)
- **Definir período**: Selecione o intervalo de datas desejado

### 5.3 Visualizando Resultados

O dashboard exibe:

- **KPIs principais**: Receita total, quantidade vendida, produtos diferentes
- **Gráfico de série temporal**: Vendas mensais ao longo do tempo
- **Top 10 produtos**: Produtos mais vendidos por quantidade
- **Receita por loja**: Detalhamento da receita por estabelecimento

### 5.4 Exportando Dados

Clique no botão **"Baixar dados filtrados (CSV)"** para exportar os dados filtrados.

---

## 6. Dashboard de Estoque

### 6.1 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Dados de estoque serão gerados automaticamente

2. **Carregar seu próprio arquivo**
   - Faça upload de um arquivo CSV/XLSX
   - O arquivo deve conter as colunas: `product_id`, `product_name`, `category`, `supplier`, `quantity`, `min_stock`, `unit_cost`, `last_update`

### 6.2 Aplicando Filtros

Na barra lateral, você pode:

- **Filtrar por categoria**: Selecione uma categoria específica ou "Todas"
- **Buscar produto**: Digite parte do nome do produto para busca rápida
- **Mostrar apenas alertas**: Marque para ver somente produtos abaixo do estoque mínimo

### 6.3 Visualizando Resultados

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

### 6.4 Exportando Dados

Clique no botão **"Baixar dados filtrados (CSV)"** para exportar os dados filtrados.

---

## 7. Dashboard de Compras e Fornecedores

### 7.1 Objetivo

Analisar desempenho de fornecedores, monitorar gastos e planejar compras estratégicas. Identifique fornecedores mais eficientes e otimize o volume de compras.

### 7.2 Carregando Dados

Você tem duas opções:

1. **Usar dados de exemplo** (marcado por padrão)
   - Dados de compras serão gerados automaticamente

2. **Carregar seu próprio arquivo**
   - Faça upload de um arquivo CSV/XLSX
   - O arquivo deve conter as colunas: `date`, `supplier`, `product_name`, `quantity`, `unit_price`, `delivery_days`

### 7.3 Aplicando Filtros

Na barra lateral, você pode:

- **Fornecedor(s)**: Selecione um ou mais fornecedores para análise
- **Produto(s)**: Filtre por produtos específicos (opcional)
- **Período**: Selecione o intervalo de datas desejado

### 7.4 Visualizando Resultados

O dashboard exibe:

- **KPIs principais**: 
  - Total gasto em compras
  - Quantidade total comprada
  - Fornecedores únicos
  - Número de transações

- **1️⃣ Comparativo entre Fornecedores**: 
  - Gráfico scatter com preço médio vs prazo médio
  - Tamanho das bolhas representa volume comprado
  - Tabela com detalhes de cada fornecedor
  - Identifique fornecedores mais eficientes em preço e prazo

- **2️⃣ Volume de Compras por Mês**: 
  - Gráfico de série temporal com gasto mensal
  - Identifique períodos de maior/menor gasto
  - Planeje compras futuras com base em tendências

- **3️⃣ Produtos com Maior Gasto**: 
  - Gráfico de barras com top 15 produtos
  - Tabela interativa com ranking de investimento
  - Identifique produtos estratégicos

- **💡 Recomendações Estratégicas**: 
  - Fornecedores com melhor preço
  - Fornecedores com melhor prazo de entrega
  - Oportunidades de redução de custos
  - Planejamento de compras com base em histórico

### 7.5 Decisões Apoiadas

Com base nos dados apresentados, gestores podem:

- **a) Escolher fornecedores mais eficientes**: Compare preço médio e prazo médio para identificar parceiros com melhor custo-benefício
- **b) Planejar compras estratégicas**: Use histórico de gastos mensais para reduzir custos e otimizar volume
- **c) Otimizar estoque**: Correlacione histórico de compras com níveis ideais de inventário

### 7.6 Exportando Dados

Clique no botão **"Baixar dados filtrados (CSV)"** para exportar os dados filtrados para análises adicionais.

---
