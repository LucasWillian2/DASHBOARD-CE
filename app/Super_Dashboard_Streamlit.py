"""
Super-Dashboard Consolidado — Visão 360° de Produtos

Este dashboard integra dados de Estoque, Vendas e Compras, permitindo aos gestores:
- Análise consolidada de cada produto
- Identificação de riscos (ruptura, excesso de estoque)
- Oportunidades de redução de custos
- Decisões estratégicas baseadas em dados

Funcionalidades principais:
1. Filtros interativos (produto, categoria, loja, período)
2. Painel de visão 360° do produto (estoque vs vendas vs compras)
3. Indicadores estratégicos (críticos, top vendidos, maior gasto)
4. Gráficos de suporte à decisão (série temporal, comparativo, heatmap)
5. Alertas visuais para riscos e oportunidades
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Super-Dashboard CE — Visão 360°",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 28px; }
    .stAlert { font-size: 14px; }
    .critical { background-color: #ffcccc; color: #cc0000; font-weight: bold; padding: 8px; border-radius: 4px; }
    .warning { background-color: #ffe6cc; color: #ff8c00; font-weight: bold; padding: 8px; border-radius: 4px; }
    .success { background-color: #ccffcc; color: #009900; font-weight: bold; padding: 8px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPERS — GERAÇÃO E CARREGAMENTO DE DADOS
# ============================================================================

@st.cache_data
def generate_sample_estoque(n_products=80, seed=42):
    """Gera dados de estoque sintéticos para teste"""
    np.random.seed(seed)
    categories = ["Eletrônicos", "Alimentos", "Higiene", "Ferramentas", "Têxtil"]
    suppliers = ["Fornecedor A", "Fornecedor B", "Fornecedor C", "Fornecedor D", "Fornecedor E"]
    
    products = [f"Produto_{i:03d}" for i in range(1, n_products + 1)]
    
    return pd.DataFrame({
        "product_id": range(1, n_products + 1),
        "product_name": products,
        "category": np.random.choice(categories, n_products),
        "supplier": np.random.choice(suppliers, n_products),
        "quantity": np.random.poisson(50, n_products),
        "min_stock": np.random.randint(10, 30, n_products),
        "unit_cost": np.random.uniform(10, 500, n_products),
        "last_update": pd.date_range("2024-01-01", periods=n_products, freq="D").repeat(1)[:n_products]
    })

@st.cache_data
def generate_sample_vendas(n_days=365, seed=42):
    """Gera dados de vendas sintéticos para teste"""
    np.random.seed(seed)
    n_products = 80
    n_stores = 5
    products = [f"Produto_{i:03d}" for i in range(1, n_products + 1)]
    stores = [f"Loja_{i}" for i in range(1, n_stores + 1)]
    
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    n_records = np.random.poisson(15, n_days).sum()
    
    return pd.DataFrame({
        "date": np.random.choice(dates, n_records),
        "store": np.random.choice(stores, n_records),
        "product_name": np.random.choice(products, n_records),
        "quantity": np.random.poisson(3, n_records) + 1,
        "unit_price": np.random.uniform(20, 400, n_records)
    })

@st.cache_data
def generate_sample_compras(n_days=365, seed=42):
    """Gera dados de compras sintéticos para teste"""
    np.random.seed(seed)
    n_products = 80
    products = [f"Produto_{i:03d}" for i in range(1, n_products + 1)]
    suppliers = ["Fornecedor A", "Fornecedor B", "Fornecedor C", "Fornecedor D", "Fornecedor E"]
    
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    n_records = np.random.poisson(8, n_days).sum()
    
    return pd.DataFrame({
        "date": np.random.choice(dates, n_records),
        "supplier": np.random.choice(suppliers, n_records),
        "product_name": np.random.choice(products, n_records),
        "quantity": np.random.poisson(5, n_records) + 1,
        "unit_price": np.random.uniform(15, 350, n_records),
        "delivery_days": np.random.randint(1, 30, n_records)
    })

@st.cache_data
def load_estoque_file(uploaded_file):
    """Carrega arquivo de estoque com validação de colunas"""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    required_cols = ['product_name', 'quantity', 'min_stock', 'unit_cost']
    for col in required_cols:
        if col not in df.columns:
            if col == 'quantity': df[col] = 0
            elif col == 'min_stock': df[col] = 10
            elif col == 'unit_cost': df[col] = 0.0
            elif col == 'product_name': df[col] = f"Produto_{range(len(df))}"
    
    return df[required_cols + [c for c in df.columns if c not in required_cols]]

@st.cache_data
def load_vendas_file(uploaded_file):
    """Carrega arquivo de vendas com validação de colunas"""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    required_cols = ['date', 'product_name', 'quantity', 'unit_price']
    for col in required_cols:
        if col not in df.columns:
            if col == 'date': df[col] = datetime.now()
            elif col == 'product_name': df[col] = f"Produto_{range(len(df))}"
            elif col == 'quantity': df[col] = 1
            elif col == 'unit_price': df[col] = 0.0
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

@st.cache_data
def load_compras_file(uploaded_file):
    """Carrega arquivo de compras com validação de colunas"""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    required_cols = ['date', 'product_name', 'quantity', 'unit_price', 'delivery_days']
    for col in required_cols:
        if col not in df.columns:
            if col == 'date': df[col] = datetime.now()
            elif col == 'product_name': df[col] = f"Produto_{range(len(df))}"
            elif col == 'quantity': df[col] = 1
            elif col == 'unit_price': df[col] = 0.0
            elif col == 'delivery_days': df[col] = 0
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

@st.cache_data
def to_csv_bytes(df):
    """Converte DataFrame para bytes CSV"""
    return df.to_csv(index=False).encode('utf-8')

# ============================================================================
# TÍTULO E DESCRIÇÃO
# ============================================================================

st.title("📊 Super-Dashboard CE — Visão 360° de Produtos")
st.markdown("""
**Consolidação de Estoque, Vendas e Compras** para decisões estratégicas em tempo real.
Identifique riscos, oportunidades e otimize a operação com indicadores integrados.
""")

# ============================================================================
# CARREGAMENTO DE DADOS
# ============================================================================

st.sidebar.markdown("## 📁 Dados")
use_sample = st.sidebar.checkbox("📌 Usar dados de exemplo", value=True)

if use_sample:
    df_estoque = generate_sample_estoque()
    df_vendas = generate_sample_vendas()
    df_compras = generate_sample_compras()
    st.sidebar.success("✅ Dados de exemplo carregados")
else:
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        file_estoque = st.file_uploader("Estoque (CSV/XLSX)", type=['csv', 'xlsx'], key='estoque')
        if file_estoque:
            df_estoque = load_estoque_file(file_estoque)
    
    with col2:
        file_vendas = st.file_uploader("Vendas (CSV/XLSX)", type=['csv', 'xlsx'], key='vendas')
        if file_vendas:
            df_vendas = load_vendas_file(file_vendas)
    
    with col3:
        file_compras = st.file_uploader("Compras (CSV/XLSX)", type=['csv', 'xlsx'], key='compras')
        if file_compras:
            df_compras = load_compras_file(file_compras)

# ============================================================================
# FILTROS INTERATIVOS
# ============================================================================

st.sidebar.markdown("## 🔍 Filtros")

# Obter lista de produtos e categorias únicas
produtos_unicos = sorted(df_estoque['product_name'].unique()) if 'product_name' in df_estoque.columns else []
categorias_unicas = sorted(df_estoque['category'].unique()) if 'category' in df_estoque.columns else []
lojas_unicas = sorted(df_vendas['store'].unique()) if 'store' in df_vendas.columns else []

# Filtro: Produto
produtos_selecionados = st.sidebar.multiselect(
    "🏷️ Produto(s)",
    options=produtos_unicos,
    default=produtos_unicos[:5] if len(produtos_unicos) > 5 else produtos_unicos
)

# Filtro: Categoria
categorias_selecionadas = st.sidebar.multiselect(
    "📦 Categoria(s)",
    options=categorias_unicas,
    default=categorias_unicas
)

# Filtro: Loja
lojas_selecionadas = st.sidebar.multiselect(
    "🏪 Loja(s)",
    options=lojas_unicas,
    default=lojas_unicas
)

# Filtro: Período
col1, col2 = st.sidebar.columns(2)
with col1:
    data_inicio = st.date_input("📅 De:", min_value=df_vendas['date'].min(), value=df_vendas['date'].min())
with col2:
    data_fim = st.date_input("📅 Até:", min_value=df_vendas['date'].min(), value=df_vendas['date'].max())

# ============================================================================
# PREPARAÇÃO DE DADOS COM FILTROS APLICADOS
# ============================================================================

# Filtrar estoque
df_estoque_filtered = df_estoque[
    (df_estoque['product_name'].isin(produtos_selecionados)) &
    (df_estoque['category'].isin(categorias_selecionadas))
].copy()

# Filtrar vendas
df_vendas['date'] = pd.to_datetime(df_vendas['date'])
df_vendas_filtered = df_vendas[
    (df_vendas['product_name'].isin(produtos_selecionados)) &
    (df_vendas['store'].isin(lojas_selecionadas)) &
    (df_vendas['date'].dt.date >= data_inicio) &
    (df_vendas['date'].dt.date <= data_fim)
].copy()

# Adicionar coluna de receita em vendas
df_vendas_filtered['revenue'] = df_vendas_filtered['quantity'] * df_vendas_filtered['unit_price']

# Filtrar compras
df_compras['date'] = pd.to_datetime(df_compras['date'])
df_compras_filtered = df_compras[
    (df_compras['product_name'].isin(produtos_selecionados)) &
    (df_compras['date'].dt.date >= data_inicio) &
    (df_compras['date'].dt.date <= data_fim)
].copy()

# Adicionar coluna de custo em compras
df_compras_filtered['total_cost'] = df_compras_filtered['quantity'] * df_compras_filtered['unit_price']

# ============================================================================
# CONSOLIDAÇÃO: MERGE DOS DADOS POR PRODUTO
# ============================================================================

# Resumo de vendas por produto
vendas_resumo = df_vendas_filtered.groupby('product_name').agg({
    'quantity': 'sum',
    'revenue': 'sum'
}).reset_index().rename(columns={'quantity': 'qty_vendida', 'revenue': 'receita_total'})

# Resumo de compras por produto
compras_resumo = df_compras_filtered.groupby('product_name').agg({
    'quantity': 'sum',
    'total_cost': 'sum',
    'delivery_days': 'mean'
}).reset_index().rename(columns={'quantity': 'qty_comprada', 'total_cost': 'gasto_compras', 'delivery_days': 'prazo_medio'})

# Consolidação: Estoque + Vendas + Compras
df_consolidado = df_estoque_filtered[['product_name', 'category', 'supplier', 'quantity', 'min_stock', 'unit_cost']].copy()
df_consolidado = df_consolidado.merge(vendas_resumo, on='product_name', how='left').fillna(0)
df_consolidado = df_consolidado.merge(compras_resumo, on='product_name', how='left').fillna(0)

# Adicionar coluna de valor do estoque
df_consolidado['valor_estoque'] = df_consolidado['quantity'] * df_consolidado['unit_cost']

# Flags de risco e oportunidade
df_consolidado['risco_ruptura'] = df_consolidado['quantity'] < df_consolidado['min_stock']
df_consolidado['excesso_estoque'] = df_consolidado['quantity'] > (df_consolidado['min_stock'] * 3)
df_consolidado['lucratividade'] = (df_consolidado['receita_total'] - (df_consolidado['qty_vendida'] * df_consolidado['unit_cost'])).fillna(0)

# ============================================================================
# INDICADORES ESTRATÉGICOS (KPIs)
# ============================================================================

st.markdown("## 🎯 Indicadores Estratégicos")

kpi_cols = st.columns(6)

with kpi_cols[0]:
    receita_total = df_vendas_filtered['revenue'].sum()
    st.metric(
        label="💰 Receita Total",
        value=f"R$ {receita_total:,.2f}"
    )

with kpi_cols[1]:
    valor_estoque_total = df_consolidado['valor_estoque'].sum()
    st.metric(
        label="📦 Valor Estoque",
        value=f"R$ {valor_estoque_total:,.2f}"
    )

with kpi_cols[2]:
    gasto_compras = df_compras_filtered['total_cost'].sum()
    st.metric(
        label="💳 Gasto em Compras",
        value=f"R$ {gasto_compras:,.2f}"
    )

with kpi_cols[3]:
    qtd_critica = (df_consolidado['risco_ruptura']).sum()
    st.metric(
        label="⚠️ Produtos Críticos",
        value=int(qtd_critica)
    )

with kpi_cols[4]:
    qtd_excesso = (df_consolidado['excesso_estoque']).sum()
    st.metric(
        label="⛔ Excesso Estoque",
        value=int(qtd_excesso)
    )

with kpi_cols[5]:
    produtos_analisados = len(df_consolidado)
    st.metric(
        label="📊 Produtos",
        value=int(produtos_analisados)
    )

# ============================================================================
# PAINEL DE VISÃO 360° DO PRODUTO
# ============================================================================

st.markdown("## 👁️ Visão 360° do Produto")

if len(df_consolidado) > 0:
    produto_selecionado = st.selectbox(
        "Selecione um produto para análise detalhada:",
        options=df_consolidado['product_name'].unique()
    )
    
    produto_data = df_consolidado[df_consolidado['product_name'] == produto_selecionado].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 ESTOQUE")
        qtd_atual = produto_data['quantity']
        min_stock = produto_data['min_stock']
        em_risco = "🔴 CRÍTICO" if qtd_atual < min_stock else "🟢 OK"
        st.metric("Quantidade Atual", int(qtd_atual))
        st.metric("Mínimo Recomendado", int(min_stock))
        st.markdown(f"Status: {em_risco}")
    
    with col2:
        st.markdown("### 💹 VENDAS")
        qty_vendida = produto_data['qty_vendida']
        receita = produto_data['receita_total']
        st.metric("Quantidade Vendida", int(qty_vendida))
        st.metric("Receita", f"R$ {receita:,.2f}")
    
    with col3:
        st.markdown("### 🛒 COMPRAS")
        qty_comprada = produto_data['qty_comprada']
        gasto = produto_data['gasto_compras']
        prazo = produto_data['prazo_medio']
        st.metric("Quantidade Comprada", int(qty_comprada))
        st.metric("Gasto Total", f"R$ {gasto:,.2f}")
        st.metric("Prazo Médio (dias)", f"{prazo:.1f}")
    
    # Alertas personalizados
    st.markdown("### 🚨 Alertas e Oportunidades")
    
    if produto_data['risco_ruptura']:
        st.markdown("""
        <div class="critical">
        ⚠️ RISCO DE RUPTURA: Quantidade abaixo do mínimo!
        Recomendação: Aumentar pedido de compra imediatamente.
        </div>
        """, unsafe_allow_html=True)
    
    if produto_data['excesso_estoque']:
        st.markdown("""
        <div class="warning">
        ⛔ EXCESSO DE ESTOQUE: Quantidade muito acima do mínimo.
        Recomendação: Considerar promoções ou reduzir pedidos.
        </div>
        """, unsafe_allow_html=True)
    
    if produto_data['lucratividade'] > 0:
        st.markdown(f"""
        <div class="success">
        ✅ LUCRATIVO: Margem de lucro de R$ {produto_data['lucratividade']:,.2f}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("⚠️ Nenhum produto disponível com os filtros selecionados.")

# ============================================================================
# ANÁLISES CONSOLIDADAS
# ============================================================================

st.markdown("## 📈 Análises Consolidadas")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔴 Produtos Críticos",
    "📊 Série Temporal",
    "🤝 Comparativo Fornecedores",
    "🔥 Heatmap Estoque-Vendas-Compras"
])

with tab1:
    st.subheader("Produtos em Risco de Ruptura")
    criticos = df_consolidado[df_consolidado['risco_ruptura']][
        ['product_name', 'category', 'quantity', 'min_stock', 'qty_vendida', 'receita_total']
    ].sort_values('quantity')
    
    if len(criticos) > 0:
        st.dataframe(criticos, use_container_width=True)
        csv = to_csv_bytes(criticos)
        st.download_button(
            label="📥 Baixar Lista de Críticos (CSV)",
            data=csv,
            file_name="produtos_criticos.csv",
            mime="text/csv"
        )
    else:
        st.success("✅ Nenhum produto crítico detectado!")

with tab2:
    st.subheader("Série Temporal: Vendas vs Compras")
    
    # Agregação mensal
    vendas_mensal = df_vendas_filtered.copy()
    vendas_mensal['mes'] = pd.to_datetime(vendas_mensal['date']).dt.to_period('M').dt.to_timestamp()
    vendas_mensal = vendas_mensal.groupby('mes')['revenue'].sum().reset_index()
    
    compras_mensal = df_compras_filtered.copy()
    compras_mensal['mes'] = pd.to_datetime(compras_mensal['date']).dt.to_period('M').dt.to_timestamp()
    compras_mensal = compras_mensal.groupby('mes')['total_cost'].sum().reset_index()
    
    # Merge
    serie_temporal = vendas_mensal.merge(compras_mensal, on='mes', how='outer').fillna(0)
    
    if len(serie_temporal) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=serie_temporal['mes'], y=serie_temporal['revenue'],
            mode='lines+markers', name='Receita (Vendas)',
            line=dict(color='green', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=serie_temporal['mes'], y=serie_temporal['total_cost'],
            mode='lines+markers', name='Gasto (Compras)',
            line=dict(color='red', width=3)
        ))
        fig.update_layout(
            title="Receita vs Gasto por Mês",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Dados insuficientes para série temporal.")

with tab3:
    st.subheader("Comparativo de Fornecedores")
    
    fornecedores = df_compras_filtered.groupby('supplier').agg({
        'unit_price': 'mean',
        'delivery_days': 'mean',
        'quantity': 'sum',
        'total_cost': 'sum'
    }).reset_index().rename(columns={
        'unit_price': 'preco_medio',
        'delivery_days': 'prazo_medio',
        'quantity': 'qtd_total',
        'total_cost': 'gasto_total'
    })
    
    if len(fornecedores) > 0:
        fig = px.scatter(
            fornecedores,
            x='prazo_medio',
            y='preco_medio',
            size='qtd_total',
            color='gasto_total',
            hover_data=['supplier'],
            title='Comparativo: Preço Médio vs Prazo Médio',
            labels={'prazo_medio': 'Prazo Médio (dias)', 'preco_medio': 'Preço Médio'},
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(fornecedores, use_container_width=True)
    else:
        st.info("ℹ️ Dados de compras insuficientes.")

with tab4:
    st.subheader("Heatmap: Estoque vs Vendas vs Compras")
    
    top_produtos = df_consolidado.nlargest(15, 'receita_total')[
        ['product_name', 'quantity', 'qty_vendida', 'qty_comprada']
    ].set_index('product_name')
    
    if len(top_produtos) > 0:
        fig = px.imshow(
            top_produtos.T,
            labels=dict(x='Produto', y='Métrica', color='Quantidade'),
            title='Heatmap: Top 15 Produtos (Estoque vs Vendas vs Compras)',
            color_continuous_scale='Viridis',
            aspect='auto'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Dados insuficientes para heatmap.")

# ============================================================================
# RECOMENDAÇÕES ESTRATÉGICAS
# ============================================================================

st.markdown("## 💡 Recomendações Estratégicas para Gestores")

rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.markdown("### 🔴 Ruptura Iminente")
    criticos_count = (df_consolidado['risco_ruptura']).sum()
    if criticos_count > 0:
        st.warning(f"⚠️ {int(criticos_count)} produto(s) abaixo do mínimo. Prioritize reposição!")
    else:
        st.success("✅ Nenhum produto crítico.")

with rec_col2:
    st.markdown("### 💰 Otimização de Custos")
    fornecedor_melhor_preco = df_compras_filtered.groupby('supplier')['unit_price'].mean().idxmin()
    if pd.notna(fornecedor_melhor_preco):
        st.info(f"💡 Fornecedor com melhor preço: **{fornecedor_melhor_preco}**")
    else:
        st.info("💡 Analise histórico de compras para otimizar custos.")

with rec_col3:
    st.markdown("### 📈 Oportunidades de Venda")
    top_vendido = df_consolidado.nlargest(1, 'receita_total')['product_name'].values
    if len(top_vendido) > 0:
        st.success(f"🏆 Produto mais lucrativo: **{top_vendido[0]}**")
    else:
        st.info("💡 Identifique produtos com maior potencial.")

# ============================================================================
# TABELA CONSOLIDADA E EXPORTAÇÃO
# ============================================================================

st.markdown("## 📋 Dados Consolidados Completos")

if st.checkbox("Mostrar tabela completa"):
    st.dataframe(
        df_consolidado[[
            'product_name', 'category', 'supplier',
            'quantity', 'min_stock', 'qty_vendida', 'receita_total',
            'qty_comprada', 'gasto_compras', 'prazo_medio'
        ]],
        use_container_width=True
    )
    
    csv = to_csv_bytes(df_consolidado)
    st.download_button(
        label="📥 Baixar Dados Consolidados (CSV)",
        data=csv,
        file_name="super_dashboard_consolidado.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("""
**Desenvolvido com Streamlit, Pandas e Plotly**  
*Dashboard Educacional — Período 7 — Análise de Dados*
""")
