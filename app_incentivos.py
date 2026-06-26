import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Gerencial", layout="wide")

st.title("📊 Dashboard Gerencial de Ventas")

# Cargar archivo
archivo = st.file_uploader("Sube tu Excel")

if archivo:
    df = pd.read_excel(archivo)
else:
    st.warning("Usando datos de ejemplo")
    df = pd.DataFrame({
        "Fecha": pd.date_range("2026-06-01", periods=10),
        "Gestor": ["Juan","Ana","Luis","Maria","Juan","Ana","Luis","Maria","Juan","Ana"],
        "Departamento": ["Lima","Cusco","Lima","Cusco","Lima","Cusco","Lima","Cusco","Lima","Cusco"],
        "Producto": ["Prepago","Postpago","OSS","Prepago","Postpago","OSS","Prepago","Postpago","OSS","Prepago"],
        "Ventas": [10,20,15,12,18,22,14,19,25,30]
    })

# Convertir fecha
df["Fecha"] = pd.to_datetime(df["Fecha"])

# ======================
# FILTROS
# ======================
st.sidebar.header("🔎 Filtros")

producto = st.sidebar.multiselect("Producto", df["Producto"].unique(), df["Producto"].unique())
gestor = st.sidebar.multiselect("Gestor", df["Gestor"].unique(), df["Gestor"].unique())
depto = st.sidebar.multiselect("Departamento", df["Departamento"].unique(), df["Departamento"].unique())

df = df[
    (df["Producto"].isin(producto)) &
    (df["Gestor"].isin(gestor)) &
    (df["Departamento"].isin(depto))
]

# ======================
# KPIs
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", df["Ventas"].sum())
col2.metric("Promedio Diario", round(df["Ventas"].mean(),2))
col3.metric("Días activos", df["Fecha"].nunique())

# ======================
# EVOLUCIÓN
# ======================
st.subheader("📈 Evolución de Ventas")

df_evo = df.groupby("Fecha")["Ventas"].sum().reset_index()

fig = px.line(df_evo, x="Fecha", y="Ventas")
st.plotly_chart(fig, use_container_width=True)

# ======================
# PRODUCTO
# ======================
st.subheader("📦 Ventas por Producto")

fig2 = px.bar(df.groupby("Producto")["Ventas"].sum().reset_index(),
              x="Producto", y="Ventas")

st.plotly_chart(fig2, use_container_width=True)

# ======================
# DEPARTAMENTO
# ======================
st.subheader("🏢 Ventas por Departamento")

fig3 = px.bar(df.groupby("Departamento")["Ventas"].sum().reset_index(),
              x="Departamento", y="Ventas")

st.plotly_chart(fig3, use_container_width=True)

# ======================
# DETALLE
# ======================
st.subheader("📋 Detalle")
st.dataframe(df)
