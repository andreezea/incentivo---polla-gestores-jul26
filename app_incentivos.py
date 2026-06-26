# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Incentivo de Ventas", layout="wide", page_icon="🏆")

# ----------------------------------------------------------------------------
# PARÁMETROS
# ----------------------------------------------------------------------------
BANDAS_CUMPLIMIENTO = [
    (0, 79.999, 0),
    (80, 99.999, 1),
    (100, 109.999, 2),
    (110, 129.999, 4),
    (130, 149.999, 6),
    (150, 179.999, 8),
    (180, 1e12, 12),
]

BONO_CONSISTENCIA = 5
BONO_ELITE = 5

# ----------------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------------
def puntos_cumplimiento(pct):
    for lo, hi, pts in BANDAS_CUMPLIMIENTO:
        if lo <= pct <= hi:
            return pts
    return 0


def procesar(df):
    df = df.copy()
    df["Cumplimiento_%"] = (df["Venta"] / df["Cuota"] * 100).round(1)

    df["Puntos_Base"] = df["Cumplimiento_%"].apply(puntos_cumplimiento)

    df["Total_Puntos"] = df["Puntos_Base"]

    df["Semaforo"] = df["Cumplimiento_%"].apply(
        lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
    )

    return df


def datos_demo():
    return pd.DataFrame({
        "Gestor": ["Juan","Ana","Luis","Maria"],
        "Departamento": ["Lima","Cusco","Lima","Cusco"],
        "Mes": ["Junio","Junio","Junio","Junio"],
        "Cuota": [100,100,100,100],
        "Venta": [120,90,70,150],
        "VentaMesAnterior": [100,80,60,140]
    })


# ----------------------------------------------------------------------------
# CARGA
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuración")

archivo = st.sidebar.file_uploader("Sube tu Excel", type=["xlsx","csv"])

if archivo:
    if archivo.name.endswith(".csv"):
        df_raw = pd.read_csv(archivo)
    else:
        df_raw = pd.read_excel(archivo)
else:
    df_raw = datos_demo()

df = procesar(df_raw)

# ----------------------------------------------------------------------------
# FILTROS
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")

deptos = ["Todos"] + sorted(df["Departamento"].unique())
gestores = ["Todos"] + sorted(df["Gestor"].unique())

depto_sel = st.sidebar.selectbox("🏢 Departamento", deptos)
gestor_sel = st.sidebar.selectbox("👤 Gestor", gestores)

df_f = df.copy()

if depto_sel != "Todos":
    df_f = df_f[df_f["Departamento"] == depto_sel]

if gestor_sel != "Todos":
    df_f = df_f[df_f["Gestor"] == gestor_sel]


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.title("🏆 Dashboard Gerencial de Incentivos")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Gestores", df_f["Gestor"].nunique())
col2.metric("Cumplimiento Promedio", f"{df_f['Cumplimiento_%'].mean():.1f}%")
col3.metric("Total Puntos", int(df_f["Total_Puntos"].sum()))

venta_actual = df_f["Venta"].sum()
venta_ant = df_f["VentaMesAnterior"].sum()

var = ((venta_actual - venta_ant) / venta_ant * 100) if venta_ant != 0 else 0

col4.metric("Variación vs Mes Ant.", f"{var:.1f}%")


st.markdown("---")

# ----------------------------------------------------------------------------
# TOP 3
# ----------------------------------------------------------------------------
st.subheader("🥇 Top Performers")

rank = (
    df_f.groupby("Gestor")["Total_Puntos"]
    .sum()
    .reset_index()
    .sort_values("Total_Puntos", ascending=False)
)

top3 = rank.head(3)

cols = st.columns(3)
emojis = ["🥇","🥈","🥉"]

for i, row in enumerate(top3.itertuples()):
    cols[i].metric(f"{emojis[i]} {row.Gestor}", int(row.Total_Puntos))


# ----------------------------------------------------------------------------
# RANKING
# ----------------------------------------------------------------------------
st.subheader("🏆 Ranking General")

rank.insert(0, "Puesto", range(1, len(rank)+1))

colA, colB = st.columns([2,1])

with colA:
    fig = px.bar(
        rank.sort_values("Total_Puntos"),
        x="Total_Puntos",
        y="Gestor",
        orientation="h",
        text="Total_Puntos"
    )
    st.plotly_chart(fig, use_container_width=True)

with colB:
    st.subheader("🏆 Puntos obtenidos")
    st.dataframe(rank[["Puesto","Gestor","Total_Puntos"]], use_container_width=True)


# ----------------------------------------------------------------------------
# EVOLUCIÓN
# ----------------------------------------------------------------------------
st.subheader("📈 Evolución")

evo = df_f.groupby("Mes")["Cumplimiento_%"].mean().reset_index()

fig2 = px.line(evo, x="Mes", y="Cumplimiento_%", markers=True)
fig2.add_hline(y=100)

st.plotly_chart(fig2, use_container_width=True)


# ----------------------------------------------------------------------------
# SEMÁFORO
# ----------------------------------------------------------------------------
st.subheader("🚦 Estado")

sem = df_f["Semaforo"].value_counts().reset_index()
sem.columns = ["Estado","Cantidad"]

fig3 = px.pie(sem, names="Estado", values="Cantidad")

st.plotly_chart(fig3, use_container_width=True)


# ----------------------------------------------------------------------------
# TABLA FINAL
# ----------------------------------------------------------------------------
st.subheader("📋 Detalle Ejecutivo")

st.dataframe(
    df_f[[
        "Gestor",
        "Departamento",
        "Venta",
        "Cumplimiento_%",
        "Total_Puntos",
        "Semaforo"
    ]].sort_values("Total_Puntos", ascending=False),
    use_container_width=True
)
