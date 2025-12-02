# Instruções para Agentes AI — Dashboard CE

## 1. Objetivo do Projeto

Desenvolver **Dashboards interativos** para gestores analisarem negócios em tempo real. O projeto oferece:

- **Super-Dashboard (Consolidado)**: Visão 360° integrada de Estoque, Vendas e Compras por produto
  - Identificação de riscos (ruptura, excesso de estoque)
  - Oportunidades de otimização (custo, lucratividade)
  - Decisões estratégicas baseadas em dados consolidados

- **Dashboards Individuais**: Análise isolada de cada fonte
  - **Vendas**: Receita, produtos mais vendidos, série temporal de vendas
  - **Estoque**: Monitoramento de inventário, alertas de baixo estoque, recomendações de reposição
  - **Compras**: Comparativo de fornecedores, volume de compras mensal, produtos com maior gasto

---

## 2. Visão Geral da Arquitetura

Este projeto contém **um Super-Dashboard consolidado + 3 dashboards Streamlit individuais** para análise de negócios:

- **Super-Dashboard (app/Super_Dashboard_Streamlit.py)**: Integração 360° de Estoque, Vendas e Compras
  - Consolidação por produto
  - Indicadores estratégicos integrados
  - Visão unificada para decisões cross-funcionais

- **Dashboard de Vendas** (app/Dashboard_Vendas_Streamlit.py): Análise isolada de receita, produtos mais vendidos, série temporal
- **Dashboard de Estoque** (app/Dashboard_Estoque_Streamlit.py): Monitoramento de inventário, alertas, recomendações
- **Dashboard de Compras** (app/Dashboard_Compras_Streamlit.py): Comparativo de fornecedores, volume mensal, top produtos

Todos seguem o mesmo padrão arquitetural: **helpers de carga/processamento de dados + UI Streamlit com filtros dinâmicos + visualizações Plotly**.

---

## Arquitetura & Padrões

### Estrutura de Arquivos
```
app/
  ├── Super_Dashboard_Streamlit.py       # Super-Dashboard consolidado (visão 360°)
  ├── Dashboard_Vendas_Streamlit.py       # Vendas com KPIs, série temporal, top 10
  ├── Dashboard_Estoque_Streamlit.py      # Estoque com alertas, valor total, recomendações
  └── Dashboard_Compras_Streamlit.py      # Compras com fornecedores, volume mensal, top produtos
docs/
  └── manual_execucao.md                  # Instruções para usuários finais
```

### Padrão Comum (Ambos Dashboards)

1. **Helpers com `@st.cache_data`**
   - `generate_sample_*()`: Dados sintéticos reproduzíveis (seed=42)
   - `load_*_file()`: Suporta CSV e XLSX com fallback para openpyxl
   - Garantem colunas mínimas esperadas (defaults sensatos)

2. **Preparo de Dados**
   - Conversão de tipos (`pd.to_numeric`, `pd.to_datetime`)
   - Cálculos derivados (`revenue = quantity * unit_price`, `value = quantity * unit_cost`)
   - Flags booleanas (`below_min = quantity < min_stock`)

3. **Filtros no Sidebar**
   - Upload de arquivo OU dados de exemplo (checkbox)
   - Multiselect para lojas/produtos/categorias
   - Date range picker ou selectbox de categoria
   - Aplicados via `.isin()` ou `.str.contains()`

4. **Indicadores & Visualizações**
   - KPIs em `st.columns()` com `st.metric()`
   - Gráficos Plotly (px.line, px.bar) com `use_container_width=True`
   - Download CSV via `st.download_button()` com `@st.cache_data`

---

## Convenções Projeto-Específicas

### Super-Dashboard — Padrão de Consolidação

O Super-Dashboard integra 3 fontes de dados através de consolidação por `product_name`:

1. **Carregamento Independente**:
   - `generate_sample_estoque()`: Cria 80 produtos com quantidade, min_stock, unit_cost
   - `generate_sample_vendas()`: Cria eventos de venda com quantity, unit_price
   - `generate_sample_compras()`: Cria eventos de compra com quantity, unit_price, delivery_days

2. **Merge Consolidado**:
   ```python
   # Estoque base
   df_consolidado = df_estoque[['product_name', 'category', 'supplier', 'quantity', 'min_stock', 'unit_cost']]
   
   # Merge com resumo de vendas (groupby product_name)
   df_consolidado = df_consolidado.merge(vendas_resumo, on='product_name', how='left').fillna(0)
   
   # Merge com resumo de compras (groupby product_name)
   df_consolidado = df_consolidado.merge(compras_resumo, on='product_name', how='left').fillna(0)
   ```

3. **Colunas Derivadas**:
   - `valor_estoque = quantity * unit_cost`
   - `receita_vendas = qty_vendida * unit_price` (agregado de vendas)
   - `gasto_compras = qty_comprada * unit_price` (agregado de compras)
   - `risco_ruptura = quantity < min_stock` (flag booleana)
   - `excesso_estoque = quantity > (min_stock * 3)` (flag booleana)
   - `lucratividade = receita_total - (qty_vendida * unit_cost)` (margem)

4. **Filtros Multidimensionais**:
   - Produtos selecionados → filtro em estoque, vendas, compras
   - Categorias → filtro em estoque
   - Lojas → filtro em vendas
   - Período → date range em vendas e compras

### Formato de Dados Esperados

**Dashboard de Vendas** (`date`, `store`, `product_name`, `quantity`, `unit_price`):
```python
# O código autocompleta colunas faltantes com defaults
# - store → "Store_1"
# - quantity → 1
# - unit_price → 0.0
```

**Dashboard de Compras** (`date`, `supplier`, `product_name`, `quantity`, `unit_price`, `delivery_days`):
```python
# Completamento automático de colunas faltantes
# - supplier → "Desconhecido"
# - quantity → 1
# - unit_price → 0.0
# - delivery_days → 0
```

### Métodos de Geração de Dados (Desenvolvimento)

- **Vendas**: `np.random.poisson(8)` eventos/dia, distribuição de produtos não-uniforme (Linspace)
- **Estoque**: `np.random.poisson(40)` unidades médias, categorias com `np.random.dirichlet`
- Sempre usar `seed=42` para reprodutibilidade

### Styling & UX

- Linhas críticas: `background-color: #ffdcdc` (vermelho suave) para produtos abaixo do mínimo
- Indicadores: Ícones Unicode (`💰`, `📦`, `⚠️`, `🏷️`) antes do label
- Expanders para tabelas detalhadas (padrão: `expanded=False`)
- Info boxes (`st.info()`) quando nenhum dado está disponível

---

## Fluxos de Trabalho Principais

### Executar Dashboards Localmente
```powershell
# Windows PowerShell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Super-Dashboard (Recomendado - visão consolidada 360°)
streamlit run app/Super_Dashboard_Streamlit.py

# Vendas (individual)
streamlit run app/Dashboard_Vendas_Streamlit.py

# Estoque (individual)
streamlit run app/Dashboard_Estoque_Streamlit.py

# Compras e Fornecedores (individual)
streamlit run app/Dashboard_Compras_Streamlit.py
```

### Estrutura Típica de Modificação

1. **Adicionar métrica KPI**: Criar cálculo em preparo, exibir em `st.columns()` com `st.metric()`
2. **Novo filtro**: Adicionar `st.multiselect()` ou `st.selectbox()` no sidebar, aplicar filtro via `.isin()` ou `.str.contains()`
3. **Novo gráfico**: Usar `px.*()` (line, bar, scatter), atualizar layout, renderizar com `st.plotly_chart(..., use_container_width=True)`
4. **Exportação**: Usar `@st.cache_data def to_csv_bytes(df)` + `st.download_button()`

---

## Integrações & Dependências Críticas

| Biblioteca | Uso | Versão Mínima |
|---|---|---|
| `streamlit` | Framework UI interativo | 1.28.0 |
| `pandas` | Manipulação de dados, groupby, merge | 2.0.0 |
| `plotly.express` | Gráficos interativos | 5.17.0 |
| `numpy` | Arrays, random, operações numéricas | 1.24.0 |
| `openpyxl` | Fallback para leitura XLSX | 3.1.0 |

**Sem ORM, banco de dados ou APIs externas** — dados são sempre arquivo+memória.

---

## Decisões Arquiteturais & Limitações

- **Por que dados em memória?**: Escopo educacional; integrações de banco estão documentadas como "extensão futura"
- **Caching com `@st.cache_data`**: Evita recálculos, respeitando imutabilidade de entrada
- **Fallback CSV → XLSX**: Permite usuários escolherem formato sem recoding
- **Geração sintética com seed**: Permite demo reprodutível sem arquivo de entrada
- **Top 40 mais críticos no gráfico**: Limite visual para evitar sobrecarga (gráfico de 400 barras fica ilegível)

---

## Dashboard de Compras e Fornecedores (Implementado)

### Requisitos Funcionais (Implementados)

O novo dashboard deve incluir:

1. **Comparativo entre Fornecedores**
   - Preço médio de compra por fornecedor
   - Prazo médio de entrega por fornecedor
   - Gráfico comparativo para identificar fornecedores mais eficientes

2. **Volume de Compras por Mês**
   - Série temporal com volume/valor de compras mensais
   - Identificar períodos de maior/menor gasto
   - Apoiar planejamento de compras futuras

3. **Produtos com Maior Gasto**
   - Top N produtos por investimento acumulado
   - Gráfico de barras ou tabela interativa
   - Destacar produtos estratégicos/alto impacto financeiro

### Formato de Dados Esperados (Dashboard Compras)

```python
# Colunas esperadas: date, supplier, product_name, quantity, unit_price, delivery_days
# Auto-completa com defaults:
# - unit_price → 0.0
# - delivery_days → 0
# - supplier → "Desconhecido"
```

---

## Decisões para Gestores (Insights Esperados)

Cada dashboard deve capacitar tomadas de decisão:

### Dashboard de Vendas
- Identificar produtos com maior receita
- Analisar tendências mensais para planejamento
- Comparar desempenho por loja

### Dashboard de Estoque
- Reposição prioritária de produtos críticos (abaixo do mínimo)
- Otimizar valor total investido em inventário
- Monitorar atualização de dados por fornecedor

### Dashboard de Compras (Futuro)
- **Escolher fornecedores mais eficientes**: Comparar preço médio e prazo médio
- **Planejar compras estratégicas**: Usar volume histórico para reduzir custos
- **Otimizar estoque**: Correlacionar histórico de compras com níveis ideais

---

## Pontos de Entrada para Novas Features

1. **Filtros adicionais**: Sidebar → multiselect/selectbox → máscara em df_filtered
2. **KPIs customizados**: Adicionar cálculo no preparo, renderizar em st.columns()
3. **Alertas de gestores**: Criar tabela filtrada (ex: estoque crítico, faturamento baixo)
4. **Exportação em formato novo**: Adaptar função `to_*_bytes()` (ex: Excel, JSON)
5. **Tema/Paleta de cores**: Usar `st.set_page_config(theme="...") ` ou Plotly `color_discrete_map`
6. **Novo Dashboard de Compras**: Seguir padrão existente — helpers com `@st.cache_data`, filtros sidebar, visualizações Plotly

---

## Verificação Rápida (Debug)

- Dados faltam? Verificar se arquivo tem colunas esperadas (ver helpers `load_*_file()`)
- Gráfico em branco? Confirmar `if not df_filtered.empty:` antes de plotar
- Tipo incorreto? Usar `pd.to_numeric(..., errors="coerce")` com fallback `.fillna()`
- Cache obsoleto? Usuários podem forçar refresh: `Ctrl+Shift+R` no Streamlit
