# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import random

st.set_page_config(page_title="Incentivo de Ventas", layout="wide", page_icon="🏆")

# ============================================================================
# PARÁMETROS — SISTEMA BASE
# ============================================================================
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

# ============================================================================
# PARÁMETROS — NUEVO MOTOR POR PRODUCTO
# ============================================================================
# 1. Puntos por cumplir cuota diaria (por producto, por día)
PTS_CUOTA_DIARIA = {
    "Prepago":  2,
    "Porta Pre": 3,
    "Postpago": 2,
    "OSS":      3,
}

# 5. Puntos por cada venta adicional sobre cuota diaria (solo si ya cumplió)
PTS_EXTRA_DIARIA = {
    "Prepago":  3,
    "Porta Pre": 4,
    "Postpago": 3,
    "OSS":      4,
}

PTS_CUOTA_SEMANAL = 10   # 2. Por semana cumplida
PTS_CUOTA_MENSUAL = 40   # 3. Por mes cumplido
PTS_MES_ANTERIOR  = 15   # 4. Por superar venta del mes anterior
PTS_UR            = 15   # 6. UR: Prepago >= 55% de su cuota mensual
UR_UMBRAL         = 0.55

# ============================================================================
# FUNCIONES — SISTEMA BASE
# ============================================================================
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
    """Calcula métricas y puntos base por fila (Gestor × Producto)."""
    df = df.copy()
    df["Cumplimiento_%"] = (df["Venta"] / df["Cuota"] * 100).round(1)
    df["Puntos_Base"]    = df["Cumplimiento_%"].apply(puntos_cumplimiento)

    if "VentaDiaria" in df.columns and "CuotaDiaria" in df.columns:
        df["Puntos_Diario"] = (
            (df["VentaDiaria"] - df["CuotaDiaria"]).clip(lower=0).round(0).astype(int)
        )
    else:
        df["Puntos_Diario"] = 0

    if "VentaMesAnterior" in df.columns:
        df["Crec_%"]      = ((df["Venta"] - df["VentaMesAnterior"]) / df["VentaMesAnterior"] * 100).round(1)
        df["Puntos_Crec"] = df["Crec_%"].apply(puntos_crecimiento)
    else:
        df["Crec_%"]      = 0.0
        df["Puntos_Crec"] = 0

    # Total_Puntos se completará después de merge con Puntos_Producto
    df["Total_Puntos"] = df["Puntos_Base"] + df["Puntos_Diario"] + df["Puntos_Crec"]

    df["Semaforo"] = df["Cumplimiento_%"].apply(
        lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
    )
    return df

# ============================================================================
# NUEVO MOTOR — calcular_puntos_producto()
# ============================================================================
def calcular_puntos_producto(df_mensual: pd.DataFrame, df_diario: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Puntos_Producto por Gestor × Producto.

    Reglas:
      1. PD_Diario   : puntos fijos por cada día donde Venta_Dia >= CuotaDiaria
      2. PD_Semanal  : 10 pts por cada semana donde Venta_semana >= CuotaDiaria × 5
      3. PD_Mensual  : 40 pts si Venta >= Cuota mensual
      4. PD_MesAnt   : 15 pts si Venta > VentaMesAnterior
      5. PD_Extra    : N pts por cada unidad adicional sobre cuota diaria (solo días cumplidos)
      6. PD_UR       : 15 pts si Prepago alcanza >= 55 % de su cuota mensual (fila Prepago)

    Retorna DataFrame con columnas:
      Gestor, Producto, PD_Diario, PD_Extra, PD_Semanal,
      PD_Mensual, PD_MesAnt, PD_UR, Puntos_Producto
    """
    filas = []

    for (gestor, producto), grp_m in df_mensual.groupby(["Gestor", "Producto"]):
        row       = grp_m.iloc[0]
        cuota_m   = float(row["Cuota"])
        venta_m   = float(row["Venta"])
        venta_ant = float(row.get("VentaMesAnterior", 0) or 0)
        cuota_d   = float(row.get("CuotaDiaria", cuota_m / 22) or cuota_m / 22)

        pts_dia_u   = PTS_CUOTA_DIARIA.get(producto, 2)
        pts_extra_u = PTS_EXTRA_DIARIA.get(producto, 3)

        pd_diario = pd_extra = pd_semanal = 0

        # ── Datos diarios ────────────────────────────────────────────────────
        if not df_diario.empty and "Gestor" in df_diario.columns:
            mask  = (df_diario["Gestor"] == gestor) & (df_diario["Producto"] == producto)
            grp_d = df_diario[mask].copy()

            if not grp_d.empty:
                cd_col = grp_d["CuotaDiaria"] if "CuotaDiaria" in grp_d.columns else cuota_d

                # 1. Días con cuota cumplida
                dias_ok   = grp_d["Venta_Dia"] >= cd_col
                pd_diario = int(dias_ok.sum()) * pts_dia_u

                # 5. Unidades extra (solo en días cumplidos)
                grp_d["_extra"] = (grp_d["Venta_Dia"] - cd_col).clip(lower=0)
                pd_extra = int(grp_d.loc[dias_ok, "_extra"].sum()) * pts_extra_u

                # 2. Cuota semanal (cuota diaria × 5 días hábiles)
                grp_d["_semana"] = grp_d["Fecha"].dt.isocalendar().week.astype(int)
                cuota_sem        = cuota_d * 5
                semanas_ok       = (grp_d.groupby("_semana")["Venta_Dia"].sum() >= cuota_sem).sum()
                pd_semanal       = int(semanas_ok) * PTS_CUOTA_SEMANAL

        # 3. Cuota mensual
        pd_mensual = PTS_CUOTA_MENSUAL if venta_m >= cuota_m else 0

        # 4. Mes anterior
        pd_mes_ant = PTS_MES_ANTERIOR if (venta_ant > 0 and venta_m > venta_ant) else 0

        total = pd_diario + pd_extra + pd_semanal + pd_mensual + pd_mes_ant

        filas.append({
            "Gestor":   gestor,
            "Producto": producto,
            "PD_Diario":  pd_diario,
            "PD_Extra":   pd_extra,
            "PD_Semanal": pd_semanal,
            "PD_Mensual": pd_mensual,
            "PD_MesAnt":  pd_mes_ant,
            "PD_UR":      0,           # se rellena abajo
            "Puntos_Producto": total,
        })

    if not filas:
        cols = ["Gestor","Producto","PD_Diario","PD_Extra","PD_Semanal",
                "PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto"]
        return pd.DataFrame(columns=cols)

    df_pts = pd.DataFrame(filas)

    # 6. UR: Prepago cumplimiento >= 55 % → 15 pts (asignado a la fila Prepago)
    prepago_m = df_mensual[df_mensual["Producto"] == "Prepago"][["Gestor","Cuota","Venta"]].copy()
    prepago_m["_cumpl_pre"] = prepago_m["Venta"] / prepago_m["Cuota"]
    ur_map = (
        prepago_m.set_index("Gestor")["_cumpl_pre"]
        .apply(lambda x: PTS_UR if x >= UR_UMBRAL else 0)
        .to_dict()
    )
    mask_pre = df_pts["Producto"] == "Prepago"
    df_pts.loc[mask_pre, "PD_UR"] = (
        df_pts.loc[mask_pre, "Gestor"].map(ur_map).fillna(0).astype(int)
    )
    df_pts.loc[mask_pre, "Puntos_Producto"] += df_pts.loc[mask_pre, "PD_UR"]

    return df_pts

# ============================================================================
# PIVOT HELPERS
# ============================================================================
def build_pivot(df_src, index_col):
    grp = (
        df_src.groupby([index_col, "Producto"])
        .agg(Cuota=("Cuota","sum"), Venta=("Venta","sum"))
        .reset_index()
    )
    p_cuota = grp.pivot(index=index_col, columns="Producto", values="Cuota").reindex(columns=PRODUCTOS_ORDEN)
    p_venta = grp.pivot(index=index_col, columns="Producto", values="Venta").reindex(columns=PRODUCTOS_ORDEN)
    p_cumpl = (p_venta / p_cuota * 100).round(0)

    tuples = [(p, m) for p in PRODUCTOS_ORDEN for m in ["Cuota","Ventas","Cumpl%"]]
    midx   = pd.MultiIndex.from_tuples(tuples)
    result = pd.DataFrame(index=p_cuota.index, columns=midx)
    result.index.name = index_col

    for p in PRODUCTOS_ORDEN:
        result[(p,"Cuota")]  = p_cuota[p].fillna(0).astype(int)
        result[(p,"Ventas")] = p_venta[p].fillna(0).astype(int)
        result[(p,"Cumpl%")] = p_cumpl[p].fillna(0).astype(int)

    return result

def style_pivot(df):
    style = pd.DataFrame("", index=df.index, columns=df.columns)
    for p in PRODUCTOS_ORDEN:
        col = (p,"Cumpl%")
        if col not in df.columns:
            continue
        for idx in df.index:
            try:
                v = float(str(df.loc[idx, col]).replace("%",""))
                if v >= 100:
                    style.loc[idx, col] = "background-color:#d4edda;color:#155724;font-weight:bold"
                elif v >= 80:
                    style.loc[idx, col] = "background-color:#fff3cd;color:#856404;font-weight:bold"
                else:
                    style.loc[idx, col] = "background-color:#f8d7da;color:#721c24;font-weight:bold"
            except (TypeError, ValueError):
                pass
    return style

def show_pivot(df_src, index_col):
    pv = build_pivot(df_src, index_col)
    pv_disp = pv.copy()
    for p in PRODUCTOS_ORDEN:
        pv_disp[(p,"Cumpl%")] = pv[(p,"Cumpl%")].apply(lambda x: f"{x}%")
    st.dataframe(pv_disp.style.apply(style_pivot, axis=None), use_container_width=True)

# ============================================================================
# DATOS DEMO
# ============================================================================
def datos_demo():
    random.seed(42)
    gestores = ["Juan","Ana","Luis","Maria","Carlos","Sofia"]
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

    hoy    = date.today()
    dias   = [(hoy - timedelta(days=i)) for i in range(21, -1, -1)]
    rows_d = []
    for g in gestores:
        for p in PRODUCTOS_ORDEN:
            cd = random.uniform(3, 6)
            for d in dias:
                rows_d.append({
                    "Gestor": g, "Departamento": deptos[g],
                    "Producto": p,
                    "Fecha": d.strftime("%Y-%m-%d"),
                    "Venta_Dia": round(random.uniform(0, cd * 1.6), 1),
                    "CuotaDiaria": round(cd, 2),
                })
    df_diario = pd.DataFrame(rows_d)
    return df_mensual, df_diario

# ============================================================================
# CARGA DE DATOS
# ============================================================================
st.sidebar.title("⚙️ Configuración")
archivo = st.sidebar.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"])

def normalizar_columnas(df):
    """Quita asteriscos y espacios extra de los nombres de columna."""
    df.columns = [str(c).replace("*", "").strip() for c in df.columns]
    return df

def leer_hoja(xls, sheet_name):
    """
    Lee una hoja tolerando:
      - Formato simple: encabezados en fila 1
      - Plantilla con título decorativo: encabezados en fila 3, tooltips en fila 4
    También normaliza nombres de columna (quita asteriscos).
    """
    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
    # Detectar si los encabezados reales están más abajo
    primera_col = str(df.columns[0]).upper()
    if "GESTOR" not in primera_col and primera_col not in ("GESTOR", "NAN"):
        # Los encabezados están en fila 3 (índice 2)
        # La fila siguiente (índice 0 del df resultante) es el tooltip → se elimina
        df = pd.read_excel(xls, sheet_name=sheet_name, header=2).iloc[1:].reset_index(drop=True)
    return normalizar_columnas(df)

if archivo:
    xls       = pd.ExcelFile(archivo)
    df_raw    = leer_hoja(xls, "Mensual")
    df_diario = leer_hoja(xls, "Diario") if "Diario" in xls.sheet_names else pd.DataFrame()
else:
    df_raw, df_diario = datos_demo()
    st.sidebar.info("Usando datos de demo. Sube tu Excel con hojas **Mensual** y **Diario**.")

if not df_diario.empty:
    try:
        df_diario["Fecha"] = pd.to_datetime(df_diario["Fecha"])
    except Exception:
        st.sidebar.error(
            "⚠️ **Hoja Diario — error en columna Fecha.**\n\n"
            "El formato debe ser `YYYY-MM-DD` (ej: `2024-06-15`). "
            "Revisa que la columna Fecha contenga fechas reales, "
            "no nombres de producto ni de mes."
        )
        df_diario = pd.DataFrame()   # se ignora la hoja Diario hasta que se corrija

# ── Procesar base ────────────────────────────────────────────────────────────
df = procesar(df_raw)

# ── Calcular nuevo motor por producto ────────────────────────────────────────
df_pts_prod = calcular_puntos_producto(df_raw, df_diario)

# ── Merge y actualizar Total_Puntos ──────────────────────────────────────────
COLS_PROD = ["PD_Diario","PD_Extra","PD_Semanal","PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto"]
if not df_pts_prod.empty:
    df = df.merge(df_pts_prod[["Gestor","Producto"] + COLS_PROD],
                  on=["Gestor","Producto"], how="left")
else:
    for c in COLS_PROD:
        df[c] = 0

df[COLS_PROD] = df[COLS_PROD].fillna(0).astype(int)
df["Total_Puntos"] = (
    df["Puntos_Base"] + df["Puntos_Diario"] + df["Puntos_Crec"] + df["Puntos_Producto"]
)

# ============================================================================
# FILTROS GLOBALES
# ============================================================================
st.sidebar.markdown("---")
deptos_opts   = ["Todos"] + sorted(df["Departamento"].unique())
gestores_opts = ["Todos"] + sorted(df["Gestor"].unique())
depto_sel     = st.sidebar.selectbox("🏢 Departamento", deptos_opts)
gestor_sel    = st.sidebar.selectbox("👤 Gestor",       gestores_opts)

df_f = df.copy()
if depto_sel  != "Todos": df_f = df_f[df_f["Departamento"] == depto_sel]
if gestor_sel != "Todos": df_f = df_f[df_f["Gestor"]       == gestor_sel]

# Agrupado por gestor
AGG_COLS = {
    "Venta":           ("Venta",           "sum"),
    "Cuota":           ("Cuota",           "sum"),
    "VentaMesAnterior":("VentaMesAnterior","sum"),
    "Puntos_Base":     ("Puntos_Base",     "sum"),
    "Puntos_Diario":   ("Puntos_Diario",   "sum"),
    "Puntos_Crec":     ("Puntos_Crec",     "sum"),
    "Puntos_Producto": ("Puntos_Producto", "sum"),
    "PD_Diario":       ("PD_Diario",       "sum"),
    "PD_Extra":        ("PD_Extra",        "sum"),
    "PD_Semanal":      ("PD_Semanal",      "sum"),
    "PD_Mensual":      ("PD_Mensual",      "sum"),
    "PD_MesAnt":       ("PD_MesAnt",       "sum"),
    "PD_UR":           ("PD_UR",           "sum"),
    "Total_Puntos":    ("Total_Puntos",    "sum"),
}
df_gestor = df_f.groupby(["Gestor","Departamento"]).agg(**AGG_COLS).reset_index()
df_gestor["Cumplimiento_%"] = (df_gestor["Venta"] / df_gestor["Cuota"] * 100).round(1)
df_gestor["Semaforo"] = df_gestor["Cumplimiento_%"].apply(
    lambda x: "🟢 Verde" if x >= 100 else ("🟡 Amarillo" if x >= 80 else "🔴 Rojo")
)

# Sidebar — leyenda de puntos
with st.sidebar.expander("ℹ️ Tabla de puntos base"):
    st.dataframe(pd.DataFrame(BANDAS_CUMPLIMIENTO, columns=["Desde%","Hasta%","Pts"]), hide_index=True)
with st.sidebar.expander("🆕 Motor por producto"):
    st.markdown("""
| Regla | Pts |
|---|---|
| Cuota diaria Prepago/Postpago | 2 |
| Cuota diaria Porta Pre/OSS | 3 |
| Cuota semanal | 10 |
| Cuota mensual | 40 |
| Supera mes anterior | 15 |
| Extra Prepago/Postpago /ud | 3 |
| Extra Porta Pre/OSS /ud | 4 |
| UR Prepago ≥ 55 % cuota | 15 |
""")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "📦 Detalle por Producto", "📅 Seguimiento Diario"])

# ============================================================================
# TAB 1 — RESUMEN GENERAL
# ============================================================================
with tab1:
    st.title("🏆 Dashboard Gerencial de Incentivos")

    # ── KPIs principales ─────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gestores",              df_gestor["Gestor"].nunique())
    k2.metric("Cumplimiento Promedio", f"{df_gestor['Cumplimiento_%'].mean():.1f}%")
    k3.metric("Total Puntos",          int(df_gestor["Total_Puntos"].sum()))
    v_act = df_gestor["Venta"].sum(); v_ant = df_gestor["VentaMesAnterior"].sum()
    var   = ((v_act - v_ant) / v_ant * 100) if v_ant else 0
    k4.metric("Variación vs Mes Ant.", f"{var:.1f}%", delta=f"{var:.1f}%")

    st.markdown("---")

    # ── Desglose de puntos — sistema base ────────────────────────────────────
    st.subheader("📌 Sistema Base")
    b1, b2, b3 = st.columns(3)
    b1.metric("Puntos Base (Cuota)",       int(df_gestor["Puntos_Base"].sum()))
    b2.metric("Puntos Diarios (extra ud)", int(df_gestor["Puntos_Diario"].sum()))
    b3.metric("Puntos Crecimiento",        int(df_gestor["Puntos_Crec"].sum()))

    # ── Desglose de puntos — nuevo motor ─────────────────────────────────────
    st.subheader("🆕 Motor por Producto")
    n1, n2, n3, n4, n5, n6 = st.columns(6)
    n1.metric("Diario",   int(df_gestor["PD_Diario"].sum()))
    n2.metric("Extra",    int(df_gestor["PD_Extra"].sum()))
    n3.metric("Semanal",  int(df_gestor["PD_Semanal"].sum()))
    n4.metric("Mensual",  int(df_gestor["PD_Mensual"].sum()))
    n5.metric("Mes Ant.", int(df_gestor["PD_MesAnt"].sum()))
    n6.metric("UR",       int(df_gestor["PD_UR"].sum()))

    st.markdown("---")

    # ── Top 3 ────────────────────────────────────────────────────────────────
    st.subheader("🥇 Top Performers")
    rank = df_gestor.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
    t_cols = st.columns(3)
    for i, row in enumerate(rank.head(3).itertuples()):
        t_cols[i].metric(
            f"{'🥇🥈🥉'[i]} {row.Gestor}", int(row.Total_Puntos),
            f"Base {int(row.Puntos_Base)} · Motor {int(row.Puntos_Producto)}"
        )

    # ── Ranking ──────────────────────────────────────────────────────────────
    st.subheader("🏆 Ranking General")
    rank_disp = rank.copy()
    rank_disp.insert(0, "Puesto", range(1, len(rank_disp)+1))
    colA, colB = st.columns([2,1])
    with colA:
        fig_r = px.bar(
            rank.sort_values("Total_Puntos"), x="Total_Puntos", y="Gestor",
            orientation="h", text="Total_Puntos",
            color="Total_Puntos", color_continuous_scale="Blues"
        )
        fig_r.update_traces(textposition="outside")
        fig_r.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_r, use_container_width=True)
    with colB:
        st.dataframe(
            rank_disp[["Puesto","Gestor","Total_Puntos","Puntos_Producto","Cumplimiento_%","Semaforo"]],
            use_container_width=True, hide_index=True
        )

    # ── Stacked bar: composición total de puntos ──────────────────────────────
    st.subheader("📊 Composición de Puntos por Gestor")
    comp_cols = {
        "Base (Cuota)":    "Puntos_Base",
        "Diario Base":     "Puntos_Diario",
        "Crecimiento":     "Puntos_Crec",
        "Motor · Diario":  "PD_Diario",
        "Motor · Extra":   "PD_Extra",
        "Motor · Semanal": "PD_Semanal",
        "Motor · Mensual": "PD_Mensual",
        "Motor · Mes Ant": "PD_MesAnt",
        "Motor · UR":      "PD_UR",
    }
    melt_rows = []
    for label, col in comp_cols.items():
        for _, row in rank.iterrows():
            melt_rows.append({"Gestor": row["Gestor"], "Tipo": label, "Puntos": int(row[col])})
    df_melt = pd.DataFrame(melt_rows)

    fig_s = px.bar(
        df_melt, x="Gestor", y="Puntos", color="Tipo", barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_s, use_container_width=True)

    # ── Detalle motor por producto (tabla expandible) ─────────────────────────
    with st.expander("🔍 Desglose Motor por Producto — tabla completa"):
        cols_show = ["Gestor","Producto","PD_Diario","PD_Extra","PD_Semanal",
                     "PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto","Total_Puntos"]
        st.dataframe(
            df_f[cols_show].sort_values(["Gestor","Producto"]),
            use_container_width=True, hide_index=True
        )

    # ── Semáforo ──────────────────────────────────────────────────────────────
    colS, colE = st.columns(2)
    with colS:
        st.subheader("🚦 Estado")
        sem = df_gestor["Semaforo"].value_counts().reset_index()
        sem.columns = ["Estado","Cantidad"]
        fig_pie = px.pie(sem, names="Estado", values="Cantidad", color="Estado",
                         color_discrete_map={"🟢 Verde":"#54A24B","🟡 Amarillo":"#F4D03F","🔴 Rojo":"#E45756"})
        st.plotly_chart(fig_pie, use_container_width=True)
    with colE:
        st.subheader("📋 Detalle Ejecutivo")
        st.dataframe(
            df_gestor[[
                "Gestor","Departamento","Venta","Cuota","Cumplimiento_%",
                "Puntos_Base","Puntos_Diario","Puntos_Crec",
                "Puntos_Producto","Total_Puntos","Semaforo"
            ]].sort_values("Total_Puntos", ascending=False),
            use_container_width=True, hide_index=True
        )

# ============================================================================
# TAB 2 — DETALLE POR PRODUCTO
# ============================================================================
with tab2:
    st.title("📦 Detalle por Producto")

    if "Producto" not in df_f.columns:
        st.warning("El dataset no contiene columna 'Producto'.")
        st.stop()

    st.subheader("🏢 Por Departamento")
    show_pivot(df_f, "Departamento")

    st.markdown("---")

    st.subheader("👤 Por Gestor")
    show_pivot(df_f, "Gestor")

    st.markdown("---")

    # ── Gráficos ──────────────────────────────────────────────────────────────
    st.subheader("📊 Cumplimiento % por Producto")
    vista_sel = st.radio("Agrupar por:", ["Departamento","Gestor"], horizontal=True)
    df_chart  = (
        df_f.groupby([vista_sel,"Producto"])
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
        .reset_index()
    )
    df_chart["Cumplimiento_%"] = (df_chart["Venta"] / df_chart["Cuota"] * 100).round(1)
    fig_prod = px.bar(
        df_chart, x="Producto", y="Cumplimiento_%", color=vista_sel,
        barmode="group", text="Cumplimiento_%",
        category_orders={"Producto": PRODUCTOS_ORDEN}
    )
    fig_prod.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Meta 100%")
    fig_prod.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    st.plotly_chart(fig_prod, use_container_width=True)

    st.subheader("🌡️ Mapa de Calor — Cumplimiento")
    df_pa = (
        df_f.groupby(["Gestor","Producto"])
        .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
        .reset_index()
    )
    df_pa["Cumplimiento_%"] = (df_pa["Venta"] / df_pa["Cuota"] * 100).round(1)
    pivot_heat = df_pa.pivot(index="Gestor", columns="Producto", values="Cumplimiento_%").fillna(0)
    cols_ok    = [p for p in PRODUCTOS_ORDEN if p in pivot_heat.columns]
    fig_heat   = px.imshow(pivot_heat[cols_ok], text_auto=".0f",
                            color_continuous_scale="RdYlGn", zmin=0, zmax=150, aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Puntos Producto por gestor y producto ────────────────────────────────
    st.subheader("🆕 Puntos Motor por Gestor y Producto")
    df_motor = df_f.groupby(["Gestor","Producto"]).agg(
        PD_Diario=("PD_Diario","sum"), PD_Extra=("PD_Extra","sum"),
        PD_Semanal=("PD_Semanal","sum"), PD_Mensual=("PD_Mensual","sum"),
        PD_MesAnt=("PD_MesAnt","sum"), PD_UR=("PD_UR","sum"),
        Puntos_Producto=("Puntos_Producto","sum")
    ).reset_index()
    st.dataframe(df_motor, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3 — SEGUIMIENTO DIARIO
# ============================================================================
with tab3:
    st.title("📅 Seguimiento Diario de Ventas")

    if df_diario.empty:
        st.warning("No se encontró la hoja **Diario** en el Excel.")
        st.stop()

    prod_sel = st.selectbox("📦 Producto", ["Todos"] + PRODUCTOS_ORDEN, key="d_prod")

    df_d = df_diario.copy()
    if gestor_sel != "Todos": df_d = df_d[df_d["Gestor"] == gestor_sel]
    if depto_sel  != "Todos": df_d = df_d[df_d["Departamento"] == depto_sel]
    if prod_sel   != "Todos": df_d = df_d[df_d["Producto"] == prod_sel]

    # KPIs del último día
    ultimo_dia  = df_d["Fecha"].max()
    df_hoy_all  = df_d[df_d["Fecha"] == ultimo_dia]
    v_hoy = df_hoy_all["Venta_Dia"].sum()
    c_hoy = df_hoy_all["CuotaDiaria"].sum()
    cp_hoy = (v_hoy / c_hoy * 100) if c_hoy else 0
    emoji_hoy = "🟢" if cp_hoy >= 100 else ("🟡" if cp_hoy >= 80 else "🔴")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📅 Último día",    str(ultimo_dia)[:10])
    k2.metric("Venta Total",      f"{v_hoy:.0f}")
    k3.metric("Cuota Total",      f"{c_hoy:.0f}")
    k4.metric(f"{emoji_hoy} Cumpl. del Día", f"{cp_hoy:.0f}%")

    st.markdown("---")

    # ── Tabla pivot gestores × productos (último día) ─────────────────────────
    st.subheader(f"📋 Estado por Gestor — {str(ultimo_dia)[:10]}")

    df_hoy_base = df_diario[df_diario["Fecha"] == ultimo_dia].copy()
    if depto_sel  != "Todos": df_hoy_base = df_hoy_base[df_hoy_base["Departamento"] == depto_sel]
    if prod_sel   != "Todos": df_hoy_base = df_hoy_base[df_hoy_base["Producto"] == prod_sel]

    grp_h = (
        df_hoy_base.groupby(["Gestor","Producto"])
        .agg(Cuota=("CuotaDiaria","sum"), Venta=("Venta_Dia","sum"))
        .reset_index()
    )
    prods_h = [p for p in PRODUCTOS_ORDEN if p in grp_h["Producto"].unique()] \
              if prod_sel == "Todos" else [prod_sel]

    p_c = grp_h.pivot(index="Gestor", columns="Producto", values="Cuota").reindex(columns=prods_h)
    p_v = grp_h.pivot(index="Gestor", columns="Producto", values="Venta").reindex(columns=prods_h)
    p_k = (p_v / p_c * 100).round(0)

    tuples_h = [(p, m) for p in prods_h for m in ["Cuota","Ventas","Cumpl%"]]
    pivot_h  = pd.DataFrame(index=p_c.index,
                             columns=pd.MultiIndex.from_tuples(tuples_h))
    pivot_h.index.name = "Gestor"
    for p in prods_h:
        pivot_h[(p,"Cuota")]  = p_c[p].fillna(0).round(0).astype(int)
        pivot_h[(p,"Ventas")] = p_v[p].fillna(0).round(0).astype(int)
        pivot_h[(p,"Cumpl%")] = p_k[p].fillna(0).astype(int)

    pivot_h_disp = pivot_h.copy()
    for p in prods_h:
        pivot_h_disp[(p,"Cumpl%")] = pivot_h[(p,"Cumpl%")].apply(lambda x: f"{x}%")

    def style_hoy(df):
        style = pd.DataFrame("", index=df.index, columns=df.columns)
        for p in prods_h:
            col = (p,"Cumpl%")
            if col not in df.columns:
                continue
            for idx in df.index:
                try:
                    v = float(str(df.loc[idx, col]).replace("%",""))
                    if v >= 100:
                        style.loc[idx, col] = "background-color:#d4edda;color:#155724;font-weight:bold"
                    elif v >= 80:
                        style.loc[idx, col] = "background-color:#fff3cd;color:#856404;font-weight:bold"
                    else:
                        style.loc[idx, col] = "background-color:#f8d7da;color:#721c24;font-weight:bold"
                except (TypeError, ValueError):
                    pass
        return style

    st.dataframe(pivot_h_disp.style.apply(style_hoy, axis=None), use_container_width=True)

    st.markdown("---")

    # ── Acumulado mes ─────────────────────────────────────────────────────────
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
        x=df_dia_agg["Fecha"], y=df_dia_agg["Venta_Dia"], name="Venta Día",
        marker_color=df_dia_agg["Cumpl_Dia_%"].apply(
            lambda x: "#54A24B" if x >= 100 else ("#F4D03F" if x >= 80 else "#E45756"))
    ))
    fig_bar.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["CuotaDiaria"],
        mode="lines", name="Cuota Día", line=dict(color="red", dash="dot", width=2)
    ))
    fig_bar.update_layout(xaxis_title="Fecha", yaxis_title="Unidades", legend=dict(orientation="h"))
    st.plotly_chart(fig_bar, use_container_width=True)
