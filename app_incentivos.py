# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import random

st.set_page_config(page_title="Incentivo de Ventas", layout="wide", page_icon="🏆")

# ----------------------------------------------------------------------------
# PARÁMETROS
# ----------------------------------------------------------------------------
PRODUCTOS_ORDEN = ["Prepago", "Porta Pre", "Postpago", "OSS"]

BANDAS_CUMPLIMIENTO = [
    (0,    79.999,  0),
    (80,   99.999,  1),
    (100, 109.999,  2),
    (110, 129.999,  4),
    (130, 149.999,  6),
    (150, 179.999,  8),
    (180,  1e12,   12),
]

BANDAS_CRECIMIENTO = [
    (20,   1e12,   3),
    (10,  19.999,  2),
    (5,    9.999,  1),
    (-1e12, 4.999, 0),
]

# ----------------------------------------------------------------------------
# FUNCIONES — CÁLCULO
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
    df["Cumplimiento_%"] = (df["Venta"] / df["Cuota"] * 100).round(1)
    df["Puntos_Base"]    = df["Cumplimiento_%"].apply(puntos_cumplimiento)

    if "VentaDiaria" in df.columns and "CuotaDiaria" in df.columns:
        df["Puntos_Diario"] = (df["VentaDiaria"] - df["CuotaDiaria"]).clip(lower=0).round(0).astype(int)
    else:
        df["Puntos_Diario"] = 0

    if "VentaMesAnterior" in df.columns:
        df["Crec_%"]      = ((df["Venta"] - df["VentaMesAnterior"]) / df["VentaMesAnterior"] * 100).round(1)
        df["Puntos_Crec"] = df["Crec_%"].apply(puntos_crecimiento)
    else:
        df["Crec_%"]      = 0.0
        df["Puntos_Crec"] = 0

    df["Total_Puntos"] = df["Puntos_Base"] + df["Puntos_Diario"] + df["Puntos_Crec"]
    df["Semaforo"]     = df["Cumplimiento_%"].apply(
        lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
    )
    return df

# ----------------------------------------------------------------------------
# DATOS DEMO
# ----------------------------------------------------------------------------
def datos_demo():
    random.seed(42)
    gestores = ["Juan", "Ana", "Luis", "Maria"]
    deptos   = {"Juan": "Lima", "Ana": "Cusco", "Luis": "Lima", "Maria": "Cusco"}

    # -- Hoja Mensual --
    rows = []
    for g in gestores:
        for p in PRODUCTOS_ORDEN:
            cuota     = random.randint(80, 120)
            venta     = random.randint(60, 180)
            venta_ant = random.randint(50, 150)
            cuota_d   = round(cuota / 22, 2)
            venta_d   = round(venta / 22 * random.uniform(0.7, 1.4), 2)
            rows.append({
                "Gestor": g, "Departamento": deptos[g], "Mes": "Junio",
                "Producto": p, "Cuota": cuota, "Venta": venta,
                "VentaMesAnterior": venta_ant,
                "CuotaDiaria": cuota_d, "VentaDiaria": venta_d,
            })
    df_mensual = pd.DataFrame(rows)

    # -- Hoja Diario: últimos 22 días hábiles --
    hoy   = date.today()
    dias  = [(hoy - timedelta(days=i)) for i in range(21, -1, -1)]
    rows_d = []
    for g in gestores:
        for p in PRODUCTOS_ORDEN:
            cuota_d = random.uniform(3, 6)
            for d in dias:
                rows_d.append({
                    "Gestor": g, "Departamento": deptos[g],
                    "Producto": p,
                    "Fecha": d.strftime("%Y-%m-%d"),
                    "Venta_Dia": round(random.uniform(0, cuota_d * 1.6), 1),
                    "CuotaDiaria": round(cuota_d, 2),
                })
    df_diario = pd.DataFrame(rows_d)
    return df_mensual, df_diario

# ----------------------------------------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuración")
archivo = st.sidebar.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"])

if archivo:
    xls        = pd.ExcelFile(archivo)
    df_raw     = pd.read_excel(xls, sheet_name="Mensual")
    df_diario  = pd.read_excel(xls, sheet_name="Diario") if "Diario" in xls.sheet_names else pd.DataFrame()
else:
    df_raw, df_diario = datos_demo()
    st.sidebar.info("Usando datos de demo. Sube tu Excel con hojas **Mensual** y **Diario**.")

df = procesar(df_raw)

# Normalizar fechas
if not df_diario.empty:
    df_diario["Fecha"] = pd.to_datetime(df_diario["Fecha"])

# ----------------------------------------------------------------------------
# FILTROS GLOBALES
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")
deptos_opts   = ["Todos"] + sorted(df["Departamento"].unique())
gestores_opts = ["Todos"] + sorted(df["Gestor"].unique())
depto_sel     = st.sidebar.selectbox("🏢 Departamento", deptos_opts)
gestor_sel    = st.sidebar.selectbox("👤 Gestor",       gestores_opts)

df_f = df.copy()
if depto_sel  != "Todos": df_f = df_f[df_f["Departamento"] == depto_sel]
if gestor_sel != "Todos": df_f = df_f[df_f["Gestor"]       == gestor_sel]

# Agrupado por gestor
df_gestor = (
    df_f.groupby(["Gestor", "Departamento"])
    .agg(
        Venta=("Venta","sum"), Cuota=("Cuota","sum"),
        VentaMesAnterior=("VentaMesAnterior","sum"),
        Puntos_Base=("Puntos_Base","sum"),
        Puntos_Diario=("Puntos_Diario","sum"),
        Puntos_Crec=("Puntos_Crec","sum"),
        Total_Puntos=("Total_Puntos","sum"),
    ).reset_index()
)
df_gestor["Cumplimiento_%"] = (df_gestor["Venta"] / df_gestor["Cuota"] * 100).round(1)
df_gestor["Semaforo"] = df_gestor["Cumplimiento_%"].apply(
    lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
)

# Leyenda de puntos
with st.sidebar.expander("ℹ️ Tabla de puntos"):
    st.markdown("**Cumplimiento de cuota**")
    st.dataframe(pd.DataFrame(BANDAS_CUMPLIMIENTO, columns=["Desde %","Hasta %","Pts"]), hide_index=True)
    st.markdown("**Crecimiento vs mes ant.**")
    st.dataframe(pd.DataFrame(BANDAS_CRECIMIENTO, columns=["Desde %","Hasta %","Pts"]), hide_index=True)
    st.markdown("**Diario:** +1 pt por cada venta sobre cuota diaria")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "📦 Detalle por Producto", "📅 Seguimiento Diario"])

# ============================================================================
# TAB 1 — RESUMEN GENERAL
# ============================================================================
with tab1:
    st.title("🏆 Dashboard Gerencial de Incentivos")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gestores",              df_gestor["Gestor"].nunique())
    k2.metric("Cumplimiento Promedio", f"{df_gestor['Cumplimiento_%'].mean():.1f}%")
    k3.metric("Total Puntos",          int(df_gestor["Total_Puntos"].sum()))
    v_act = df_gestor["Venta"].sum(); v_ant = df_gestor["VentaMesAnterior"].sum()
    var   = ((v_act - v_ant) / v_ant * 100) if v_ant else 0
    k4.metric("Variación vs Mes Ant.", f"{var:.1f}%", delta=f"{var:.1f}%")

    st.markdown("---")

    p1, p2, p3 = st.columns(3)
    p1.metric("📌 Puntos Base",       int(df_gestor["Puntos_Base"].sum()))
    p2.metric("📅 Puntos Diarios",    int(df_gestor["Puntos_Diario"].sum()))
    p3.metric("📈 Puntos Crecimiento",int(df_gestor["Puntos_Crec"].sum()))

    st.markdown("---")

    # Top 3
    st.subheader("🥇 Top Performers")
    rank = df_gestor.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
    t_cols = st.columns(3)
    for i, row in enumerate(rank.head(3).itertuples()):
        t_cols[i].metric(
            f"{'🥇🥈🥉'[i]} {row.Gestor}", int(row.Total_Puntos),
            f"Base {int(row.Puntos_Base)} · Diario {int(row.Puntos_Diario)} · Crec {int(row.Puntos_Crec)}"
        )

    # Ranking
    st.subheader("🏆 Ranking General")
    rank_disp = rank.copy(); rank_disp.insert(0, "Puesto", range(1, len(rank_disp)+1))
    colA, colB = st.columns([2,1])
    with colA:
        fig_r = px.bar(rank.sort_values("Total_Puntos"), x="Total_Puntos", y="Gestor",
                       orientation="h", text="Total_Puntos",
                       color="Total_Puntos", color_continuous_scale="Blues")
        fig_r.update_traces(textposition="outside")
        fig_r.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_r, use_container_width=True)
    with colB:
        st.dataframe(rank_disp[["Puesto","Gestor","Total_Puntos","Cumplimiento_%","Semaforo"]],
                     use_container_width=True, hide_index=True)

    # Composición de puntos
    st.subheader("📊 Composición de Puntos por Gestor")
    melt = rank[["Gestor","Puntos_Base","Puntos_Diario","Puntos_Crec"]].melt(
        id_vars="Gestor", var_name="Tipo", value_name="Puntos")
    melt["Tipo"] = melt["Tipo"].map({"Puntos_Base":"Base (Cuota)",
                                      "Puntos_Diario":"Diario (Extra)",
                                      "Puntos_Crec":"Crecimiento"})
    fig_s = px.bar(melt, x="Gestor", y="Puntos", color="Tipo", barmode="stack", text_auto=True,
                   color_discrete_map={"Base (Cuota)":"#4C78A8","Diario (Extra)":"#F58518","Crecimiento":"#54A24B"})
    st.plotly_chart(fig_s, use_container_width=True)

    # Semáforo + tabla
    colS, colE = st.columns(2)
    with colS:
        st.subheader("🚦 Estado")
        sem = df_gestor["Semaforo"].value_counts().reset_index(); sem.columns=["Estado","Cantidad"]
        fig_pie = px.pie(sem, names="Estado", values="Cantidad",
                         color="Estado",
                         color_discrete_map={"🟢 Verde":"#54A24B","🟡 Amarillo":"#F4D03F","🔴 Rojo":"#E45756"})
        st.plotly_chart(fig_pie, use_container_width=True)
    with colE:
        st.subheader("📋 Detalle Ejecutivo")
        st.dataframe(
            df_gestor[["Gestor","Departamento","Venta","Cuota","Cumplimiento_%",
                        "Puntos_Base","Puntos_Diario","Puntos_Crec","Total_Puntos","Semaforo"]]
            .sort_values("Total_Puntos", ascending=False),
            use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2 — DETALLE POR PRODUCTO  (productos como columnas)
# ============================================================================
with tab2:
    st.title("📦 Detalle por Producto")

    if "Producto" not in df_f.columns:
        st.warning("El dataset no contiene columna 'Producto'.")
        st.stop()

    g_opts      = ["Todos"] + sorted(df_f["Gestor"].unique())
    gestor_prod = st.selectbox("👤 Filtrar por Gestor", g_opts, key="tab2_gestor")

    df_p = df_f.copy()
    if gestor_prod != "Todos":
        df_p = df_p[df_p["Gestor"] == gestor_prod]

    df_pa = (
        df_p.groupby(["Gestor","Producto"])
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"), Total_Puntos=("Total_Puntos","sum"))
        .reset_index()
    )
    df_pa["Cumplimiento_%"] = (df_pa["Venta"] / df_pa["Cuota"] * 100).round(1)

    # ── Tabla pivotada: productos como columnas ──────────────────────────────
    st.subheader("📋 Tabla de Resultados por Producto")

    def tabla_pivot_gestor(gestor_nombre):
        sub = df_pa[df_pa["Gestor"] == gestor_nombre].copy()
        sub["Producto"] = pd.Categorical(sub["Producto"], categories=PRODUCTOS_ORDEN, ordered=True)
        sub = sub.sort_values("Producto")

        filas = {"Indicador": ["Cuota", "Ventas", "Cumpl. %"]}
        for _, row in sub.iterrows():
            emoji = "🟢" if row["Cumplimiento_%"] >= 100 else ("🟡" if row["Cumplimiento_%"] >= 80 else "🔴")
            filas[f"{emoji} {row['Producto']}"] = [
                int(row["Cuota"]),
                int(row["Venta"]),
                f"{row['Cumplimiento_%']}%",
            ]
        return pd.DataFrame(filas)

    if gestor_prod == "Todos":
        for g in sorted(df_pa["Gestor"].unique()):
            st.markdown(f"**👤 {g}**")
            st.dataframe(tabla_pivot_gestor(g), use_container_width=True, hide_index=True)
            st.markdown("")
    else:
        st.dataframe(tabla_pivot_gestor(gestor_prod), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Gráfico de cumplimiento ───────────────────────────────────────────────
    st.subheader("📊 Cumplimiento % por Producto")
    if gestor_prod == "Todos":
        fig_prod = px.bar(df_pa, x="Producto", y="Cumplimiento_%", color="Gestor",
                          barmode="group", text="Cumplimiento_%",
                          category_orders={"Producto": PRODUCTOS_ORDEN})
    else:
        df_pa["SemaforoColor"] = df_pa["Cumplimiento_%"].apply(
            lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo"))
        fig_prod = px.bar(df_pa, x="Producto", y="Cumplimiento_%",
                          color="SemaforoColor", text="Cumplimiento_%",
                          title=f"Cumplimiento — {gestor_prod}",
                          color_discrete_map={"🟢 Verde":"#54A24B","🟡 Amarillo":"#F4D03F","🔴 Rojo":"#E45756"},
                          category_orders={"Producto": PRODUCTOS_ORDEN})
    fig_prod.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Meta 100%")
    fig_prod.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_prod, use_container_width=True)

    # ── Radar (gestor individual) ─────────────────────────────────────────────
    if gestor_prod != "Todos":
        st.subheader(f"🎯 Radar de Cumplimiento — {gestor_prod}")
        sub_r = df_pa[df_pa["Gestor"] == gestor_prod].copy()
        sub_r["Producto"] = pd.Categorical(sub_r["Producto"], categories=PRODUCTOS_ORDEN, ordered=True)
        sub_r = sub_r.sort_values("Producto")
        prods  = sub_r["Producto"].astype(str).tolist()
        vals   = sub_r["Cumplimiento_%"].tolist()
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=prods+[prods[0]], fill="toself",
            name=gestor_prod, line_color="#4C78A8"))
        fig_radar.add_trace(go.Scatterpolar(
            r=[100]*(len(prods)+1), theta=prods+[prods[0]], mode="lines",
            line=dict(color="red", dash="dash"), name="Meta 100%"))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(vals+[120])])))
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Mapa de calor ─────────────────────────────────────────────────────────
    st.subheader("🌡️ Mapa de Calor — Cumplimiento por Gestor y Producto")
    pivot_heat = df_pa.pivot(index="Gestor", columns="Producto", values="Cumplimiento_%").fillna(0)
    cols_ok    = [p for p in PRODUCTOS_ORDEN if p in pivot_heat.columns]
    fig_heat   = px.imshow(pivot_heat[cols_ok], text_auto=".1f",
                            color_continuous_scale="RdYlGn", zmin=0, zmax=150, aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)

# ============================================================================
# TAB 3 — SEGUIMIENTO DIARIO
# ============================================================================
with tab3:
    st.title("📅 Seguimiento Diario de Ventas")

    if df_diario.empty:
        st.warning("No se encontró la hoja **Diario** en el Excel. Sube el archivo con el formato correcto.")
        st.stop()

    # Filtros del tab
    c1, c2, c3 = st.columns(3)
    g_diario = c1.selectbox("👤 Gestor", ["Todos"]+sorted(df_diario["Gestor"].unique()), key="d_gestor")
    p_diario = c2.selectbox("📦 Producto", ["Todos"]+PRODUCTOS_ORDEN, key="d_prod")

    df_d = df_diario.copy()
    if g_diario != "Todos": df_d = df_d[df_d["Gestor"] == g_diario]
    if p_diario != "Todos": df_d = df_d[df_d["Producto"] == p_diario]

    # Agrupar por fecha
    df_dia_agg = (
        df_d.groupby("Fecha")
        .agg(Venta_Dia=("Venta_Dia","sum"), CuotaDiaria=("CuotaDiaria","sum"))
        .reset_index()
        .sort_values("Fecha")
    )
    df_dia_agg["Venta_Acum"]  = df_dia_agg["Venta_Dia"].cumsum()
    df_dia_agg["Cuota_Acum"]  = df_dia_agg["CuotaDiaria"].cumsum()
    df_dia_agg["Cumpl_Dia_%"] = (df_dia_agg["Venta_Dia"] / df_dia_agg["CuotaDiaria"] * 100).round(1)

    # KPIs del día (último registro)
    hoy_datos = df_dia_agg.iloc[-1]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📅 Último día",         str(hoy_datos["Fecha"])[:10])
    k2.metric("Venta del Día",         f"{hoy_datos['Venta_Dia']:.1f}")
    k3.metric("Cuota del Día",         f"{hoy_datos['CuotaDiaria']:.1f}")
    cumpl_hoy = hoy_datos["Cumpl_Dia_%"]
    emoji_hoy = "🟢" if cumpl_hoy >= 100 else ("🟡" if cumpl_hoy >= 80 else "🔴")
    k4.metric(f"{emoji_hoy} Cumpl. del Día", f"{cumpl_hoy:.1f}%")

    st.markdown("---")

    # Acumulado real vs meta
    st.subheader("📈 Acumulado: Ventas vs Meta")
    fig_acum = go.Figure()
    fig_acum.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["Venta_Acum"],
        mode="lines+markers", name="Ventas Acumuladas",
        line=dict(color="#4C78A8", width=2.5), marker=dict(size=5)
    ))
    fig_acum.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["Cuota_Acum"],
        mode="lines", name="Meta Acumulada",
        line=dict(color="red", dash="dash", width=2)
    ))
    # Área entre curvas
    fig_acum.add_trace(go.Scatter(
        x=pd.concat([df_dia_agg["Fecha"], df_dia_agg["Fecha"][::-1]]).tolist(),
        y=pd.concat([df_dia_agg["Venta_Acum"], df_dia_agg["Cuota_Acum"][::-1]]).tolist(),
        fill="toself", fillcolor="rgba(76,120,168,0.1)",
        line=dict(color="rgba(255,255,255,0)"), showlegend=False, hoverinfo="skip"
    ))
    fig_acum.update_layout(xaxis_title="Fecha", yaxis_title="Unidades", legend=dict(orientation="h"))
    st.plotly_chart(fig_acum, use_container_width=True)

    # Barras diarias con colores por semáforo
    st.subheader("📊 Ventas Diarias vs Cuota")
    df_dia_agg["Color"] = df_dia_agg["Cumpl_Dia_%"].apply(
        lambda x: "🟢 Sobre meta" if x >= 100 else ("🟡 Cerca" if x >= 80 else "🔴 Bajo meta"))
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_dia_agg["Fecha"], y=df_dia_agg["Venta_Dia"],
        name="Venta Día",
        marker_color=df_dia_agg["Cumpl_Dia_%"].apply(
            lambda x: "#54A24B" if x >= 100 else ("#F4D03F" if x >= 80 else "#E45756"))
    ))
    fig_bar.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["CuotaDiaria"],
        mode="lines", name="Cuota Día",
        line=dict(color="red", dash="dot", width=2)
    ))
    fig_bar.update_layout(xaxis_title="Fecha", yaxis_title="Unidades", legend=dict(orientation="h"))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Tabla de seguimiento por gestor (último día disponible)
    st.subheader("📋 Estado por Gestor — Último Día")
    ultimo_dia = df_diario["Fecha"].max()
    df_hoy = df_diario[df_diario["Fecha"] == ultimo_dia].copy()
    if g_diario != "Todos": df_hoy = df_hoy[df_hoy["Gestor"] == g_diario]
    if p_diario != "Todos": df_hoy = df_hoy[df_hoy["Producto"] == p_diario]

    df_hoy_agg = (
        df_hoy.groupby(["Gestor","Producto"])
        .agg(Venta_Dia=("Venta_Dia","sum"), CuotaDiaria=("CuotaDiaria","sum"))
        .reset_index()
    )
    df_hoy_agg["Cumpl_%"] = (df_hoy_agg["Venta_Dia"] / df_hoy_agg["CuotaDiaria"] * 100).round(1)
    df_hoy_agg["Estado"]  = df_hoy_agg["Cumpl_%"].apply(
        lambda x: "🟢 Sobre meta" if x >= 100 else ("🟡 Cerca" if x >= 80 else "🔴 Bajo meta"))

    # Pivot: productos como columnas (igual que Tab 2)
    st.markdown(f"**Fecha: {str(ultimo_dia)[:10]}**")

    for g in sorted(df_hoy_agg["Gestor"].unique()):
        sub = df_hoy_agg[df_hoy_agg["Gestor"] == g].copy()
        sub["Producto"] = pd.Categorical(sub["Producto"], categories=PRODUCTOS_ORDEN, ordered=True)
        sub = sub.sort_values("Producto")
        filas = {"Indicador": ["Cuota Día", "Venta Día", "Cumpl. %"]}
        for _, row in sub.iterrows():
            emoji = "🟢" if row["Cumpl_%"] >= 100 else ("🟡" if row["Cumpl_%"] >= 80 else "🔴")
            filas[f"{emoji} {row['Producto']}"] = [
                f"{row['CuotaDiaria']:.1f}",
                f"{row['Venta_Dia']:.1f}",
                f"{row['Cumpl_%']}%",
            ]
        st.markdown(f"**👤 {g}**")
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)
        st.markdown("")
