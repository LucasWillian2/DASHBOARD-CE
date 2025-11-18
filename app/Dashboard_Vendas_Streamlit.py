import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# HELPERS
@st.cache_data
def generate_sample_data(n_days=365, n_stores=5, n_products=50, seed=42):
    np.random.seed(seed)
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=n_days)
    dates = pd.date_range(start, periods=n_days)

    stores = [f'Store_{i+1}' for i in range(n_stores)]
    products = [f'Product_{i+1}' for i in range(n_products)]

    rows = []
    for d in dates:
        # Número de vendas por dia
        m = np.random.poisson(8)
        for _ in range(m):
            store = np.random.choice(stores)
            product = np.random.choice(products, p=np.linspace(1, 0.1, n_products)/np.linspace(1, 0.1, n_products).sum())
            quantity = np.random.randint(1, 6)
            unit_price = float(np.round(np.random.uniform(5, 100), 2))
            rows.append((d.date().isoformat(), store, product, quantity, unit_price))

    df = pd.DataFrame(rows, columns=['date', 'store', 'product_name', 'quantity', 'unit_price'])
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data
def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, parse_dates=['date'])
    except Exception:
        # Tenta com engine openpyxl para arquivos xlsx
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    # Garante que as colunas estão no formato correto(minimas)
    expected_columns = ['date', 'store', 'product_name', 'quantity', 'unit_price']
    for col in expected_columns:
        if col not in df.columns:
            if col == "store":
                df[col] = "Store_1"
            elif col == "quantity":
                df["quantity"] = 1
            elif col == "unit_price":
                df["unit_price"] = 0.0
            else:
                df[col] = ""
    df["date"] = pd.to_datetime(df["date"])
    return df
            
# UI
st.title("Dashboard de Vendas")
st.markdown("Carregue seus dados de vendas ou use dados de amostra para explorar o dashboard.")

with st.sidebar:
    st.header("Carregar Dados / Filtros")
    uploaded_file = st.file_uploader("Carregar CSV ou XLSX com dados de vendas", type=['csv', 'xlsx'])
    use_sample_data = st.checkbox("Usar dados de exemplo (se nenhum arquivo for enviado)", value=True)

    st.markdown("---")

    # Carregamento de dados
    if uploaded_file is not None:
        df = load_csv(uploaded_file)
    elif use_sample_data:
        df = generate_sample_data(n_days=730, n_stores=6 , n_products=80)
    else:
        st.warning("Envie um arquivo CSV/XLSX ou marque 'Usar dados de exemplo'.")
        st.stop()

# Prepara as Colunas
df["store"] = df.get("store", "").astype(str)
df["product_name"] = df.get("product_name", "").astype(str)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
df["revenue"] = df["quantity"] * df["unit_price"]

# Filtros
stores = sorted(df["store"].unique().tolist())
products = sorted(df["product_name"].unique().tolist())


selected_stores = st.multiselect("Loja(s)", options=stores, default=stores)
selected_products = st.multiselect("Produto(s)", options=products, default=None)


min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.date_input("Período (início - fim)", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Filtra os dados
start_date, end_date = date_range
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
mask &= df["store"].isin(selected_stores)
if selected_products and len(selected_products) > 0:
    mask &= df["product_name"].isin(selected_products)


df_filtered = df.loc[mask].copy()

# Indicadores superiores
col1, col2, col3 = st.columns([1.5, 2, 2])


# Receita total
total_revenue = df_filtered["revenue"].sum()
# Quantidade total
total_quantity = df_filtered["quantity"].sum()
# Número de SKUs/Produtos vendidos
distinct_products = df_filtered["product_name"].nunique()


col1.metric("💰 Receita total (R$)", f"R$ {total_revenue:,.2f}")
col2.metric("📦 Quantidade total vendida", f"{int(total_quantity):,}")
col3.metric("🏷️ Produtos diferentes vendidos", f"{distinct_products}")


st.markdown("---")

# Série temporal por mês (quantidade)
st.subheader("Série temporal — Quantidade vendida por mês")
if df_filtered.empty:
    st.info("Nenhum dado disponível para os filtros selecionados.")
else:
    df_month = df_filtered.copy()
    df_month["month"] = df_month["date"].dt.to_period("M").dt.to_timestamp()
    time_series = df_month.groupby("month")["quantity"].sum().reset_index()

    fig_ts = px.line(time_series, x="month", y="quantity", markers=True, title = "Quantidade vendida por mês")
    fig_ts.update_layout(xaxis_title="Mês", yaxis_title="Quantidade vendida")
    st.plotly_chart(fig_ts, use_container_width=True)

    # Mostra a tabela agregada
    with st.expander("Ver tabela de série temporal" , expanded=False):
        st.dataframe(time_series)

# Top 10 produtos
st.subheader("Top 10 — Produtos mais vendidos (por quantidade)")
if not df_filtered.empty:
    top_products = (df_filtered.groupby("product_name")["quantity"]
                    .sum()
                    .reset_index()
                    .sort_values(by="quantity", ascending=False)
                    .head(10))
    
    fig_top = px.bar(top_products, x="quantity", y="product_name", orientation="h", title="Top 10 Produtos mais quantidade")
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

    with st.expander("Ver tabela de Top 10 Produtos", expanded=False):
        st.dataframe(top_products)

# Receita por periodo comparativo
st.subheader("Receita — Detalhamento")
if not df_filtered.empty:
    revenue_by_store = (df_filtered.groupby("store")["revenue"]
                        .sum()
                        .reset_index()
                        .sort_values(by="revenue", ascending=False))
    st.markdown("Receita por loja no período")
    st.dataframe(revenue_by_store)

# Download dos dados filtrados
@st.cache_data
def to_csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8')

if not df_filtered.empty:
    csv_bytes = to_csv_bytes(df_filtered)
    st.download_button("📥 Baixar dados filtrados (CSV)", data=csv_bytes, file_name="vendas_filtradas.csv", mime="text/csv")

    st.markdown("---")
    st.caption("Arquivo gerado automaticamente pelo template do Dashboard de Vendas. Ajuste filtros e carregue seus próprios dados quando necessário.")
    

             

