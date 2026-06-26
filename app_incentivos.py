# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Incentivo de Ventas", layout="wide", page_icon="🏆")

# ----------------------------------------------------------------------------
# PARÁMETROS
# ----------------------------------------------------------------------------
BANDAS_CUMPLIMIENTO = [
    (0,    79.999,  0),
    (80,   99.999,  1),
    (100, 109.999,  2),
    (110, 129.999,  4),
    (130, 149.999,  6),
    (150, 179.999,  8),
    (180,  1e12,   12),
]

# Puntos adicionales por crecimiento vs mes anterior
BANDAS_CRECIMIENTO = [
    (20,   1e12, 3),
    (10,  19.999, 2),
    (5,    9.999, 1),
    (-1e12, 4.999, 0),
]

# ----------------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------------
def puntos_cumplimiento(pct):
    for lo, hi, pts in BANDAS_CUMPLIMIENTO:
        if lo <= pct <= hi:
            return pts
    return 0

def puntos_crecimiento(pct_crec):
    for lo, hi, pts in BANDAS_CRECIMIENTO:
        if lo <= pct_crec <= hi:
            return pts
    return 0

def procesar(df):
    df = df.copy()

    # --- Cumplimiento base ---
    df["Cumplimiento_%"] = (df["Venta"] / df["Cuota"] * 100).round(1)
    df["Puntos_Base"] = df["Cumplimiento_%"].apply(puntos_cumplimiento)

    # --- Puntos extra: ventas diarias sobre cuota diaria ---
    if "VentaDiaria" in df.columns and "CuotaDiaria" in df.columns:
        df["Puntos_Diario"] = (df["VentaDiaria"] - df["CuotaDiaria"]).clip(lower=0).round(0).astype(int)
    else:
        df["Puntos_Diario"] = 0

    # --- Puntos por crecimiento vs mes anterior ---
    if "VentaMesAnterior" in df.columns:
        df["Crec_%"] = (
            (df["Venta"] - df["VentaMesAnterior"]) / df["VentaMesAnterior"] * 100
        ).round(1)
        df["Puntos_Crec"] = df["Crec_%"].apply(puntos_crecimiento)
    else:
        df["Crec_%"]     = 0.0
        df["Puntos_Crec"] = 0

    df["Total_Puntos"] = df["Puntos_Base"] + df["Puntos_Diario"] + df["Puntos_Crec"]

    df["Semaforo"] = df["Cumplimiento_%"].apply(
        lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
    )
    return df

def datos_demo():
    """Dataset de ejemplo con columna Producto y campos extra."""
    import random
    random.seed(42)

    productos = ["Prepago", "Porta Pre", "Postpago", "OSS"]
    gestores  = ["Juan", "Ana", "Luis", "Maria"]
    deptos    = {"Juan": "Lima", "Ana": "Cusco", "Luis": "Lima", "Maria": "Cusco"}

    rows = []
    for g in gestores:
        for p in productos:
            cuota    = random.randint(80, 120)
            venta    = random.randint(60, 180)
            venta_ant = random.randint(50, 150)
            cuota_d  = round(cuota / 22, 2)
            venta_d  = round(venta / 22 * random.uniform(0.7, 1.4), 2)
            rows.append({
                "Gestor":           g,
                "Departamento":     deptos[g],
                "Mes":              "Junio",
                "Producto":         p,
                "Cuota":            cuota,
                "Venta":            venta,
                "VentaMesAnterior": venta_ant,
                "CuotaDiaria":      cuota_d,
                "VentaDiaria":      venta_d,
            })
    return pd.DataFrame(rows)

def color_semaforo(val):
    colors = {"🟢 Verde": "#d4edda", "🟡 Amarillo": "#fff3cd", "🔴 Rojo": "#f8d7da"}
    return f"background-color: {colors.get(val, '')}"

# ----------------------------------------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuración")
archivo = st.sidebar.file_uploader("Sube tu Excel / CSV", type=["xlsx", "csv"])

if archivo:
    df_raw = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
else:
    df_raw = datos_demo()
    st.sidebar.info("Usando datos de demo. Sube tu archivo para datos reales.")

df = procesar(df_raw)

# ----------------------------------------------------------------------------
# FILTROS GLOBALES (sidebar)
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")
deptos_opts  = ["Todos"] + sorted(df["Departamento"].unique())
gestores_opts = ["Todos"] + sorted(df["Gestor"].unique())

depto_sel   = st.sidebar.selectbox("🏢 Departamento", deptos_opts)
gestor_sel  = st.sidebar.selectbox("👤 Gestor",       gestores_opts)

df_f = df.copy()
if depto_sel  != "Todos": df_f = df_f[df_f["Departamento"] == depto_sel]
if gestor_sel != "Todos": df_f = df_f[df_f["Gestor"]       == gestor_sel]

# Agrupado por gestor (suma de todos sus productos)
df_gestor = (
    df_f
    .groupby(["Gestor", "Departamento"])
    .agg(
        Venta            = ("Venta",            "sum"),
        Cuota            = ("Cuota",            "sum"),
        VentaMesAnterior = ("VentaMesAnterior", "sum"),
        Puntos_Base      = ("Puntos_Base",      "sum"),
        Puntos_Diario    = ("Puntos_Diario",    "sum"),
        Puntos_Crec      = ("Puntos_Crec",      "sum"),
        Total_Puntos     = ("Total_Puntos",     "sum"),
    )
    .reset_index()
)
df_gestor["Cumplimiento_%"] = (df_gestor["Venta"] / df_gestor["Cuota"] * 100).round(1)
df_gestor["Semaforo"] = df_gestor["Cumplimiento_%"].apply(
    lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
)

# ----------------------------------------------------------------------------
# LEYENDA DE PUNTOS (sidebar)
# ----------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ Tabla de puntos"):
    st.markdown("**Cumplimiento de cuota**")
    st.dataframe(pd.DataFrame(BANDAS_CUMPLIMIENTO, columns=["Desde %", "Hasta %", "Puntos"]))
    st.markdown("**Crecimiento vs mes ant.**")
    st.dataframe(pd.DataFrame(BANDAS_CRECIMIENTO, columns=["Desde %", "Hasta %", "Puntos"]))
    st.markdown("**Diario:** +1 pt por cada venta sobre cuota diaria")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2 = st.tabs(["📊 Resumen General", "📦 Detalle por Producto"])

# ============================================================================
# TAB 1 — RESUMEN GENERAL
# ============================================================================
with tab1:
    st.title("🏆 Dashboard Gerencial de Incentivos")

    # KPIs principales
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gestores", df_gestor["Gestor"].nunique())
    k2.metric("Cumplimiento Promedio", f"{df_gestor['Cumplimiento_%'].mean():.1f}%")
    k3.metric("Total Puntos", int(df_gestor["Total_Puntos"].sum()))
    venta_act = df_gestor["Venta"].sum()
    venta_ant = df_gestor["VentaMesAnterior"].sum()
    var_pct   = ((venta_act - venta_ant) / venta_ant * 100) if venta_ant else 0
    k4.metric("Variación vs Mes Ant.", f"{var_pct:.1f}%", delta=f"{var_pct:.1f}%")

    st.markdown("---")

    # Desglose de puntos
    st.subheader("🎯 Desglose de Puntos (Total)")
    p1, p2, p3 = st.columns(3)
    p1.metric("📌 Puntos Base (Cuota)",      int(df_gestor["Puntos_Base"].sum()))
    p2.metric("📅 Puntos Diarios (Extra)",   int(df_gestor["Puntos_Diario"].sum()))
    p3.metric("📈 Puntos Crecimiento",       int(df_gestor["Puntos_Crec"].sum()))

    st.markdown("---")

    # Top 3
    st.subheader("🥇 Top Performers")
    rank = df_gestor.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
    top3 = rank.head(3)
    t_cols  = st.columns(3)
    emojis  = ["🥇", "🥈", "🥉"]
    for i, row in enumerate(top3.itertuples()):
        delta_str = (
            f"Base {int(row.Puntos_Base)} · "
            f"Diario {int(row.Puntos_Diario)} · "
            f"Crec {int(row.Puntos_Crec)}"
        )
        t_cols[i].metric(f"{emojis[i]} {row.Gestor}", int(row.Total_Puntos), delta_str)

    # Ranking + tabla
    st.subheader("🏆 Ranking General")
    rank_disp = rank.copy()
    rank_disp.insert(0, "Puesto", range(1, len(rank_disp) + 1))

    colA, colB = st.columns([2, 1])
    with colA:
        fig_rank = px.bar(
            rank.sort_values("Total_Puntos"),
            x="Total_Puntos", y="Gestor", orientation="h",
            text="Total_Puntos",
            color="Total_Puntos",
            color_continuous_scale="Blues",
        )
        fig_rank.update_traces(textposition="outside")
        fig_rank.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_rank, use_container_width=True)
    with colB:
        st.dataframe(
            rank_disp[["Puesto", "Gestor", "Total_Puntos", "Cumplimiento_%", "Semaforo"]],
            use_container_width=True, hide_index=True
        )

    # Stacked bar — composición de puntos
    st.subheader("📊 Composición de Puntos por Gestor")
    puntos_melt = rank[["Gestor", "Puntos_Base", "Puntos_Diario", "Puntos_Crec"]].melt(
        id_vars="Gestor", var_name="Tipo", value_name="Puntos"
    )
    label_map = {
        "Puntos_Base":   "Base (Cuota)",
        "Puntos_Diario": "Diario (Extra)",
        "Puntos_Crec":   "Crecimiento"
    }
    puntos_melt["Tipo"] = puntos_melt["Tipo"].map(label_map)
    fig_stack = px.bar(
        puntos_melt, x="Gestor", y="Puntos", color="Tipo",
        barmode="stack", text_auto=True,
        color_discrete_map={
            "Base (Cuota)":   "#4C78A8",
            "Diario (Extra)": "#F58518",
            "Crecimiento":    "#54A24B",
        }
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    # Semáforo
    colS, colE = st.columns(2)
    with colS:
        st.subheader("🚦 Estado de Gestores")
        sem = df_gestor["Semaforo"].value_counts().reset_index()
        sem.columns = ["Estado", "Cantidad"]
        fig_pie = px.pie(sem, names="Estado", values="Cantidad",
                         color="Estado",
                         color_discrete_map={"🟢 Verde": "#54A24B", "🟡 Amarillo": "#F4D03F", "🔴 Rojo": "#E45756"})
        st.plotly_chart(fig_pie, use_container_width=True)

    with colE:
        st.subheader("📋 Detalle Ejecutivo")
        st.dataframe(
            df_gestor[[
                "Gestor", "Departamento", "Venta", "Cuota",
                "Cumplimiento_%", "Puntos_Base", "Puntos_Diario",
                "Puntos_Crec", "Total_Puntos", "Semaforo"
            ]].sort_values("Total_Puntos", ascending=False),
            use_container_width=True, hide_index=True
        )

# ============================================================================
# TAB 2 — DETALLE POR PRODUCTO
# ============================================================================
with tab2:
    st.title("📦 Detalle por Producto")

    if "Producto" not in df_f.columns:
        st.warning("El dataset no contiene columna 'Producto'. Agrega esa columna y vuelve a subir el archivo.")
        st.stop()

    PRODUCTOS_ORDEN = ["Prepago", "Porta Pre", "Postpago", "OSS"]

    # Filtro de gestor dentro de la pestaña
    g_opts = ["Todos"] + sorted(df_f["Gestor"].unique())
    gestor_prod = st.selectbox("👤 Filtrar por Gestor", g_opts, key="tab2_gestor")

    df_p = df_f.copy()
    if gestor_prod != "Todos":
        df_p = df_p[df_p["Gestor"] == gestor_prod]

    # Agrupado Gestor × Producto
    df_pa = (
        df_p
        .groupby(["Gestor", "Producto"])
        .agg(
            Venta        = ("Venta",        "sum"),
            Cuota        = ("Cuota",        "sum"),
            Total_Puntos = ("Total_Puntos", "sum"),
        )
        .reset_index()
    )
    df_pa["Cumplimiento_%"] = (df_pa["Venta"] / df_pa["Cuota"] * 100).round(1)
    df_pa["Semaforo"] = df_pa["Cumplimiento_%"].apply(
        lambda x: "🟢" if x >= 100 else ("🟡" if x >= 80 else "🔴")
    )
    # Ordenar productos
    df_pa["Producto"] = pd.Categorical(df_pa["Producto"], categories=PRODUCTOS_ORDEN, ordered=True)
    df_pa = df_pa.sort_values(["Gestor", "Producto"])

    # KPIs rápidos por producto (totales)
    st.subheader("📌 Resumen por Producto")
    prod_resumen = (
        df_p.groupby("Producto")
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
        .reset_index()
    )
    prod_resumen["Cumplimiento_%"] = (prod_resumen["Venta"] / prod_resumen["Cuota"] * 100).round(1)
    prod_resumen["Producto"] = pd.Categorical(prod_resumen["Producto"], categories=PRODUCTOS_ORDEN, ordered=True)
    prod_resumen = prod_resumen.sort_values("Producto")

    kp_cols = st.columns(len(prod_resumen))
    for i, row in enumerate(prod_resumen.itertuples()):
        emoji = "🟢" if row._4 >= 100 else ("🟡" if row._4 >= 80 else "🔴")
        kp_cols[i].metric(f"{emoji} {row.Producto}", f"{row._4:.1f}%", f"{int(row.Venta)} / {int(row.Cuota)}")

    st.markdown("---")

    # Tabla detallada
    st.subheader("📋 Tabla por Gestor y Producto")
    st.dataframe(
        df_pa[["Gestor", "Producto", "Venta", "Cuota", "Cumplimiento_%", "Total_Puntos", "Semaforo"]],
        use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # Gráfico de cumplimiento por producto
    st.subheader("📊 Cumplimiento % por Producto")

    if gestor_prod == "Todos":
        fig_prod = px.bar(
            df_pa, x="Producto", y="Cumplimiento_%",
            color="Gestor", barmode="group",
            text="Cumplimiento_%",
            title="Cumplimiento por Producto y Gestor",
        )
    else:
        color_map = {"🟢": "#54A24B", "🟡": "#F4D03F", "🔴": "#E45756"}
        fig_prod = px.bar(
            df_pa, x="Producto", y="Cumplimiento_%",
            color="Semaforo", text="Cumplimiento_%",
            title=f"Cumplimiento por Producto — {gestor_prod}",
            color_discrete_map=color_map,
        )

    fig_prod.add_hline(y=100, line_dash="dash", line_color="red",
                       annotation_text="Meta 100%", annotation_position="bottom right")
    fig_prod.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_prod, use_container_width=True)

    # Radar (gestor individual)
    if gestor_prod != "Todos":
        st.subheader(f"🎯 Radar de Cumplimiento — {gestor_prod}")
        productos_r = df_pa["Producto"].astype(str).tolist()
        valores_r   = df_pa["Cumplimiento_%"].tolist()
        # Cerrar el polígono
        fig_radar = go.Figure(go.Scatterpolar(
            r     = valores_r + [valores_r[0]],
            theta = productos_r + [productos_r[0]],
            fill  = "toself",
            name  = gestor_prod,
            line_color = "#4C78A8"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r     = [100] * (len(productos_r) + 1),
            theta = productos_r + [productos_r[0]],
            mode  = "lines",
            line  = dict(color="red", dash="dash"),
            name  = "Meta 100%"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(valores_r + [120])])),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Mapa de calor
    st.subheader("🌡️ Mapa de Calor — Cumplimiento por Gestor y Producto")
    pivot_data = df_pa.pivot(index="Gestor", columns="Producto", values="Cumplimiento_%").fillna(0)
    # Reordenar columnas según PRODUCTOS_ORDEN
    cols_presentes = [p for p in PRODUCTOS_ORDEN if p in pivot_data.columns]
    pivot_data = pivot_data[cols_presentes]

    fig_heat = px.imshow(
        pivot_data,
        text_auto=".1f",
        color_continuous_scale="RdYlGn",
        zmin=0, zmax=150,
        aspect="auto",
        title="% Cumplimiento por Gestor y Producto"
    )
    fig_heat.update_coloraxes(colorbar_title="% Cump.")
    st.plotly_chart(fig_heat, use_container_width=True)

    # Ventas vs Cuota por producto (side-by-side)
    st.subheader("📦 Ventas vs Cuota por Producto")
    vc_melt = df_pa.melt(
        id_vars=["Gestor", "Producto"],
        value_vars=["Venta", "Cuota"],
        var_name="Métrica", value_name="Valor"
    )
    fig_vc = px.bar(
        vc_melt, x="Producto", y="Valor",
        color="Métrica", barmode="group",
        facet_col="Gestor" if gestor_prod == "Todos" else None,
        text_auto=True,
        color_discrete_map={"Venta": "#4C78A8", "Cuota": "#BDBDBD"},
        title="Ventas vs Cuota" + (f" — {gestor_prod}" if gestor_prod != "Todos" else " — Todos los Gestores"),
    )
    st.plotly_chart(fig_vc, use_container_width=True)
