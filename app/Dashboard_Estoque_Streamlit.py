"""
Dashboard de Controle de Estoque (Parte 1)
Arquivo: Dashboard_Estoque_Streamlit.py

Funcionalidades:
- Upload CSV/XLSX com dados de estoque (ou gera dados de exemplo)
- Filtro por Categoria (e busca por nome)
- Tabela interativa que mostra: product_id, product_name, category, quantity, min_stock, unit_cost, last_update
- Indicador: número de produtos abaixo do estoque mínimo (reage aos filtros)
- Gráfico de barras: Estoque Atual vs Estoque Mínimo (produtos em alerta destacados)
- Valor total do estoque (quantidade * unit_cost), atualizado com filtros
- Download dos dados filtrados em CSV
- Código modular e anotado para facilitar extensão futura
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard de Controle de Estoque", layout="wide")

# Helpers / Modular 
@st.cache_data
def generate_sample_stock(n_products=60, seed=42):
    np.random.seed(seed)
    categories = ["Bebidas", "Higiene", "Padaria", "Laticínios", "Limpeza", "Eletrônicos", "Acessórios"]
    suppliers = [f"Fornec {i+1}" for i in range(8)]

    rows = []
    for i in range(n_products):
        product_id = f"P{i+1000}"
        product_name = f"Produto {i+1}"
        category = np.random.choice(categories, p=np.random.dirichlet(np.ones(len(categories))))
        supplier = np.random.choice(suppliers)
        quantity = int(np.random.poisson(40))  # média de unidades em estoque
        min_stock = int(np.clip(np.random.poisson(15), 1, None))  # mínimo recomendado
        unit_cost = float(np.round(np.random.uniform(1.5, 250.0), 2))
        days_ago = int(np.random.exponential(scale=30))
        last_update = (pd.Timestamp.today() - pd.Timedelta(days=days_ago)).date().isoformat()
        rows.append((product_id, product_name, category, supplier, quantity, min_stock, unit_cost, last_update))

    df = pd.DataFrame(rows, columns=[
        "product_id", "product_name", "category", "supplier",
        "quantity", "min_stock", "unit_cost", "last_update"
    ])
    df["last_update"] = pd.to_datetime(df["last_update"])
    return df

@st.cache_data
def load_stock_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["last_update"])
    except Exception:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    # garantir colunas mínimas e tipos
    expected = ["product_id", "product_name", "category", "supplier", "quantity", "min_stock", "unit_cost", "last_update"]
    for col in expected:
        if col not in df.columns:
            # preencher com padrões sensatos
            if col == "product_id":
                df[col] = [f"PID{i+1}" for i in range(len(df))]
            elif col == "product_name":
                df[col] = ""
            elif col == "category":
                df[col] = "Sem Categoria"
            elif col == "supplier":
                df[col] = "Desconhecido"
            elif col in ("quantity", "min_stock"):
                df[col] = 0
            elif col == "unit_cost":
                df[col] = 0.0
            elif col == "last_update":
                df[col] = pd.Timestamp.today()
    # tipos
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["min_stock"] = pd.to_numeric(df["min_stock"], errors="coerce").fillna(0).astype(int)
    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0.0).astype(float)
    df["last_update"] = pd.to_datetime(df["last_update"], errors="coerce").fillna(pd.Timestamp.today())
    return df[expected]

@st.cache_data
def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

def compute_value_total(df):
    return (df["quantity"] * df["unit_cost"]).sum()

def highlight_below_min(s):
    # função para pandas Styler: destaca linhas onde quantity < min_stock
    is_alert = s["quantity"] < s["min_stock"]
    return ["background-color: #ffdcdc" if v else "" for v in is_alert]

# ---------------- UI ----------------
st.title("📦 Dashboard de Controle de Estoque — Parte 1")
st.subheader("Monitore níveis, identifique produtos críticos e calcule o valor total do inventário")

with st.sidebar:
    st.header("Dados e Filtros")
    uploaded = st.file_uploader("Carregar arquivo CSV/XLSX (estoque)", type=["csv", "xlsx"])
    use_sample = st.checkbox("Usar dados de exemplo (se nenhum arquivo for enviado)", value=True)

    st.markdown("---")
    st.markdown("Opções de visualização:")
    show_only_alerts = st.checkbox("Mostrar apenas produtos abaixo do mínimo", value=False)
    st.markdown("Busca rápida:")
    search_name = st.text_input("Buscar por nome de produto (contém)")

    st.markdown("---")
    st.caption("Formato esperado das colunas: product_id, product_name, category, supplier, quantity, min_stock, unit_cost, last_update")

# Carregar dados
if uploaded is not None:
    df_stock = load_stock_file(uploaded)
elif use_sample:
    df_stock = generate_sample_stock(n_products=80)
else:
    st.warning("Envie um arquivo CSV/XLSX ou marque 'Usar dados de exemplo'.")
    st.stop()

# Preparar colunas derivadas
df_stock["value"] = df_stock["quantity"] * df_stock["unit_cost"]
df_stock["below_min"] = df_stock["quantity"] < df_stock["min_stock"]

# Filtros dinâmicos de categoria (aplica no dataframe antes das visualizações)
categories = ["Todas"] + sorted(df_stock["category"].dropna().unique().tolist())
selected_category = st.selectbox("Filtrar por Categoria", options=categories, index=0)

# Aplicar filtros
df_filtered = df_stock.copy()

if selected_category and selected_category != "Todas":
    df_filtered = df_filtered[df_filtered["category"] == selected_category]

if search_name:
    df_filtered = df_filtered[df_filtered["product_name"].str.contains(search_name, case=False, na=False)]

if show_only_alerts:
    df_filtered = df_filtered[df_filtered["below_min"] == True]

# Indicadores superiores
col1, col2, col3, col4 = st.columns([1.5, 1.2, 1.2, 2])

total_items = df_filtered["quantity"].sum()
total_skus = df_filtered["product_id"].nunique()
total_value = compute_value_total(df_filtered)
critical_count = int(df_filtered["below_min"].sum())

col1.metric("📦 Total de unidades em estoque", f"{int(total_items):,}")
col2.metric("🏷️ SKUs cadastrados (visíveis)", f"{total_skus}")
col3.metric("⚠️ Produtos abaixo do mínimo", f"{critical_count}")
col4.metric("💰 Valor total do estoque (R$)", f"R$ {total_value:,.2f}")

st.markdown("---")

# Tabela interativa 
st.subheader("Tabela de Produtos — Detalhada")
st.markdown("Use filtros à esquerda para refinar. Linhas em destaque indicam status crítico (estoque abaixo do mínimo).")

if df_filtered.empty:
    st.info("Nenhum produto corresponde aos filtros selecionados.")
else:
    # reorganiza colunas para exibir as mais relevantes primeiro
    display_cols = ["product_id", "product_name", "category", "supplier", "quantity", "min_stock", "unit_cost", "value", "last_update", "below_min"]
    df_display = df_filtered[display_cols].copy()
    df_display["unit_cost"] = df_display["unit_cost"].map(lambda x: f"R$ {x:,.2f}")
    df_display["value"] = df_display["value"].map(lambda x: f"R$ {x:,.2f}")
    df_display["last_update"] = pd.to_datetime(df_display["last_update"]).dt.date

    # estiliza para destacar linhas críticas
    def highlight_row(row):
        idx = row.name
        if idx is not None and idx < len(df_filtered):
            is_alert = df_filtered.iloc[idx]["below_min"]
            return ["background-color: #ffdcdc" if is_alert else "" for _ in row]
        return ["" for _ in row]
    
    styled = df_display.style.apply(highlight_row, axis=1)
    # streamlit pode renderizar pandas Styler
    st.dataframe(styled, use_container_width=True, height=400)

    # botão para baixar dados filtrados
    csv_bytes = to_csv_bytes(df_filtered)
    st.download_button("📥 Baixar dados filtrados (CSV)", data=csv_bytes, file_name="estoque_filtrado.csv", mime="text/csv")

st.markdown("---")

# Gráfico: Estoque Atual vs Mínimo 
st.subheader("Gráfico — Estoque Atual vs Estoque Mínimo")

if df_filtered.empty:
    st.info("Sem dados para o gráfico.")
else:
    # ordenar por diferença para destacar os mais críticos
    df_plot = df_filtered.copy()
    df_plot["diff"] = df_plot["quantity"] - df_plot["min_stock"]
    df_plot = df_plot.sort_values("diff").head(40)  # limitar para leitura (top 40 mais críticos)
    df_plot["alert_color"] = np.where(df_plot["below_min"], "Abaixo do mínimo", "Ok")

    # Criar gráfico de barras agrupadas usando plotly express
    # Primeiro, criar um dataframe no formato longo (melt) para plotly express
    df_melt = df_plot.melt(
        id_vars=["product_name", "below_min"],
        value_vars=["quantity", "min_stock"],
        var_name="tipo",
        value_name="valor"
    )
    
    # Criar o gráfico
    fig = px.bar(
        df_melt,
        x="product_name",
        y="valor",
        color="tipo",
        barmode="group",
        title="Estoque Atual vs Estoque Mínimo — (produtos mais críticos)",
        labels={"valor": "Quantidade", "product_name": "Produto", "tipo": "Tipo"},
        height=520,
        color_discrete_map={"quantity": "steelblue", "min_stock": "lightgray"}
    )
    
    # Destacar produtos abaixo do mínimo alterando a cor da barra de quantity
    # O melt cria duas linhas por produto (quantity e min_stock), então precisamos mapear corretamente
    for trace in fig.data:
        if trace.name == "quantity":
            # Criar lista de cores baseada na ordem dos produtos no df_plot
            colors = []
            for prod_name in df_plot["product_name"]:
                is_alert = df_plot[df_plot["product_name"] == prod_name]["below_min"].iloc[0]
                colors.append("indianred" if is_alert else "steelblue")
            trace.marker.color = colors
    
    fig.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Sugestões rápidas para gestores
st.subheader("Decisão para Gestores — Recomendações rápidas")
if df_filtered.empty:
    st.write("Sem produtos para analisar.")
else:
    st.markdown("- **Produtos com prioridade de reposição:**")
    top_reorder = df_filtered[df_filtered["below_min"]].sort_values("quantity").head(8)
    if top_reorder.empty:
        st.write("Nenhum produto está abaixo do mínimo nos filtros atuais.")
    else:
        st.table(top_reorder[["product_id", "product_name", "category", "quantity", "min_stock", "supplier"]])

st.markdown("---")
st.caption("Desenvolvido para a disciplina. Modular e pronto para extensão (ex.: integração com banco, agendamento de reabastecimento, thresholds por fornecedor).")
