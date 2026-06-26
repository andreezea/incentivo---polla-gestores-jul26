streamlit>=1.33
pandas>=2.0
plotly>=5.20
openpyxl>=3.1

# -*- coding: utf-8 -*-
"""
App de Incentivos de Ventas — "La Polla del Cumplimiento"
Ejecutar con: streamlit run app_incentivos.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Incentivo de Ventas", layout="wide", page_icon="🏆")

# ----------------------------------------------------------------------------
# PARÁMETROS DEL MODELO (idénticos a la hoja "Parametros" del Excel)
# ----------------------------------------------------------------------------
BANDAS_CUMPLIMIENTO = [
    (0, 79.999, 0, "< 80%"),
    (80, 99.999, 1, "80% - 99%"),
    (100, 109.999, 2, "100% - 109%"),
    (110, 129.999, 4, "110% - 129%"),
    (130, 149.999, 6, "130% - 149%"),
    (150, 179.999, 8, "150% - 179%"),
    (180, 1e12, 12, "180%+"),
]
BANDAS_CRECIMIENTO = [(0, 9.999, 0), (10, 19.999, 2), (20, 29.999, 4), (30, 1e12, 6)]
BONO_CONSISTENCIA = 5
BONO_ELITE = 5

REQUIRED_COLS = [
    "Gestor", "Mes", "Cuota", "Venta", "VentaMesAnterior",
    "Sem1", "Sem2", "Sem3", "Sem4", "TodosProductos",
]


def puntos_cumplimiento(pct: float) -> int:
    for lo, hi, pts, _ in BANDAS_CUMPLIMIENTO:
        if lo <= pct <= hi:
            return pts
    return 0


def bono_crecimiento(pct: float) -> int:
    if pct < 0:
        return 0
    for lo, hi, pts in BANDAS_CRECIMIENTO:
        if lo <= pct <= hi:
            return pts
    return 0


def procesar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Cumplimiento_%"] = (df["Venta"] / df["Cuota"] * 100).round(1)
    df["Puntos_Base"] = df["Cumplimiento_%"].apply(puntos_cumplimiento)
    df["Crecimiento_%"] = (
        (df["Venta"] - df["VentaMesAnterior"]) / df["VentaMesAnterior"].replace(0, pd.NA) * 100
    ).fillna(0).round(1)
    df["Bono_Crecimiento"] = df["Crecimiento_%"].apply(bono_crecimiento)
    df["Consistencia"] = df[["Sem1", "Sem2", "Sem3", "Sem4"]].apply(
        lambda r: all(str(v).strip().lower() in ("sí", "si", "yes", "true", "1") for v in r), axis=1
    )
    df["Bono_Consistencia"] = df["Consistencia"].map({True: BONO_CONSISTENCIA, False: 0})
    df["Elite"] = df["TodosProductos"].astype(str).str.strip().str.lower().isin(["sí", "si", "yes", "true", "1"])
    df["Bono_Elite"] = df["Elite"].map({True: BONO_ELITE, False: 0})
    df["Total_Puntos"] = (
        df["Puntos_Base"] + df["Bono_Crecimiento"] + df["Bono_Consistencia"] + df["Bono_Elite"]
    )
    df["Semaforo"] = df["Cumplimiento_%"].apply(
        lambda p: "🟢 Verde" if p >= 100 else ("🟡 Amarillo" if p >= 80 else "🔴 Rojo")
    )
    return df


def datos_demo() -> pd.DataFrame:
    import random
    random.seed(7)
    gestores = [
        "Ana Torres", "Luis Ramírez", "Carla Méndez", "Jorge Salas", "Diana Flores",
        "Pedro Ibáñez", "Sofía Castro", "Miguel Vega", "Renata Cruz", "Tomás Rojas",
    ]
    meses = ["Abril 2026", "Mayo 2026", "Junio 2026"]
    base_quota = {g: random.randint(40000, 70000) for g in gestores}
    prev_sales = {g: base_quota[g] * random.uniform(0.75, 1.05) for g in gestores}
    rows = []
    for mes in meses:
        for g in gestores:
            cuota = round(base_quota[g] * random.uniform(0.95, 1.05), 0)
            factor = random.choice([0.7, 0.85, 0.95, 1.05, 1.15, 1.35, 1.55, 1.9])
            venta = round(cuota * factor * random.uniform(0.95, 1.05), 0)
            venta_ant = round(prev_sales[g], 0)
            prev_sales[g] = venta
            semanas = [random.choice(["Sí", "Sí", "Sí", "No"]) for _ in range(4)]
            if factor >= 1.0 and random.random() < 0.6:
                semanas = ["Sí"] * 4
            todos_prod = "Sí" if (factor >= 1.1 and random.random() < 0.7) else random.choice(["Sí", "No"])
            rows.append([g, mes, cuota, venta, venta_ant] + semanas + [todos_prod])
    return pd.DataFrame(rows, columns=REQUIRED_COLS)


# ----------------------------------------------------------------------------
# SIDEBAR — Carga de datos
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown(
    "Sube tu archivo Excel/CSV con columnas:\n\n"
    "`Gestor, Mes, Cuota, Venta, VentaMesAnterior, Sem1, Sem2, Sem3, Sem4, TodosProductos`"
)
archivo = st.sidebar.file_uploader("📂 Cargar datos (Excel o CSV)", type=["xlsx", "csv"])

if archivo is not None:
    try:
        if archivo.name.endswith(".csv"):
            df_raw = pd.read_csv(archivo)
        else:
            df_raw = pd.read_excel(archivo)
        faltantes = [c for c in REQUIRED_COLS if c not in df_raw.columns]
        if faltantes:
            st.sidebar.error(f"Faltan columnas: {faltantes}. Se usarán datos demo.")
            df_raw = datos_demo()
        else:
            st.sidebar.success("Datos cargados correctamente ✅")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: {e}")
        df_raw = datos_demo()
else:
    st.sidebar.info("Usando datos de ejemplo (ficticios).")
    df_raw = datos_demo()

df = procesar(df_raw)

st.sidebar.markdown("---")
meses_disp = ["Todos"] + sorted(df["Mes"].unique().tolist())
mes_sel = st.sidebar.selectbox("📅 Filtrar por mes", meses_disp)
gestores_disp = ["Todos"] + sorted(df["Gestor"].unique().tolist())
gestor_sel = st.sidebar.selectbox("👤 Filtrar por gestor", gestores_disp)

df_f = df.copy()
if mes_sel != "Todos":
    df_f = df_f[df_f["Mes"] == mes_sel]
if gestor_sel != "Todos":
    df_f = df_f[df_f["Gestor"] == gestor_sel]

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.title("🏆 Sistema de Incentivo de Ventas")
st.caption("Modelo tipo \"polla\" por cumplimiento de cuota — puntos, bonos y sorteo")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Gestores evaluados", df_f["Gestor"].nunique())
c2.metric("Cumplimiento promedio", f"{df_f['Cumplimiento_%'].mean():.1f}%" if len(df_f) else "—")
c3.metric("Puntos totales otorgados", int(df_f["Total_Puntos"].sum()) if len(df_f) else 0)
top = df_f.groupby("Gestor")["Total_Puntos"].sum().sort_values(ascending=False)
c4.metric("Top performer", top.index[0] if len(top) else "—")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📈 Evolución", "🚦 Semáforo", "📋 Detalle"])

# ----------------------------------------------------------------------------
# TAB 1 — Ranking acumulado
# ----------------------------------------------------------------------------
with tab1:
    rank = (
        df_f.groupby("Gestor")["Total_Puntos"].sum()
        .reset_index().sort_values("Total_Puntos", ascending=False)
    )
    total_pts = rank["Total_Puntos"].sum()
    rank["Prob_Sorteo_%"] = (rank["Total_Puntos"] / total_pts * 100).round(2) if total_pts else 0
    rank.insert(0, "Puesto", range(1, len(rank) + 1))

    colA, colB = st.columns([2, 1])
    with colA:
        fig = px.bar(
            rank, x="Gestor", y="Total_Puntos", color="Total_Puntos",
            color_continuous_scale=["#C00000", "#BF8F00", "#1E7B34"],
            text="Total_Puntos", title="Ranking de puntos acumulados",
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        st.subheader("🎲 Probabilidad de sorteo")
        st.dataframe(
            rank[["Puesto", "Gestor", "Total_Puntos", "Prob_Sorteo_%"]],
            hide_index=True, use_container_width=True,
        )

# ----------------------------------------------------------------------------
# TAB 2 — Evolución mensual
# ----------------------------------------------------------------------------
with tab2:
    evo = df.groupby("Mes")["Cumplimiento_%"].mean().reset_index()
    orden_mes = {m: i for i, m in enumerate(sorted(df["Mes"].unique(), key=lambda x: x))}
    fig2 = px.line(
        evo, x="Mes", y="Cumplimiento_%", markers=True,
        title="Evolución del % de cumplimiento promedio",
    )
    fig2.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Meta 100%")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Evolución individual por gestor")
    fig3 = px.line(
        df.sort_values("Mes"), x="Mes", y="Cumplimiento_%", color="Gestor", markers=True,
    )
    fig3.add_hline(y=100, line_dash="dash", line_color="green")
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------------------------
# TAB 3 — Semáforo
# ----------------------------------------------------------------------------
with tab3:
    sem_counts = df_f["Semaforo"].value_counts().reset_index()
    sem_counts.columns = ["Semáforo", "Casos"]
    colC, colD = st.columns([1, 1])
    with colC:
        fig4 = px.pie(
            sem_counts, names="Semáforo", values="Casos",
            color="Semáforo",
            color_discrete_map={"🟢 Verde": "#1E7B34", "🟡 Amarillo": "#BF8F00", "🔴 Rojo": "#C00000"},
            title="Distribución de cumplimiento",
        )
        st.plotly_chart(fig4, use_container_width=True)
    with colD:
        st.subheader("Detalle por gestor y mes")
        def color_fila(val):
            if "Verde" in str(val):
                return "background-color:#C6EFCE;color:#1E7B34"
            if "Amarillo" in str(val):
                return "background-color:#FFEB9C;color:#9C6500"
            if "Rojo" in str(val):
                return "background-color:#FFC7CE;color:#9C0006"
            return ""
        st.dataframe(
            df_f[["Gestor", "Mes", "Cumplimiento_%", "Semaforo"]]
            .sort_values("Cumplimiento_%", ascending=False)
            .style.applymap(color_fila, subset=["Semaforo"]),
            hide_index=True, use_container_width=True,
        )

# ----------------------------------------------------------------------------
# TAB 4 — Detalle completo
# ----------------------------------------------------------------------------
with tab4:
    st.subheader("Tabla completa de cálculo (puntos y bonos)")
    cols_show = [
        "Gestor", "Mes", "Cuota", "Venta", "Cumplimiento_%", "Puntos_Base",
        "Crecimiento_%", "Bono_Crecimiento", "Bono_Consistencia", "Bono_Elite",
        "Total_Puntos", "Semaforo",
    ]
    st.dataframe(df_f[cols_show].sort_values("Total_Puntos", ascending=False),
                 hide_index=True, use_container_width=True)
    st.download_button(
        "⬇️ Descargar tabla calculada (CSV)",
        df_f[cols_show].to_csv(index=False).encode("utf-8-sig"),
        file_name="incentivo_calculado.csv", mime="text/csv",
    )

st.markdown("---")
with st.expander("ℹ️ Reglas del modelo de incentivo"):
    st.markdown(
        """
**Puntos por % de cumplimiento**
| Tramo | Puntos |
|---|---|
| < 80% | 0 |
| 80% – 99% | 1 |
| 100% – 109% | 2 |
| 110% – 129% | 4 |
| 130% – 149% | 6 |
| 150% – 179% | 8 |
| 180%+ | 12 |

**Bonos adicionales**
- Crecimiento vs. mes anterior: +10% → +2 pts · +20% → +4 pts · +30% → +6 pts
- Consistencia (cumple cuota las 4 semanas): +5 pts
- Elite (cumple el 100% de todos los productos): +5 pts

**Premio:** sorteo mensual; a más puntos acumulados, mayor probabilidad de ganar.
        """
    )
