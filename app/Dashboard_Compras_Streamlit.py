"""
Dashboard de Compras e Fornecedores
Arquivo: Dashboard_Compras_Streamlit.py

Funcionalidades:
- Upload CSV/XLSX com dados de compras (ou gera dados de exemplo)
- Filtro por fornecedor, período e produto
- Comparativo entre fornecedores: preço médio e prazo médio de entrega
- Gráfico de série temporal: volume de compras por mês
- Produtos com maior gasto: ranking de investimento acumulado
- Indicadores: total gasto, quantidade de fornecedores, número de transações
- Download dos dados filtrados em CSV
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard de Compras e Fornecedores", layout="wide")

# ================ HELPERS ================

@st.cache_data
def generate_sample_purchases(n_days=365, n_suppliers=8, n_products=50, seed=42):
    """Gera dados sintéticos de compras para demonstração"""
    np.random.seed(seed)
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=n_days)
    dates = pd.date_range(start, periods=n_days)

    suppliers = [f'Fornecedor_{i+1}' for i in range(n_suppliers)]
    products = [f'Produto_{i+1}' for i in range(n_products)]

    rows = []
    for d in dates:
        # Número de compras por dia
        m = np.random.poisson(6)
        for _ in range(m):
            supplier = np.random.choice(suppliers)
            product = np.random.choice(products, p=np.linspace(1, 0.1, n_products)/np.linspace(1, 0.1, n_products).sum())
            quantity = np.random.randint(5, 50)
            unit_price = float(np.round(np.random.uniform(10, 500), 2))
            delivery_days = int(np.random.exponential(scale=7)) + 1  # 1 a N dias
            rows.append((d.date().isoformat(), supplier, product, quantity, unit_price, delivery_days))

    df = pd.DataFrame(rows, columns=['date', 'supplier', 'product_name', 'quantity', 'unit_price', 'delivery_days'])
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def load_purchases_file(uploaded_file):
    """Carrega arquivo CSV/XLSX com dados de compras"""
    try:
        df = pd.read_csv(uploaded_file, parse_dates=['date'])
    except Exception:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Garante que as colunas mínimas estão presentes
    expected_columns = ['date', 'supplier', 'product_name', 'quantity', 'unit_price', 'delivery_days']
    for col in expected_columns:
        if col not in df.columns:
            if col == "supplier":
                df[col] = "Desconhecido"
            elif col == "product_name":
                df[col] = ""
            elif col in ("quantity",):
                df[col] = 1
            elif col in ("unit_price",):
                df[col] = 0.0
            elif col == "delivery_days":
                df[col] = 0
            else:
                df[col] = ""
    
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def to_csv_bytes(df):
    """Converte dataframe para bytes CSV para download"""
    return df.to_csv(index=False).encode('utf-8')

def compute_total_spending(df):
    """Calcula gasto total (quantidade * preço unitário)"""
    return (df["quantity"] * df["unit_price"]).sum()

# ================ UI ================

st.title("🛒 Dashboard de Compras e Fornecedores")
st.subheader("Analise desempenho de fornecedores, monitore gastos e planeje compras estratégicas")

with st.sidebar:
    st.header("Dados e Filtros")
    uploaded = st.file_uploader("Carregar arquivo CSV/XLSX (compras)", type=["csv", "xlsx"])
    use_sample = st.checkbox("Usar dados de exemplo (se nenhum arquivo for enviado)", value=True)

    st.markdown("---")
    st.markdown("**Opções de visualização:**")
    
    st.markdown("---")
    st.caption("Formato esperado das colunas: date, supplier, product_name, quantity, unit_price, delivery_days")

# Carregar dados
if uploaded is not None:
    df_purchases = load_purchases_file(uploaded)
elif use_sample:
    df_purchases = generate_sample_purchases(n_days=730, n_suppliers=10, n_products=80)
else:
    st.warning("Envie um arquivo CSV/XLSX ou marque 'Usar dados de exemplo'.")
    st.stop()

# Preparar colunas derivadas
df_purchases["total_cost"] = df_purchases["quantity"] * df_purchases["unit_price"]
df_purchases["date"] = pd.to_datetime(df_purchases["date"])

# Conversão de tipos
df_purchases["quantity"] = pd.to_numeric(df_purchases["quantity"], errors="coerce").fillna(0).astype(int)
df_purchases["unit_price"] = pd.to_numeric(df_purchases["unit_price"], errors="coerce").fillna(0.0)
df_purchases["delivery_days"] = pd.to_numeric(df_purchases["delivery_days"], errors="coerce").fillna(0).astype(int)

# Filtros dinâmicos
suppliers = sorted(df_purchases["supplier"].unique().tolist())
products = sorted(df_purchases["product_name"].unique().tolist())

col1, col2 = st.columns(2)

with col1:
    selected_suppliers = st.multiselect(
        "Fornecedor(s)",
        options=suppliers,
        default=suppliers
    )

with col2:
    selected_products = st.multiselect(
        "Produto(s)",
        options=products,
        default=None
    )

# Date range filter
min_date = df_purchases["date"].min().date()
max_date = df_purchases["date"].max().date()
date_range = st.date_input(
    "Período (início - fim)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Aplicar filtros
start_date, end_date = date_range
mask = (df_purchases["date"].dt.date >= start_date) & (df_purchases["date"].dt.date <= end_date)
mask &= df_purchases["supplier"].isin(selected_suppliers)
if selected_products and len(selected_products) > 0:
    mask &= df_purchases["product_name"].isin(selected_products)

df_filtered = df_purchases.loc[mask].copy()

# ================ INDICADORES ================

col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])

total_spending = compute_total_spending(df_filtered)
total_quantity = df_filtered["quantity"].sum()
num_suppliers = df_filtered["supplier"].nunique()
num_transactions = len(df_filtered)

col1.metric("💰 Total Gasto (R$)", f"R$ {total_spending:,.2f}")
col2.metric("📦 Quantidade Total Comprada", f"{int(total_quantity):,}")
col3.metric("🏢 Fornecedores Únicos", f"{num_suppliers}")
col4.metric("📊 Número de Transações", f"{num_transactions:,}")

st.markdown("---")

# ================ COMPARATIVO ENTRE FORNECEDORES ================

st.subheader("1️⃣ Comparativo entre Fornecedores — Preço Médio e Prazo Médio")
st.markdown("Identifique fornecedores mais eficientes em termos de custo e prazo de entrega.")

if df_filtered.empty:
    st.info("Nenhum dado disponível para os filtros selecionados.")
else:
    # Calcular médias por fornecedor
    supplier_comparison = (df_filtered.groupby("supplier")
                          .agg({
                              "unit_price": "mean",
                              "delivery_days": "mean",
                              "quantity": "sum"
                          })
                          .reset_index()
                          .rename(columns={
                              "unit_price": "Preço Médio",
                              "delivery_days": "Prazo Médio (dias)",
                              "quantity": "Qtd Total"
                          }))
    
    supplier_comparison = supplier_comparison.sort_values("Preço Médio", ascending=True)

    # Gráfico comparativo com scatter plot
    fig_supplier = px.scatter(
        supplier_comparison,
        x="Prazo Médio (dias)",
        y="Preço Médio",
        size="Qtd Total",
        hover_name="supplier",
        title="Comparativo de Fornecedores: Preço Médio vs Prazo Médio",
        labels={"Preço Médio": "Preço Médio (R$)", "Prazo Médio (dias)": "Prazo Médio (dias)"},
        color="Preço Médio",
        color_continuous_scale="RdYlGn_r",
        size_max=50
    )
    
    st.plotly_chart(fig_supplier, use_container_width=True)

    # Tabela de comparativo
    with st.expander("Ver tabela de comparativo", expanded=False):
        display_cols = supplier_comparison.copy()
        display_cols["Preço Médio"] = display_cols["Preço Médio"].map(lambda x: f"R$ {x:,.2f}")
        display_cols["Prazo Médio (dias)"] = display_cols["Prazo Médio (dias)"].map(lambda x: f"{x:.1f}")
        st.dataframe(display_cols, use_container_width=True)

st.markdown("---")

# ================ VOLUME DE COMPRAS POR MÊS ================

st.subheader("2️⃣ Volume de Compras por Mês — Série Temporal")
st.markdown("Identifique períodos de maior/menor gasto e planeje compras futuras.")

if not df_filtered.empty:
    df_month = df_filtered.copy()
    df_month["month"] = df_month["date"].dt.to_period("M").dt.to_timestamp()
    
    # Agregação mensal
    monthly_spending = (df_month.groupby("month")
                       .agg({
                           "total_cost": "sum",
                           "quantity": "sum"
                       })
                       .reset_index()
                       .rename(columns={
                           "total_cost": "Gasto Mensal",
                           "quantity": "Quantidade"
                       }))

    # Gráfico de série temporal
    fig_ts = px.line(
        monthly_spending,
        x="month",
        y="Gasto Mensal",
        markers=True,
        title="Gasto Total em Compras por Mês",
        labels={"month": "Mês", "Gasto Mensal": "Gasto (R$)"},
        color_discrete_sequence=["#1f77b4"]
    )
    
    fig_ts.update_layout(hovermode="x unified")
    st.plotly_chart(fig_ts, use_container_width=True)

    # Tabela agregada
    with st.expander("Ver tabela de série temporal", expanded=False):
        display_monthly = monthly_spending.copy()
        display_monthly["month"] = pd.to_datetime(display_monthly["month"]).dt.strftime("%Y-%m")
        display_monthly["Gasto Mensal"] = display_monthly["Gasto Mensal"].map(lambda x: f"R$ {x:,.2f}")
        st.dataframe(display_monthly, use_container_width=True, height=300)

st.markdown("---")

# ================ PRODUTOS COM MAIOR GASTO ================

st.subheader("3️⃣ Produtos com Maior Gasto em Compras")
st.markdown("Identifique produtos estratégicos com maior impacto financeiro.")

if not df_filtered.empty:
    # Top produtos por gasto
    top_products = (df_filtered.groupby("product_name")
                   .agg({
                       "total_cost": "sum",
                       "quantity": "sum"
                   })
                   .reset_index()
                   .rename(columns={
                       "total_cost": "Gasto Total",
                       "quantity": "Qtd Total"
                   })
                   .sort_values("Gasto Total", ascending=False)
                   .head(15))

    # Gráfico de barras
    fig_top = px.bar(
        top_products,
        x="Gasto Total",
        y="product_name",
        orientation="h",
        title="Top 15 Produtos com Maior Gasto",
        labels={"Gasto Total": "Gasto Total (R$)", "product_name": "Produto"},
        color="Gasto Total",
        color_continuous_scale="Viridis"
    )
    
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

    # Tabela de top produtos
    with st.expander("Ver tabela de top produtos", expanded=False):
        display_top = top_products.copy()
        display_top["Gasto Total"] = display_top["Gasto Total"].map(lambda x: f"R$ {x:,.2f}")
        st.dataframe(display_top, use_container_width=True, height=400)

st.markdown("---")

# ================ RECOMENDAÇÕES PARA GESTORES ================

st.subheader("💡 Recomendações Estratégicas para Gestores")

if df_filtered.empty:
    st.write("Sem dados para gerar recomendações.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**a) Fornecedores Mais Eficientes (Melhor Preço):**")
        best_price = (df_filtered.groupby("supplier")
                     .agg({"unit_price": "mean"})
                     .reset_index()
                     .sort_values("unit_price")
                     .head(5))
        if not best_price.empty:
            for idx, row in best_price.iterrows():
                st.write(f"- {row['supplier']}: R$ {row['unit_price']:.2f} (preço médio)")

    with col2:
        st.markdown("**a) Fornecedores com Melhor Prazo de Entrega:**")
        best_delivery = (df_filtered.groupby("supplier")
                        .agg({"delivery_days": "mean"})
                        .reset_index()
                        .sort_values("delivery_days")
                        .head(5))
        if not best_delivery.empty:
            for idx, row in best_delivery.iterrows():
                st.write(f"- {row['supplier']}: {row['delivery_days']:.1f} dias (prazo médio)")

    st.markdown("**b) Oportunidades de Redução de Custos:**")
    
    if len(suppliers) > 1:
        avg_price = df_filtered.groupby("supplier")["unit_price"].mean()
        overall_avg = avg_price.mean()
        expensive_suppliers = avg_price[avg_price > overall_avg * 1.2].sort_values(ascending=False)
        
        if not expensive_suppliers.empty:
            for supplier_name, price in expensive_suppliers.items():
                st.write(f"- Fornecedor '{supplier_name}' tem preço {((price/overall_avg - 1) * 100):.1f}% acima da média. Considere negociar ou buscar alternativas.")
    
    st.markdown("**c) Planejamento de Compras com Base em Histórico:**")
    
    # Identificar produtos com maior variação de gasto
    product_spending_variance = (df_filtered.groupby("product_name")
                                .agg({"total_cost": ["sum", "std"]})
                                .reset_index())
    product_spending_variance.columns = ["product_name", "total_gasto", "variacao"]
    product_spending_variance = product_spending_variance[product_spending_variance["variacao"] > 0].sort_values("total_gasto", ascending=False).head(5)
    
    if not product_spending_variance.empty:
        st.write("Produtos com maior investimento (considere quantidade maior em compras futuras):")
        for idx, row in product_spending_variance.iterrows():
            st.write(f"- {row['product_name']}: R$ {row['total_gasto']:,.2f} acumulado")

st.markdown("---")

# ================ DOWNLOAD DE DADOS ================

if not df_filtered.empty:
    csv_bytes = to_csv_bytes(df_filtered)
    st.download_button(
        "📥 Baixar dados filtrados (CSV)",
        data=csv_bytes,
        file_name="compras_filtradas.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Dashboard de Compras e Fornecedores — Desenvolvido com Python, Streamlit e Plotly. Modular e pronto para extensão.")
