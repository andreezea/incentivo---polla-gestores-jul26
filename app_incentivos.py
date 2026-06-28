# ════════════════════════════════════════
# IMPORTS (ESTO VA PRIMERO SIEMPRE)
# ════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.express as px

# ════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════
st.set_page_config(page_title="Dashboard Gerencial", layout="wide")

# ════════════════════════════════════════
# 🎨 ESTILO GERENCIAL PRO
# ════════════════════════════════════════
st.markdown("""
<style>
:root {
    --azul: #0A2A5E;
    --azul2: #0B5ED7;
    --gris: #5A6A85;
}

/* Fondo */
.stApp { 
    background: linear-gradient(180deg, #EEF3FB 0%, #F7FAFF 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081F4D, #0A2A5E);
}

/* KPIs */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-top: 4px solid var(--azul);
}

[data-testid="metric-value"] {
    color: var(--azul);
    font-weight: 900;
}

/* Tabs */
.stTabs [aria-selected="true"] {
    background: var(--azul);
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
# 📊 DATA (SIMULADA SI NO HAY CSV)
# ════════════════════════════════════════
@st.cache_data
def cargar_data():
    try:
        df = pd.read_csv("datos.csv")
    except:
        df = pd.DataFrame({
            "Agencia": ["Lima", "Cusco", "Arequipa", "Trujillo"],
            "Ventas": [120000, 90000, 110000, 80000],
            "Cumplimiento": [105, 95, 110, 98],
            "NPS": [70, 65, 75, 60]
        })
    return df

df = cargar_data()

# ════════════════════════════════════════
# 🎯 HEADER
# ════════════════════════════════════════
st.title("📊 Dashboard Gerencial de Ventas")

# ════════════════════════════════════════
# 📈 KPIs
# ════════════════════════════════════════
col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"S/ {df['Ventas'].sum():,.0f}")
col2.metric("Cumplimiento Promedio", f"{df['Cumplimiento'].mean():.1f}%")
col3.metric("NPS Promedio", f"{df['NPS'].mean():.1f}")

# ════════════════════════════════════════
# 📊 GRÁFICOS
# ════════════════════════════════════════
tab1, tab2 = st.tabs(["📊 Ventas", "📈 Performance"])

with tab1:
    fig = px.bar(df, x="Agencia", y="Ventas", title="Ventas por Agencia")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.scatter(
        df, 
        x="Cumplimiento", 
        y="NPS", 
        size="Ventas",
        color="Agencia",
        title="Cumplimiento vs NPS"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════
# 🏆 TABLA
# ════════════════════════════════════════
st.subheader("Detalle por Agencia")
st.dataframe(df, use_container_width=True)
