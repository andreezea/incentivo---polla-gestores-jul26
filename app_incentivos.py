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
# PIVOT HELPER — genera tabla con productos como columnas agrupadas
# ----------------------------------------------------------------------------
def build_pivot(df_src, index_col):
    """
    Retorna un DataFrame con MultiIndex de columnas:
      Producto → (Cuota | Ventas | Cumpl%)
    y filas según index_col (Departamento o Gestor).
    """
    grp = (
        df_src.groupby([index_col, "Producto"])
        .agg(Cuota=("Cuota", "sum"), Venta=("Venta", "sum"))
        .reset_index()
    )

    p_cuota = grp.pivot(index=index_col, columns="Producto", values="Cuota").reindex(columns=PRODUCTOS_ORDEN)
    p_venta = grp.pivot(index=index_col, columns="Producto", values="Venta").reindex(columns=PRODUCTOS_ORDEN)
    p_cumpl = (p_venta / p_cuota * 100).round(1)

    # Construir MultiIndex
    tuples = [(p, m) for p in PRODUCTOS_ORDEN for m in ["Cuota", "Ventas", "Cumpl%"]]
    midx   = pd.MultiIndex.from_tuples(tuples)

    result = pd.DataFrame(index=p_cuota.index, columns=midx)
    for p in PRODUCTOS_ORDEN:
        result[(p, "Cuota")]  = p_cuota[p].fillna(0).astype(int)
        result[(p, "Ventas")] = p_venta[p].fillna(0).astype(int)
        result[(p, "Cumpl%")] = p_cumpl[p].fillna(0).round(0).astype(int)

    result.index.name = index_col
    return result

def style_pivot(df):
    """Colorea las celdas Cumpl% según semáforo."""
    style = pd.DataFrame("", index=df.index, columns=df.columns)
    for p in PRODUCTOS_ORDEN:
        col = (p, "Cumpl%")
        if col in df.columns:
            for idx in df.index:
                v = df.loc[idx, col]
                try:
                    v = float(v)
                    if v >= 100:
                        style.loc[idx, col] = "background-color:#d4edda;color:#155724;font-weight:bold"
                    elif v >= 80:
                        style.loc[idx, col] = "background-color:#fff3cd;color:#856404;font-weight:bold"
                    else:
                        style.loc[idx, col] = "background-color:#f8d7da;color:#721c24;font-weight:bold"
                except (TypeError, ValueError):
                    pass
    return style

def show_pivot(df_src, index_col, titulo):
    """Muestra la tabla pivot con formato completo."""
    pv = build_pivot(df_src, index_col)

    # Formatear Cumpl% con símbolo %
    pv_display = pv.copy()
    for p in PRODUCTOS_ORDEN:
        pv_display[(p, "Cumpl%")] = pv[(p, "Cumpl%")].apply(lambda x: f"{round(x)}%")

    st.markdown(f"**{titulo}**")
    styled = pv_display.style.apply(style_pivot, axis=None)
    st.dataframe(styled, use_container_width=True)

# ----------------------------------------------------------------------------
# DATOS DEMO
# ----------------------------------------------------------------------------
def datos_demo():
    random.seed(42)
    gestores = ["Juan", "Ana", "Luis", "Maria", "Carlos", "Sofia"]
    deptos   = {
        "Juan":"Amazonas","Ana":"Cajamarca","Luis":"Huánuco",
        "Maria":"Junín","Carlos":"Loreto","Sofia":"San Martín"
    }

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
    xls       = pd.ExcelFile(archivo)
    df_raw    = pd.read_excel(xls, sheet_name="Mensual")
    df_diario = pd.read_excel(xls, sheet_name="Diario") if "Diario" in xls.sheet_names else pd.DataFrame()
else:
    df_raw, df_diario = datos_demo()
    st.sidebar.info("Usando datos de demo. Sube tu Excel con hojas **Mensual** y **Diario**.")

df = procesar(df_raw)

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

with st.sidebar.expander("ℹ️ Tabla de puntos"):
    st.markdown("**Cumplimiento**")
    st.dataframe(pd.DataFrame(BANDAS_CUMPLIMIENTO, columns=["Desde%","Hasta%","Pts"]), hide_index=True)
    st.markdown("**Crecimiento**")
    st.dataframe(pd.DataFrame(BANDAS_CRECIMIENTO, columns=["Desde%","Hasta%","Pts"]), hide_index=True)
    st.caption("+1 pt por cada venta sobre cuota diaria")

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
    p1.metric("📌 Puntos Base",        int(df_gestor["Puntos_Base"].sum()))
    p2.metric("📅 Puntos Diarios",     int(df_gestor["Puntos_Diario"].sum()))
    p3.metric("📈 Puntos Crecimiento", int(df_gestor["Puntos_Crec"].sum()))
    st.markdown("---")

    st.subheader("🥇 Top Performers")
    rank = df_gestor.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
    t_cols = st.columns(3)
    for i, row in enumerate(rank.head(3).itertuples()):
        t_cols[i].metric(
            f"{'🥇🥈🥉'[i]} {row.Gestor}", int(row.Total_Puntos),
            f"Base {int(row.Puntos_Base)} · Diario {int(row.Puntos_Diario)} · Crec {int(row.Puntos_Crec)}"
        )

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

    st.subheader("📊 Composición de Puntos por Gestor")
    melt = rank[["Gestor","Puntos_Base","Puntos_Diario","Puntos_Crec"]].melt(
        id_vars="Gestor", var_name="Tipo", value_name="Puntos")
    melt["Tipo"] = melt["Tipo"].map({"Puntos_Base":"Base (Cuota)",
                                      "Puntos_Diario":"Diario (Extra)",
                                      "Puntos_Crec":"Crecimiento"})
    fig_s = px.bar(melt, x="Gestor", y="Puntos", color="Tipo", barmode="stack", text_auto=True,
                   color_discrete_map={"Base (Cuota)":"#4C78A8","Diario (Extra)":"#F58518","Crecimiento":"#54A24B"})
    st.plotly_chart(fig_s, use_container_width=True)

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
# TAB 2 — DETALLE POR PRODUCTO
# ============================================================================
with tab2:
    st.title("📦 Detalle por Producto")

    if "Producto" not in df_f.columns:
        st.warning("El dataset no contiene columna 'Producto'.")
        st.stop()

    # ── Tabla por Departamento ────────────────────────────────────────────────
    st.subheader("🏢 Por Departamento")
    show_pivot(df_f, "Departamento", "")

    st.markdown("---")

    # ── Tabla por Gestor ──────────────────────────────────────────────────────
    st.subheader("👤 Por Gestor")
    show_pivot(df_f, "Gestor", "")

    st.markdown("---")

    # ── Gráfico y mapa de calor ───────────────────────────────────────────────
    st.subheader("📊 Cumplimiento % por Producto")

    df_pa = (
        df_f.groupby(["Gestor","Producto"])
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
        .reset_index()
    )
    df_pa["Cumplimiento_%"] = (df_pa["Venta"] / df_pa["Cuota"] * 100).round(1)

    vista_sel = st.radio("Agrupar por:", ["Departamento","Gestor"], horizontal=True)
    df_chart = (
        df_f.groupby([vista_sel, "Producto"])
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
        .reset_index()
    )
    df_chart["Cumplimiento_%"] = (df_chart["Venta"] / df_chart["Cuota"] * 100).round(1)

    fig_prod = px.bar(
        df_chart, x="Producto", y="Cumplimiento_%",
        color=vista_sel, barmode="group", text="Cumplimiento_%",
        category_orders={"Producto": PRODUCTOS_ORDEN}
    )
    fig_prod.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Meta 100%")
    fig_prod.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_prod, use_container_width=True)

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
        st.warning("No se encontró la hoja **Diario** en el Excel.")
        st.stop()

    # Filtro de producto para el tab
    prod_sel = st.selectbox("📦 Producto", ["Todos"] + PRODUCTOS_ORDEN, key="d_prod")

    df_d = df_diario.copy()
    if gestor_sel != "Todos": df_d = df_d[df_d["Gestor"] == gestor_sel]
    if depto_sel  != "Todos": df_d = df_d[df_d["Departamento"] == depto_sel]
    if prod_sel   != "Todos": df_d = df_d[df_d["Producto"] == prod_sel]

    # ── KPIs del último día (totales) ────────────────────────────────────────
    ultimo_dia = df_d["Fecha"].max()
    df_hoy_all = df_d[df_d["Fecha"] == ultimo_dia]
    v_hoy  = df_hoy_all["Venta_Dia"].sum()
    c_hoy  = df_hoy_all["CuotaDiaria"].sum()
    cp_hoy = (v_hoy / c_hoy * 100) if c_hoy else 0
    emoji_hoy = "🟢" if cp_hoy >= 100 else ("🟡" if cp_hoy >= 80 else "🔴")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📅 Último día",     str(ultimo_dia)[:10])
    k2.metric("Venta Total",       f"{v_hoy:.0f}")
    k3.metric("Cuota Total",       f"{c_hoy:.0f}")
    k4.metric(f"{emoji_hoy} Cumpl. del Día", f"{cp_hoy:.1f}%")

    st.markdown("---")

    # ── TABLA PIVOT: todos los gestores × productos (último día) ─────────────
    st.subheader(f"📋 Estado por Gestor — {str(ultimo_dia)[:10]}")

    df_hoy_base = df_diario[df_diario["Fecha"] == ultimo_dia].copy()
    if depto_sel  != "Todos": df_hoy_base = df_hoy_base[df_hoy_base["Departamento"] == depto_sel]
    if prod_sel   != "Todos": df_hoy_base = df_hoy_base[df_hoy_base["Producto"] == prod_sel]

    grp_h = (
        df_hoy_base.groupby(["Gestor","Producto"])
        .agg(Cuota=("CuotaDiaria","sum"), Venta=("Venta_Dia","sum"))
        .reset_index()
    )

    prods_presentes = [p for p in PRODUCTOS_ORDEN if p in grp_h["Producto"].unique()] if prod_sel == "Todos" else [prod_sel]

    p_cuota_h = grp_h.pivot(index="Gestor", columns="Producto", values="Cuota").reindex(columns=prods_presentes)
    p_venta_h = grp_h.pivot(index="Gestor", columns="Producto", values="Venta").reindex(columns=prods_presentes)
    p_cumpl_h = (p_venta_h / p_cuota_h * 100).round(1)

    tuples_h  = [(p, m) for p in prods_presentes for m in ["Cuota", "Ventas", "Cumpl%"]]
    midx_h    = pd.MultiIndex.from_tuples(tuples_h)
    pivot_h   = pd.DataFrame(index=p_cuota_h.index, columns=midx_h)
    pivot_h.index.name = "Gestor"

    for p in prods_presentes:
        pivot_h[(p, "Cuota")]  = p_cuota_h[p].fillna(0).round(0).astype(int)
        pivot_h[(p, "Ventas")] = p_venta_h[p].fillna(0).round(0).astype(int)
        pivot_h[(p, "Cumpl%")] = p_cumpl_h[p].fillna(0).round(0).astype(int)

    # Formatear % y aplicar color
    pivot_h_display = pivot_h.copy()
    for p in prods_presentes:
        pivot_h_display[(p, "Cumpl%")] = pivot_h[(p, "Cumpl%")].apply(lambda x: f"{x}%")

    def style_hoy(df):
        style = pd.DataFrame("", index=df.index, columns=df.columns)
        for p in prods_presentes:
            col = (p, "Cumpl%")
            if col in df.columns:
                for idx in df.index:
                    v = df.loc[idx, col]
                    try:
                        v = float(str(v).replace("%",""))
                        if v >= 100:
                            style.loc[idx, col] = "background-color:#d4edda;color:#155724;font-weight:bold"
                        elif v >= 80:
                            style.loc[idx, col] = "background-color:#fff3cd;color:#856404;font-weight:bold"
                        else:
                            style.loc[idx, col] = "background-color:#f8d7da;color:#721c24;font-weight:bold"
                    except (TypeError, ValueError):
                        pass
        return style

    st.dataframe(pivot_h_display.style.apply(style_hoy, axis=None), use_container_width=True)

    st.markdown("---")

    # ── Acumulado mes: línea real vs meta ────────────────────────────────────
    st.subheader("📈 Acumulado del Mes: Ventas vs Meta")

    df_dia_agg = (
        df_d.groupby("Fecha")
        .agg(Venta_Dia=("Venta_Dia","sum"), CuotaDiaria=("CuotaDiaria","sum"))
        .reset_index().sort_values("Fecha")
    )
    df_dia_agg["Venta_Acum"] = df_dia_agg["Venta_Dia"].cumsum()
    df_dia_agg["Cuota_Acum"] = df_dia_agg["CuotaDiaria"].cumsum()

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
    fig_acum.add_trace(go.Scatter(
        x=pd.concat([df_dia_agg["Fecha"], df_dia_agg["Fecha"][::-1]]).tolist(),
        y=pd.concat([df_dia_agg["Venta_Acum"], df_dia_agg["Cuota_Acum"][::-1]]).tolist(),
        fill="toself", fillcolor="rgba(76,120,168,0.1)",
        line=dict(color="rgba(255,255,255,0)"), showlegend=False, hoverinfo="skip"
    ))
    fig_acum.update_layout(xaxis_title="Fecha", yaxis_title="Unidades", legend=dict(orientation="h"))
    st.plotly_chart(fig_acum, use_container_width=True)

    # ── Barras diarias ────────────────────────────────────────────────────────
    st.subheader("📊 Ventas Diarias vs Cuota")

    df_dia_agg["Cumpl_Dia_%"] = (df_dia_agg["Venta_Dia"] / df_dia_agg["CuotaDiaria"] * 100).round(1)
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
