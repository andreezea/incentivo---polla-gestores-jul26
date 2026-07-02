# -*- coding: utf-8 -*-
import os
import io
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import base64
import random


# ── Logo corporativo ─────────────────────────────────────────────────────────
_LOGO_B64 = "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"
_logo_html = f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:58px;object-fit:contain;" alt="Fanero SAC">'



st.set_page_config(page_title="Incentivo Fanero Julio 2026", layout="wide", page_icon="🏆",
                   initial_sidebar_state="expanded")

# ============================================================================
# ESTILOS GLOBALES — Power BI look
# ============================================================================
st.markdown("""
<style>
/* ══════════════════════════════════════════════════
   PALETA PRO — Azul Corporativo + Verde/Amarillo/Rojo Rendimiento
   ══════════════════════════════════════════════════ */

/* ── Fondo general ── */
.stApp { background-color: #F0F4FA; }
.main .block-container { padding-top: 1rem; padding-bottom: 1rem; }

/* ── Ocultar menú y footer de Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ejecutivo oscuro ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2A5E 0%, #0A3A7A 60%, #0A4A8A 100%);
    border-right: 2px solid #C9982A;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div {
    background-color: rgba(255,255,255,0.10);
    border: 1px solid rgba(201,152,42,0.45);
    color: white;
    border-radius: 6px;
}
[data-testid="stSidebar"] .stExpander {
    background-color: rgba(255,255,255,0.07);
    border: 1px solid rgba(201,152,42,0.30);
    border-radius: 8px;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(201,152,42,0.18);
    border: 1px solid #C9982A;
    color: #FFD97A !important;
    border-radius: 6px;
    font-weight: 600;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(201,152,42,0.35);
}

/* ── TABS — alto contraste gerencial ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    background: linear-gradient(90deg, #0A2A5E 0%, #0A3A7A 100%);
    padding: 6px 8px;
    border-radius: 10px;
    margin-bottom: 16px;
    box-shadow: 0 3px 12px rgba(0,33,71,0.30);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    color: rgba(255,255,255,0.80) !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 9px 20px !important;
    background-color: transparent !important;
    border: none !important;
    letter-spacing: 0.2px;
    transition: all 0.15s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #FFD97A !important;
    background-color: rgba(201,152,42,0.15) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #C9982A 0%, #E8B84B 100%) !important;
    color: #0A2A5E !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 10px rgba(201,152,42,0.50) !important;
}

/* ── KPI cards ejecutivas — fondo azul corporativo, texto blanco ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0A2A5E 0%, #0B5ED7 100%);
    border-radius: 12px;
    padding: 18px 20px 14px 20px;
    box-shadow: 0 4px 18px rgba(0,33,71,0.30);
    border-left: 5px solid #C9982A;
    border-top: none;
    min-height: 90px;
}
[data-testid="metric-label"] > div {
    font-size: 11px !important;
    color: rgba(255,255,255,0.70) !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
[data-testid="metric-value"] > div {
    font-size: 30px !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
}
[data-testid="metric-delta"] > div {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: rgba(255,255,255,0.85) !important;
}

/* ── Títulos ── */
h1 { color: #0A2A5E !important; font-weight: 900 !important; letter-spacing: -0.8px; }
h2, h3 { color: #0A3A7A !important; font-weight: 700 !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,33,71,0.09);
    border: 1px solid #DDE4EE;
}

/* ── Subheader divisor gerencial ── */
.section-header {
    background: linear-gradient(90deg, #0A2A5E 0%, #0B5ED7 80%, #1565C0 100%);
    color: white !important;
    padding: 7px 18px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
    margin: 16px 0 10px 0;
    letter-spacing: 0.5px;
    border-left: 4px solid #C9982A;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: white;
    border-radius: 10px;
    border: 1px solid #DDE4EE;
    box-shadow: 0 1px 6px rgba(0,33,71,0.06);
}

/* ── Botón primario ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0A2A5E, #0B5ED7) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    box-shadow: 0 3px 10px rgba(0,33,71,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0A3A7A, #1565C0) !important;
    box-shadow: 0 4px 14px rgba(0,33,71,0.35) !important;
}

/* ── Transparentar wrappers de columna para que kpi_card sea visible ── */
[data-testid="column"] > div,
[data-testid="column"] .stMarkdown,
[data-testid="column"] .element-container,
[data-testid="stVerticalBlock"] > div.element-container {
    background: transparent !important;
}

/* ── Barra superior con logo ── */
.logo-topbar {
    display: flex;
    align-items: center;
    background: linear-gradient(90deg, #0A2A5E 0%, #0B5ED7 100%);
    padding: 8px 20px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0,33,71,0.25);
    border-bottom: 2px solid #C9982A;
}
.logo-topbar span {
    color: rgba(255,255,255,0.60);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-left: 14px;
    border-left: 1px solid rgba(255,255,255,0.25);
    padding-left: 14px;
}

/* ── Barra superior logo ── */
.logo-topbar {
    display:flex; align-items:center;
    background:linear-gradient(90deg,#0A2A5E 0%,#0B5ED7 100%);
    padding:8px 20px; border-radius:10px; margin-bottom:12px;
    box-shadow:0 3px 12px rgba(0,33,71,0.25);
    border-bottom:2px solid #C9982A;
}
.logo-topbar .logo-sep {
    color:rgba(255,255,255,0.55); font-size:11px; font-weight:600;
    letter-spacing:1.2px; text-transform:uppercase;
    margin-left:14px; border-left:1px solid rgba(255,255,255,0.20);
    padding-left:14px;
}

/* ── Dataframes — fondo gris humo, texto azul ── */
[data-testid="stDataFrame"] [data-testid="glideDataEditor"] {
    background-color: #F5F6FA !important;
}
[data-testid="stDataFrame"] .dvn-scroller,
[data-testid="stDataFrame"] canvas {
    background-color: #F5F6FA !important;
}
</style>
""", unsafe_allow_html=True)

# ── Paleta gerencial para gráficos ───────────────────────────────────────────
PALETA = [
    "#0A2A5E",  # Azul oscuro
    "#0B5ED7",  # Azul principal
    "#C9982A",  # Executive Gold
    "#198754",  # Verde rendimiento
    "#DC3545",  # Rojo rendimiento
    "#4A5FA8",  # Steel Blue
    "#2E8B8B",  # Teal
    "#7B4EA8",  # Corporate Purple
]

def subheader(texto):
    """Encabezado de sección estilo Power BI."""
    st.markdown(f'<div class="section-header">{texto}</div>', unsafe_allow_html=True)

def _kpi_html(label, value, delta=None, color="#0B5ED7", flex="1"):
    """Devuelve el HTML de una KPI card (sin renderizar)."""
    delta_html = ""
    if delta is not None:
        s = str(delta)
        is_pos = s.startswith("+") or (not s.startswith("-") and s not in ("", "0"))
        delta_html = (f'<p style="font-size:12px;color:{"#7DFFB3" if is_pos else "#FFB3B3"};'
                      f'font-weight:700;margin:4px 0 0 0;">{s}</p>')
    return (
        f'<div style="flex:{flex};min-width:0;'
        f'background:linear-gradient(135deg,#0A2A5E 0%,{color} 100%);'
        f'border-radius:12px;padding:18px 20px 14px 20px;'
        f'box-shadow:0 4px 18px rgba(0,33,71,0.30);'
        f'border-left:5px solid #C9982A;min-height:90px;margin-bottom:4px;">'
        f'<p style="font-size:11px;color:rgba(255,255,255,0.65);font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.8px;margin:0 0 6px 0;">{label}</p>'
        f'<p style="font-size:28px;color:#FFFFFF;font-weight:800;margin:0;line-height:1.1;">{value}</p>'
        f'{delta_html}</div>'
    )

def render_kpi_row(cards, gap="12px"):
    """Renderiza una fila de KPI cards en un solo bloque HTML con flexbox.
    cards: lista de dicts {label, value, delta (opt), color (opt), flex (opt)}
    Usa st.markdown() directo (no col.markdown) para evitar que el wrapper
    de columna de Streamlit tape el gradiente.
    """
    inner = "".join(
        _kpi_html(
            c["label"], c["value"],
            c.get("delta"), c.get("color","#0B5ED7"), c.get("flex","1")
        ) for c in cards
    )
    st.markdown(
        f'<div style="display:flex;gap:{gap};flex-wrap:wrap;margin-bottom:6px;">{inner}</div>',
        unsafe_allow_html=True
    )

def kpi_card(col, label, value, delta=None, color="#0B5ED7"):
    """Mantiene compatibilidad — delega a render_kpi_row con 1 sola tarjeta."""
    render_kpi_row([{"label":label,"value":value,"delta":delta,"color":color}])

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

def _cumpl_color(v):
    """Color solo del número según umbral gerencial."""
    try:
        n = float(str(v).replace("%",""))
    except (TypeError, ValueError):
        return "#0A2A5E"
    if n >= 97.5:
        return "#198754"   # verde
    elif n >= 93:
        return "#B45309"   # amarillo/ámbar
    else:
        return "#DC3545"   # rojo

def _pivot_to_html(pv, index_col, prods):
    """Renderiza un DataFrame MultiIndex como tabla HTML con estilo gerencial."""
    CELL = (
        "padding:7px 12px;border:1px solid #BFCDE0;"
        "color:#0A2A5E;font-size:12.5px;text-align:right;"
        "background:#F5F7FB;"
    )
    HEAD_TOP = (
        "padding:7px 12px;background:#0A2A5E;color:#FFFFFF;"
        "font-size:11px;font-weight:700;text-align:center;"
        "border:1px solid #1565C0;text-transform:uppercase;letter-spacing:0.5px;"
    )
    HEAD_SUB = (
        "padding:5px 10px;background:#0B5ED7;color:#FFFFFF;"
        "font-size:10.5px;font-weight:700;text-align:center;"
        "border:1px solid #1976D2;letter-spacing:0.3px;"
    )
    IDX_CELL = (
        "padding:7px 12px;border:1px solid #BFCDE0;"
        "color:#0A2A5E;font-weight:600;font-size:12.5px;"
        "background:#EBF0FA;text-align:left;"
    )

    rows_html = []
    # Fila 1: productos (span 3 cada uno) + celda índice
    header1 = f'<th style="{HEAD_TOP};text-align:left;" rowspan="2">{index_col}</th>'
    for p in prods:
        if p in [c[0] for c in pv.columns]:
            header1 += f'<th style="{HEAD_TOP}" colspan="3">{p}</th>'
    rows_html.append(f"<tr>{header1}</tr>")

    # Fila 2: sub-columnas
    header2 = ""
    for p in prods:
        if p in [c[0] for c in pv.columns]:
            for m in ["Cuota","Ventas","Cumpl%"]:
                header2 += f'<th style="{HEAD_SUB}">{m}</th>'
    rows_html.append(f"<tr>{header2}</tr>")

    # Filas de datos
    for idx in pv.index:
        cols_td = f'<td style="{IDX_CELL}">{idx}</td>'
        for p in prods:
            if p not in [c[0] for c in pv.columns]:
                continue
            cuota = pv.loc[idx, (p,"Cuota")]
            venta = pv.loc[idx, (p,"Ventas")]
            cumpl = pv.loc[idx, (p,"Cumpl%")]
            color = _cumpl_color(cumpl)
            cols_td += f'<td style="{CELL}">{int(cuota) if pd.notna(cuota) else "-"}</td>'
            cols_td += f'<td style="{CELL}">{int(venta) if pd.notna(venta) else "-"}</td>'
            cols_td += (
                f'<td style="{CELL}color:{color};font-weight:800;">' +
                f'{int(cumpl) if pd.notna(cumpl) else "-"}%</td>'
            )
        rows_html.append(f"<tr>{cols_td}</tr>")

    table = (
        '<div style="overflow-x:auto;border-radius:10px;border:1.5px solid #BFCDE0;' +
        'box-shadow:0 2px 8px rgba(10,42,94,0.09);margin-bottom:4px;">' +
        '<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif;">' +
        "<thead>" + "".join(rows_html[:2]) + "</thead>" +
        "<tbody>" + "".join(rows_html[2:]) + "</tbody>" +
        "</table></div>"
    )
    return table

def show_pivot(df_src, index_col):
    pv = build_pivot(df_src, index_col)
    prods = [p for p in PRODUCTOS_ORDEN if p in [c[0] for c in pv.columns]]
    st.markdown(_pivot_to_html(pv, index_col, prods), unsafe_allow_html=True)

def _build_tabla_regional(df_src, col_idx, label_idx, tabla_id):
    """
    Genera HTML de tabla con jerarquía Región → filas (dept o gestor),
    fila de total al final llamada 'Fanero'.
    Reutilizada por show_pivot_regional y show_pivot_gestor_regional.
    """
    avail = [p for p in PRODUCTOS_ORDEN if p in df_src["Producto"].unique()]
    if not avail:
        return None, 0

    # Pivots
    pv_item = build_pivot(df_src, col_idx)
    df_r    = df_src.copy()
    df_r["_Region"] = df_r["Departamento"].map(DEPTO_A_REGION).fillna("Otros")
    pv_reg  = build_pivot(df_r, "_Region")

    # Para el total Fanero
    df_tot       = df_src.copy()
    df_tot["_T"] = "Fanero"
    pv_tot       = build_pivot(df_tot, "_T")

    # Estilos
    CELL  = "padding:7px 11px;border:1px solid #BFCDE0;font-size:12.5px;text-align:right;background:#F5F7FB;"
    IDX   = "padding:7px 14px;border:1px solid #BFCDE0;font-size:12.5px;background:#EBF0FA;text-align:left;color:#0A2A5E;"
    REG   = "padding:9px 14px;border:1px solid #0A2A5E;font-size:13px;font-weight:800;color:#FFD97A;background:#0A2A5E;text-align:left;cursor:pointer;user-select:none;"
    REGC  = "padding:7px 11px;border:1px solid #0A2A5E;font-size:12.5px;text-align:right;background:#0A2A5E;color:#FFD97A;font-weight:700;"
    TOT   = "padding:9px 14px;border:2px solid #C9982A;font-size:13px;font-weight:800;color:#0A2A5E;background:#FFF3CD;text-align:left;"
    TOTC  = "padding:7px 11px;border:2px solid #C9982A;font-size:12.5px;text-align:right;background:#FFF3CD;color:#0A2A5E;font-weight:800;"
    HEAD1 = "padding:7px 12px;background:#0A2A5E;color:#FFF;font-size:11px;font-weight:700;text-align:center;border:1px solid #1565C0;text-transform:uppercase;letter-spacing:0.5px;"
    HEAD2 = "padding:5px 10px;background:#0B5ED7;color:#FFF;font-size:10.5px;font-weight:700;text-align:center;border:1px solid #1976D2;"

    # Cabecera
    h1 = f'<th style="{HEAD1};text-align:left" rowspan="2">{label_idx.upper()}</th>'
    h2 = ""
    for p in avail:
        h1 += f'<th style="{HEAD1}" colspan="3">{p}</th>'
        for m in ["Cuota", "Ventas", "Cumpl%"]:
            h2 += f'<th style="{HEAD2}">{m}</th>'
    thead = f"<thead><tr>{h1}</tr><tr>{h2}</tr></thead>"

    def _celdas(pv, ix, cel, modo):
        out = ""
        for p in avail:
            cu = pv.loc[ix, (p, "Cuota")]  if (p, "Cuota")  in pv.columns else 0
            ve = pv.loc[ix, (p, "Ventas")] if (p, "Ventas") in pv.columns else 0
            cm = pv.loc[ix, (p, "Cumpl%")] if (p, "Cumpl%") in pv.columns else 0
            try:   cm_n = float(str(cm).replace("%", ""))
            except: cm_n = 0
            clr = "#FFD97A" if modo == "region" else ("#C9982A" if modo == "total" else _cumpl_color(cm_n))
            out += f'<td style="{cel}">{int(cu) if pd.notna(cu) else "-"}</td>'
            out += f'<td style="{cel}">{int(ve) if pd.notna(ve) else "-"}</td>'
            out += f'<td style="{cel}color:{clr};font-weight:800;">{int(cm_n) if pd.notna(cm) else "-"}%</td>'
        return out

    tbody = "<tbody>"
    orden_regiones = [r for r in ["Oriente", "Centro", "Otros"] if r in pv_reg.index]
    n_filas = 0

    for region in orden_regiones:
        rid = f"{tabla_id}_{region.lower()}"
        reg_celdas = _celdas(pv_reg, region, REGC, "region")
        tbody += (
            f'<tr onclick="toggleRegion(\'{rid}\')" title="Clic para expandir/colapsar">'
            f'<td style="{REG}"><span id="ind-{rid}" style="margin-right:8px;font-size:14px;">▼</span>🌎 {region}</td>'
            f'{reg_celdas}</tr>'
        )
        # Filas hijas (departamentos o gestores de esa región)
        if col_idx == "Gestor":
            # gestores cuyo departamento pertenece a la región
            gest_region = sorted([
                g for g in pv_item.index
                if DEPTO_A_REGION.get(
                    df_src[df_src["Gestor"] == g]["Departamento"].iloc[0]
                    if not df_src[df_src["Gestor"] == g].empty else "", ""
                ) == region
                or (region == "Otros" and DEPTO_A_REGION.get(
                    df_src[df_src["Gestor"] == g]["Departamento"].iloc[0]
                    if not df_src[df_src["Gestor"] == g].empty else "", None
                ) is None)
            ])
            for item in gest_region:
                if item not in pv_item.index:
                    continue
                tbody += (
                    f'<tr class="deptrow-{rid}" style="display:table-row;">'
                    f'<td style="{IDX}">&nbsp;&nbsp;&nbsp;&nbsp;{item}</td>'
                    f'{_celdas(pv_item, item, CELL, "item")}</tr>'
                )
                n_filas += 1
        else:
            deptos_r = sorted(REGIONES.get(region, [
                d for d in pv_item.index
                if (DEPTO_A_REGION.get(d) == region)
                   or (region == "Otros" and d not in DEPTO_A_REGION)
            ]))
            for depto in deptos_r:
                if depto not in pv_item.index:
                    continue
                tbody += (
                    f'<tr class="deptrow-{rid}" style="display:table-row;">'
                    f'<td style="{IDX}">&nbsp;&nbsp;&nbsp;&nbsp;{depto}</td>'
                    f'{_celdas(pv_item, depto, CELL, "item")}</tr>'
                )
                n_filas += 1

    # ── Fila total Fanero ─────────────────────────────────────────────────────
    if "Fanero" in pv_tot.index:
        tot_celdas = _celdas(pv_tot, "Fanero", TOTC, "total")
        tbody += (
            f'<tr>'
            f'<td style="{TOT}">🏆 Fanero</td>'
            f'{tot_celdas}</tr>'
        )
    tbody += "</tbody>"

    js = f"""
    <script>
    var _exp_{tabla_id} = {{}};
    function toggleRegion(rid) {{
        var rows = document.querySelectorAll('.deptrow-' + rid);
        var ind  = document.getElementById('ind-' + rid);
        _exp_{tabla_id}[rid] = !_exp_{tabla_id}[rid];
        rows.forEach(function(r) {{
            r.style.display = _exp_{tabla_id}[rid] ? 'none' : 'table-row';
        }});
        ind.textContent = _exp_{tabla_id}[rid] ? '▶' : '▼';
    }}
    </script>
    """

    altura = 90 + len(orden_regiones) * 44 + n_filas * 38 + 50
    html = (
        '<div style="overflow-x:auto;border-radius:10px;border:1.5px solid #BFCDE0;'
        'box-shadow:0 2px 8px rgba(10,42,94,0.09);margin-bottom:4px;">'
        '<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif;">'
        + thead + tbody + '</table></div>' + js
    )
    return html, altura


def show_pivot_regional(df_src):
    """Tabla Por Departamento con regiones colapsables y fila Fanero."""
    import streamlit.components.v1 as components
    html, altura = _build_tabla_regional(df_src, "Departamento", "Departamento", "dept")
    if html:
        components.html(html, height=altura, scrolling=True)


def show_pivot_gestor_regional(df_src):
    """Tabla Por Gestor con regiones colapsables y fila Fanero."""
    import streamlit.components.v1 as components
    html, altura = _build_tabla_regional(df_src, "Gestor", "Gestor", "gest")
    if html:
        components.html(html, height=altura, scrolling=True)

# ============================================================================
# DATOS DEMO
# ============================================================================
# ============================================================================
# FUNCIONES — VENTAS SEMANALES Y PUNTOS ADICIONALES
# ============================================================================
def calcular_ventas_semanales(df_diario: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa df_diario por Gestor, Producto y semana del mes.
    Semana 1 = días 1-7, Semana 2 = 8-14, Semana 3 = 15-21, Semana 4 = 22+.
    Retorna columnas: Gestor, Departamento, Producto, Mes_Año, Semana_Mes,
                      Ventas_Semana, Cuota_Semana, Dias_Activos, Cumpl_Sem_%, Semaforo.
    """
    if df_diario.empty or "Fecha" not in df_diario.columns:
        return pd.DataFrame()
    df = df_diario.copy()
    df["Fecha"]      = pd.to_datetime(df["Fecha"])
    df["Semana_Mes"] = df["Fecha"].dt.day.apply(lambda d: (d - 1) // 7 + 1)
    df["Mes_Año"]    = df["Fecha"].dt.to_period("M").astype(str)
    dept_col = "Departamento" if "Departamento" in df.columns else None
    grp_cols = ["Gestor","Producto","Mes_Año","Semana_Mes"]
    if dept_col:
        grp_cols = ["Gestor","Departamento","Producto","Mes_Año","Semana_Mes"]
    sem = (df.groupby(grp_cols)
             .agg(
                 Ventas_Semana = ("Venta_Dia",   "sum"),
                 Cuota_Semana  = ("CuotaDiaria", "sum"),
                 Dias_Activos  = ("Venta_Dia",   "count"),
             ).reset_index())
    sem["Cumpl_Sem_%"] = (sem["Ventas_Semana"] /
                          sem["Cuota_Semana"].replace(0, 1) * 100).round(1)
    sem["Semaforo"] = sem["Cumpl_Sem_%"].apply(
        lambda x: "🟢" if x >= 100 else ("🟡" if x >= 80 else "🔴"))
    return sem

def calcular_puntos_adicionales(df_diario: pd.DataFrame,
                                df_raw: pd.DataFrame,
                                df_sem_ant: pd.DataFrame = None) -> tuple:
    """
    Puntos adicionales sobre el sistema base:
      • +1 punto por cada DÍA en que se supera la cuota diaria
      • +PTS_CUOTA_SEMANAL por cada SEMANA con cumplimiento ≥ 100 %
      • +PTS_MES_ANTERIOR si ventas de la semana N > ventas de la semana N del mes anterior
        Fuente preferida: hoja Semanal_MesAnt (Gestor × Producto × Semana × Venta_Semana)
        Fallback: VentaMesAnterior / 4 si no hay hoja semanal

    Retorna (df_resultado, df_semanal):
      df_resultado  → Gestor × Producto con totales de Pts_Adicionales
      df_semanal    → detalle semana a semana con semáforo
    """
    _vacio = pd.DataFrame()
    if df_diario.empty or "Fecha" not in df_diario.columns:
        return _vacio, _vacio
    df = df_diario.copy()
    df["Fecha"]      = pd.to_datetime(df["Fecha"])
    df["Semana_Mes"] = df["Fecha"].dt.day.apply(lambda d: (d - 1) // 7 + 1)

    # +1 por día que supera cuota diaria
    df["Pts_Dia_Extra"] = (df["Venta_Dia"] > df["CuotaDiaria"]).astype(int)

    # Agrupación semanal
    sem = (df.groupby(["Gestor","Producto","Semana_Mes"])
             .agg(
                 Ventas_Sem = ("Venta_Dia",    "sum"),
                 Cuota_Sem  = ("CuotaDiaria",  "sum"),
                 Pts_Dia    = ("Pts_Dia_Extra", "sum"),
             ).reset_index())
    sem["Cumpl_Sem_%"] = (sem["Ventas_Sem"] /
                          sem["Cuota_Sem"].replace(0, 1) * 100).round(1)
    sem["Pts_Sem"]     = (sem["Cumpl_Sem_%"] >= 100).astype(int) * PTS_CUOTA_SEMANAL

    # ── Puntos vs semana equivalente del mes anterior ────────────────────────
    # Fuente 1: hoja Semanal_MesAnt → comparación semana exacta vs semana exacta
    usar_semanal_ant = (
        df_sem_ant is not None and not df_sem_ant.empty and
        all(c in df_sem_ant.columns for c in ["Gestor", "Producto", "Semana", "Venta_Semana"])
    )
    if usar_semanal_ant:
        # Construir mapa (Gestor, Producto, Semana) → Venta_Semana_MesAnt
        ant_map = {}
        for _, row in df_sem_ant.iterrows():
            key = (str(row["Gestor"]).strip(),
                   str(row["Producto"]).strip(),
                   int(float(row["Semana"])))
            ant_map[key] = float(row.get("Venta_Semana", 0) or 0)
        sem["Venta_Ant_Sem"] = sem.apply(
            lambda r: ant_map.get(
                (str(r["Gestor"]).strip(), str(r["Producto"]).strip(), int(r["Semana_Mes"])),
                0.0), axis=1)
    # Fuente 2: fallback — total mes anterior / 4 (estimación)
    elif "Gestor" in df_raw.columns and "VentaMesAnterior" in df_raw.columns:
        ant_map = (df_raw.drop_duplicates(["Gestor","Producto"])
                         .set_index(["Gestor","Producto"])["VentaMesAnterior"]
                         .apply(lambda v: float(v) / 4)
                         .to_dict())
        sem["Venta_Ant_Sem"] = sem.apply(
            lambda r: float(ant_map.get((r["Gestor"], r["Producto"]), 0)), axis=1)
    else:
        sem["Venta_Ant_Sem"] = 0.0

    sem["Pts_vs_Ant"]    = (sem["Ventas_Sem"] > sem["Venta_Ant_Sem"]).astype(int) * PTS_MES_ANTERIOR
    sem["Pts_Total_Sem"] = sem["Pts_Dia"] + sem["Pts_Sem"] + sem["Pts_vs_Ant"]
    sem["Semaforo"]      = sem["Cumpl_Sem_%"].apply(
        lambda x: "🟢" if x >= 100 else ("🟡" if x >= 80 else "🔴"))

    # Totales por Gestor × Producto
    res = (sem.groupby(["Gestor","Producto"])
              .agg(
                  Pts_Extra_Diario = ("Pts_Dia",       "sum"),
                  Pts_Semanal      = ("Pts_Sem",       "sum"),
                  Pts_Sem_vs_Ant   = ("Pts_vs_Ant",    "sum"),
                  Pts_Adicionales  = ("Pts_Total_Sem", "sum"),
              ).reset_index())
    return res, sem

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
# PERSISTENCIA CSV + SESSION STATE — Registro Diario
# Compatible con Streamlit Cloud y servidores locales.
# Primario: CSV en disco (persiste entre sesiones en servidores).
# Fallback: st.session_state (persiste en la sesión actual).
# ============================================================================
CSV_PATH  = "ventas_registro.csv"
DNI_PATH  = "gestores_dni.csv"
_CSV_COLS = ["id","timestamp","dni","gestor","departamento",
             "producto","fecha","venta_dia","cuota_diaria"]
_DNI_COLS = ["dni","gestor","departamento"]

def _df_vacio():
    return pd.DataFrame(columns=_CSV_COLS)

def cargar_registros_db():
    """Carga registros desde CSV (si existe) y fusiona con session_state."""
    # Primero session_state (tiene los datos de esta sesión)
    df_ss = st.session_state.get("_registros", _df_vacio())
    # Intentar leer CSV del disco
    if os.path.exists(CSV_PATH):
        try:
            df_csv = pd.read_csv(CSV_PATH, dtype={"id": int})
            # Fusionar: prioridad CSV (tiene histórico), session_state agrega lo nuevo
            if not df_ss.empty and not df_csv.empty:
                df_merged = pd.concat([df_csv, df_ss], ignore_index=True)
                df_merged = df_merged.drop_duplicates(subset=["id"]).sort_values(
                    ["fecha","timestamp"], ascending=False)
                return df_merged
            return df_csv if not df_csv.empty else df_ss
        except Exception:
            pass
    return df_ss

def _guardar_csv(df: pd.DataFrame):
    """Intenta escribir el CSV en disco; silencioso si no hay permisos."""
    try:
        df.to_csv(CSV_PATH, index=False)
    except Exception:
        pass  # Streamlit Cloud sin permisos de escritura → solo session_state

def insertar_registro_db(gestor, departamento, producto, fecha,
                         venta_dia, cuota_diaria, dni=""):
    """Inserta o reemplaza el registro para gestor+producto+fecha (upsert)."""
    from datetime import datetime
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df  = cargar_registros_db()

    # Eliminar registro previo del mismo gestor+producto+fecha (reemplazar, no sumar)
    if not df.empty:
        mask_dup = ((df["gestor"] == gestor) &
                    (df["producto"] == producto) &
                    (df["fecha"] == str(fecha)))
        df = df[~mask_dup].reset_index(drop=True)

    nid = int(df["id"].max()) + 1 if (not df.empty and "id" in df.columns
                                       and pd.notna(df["id"].max())) else 1
    nueva = pd.DataFrame([{
        "id": nid, "timestamp": ts,
        "dni": str(dni), "gestor": gestor, "departamento": departamento,
        "producto": producto, "fecha": str(fecha),
        "venta_dia": float(venta_dia), "cuota_diaria": float(cuota_diaria),
    }])
    df = pd.concat([df, nueva], ignore_index=True)
    _guardar_csv(df)
    st.session_state["_registros"] = df

def existe_registro_db(gestor, producto, fecha):
    """True si ya hay un registro para ese gestor+producto+fecha en la sesión."""
    df = cargar_registros_db()
    if df.empty:
        return False
    return ((df["gestor"] == gestor) &
            (df["producto"] == producto) &
            (df["fecha"] == str(fecha))).any()

def eliminar_registro_db(record_id: int):
    """Elimina un registro por ID."""
    df = cargar_registros_db()
    df = df[df["id"] != record_id].reset_index(drop=True)
    _guardar_csv(df)
    st.session_state["_registros"] = df

def db_a_diario(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte registros CSV/session al formato de df_diario:
    Gestor, Departamento, Producto, Fecha (datetime), Venta_Dia, CuotaDiaria.
    Agrupa por Gestor+Producto+Fecha (suma del día).
    """
    df = cargar_registros_db()
    if df.empty:
        return pd.DataFrame()

    # Completar CuotaDiaria desde datos mensuales si la columna falta o es 0
    if "Gestor" in df_raw.columns and "CuotaDiaria" in df_raw.columns:
        cuota_map = (df_raw.drop_duplicates(["Gestor","Producto"])
                           .set_index(["Gestor","Producto"])["CuotaDiaria"]
                           .to_dict())
        def _cd(row):
            v = float(row.get("cuota_diaria") or 0)
            if v == 0:
                v = float(cuota_map.get((row["gestor"], row["producto"]), 0))
            return v
        df["cuota_diaria"] = df.apply(_cd, axis=1)

    agg = (df.groupby(["gestor","departamento","producto","fecha"])
             .agg(Venta_Dia=("venta_dia","sum"), CuotaDiaria=("cuota_diaria","first"))
             .reset_index())
    agg.columns = ["Gestor","Departamento","Producto","Fecha","Venta_Dia","CuotaDiaria"]
    agg["Fecha"] = pd.to_datetime(agg["Fecha"])
    return agg

# ============================================================================
# GESTIÓN DNI — mapeo DNI → Gestor
# ============================================================================
def cargar_dni_map() -> dict:
    """Devuelve {dni: {gestor, departamento}} desde CSV o session_state."""
    if os.path.exists(DNI_PATH):
        try:
            df = pd.read_csv(DNI_PATH, dtype=str).fillna("")
            mapa = {str(r["dni"]).strip(): {"gestor": r["gestor"],
                                             "departamento": r["departamento"]}
                    for _, r in df.iterrows()}
            st.session_state["_dni_map"] = mapa
            return mapa
        except Exception:
            pass
    return st.session_state.get("_dni_map", {})

def guardar_dni_map(mapa: dict):
    """Guarda el mapa DNI en CSV y session_state."""
    st.session_state["_dni_map"] = mapa
    rows = [{"dni": k, "gestor": v["gestor"], "departamento": v["departamento"]}
            for k, v in mapa.items()]
    df = pd.DataFrame(rows, columns=_DNI_COLS)
    try:
        df.to_csv(DNI_PATH, index=False)
    except Exception:
        pass

def buscar_por_dni(dni: str):
    """Retorna (gestor, departamento) o (None, '') si no existe."""
    info = cargar_dni_map().get(str(dni).strip())
    if info:
        return info["gestor"], info["departamento"]
    return None, ""

# ============================================================================
# CARGA DE DATOS
# ============================================================================
ADMIN_PASSWORD = "admin2025"      # ← cambia esta contraseña

# ── Mapa de regiones ──────────────────────────────────────────────────────────
REGIONES = {
    "Oriente": ["Amazonas", "Cajamarca", "Loreto", "San Martín", "Ucayali"],
    "Centro":  ["Huancavelica", "Huánuco", "Junín", "Pasco"],
}
DEPTO_A_REGION = {d: r for r, deptos in REGIONES.items() for d in deptos}

# ── Admin session state ───────────────────────────────────────────────────────
if "es_admin" not in st.session_state:
    st.session_state["es_admin"] = False
DATA_PATH      = "datos_incentivos.xlsx"   # archivo guardado en el servidor

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
    primera_col = str(df.columns[0]).upper()
    if "GESTOR" not in primera_col and primera_col not in ("GESTOR", "NAN"):
        df = pd.read_excel(xls, sheet_name=sheet_name, header=2).iloc[1:].reset_index(drop=True)
    return normalizar_columnas(df)

def cargar_excel(fuente):
    """Carga Mensual, Diario y Semanal_MesAnt desde un archivo o buffer."""
    xls       = pd.ExcelFile(fuente)
    df_m      = leer_hoja(xls, "Mensual")
    df_d      = leer_hoja(xls, "Diario")          if "Diario"          in xls.sheet_names else pd.DataFrame()
    df_sa     = leer_hoja(xls, "Semanal_MesAnt")  if "Semanal_MesAnt"  in xls.sheet_names else pd.DataFrame()
    return df_m, df_d, df_sa

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    f'''<div style="padding:10px 8px 14px 8px; text-align:center;
                    border-bottom:1px solid rgba(201,152,42,0.35); margin-bottom:8px;">
        {_logo_html}
    </div>''',
    unsafe_allow_html=True
)
st.sidebar.title("⚙️ Configuración")

# ── Carga de archivo Excel (solo cuando admin está activo) ───────────────────
if st.session_state.get("es_admin"):
    with st.sidebar.expander("📤 Cargar datos Excel", expanded=True):
        archivo_subido = st.file_uploader("Archivo .xlsx", type=["xlsx"])
        if archivo_subido:
            bytes_data = archivo_subido.read()
            with open(DATA_PATH, "wb") as f:
                f.write(bytes_data)
            st.success("✅ Datos guardados — todos los usuarios verán la actualización")
else:
    archivo_subido = None

# ── es_admin desde session_state ─────────────────────────────────────────────
es_admin = st.session_state.get("es_admin", False)
if not es_admin:
    archivo_subido = None

if archivo_subido:
    import io
    archivo_subido.seek(0)
    df_raw, df_diario, df_sem_ant = cargar_excel(io.BytesIO(archivo_subido.read()))
elif os.path.exists(DATA_PATH):
    df_raw, df_diario, df_sem_ant = cargar_excel(DATA_PATH)
    if es_admin:
        import time
        mod_time = os.path.getmtime(DATA_PATH)
        fecha_mod = date.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")
        st.sidebar.caption(f"📂 Datos activos · cargados el {fecha_mod}")
else:
    df_raw, df_diario = datos_demo()
    df_sem_ant = pd.DataFrame()
    if es_admin:
        st.sidebar.info("No hay datos guardados. Sube tu Excel para activarlos.")

# ── Gestión DNI en el sidebar (solo admin, requiere df_raw) ──────────────────
_depto_map_sb = (df_raw.drop_duplicates("Gestor").set_index("Gestor")["Departamento"].to_dict()
                 if "Gestor" in df_raw.columns and "Departamento" in df_raw.columns else {})
_gestores_sb  = sorted(df_raw["Gestor"].unique().tolist()) if "Gestor" in df_raw.columns else []

with st.sidebar.expander("👥 Gestores · DNI"):
    if not es_admin:
        st.info("Solo el administrador puede gestionar DNIs.")
    else:
        mapa_dni = cargar_dni_map()
        if mapa_dni:
            df_mapa_sb = pd.DataFrame(
                [{"DNI": k, "Nombre": v["gestor"], "Depto": v["departamento"]}
                 for k, v in mapa_dni.items()])
            st.dataframe(df_mapa_sb, hide_index=True, use_container_width=True)
        else:
            st.caption("Sin gestores registrados aún.")

        st.markdown("**Agregar gestor**")
        sb_dni  = st.text_input("DNI", key="sb_dni_add", max_chars=15)
        if _gestores_sb:
            sb_gst  = st.selectbox("Gestor", _gestores_sb, key="sb_gst_add")
            sb_dept = _depto_map_sb.get(sb_gst, "")
            st.caption(f"Departamento: {sb_dept}")
        else:
            sb_gst  = st.text_input("Gestor", key="sb_gst_txt")
            sb_dept = st.text_input("Departamento", key="sb_dept_txt")

        if st.button("➕ Agregar gestor", key="btn_add_dni_sb"):
            if sb_dni.strip() and sb_gst:
                mapa_dni[sb_dni.strip()] = {"gestor": sb_gst, "departamento": sb_dept}
                guardar_dni_map(mapa_dni)
                st.success(f"✅ {sb_gst} · DNI {sb_dni.strip()}")
                st.rerun()
            else:
                st.error("Completa DNI y nombre.")

        if mapa_dni:
            st.markdown("**Eliminar gestor**")
            dni_quitar = st.selectbox(
                "DNI a quitar",
                list(mapa_dni.keys()),
                format_func=lambda d: f"{d} — {mapa_dni[d]['gestor']}",
                key="dni_quitar_sb")
            if st.button("🗑️ Quitar", key="btn_del_dni_sb"):
                del mapa_dni[dni_quitar]
                guardar_dni_map(mapa_dni)
                st.rerun()

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
        df_diario = pd.DataFrame()

# ── Merge datos SQLite (Registro Diario) → df_diario ─────────────────────────
# Regla de prioridad: Excel Diario > SQLite (app).
# Si el Excel ya tiene un registro para Gestor+Producto+Fecha, ese gana.
# Solo se usan los registros SQLite para fechas que NO están en el Excel.
df_diario_sqlite = db_a_diario(df_raw)
if not df_diario_sqlite.empty:
    if not df_diario.empty:
        # Claves que ya cubre el Excel
        excel_keys = set(
            zip(df_diario["Gestor"].astype(str),
                df_diario["Producto"].astype(str),
                df_diario["Fecha"].astype(str))
        )
        # Solo mantener filas SQLite que NO tienen registro en Excel
        mask_nuevas = ~df_diario_sqlite.apply(
            lambda r: (str(r["Gestor"]), str(r["Producto"]), str(r["Fecha"])) in excel_keys,
            axis=1
        )
        df_diario = pd.concat([df_diario, df_diario_sqlite[mask_nuevas]], ignore_index=True)
    else:
        df_diario = df_diario_sqlite

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

# ── Ventas semanales y puntos adicionales ─────────────────────────────────────
df_semanal_resumen = calcular_ventas_semanales(df_diario)
df_pts_add, df_sem_detalle = calcular_puntos_adicionales(df_diario, df_raw, df_sem_ant)
if not df_pts_add.empty:
    df = df.merge(df_pts_add[["Gestor","Producto","Pts_Adicionales",
                               "Pts_Extra_Diario","Pts_Semanal","Pts_Sem_vs_Ant"]],
                  on=["Gestor","Producto"], how="left")
else:
    df["Pts_Adicionales"]  = 0
    df["Pts_Extra_Diario"] = 0
    df["Pts_Semanal"]      = 0
    df["Pts_Sem_vs_Ant"]   = 0
for c in ["Pts_Adicionales","Pts_Extra_Diario","Pts_Semanal","Pts_Sem_vs_Ant"]:
    df[c] = df[c].fillna(0).astype(int)

df["Total_Puntos"] = (
    df["Puntos_Base"] + df["Puntos_Diario"] + df["Puntos_Crec"] +
    df["Puntos_Producto"] + df["Pts_Adicionales"]
)

# ============================================================================
# FILTROS GLOBALES
# ============================================================================
st.sidebar.markdown("---")

# ── Filtro por Región ─────────────────────────────────────────────────────────
region_sel = st.sidebar.selectbox(
    "🌎 Región",
    ["Todas", "Oriente", "Centro"],
    help="Oriente: Amazonas, Cajamarca, Loreto, San Martín, Ucayali\nCentro: Huancavelica, Huánuco, Junín, Pasco"
)

# Departamentos disponibles según región elegida
if region_sel == "Todas":
    deptos_disponibles = sorted(df["Departamento"].unique())
else:
    deptos_disponibles = sorted(
        d for d in df["Departamento"].unique()
        if DEPTO_A_REGION.get(d) == region_sel
    )

deptos_opts   = ["Todos"] + deptos_disponibles
depto_sel     = st.sidebar.selectbox("🏢 Departamento", deptos_opts)

# Gestores filtrados por región/depto
df_region = df.copy()
if region_sel != "Todas":
    df_region = df_region[df_region["Departamento"].map(DEPTO_A_REGION) == region_sel]
if depto_sel != "Todos":
    df_region = df_region[df_region["Departamento"] == depto_sel]

gestores_opts = ["Todos"] + sorted(df_region["Gestor"].unique())
gestor_sel    = st.sidebar.selectbox("👤 Gestor", gestores_opts)

df_f = df_region.copy()
if gestor_sel != "Todos": df_f = df_f[df_f["Gestor"] == gestor_sel]

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
# BOTÓN ADMIN — esquina superior derecha
# ============================================================================
_col_space, _col_adm = st.columns([8, 2])
with _col_adm:
    _lbl = "🔓 Admin activo" if st.session_state.get("es_admin") else "🔐 Administrador"
    with st.popover(_lbl, use_container_width=True):
        if not st.session_state.get("es_admin"):
            st.markdown("#### Acceso Administrador")
            _pwd = st.text_input("Contraseña", type="password", key="admin_pwd_top")
            if st.button("Entrar", key="btn_admin_enter", use_container_width=True):
                if _pwd == ADMIN_PASSWORD:
                    st.session_state["es_admin"] = True
                    st.rerun()
                elif _pwd:
                    st.error("Contraseña incorrecta")
        else:
            st.success("✅ Modo administrador activo")
            st.caption("El menú de carga de datos aparece en el sidebar izquierdo.")
            st.markdown("---")
            if st.button("🔓 Cerrar sesión", key="logout_top", use_container_width=True):
                st.session_state["es_admin"] = False
                st.rerun()

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumen General",
    "📦 Detalle por Producto",
    "📅 Seguimiento Diario",
    "📝 Registro Diario",
])

# ============================================================================
# TAB 1 — RESUMEN GENERAL
# ============================================================================
# ── Barra de logo superior ───────────────────────────────────────────────────
st.markdown(
    f'''<div class="logo-topbar">
        {_logo_html}
        <span>Sistema de Incentivos de Ventas</span>
    </div>''',
    unsafe_allow_html=True
)

with tab1:
    # ── Header estilo Power BI ────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2A5E 0%,#0B5ED7 100%);
                border-radius:12px; padding:22px 30px 18px 30px; margin-bottom:20px;
                box-shadow:0 4px 16px rgba(31,56,100,0.25);">
        <p style="color:#FFFFFF; margin:0; font-size:26px; font-weight:800; letter-spacing:-0.3px;">🏆 Incentivo Fanero Julio 2026</p>
        <p style="color:#FFFFFF; margin:4px 0 0 0; font-size:13px;">
            Seguimiento de ventas · Ranking · Puntos por Producto
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs principales (5 tarjetas estilo Power BI) ────────────────────────
    v_act = df_gestor["Venta"].sum()
    v_ant = df_gestor["VentaMesAnterior"].sum()
    var   = ((v_act - v_ant) / v_ant * 100) if v_ant else 0
    cumpl_prom = df_gestor["Cumplimiento_%"].mean()

    render_kpi_row([
        {"label":"Gestores",              "value":str(df_gestor["Gestor"].nunique()),          "color":"#0A2A5E"},
        {"label":"Cumplimiento Promedio", "value":f"{cumpl_prom:.0f}%",
         "delta":"🟢 Sobre meta" if cumpl_prom >= 100 else "🔴 Bajo meta",                    "color":"#0B5ED7"},
        {"label":"Total Puntos",          "value":f"{int(df_gestor['Total_Puntos'].sum()):,}", "color":"#0B5ED7"},
        {"label":"Ventas del Mes",        "value":f"{int(v_act):,}",                            "color":"#0B5ED7"},
        {"label":"Variación vs Mes Ant.", "value":f"{var:+.1f}%",
         "delta":"▲ Crecimiento" if var >= 0 else "▼ Caída",
         "color":"#198754" if var >= 0 else "#DC3545"},
    ])

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Puntos sistema base + motor (2 filas de KPIs pequeños) ───────────────
    subheader("📌 Sistema Base de Puntos")
    render_kpi_row([
        {"label":"Puntos Cuota",       "value":str(int(df_gestor["Puntos_Base"].sum())),   "color":"#0A2A5E", "flex":"1"},
        {"label":"Puntos Diario Base", "value":str(int(df_gestor["Puntos_Diario"].sum())), "color":"#0B5ED7", "flex":"1"},
        {"label":"Puntos Crecimiento", "value":str(int(df_gestor["Puntos_Crec"].sum())),   "color":"#0B5ED7", "flex":"1"},
        {"label":"",                   "value":"",                                          "color":"transparent", "flex":"1"},
    ])

    st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
    subheader("🆕 Motor por Producto")
    render_kpi_row([
        {"label":"Diario",   "value":str(int(df_gestor["PD_Diario"].sum())),  "color":"#0A2A5E"},
        {"label":"Extra",    "value":str(int(df_gestor["PD_Extra"].sum())),   "color":"#0B5ED7"},
        {"label":"Semanal",  "value":str(int(df_gestor["PD_Semanal"].sum())), "color":"#0B5ED7"},
        {"label":"Mensual",  "value":str(int(df_gestor["PD_Mensual"].sum())), "color":"#0A2A5E"},
        {"label":"Mes Ant.", "value":str(int(df_gestor["PD_MesAnt"].sum())),  "color":"#0B5ED7"},
        {"label":"UR",       "value":str(int(df_gestor["PD_UR"].sum())),      "color":"#198754"},
    ])

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Resumen por Región (solo visible cuando se muestra "Todas") ───────────
    if region_sel == "Todas":
        subheader("🌎 Comparativo por Región")
        _col_or, _col_ce = st.columns(2)
        for _col, _region in [(_col_or, "Oriente"), (_col_ce, "Centro")]:
            with _col:
                _deptos_r = REGIONES[_region]
                _df_r = df_gestor[df_gestor["Departamento"].isin(_deptos_r)]
                _ventas  = int(_df_r["Venta"].sum())
                _cuota   = int(_df_r["Cuota"].sum())
                _pts     = int(_df_r["Total_Puntos"].sum())
                _gest    = _df_r["Gestor"].nunique()
                _cumpl   = round(_df_r["Cumplimiento_%"].mean(), 1) if not _df_r.empty else 0
                _color_r = "#0B5ED7" if _region == "Oriente" else "#198754"
                st.markdown(f"""
                <div style="background:{_color_r}; border-radius:12px; padding:18px 20px;
                            box-shadow:0 4px 14px rgba(0,0,0,0.20); margin-bottom:10px;">
                    <div style="color:#FFD97A; font-size:17px; font-weight:800;
                                margin-bottom:10px;">🌎 Región {_region}</div>
                    <div style="display:flex; gap:12px; flex-wrap:wrap;">
                        <div style="flex:1; min-width:80px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 12px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Gestores</div>
                            <div style="color:#fff; font-size:22px; font-weight:800;">{_gest}</div>
                        </div>
                        <div style="flex:1; min-width:80px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 12px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Cumpl.%</div>
                            <div style="color:#FFD97A; font-size:22px; font-weight:800;">{_cumpl}%</div>
                        </div>
                        <div style="flex:1; min-width:80px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 12px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Ventas</div>
                            <div style="color:#fff; font-size:22px; font-weight:800;">{_ventas:,}</div>
                        </div>
                        <div style="flex:1; min-width:80px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 12px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Puntos</div>
                            <div style="color:#fff; font-size:22px; font-weight:800;">{_pts:,}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px; color:rgba(255,255,255,0.65); font-size:11px;">
                        {" · ".join(_deptos_r)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Top 3 ────────────────────────────────────────────────────────────────
    subheader("🥇 Top Performers")
    rank = df_gestor.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
    medal_colors = ["#B8960C", "#6B7280", "#92400E"]
    top_cards = []
    for i, row in enumerate(rank.head(3).itertuples()):
        top_cards.append({
            "label": f"{'🥇🥈🥉'[i]}  {row.Gestor}",
            "value": f"{int(row.Total_Puntos):,} pts",
            "delta": f"Base {int(row.Puntos_Base)} · Motor {int(row.Puntos_Producto)}",
            "color": medal_colors[i],
        })
    render_kpi_row(top_cards)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Ranking + tabla (2 columnas) ─────────────────────────────────────────
    subheader("🏆 Ranking General")
    rank_disp = rank.copy()
    rank_disp.insert(0, "Puesto", range(1, len(rank_disp)+1))
    colA, colB = st.columns([3, 2])
    with colA:
        fig_r = px.bar(
            rank.sort_values("Total_Puntos"), x="Total_Puntos", y="Gestor",
            orientation="h", text="Total_Puntos",
            color_discrete_sequence=["#2E75B6"]
        )
        fig_r.update_traces(textposition="outside", marker_line_width=0,
                             textfont=dict(size=11, color="#1F3864", family="Arial"))
        fig_r.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#EEF2F7", title=""),
            yaxis=dict(title="", tickfont=dict(size=11)),
            margin=dict(l=10, r=30, t=10, b=10),
            height=max(300, len(rank) * 38)
        )
        st.plotly_chart(fig_r, use_container_width=True)
    with colB:
        st.dataframe(
            rank_disp[["Puesto","Gestor","Total_Puntos","Puntos_Producto","Cumplimiento_%","Semaforo"]],
            use_container_width=True, hide_index=True, height=max(300, len(rank) * 38)
        )

    # ── Composición de puntos + semáforo (2 columnas) ────────────────────────
    st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)
    subheader("📊 Composición de Puntos · Estado de Gestores")
    colC, colD = st.columns([3, 2])

    with colC:
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
        fig_s = px.bar(df_melt, x="Gestor", y="Puntos", color="Tipo", barmode="stack",
                       color_discrete_sequence=PALETA)
        fig_s.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
            xaxis=dict(title="", tickfont=dict(size=10)),
            yaxis=dict(title="Puntos", gridcolor="#EEF2F7"),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_s, use_container_width=True)

    with colD:
        sem = df_gestor["Semaforo"].value_counts().reset_index()
        sem.columns = ["Estado","Cantidad"]
        fig_pie = px.pie(
            sem, names="Estado", values="Cantidad", hole=0.55,
            color="Estado",
            color_discrete_map={"🟢 Verde":"#198754","🟡 Amarillo":"#FFC107","🔴 Rojo":"#DC3545"}
        )
        fig_pie.update_traces(textinfo="label+percent", textfont_size=12)
        fig_pie.update_layout(
            showlegend=False, paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=10),
            annotations=[dict(text="Estado", x=0.5, y=0.5,
                              font=dict(size=14, color="#0A2A5E"), showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Detalle ejecutivo expandible ──────────────────────────────────────────
    with st.expander("📋 Detalle Ejecutivo Completo"):
        st.dataframe(
            df_gestor[[
                "Gestor","Departamento","Venta","Cuota","Cumplimiento_%",
                "Puntos_Base","Puntos_Diario","Puntos_Crec",
                "Puntos_Producto","Total_Puntos","Semaforo"
            ]].sort_values("Total_Puntos", ascending=False),
            use_container_width=True, hide_index=True
        )
    with st.expander("🔍 Desglose Motor por Producto"):
        cols_show = ["Gestor","Producto","PD_Diario","PD_Extra","PD_Semanal",
                     "PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto","Total_Puntos"]
        st.dataframe(df_f[cols_show].sort_values(["Gestor","Producto"]),
                     use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2 — DETALLE POR PRODUCTO
# ============================================================================
with tab2:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2A5E 0%,#0B5ED7 100%);
                border-radius:12px; padding:18px 30px 14px 30px; margin-bottom:20px;
                box-shadow:0 4px 16px rgba(31,56,100,0.25);">
        <p style="color:#FFFFFF; margin:0; font-size:22px; font-weight:800;">📦 Detalle por Producto</p>
    </div>""", unsafe_allow_html=True)

    if "Producto" not in df_f.columns:
        st.warning("El dataset no contiene columna 'Producto'.")
        st.stop()

    subheader("🏢 Por Departamento")
    show_pivot_regional(df_f)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    subheader("👤 Por Gestor")
    show_pivot_gestor_regional(df_f)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    subheader("📊 Cumplimiento % por Producto")
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
        category_orders={"Producto": PRODUCTOS_ORDEN},
        color_discrete_sequence=PALETA
    )
    fig_prod.add_hline(y=100, line_dash="dash", line_color="#E45756", annotation_text="Meta 100%")
    fig_prod.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    fig_prod.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                           yaxis=dict(gridcolor="#EEF2F7"),
                           margin=dict(t=20, b=10))
    st.plotly_chart(fig_prod, use_container_width=True)

    subheader("🌡️ Mapa de Calor — Cumplimiento")
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
    subheader("🆕 Puntos Motor por Gestor y Producto")
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
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2A5E 0%,#0B5ED7 100%);
                border-radius:12px; padding:18px 30px 14px 30px; margin-bottom:20px;
                box-shadow:0 4px 16px rgba(31,56,100,0.25);">
        <p style="color:#FFFFFF; margin:0; font-size:22px; font-weight:800;">📅 Seguimiento Diario de Ventas</p>
    </div>""", unsafe_allow_html=True)

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

    render_kpi_row([
        {"label":"📅 Último día",       "value": str(ultimo_dia)[:10],   "color":"#0A2A5E"},
        {"label":"Venta Total",         "value": f"{v_hoy:.0f}",         "color":"#0B5ED7"},
        {"label":"Cuota Total",         "value": f"{c_hoy:.0f}",         "color":"#0B5ED7"},
        {"label":f"{emoji_hoy} Cumpl. del Día",
         "value": f"{cp_hoy:.0f}%",
         "color":"#198754" if cp_hoy >= 100 else ("#B45309" if cp_hoy >= 80 else "#DC3545")},
    ])

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    # ── Tabla pivot gestores × productos (último día) ─────────────────────────
    subheader(f"📋 Estado por Gestor — {str(ultimo_dia)[:10]}")

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

    st.markdown(_pivot_to_html(pivot_h, "Gestor", prods_h), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Acumulado mes ─────────────────────────────────────────────────────────
    subheader("📈 Acumulado del Mes: Ventas vs Meta")
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
        line=dict(color="#2E75B6", width=2.5), marker=dict(size=5)
    ))
    fig_acum.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["Cuota_Acum"],
        mode="lines", name="Meta Acumulada",
        line=dict(color="#E45756", dash="dash", width=2)
    ))
    fig_acum.add_trace(go.Scatter(
        x=pd.concat([df_dia_agg["Fecha"], df_dia_agg["Fecha"][::-1]]).tolist(),
        y=pd.concat([df_dia_agg["Venta_Acum"], df_dia_agg["Cuota_Acum"][::-1]]).tolist(),
        fill="toself", fillcolor="rgba(76,120,168,0.1)",
        line=dict(color="rgba(255,255,255,0)"), showlegend=False, hoverinfo="skip"
    ))
    fig_acum.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="", gridcolor="#EEF2F7"),
        yaxis=dict(title="Unidades", gridcolor="#EEF2F7"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_acum, use_container_width=True)

    subheader("📊 Ventas Diarias vs Cuota")
    df_dia_agg["Cumpl_Dia_%"] = (df_dia_agg["Venta_Dia"] / df_dia_agg["CuotaDiaria"] * 100).round(1)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_dia_agg["Fecha"], y=df_dia_agg["Venta_Dia"], name="Venta Día",
        marker_color=df_dia_agg["Cumpl_Dia_%"].apply(
            lambda x: "#54A24B" if x >= 100 else ("#F4D03F" if x >= 80 else "#E45756"))
    ))
    fig_bar.add_trace(go.Scatter(
        x=df_dia_agg["Fecha"], y=df_dia_agg["CuotaDiaria"],
        mode="lines", name="Cuota Día", line=dict(color="#E45756", dash="dot", width=2)
    ))
    fig_bar.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="", gridcolor="#EEF2F7"),
        yaxis=dict(title="Unidades", gridcolor="#EEF2F7"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Resumen Semanal ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    subheader("📆 Resumen Semanal por Gestor")

    if not df_semanal_resumen.empty:
        # Filtros de seguimiento diario aplicados
        df_sem_f = df_semanal_resumen.copy()
        if gestor_sel != "Todos" and "Gestor" in df_sem_f.columns:
            df_sem_f = df_sem_f[df_sem_f["Gestor"] == gestor_sel]
        if depto_sel != "Todos" and "Departamento" in df_sem_f.columns:
            df_sem_f = df_sem_f[df_sem_f["Departamento"] == depto_sel]

        # Tabla resumen semanal con semáforo
        cols_sem = [c for c in ["Semaforo","Gestor","Producto","Semana_Mes",
                                 "Ventas_Semana","Cuota_Semana","Cumpl_Sem_%",
                                 "Dias_Activos"] if c in df_sem_f.columns]
        df_sem_show = df_sem_f[cols_sem].copy()
        df_sem_show.rename(columns={
            "Semaforo":"","Semana_Mes":"Semana",
            "Ventas_Semana":"Ventas","Cuota_Semana":"Cuota",
            "Cumpl_Sem_%":"Cumpl %","Dias_Activos":"Días"
        }, inplace=True)
        for c in ["Ventas","Cuota"]:
            if c in df_sem_show.columns:
                df_sem_show[c] = df_sem_show[c].round(0).astype(int)
        st.dataframe(df_sem_show, use_container_width=True, hide_index=True)

        # Totales de puntos adicionales por gestor
        if not df_sem_detalle.empty:
            subheader("🏅 Puntos Adicionales Semanales")
            df_pts_sem_show = (df_sem_detalle
                .groupby(["Gestor","Producto"])
                .agg(
                    Días_Sobre_Cuota = ("Pts_Dia",       "sum"),
                    Pts_Semanales    = ("Pts_Sem",       "sum"),
                    Pts_vs_MesAnt    = ("Pts_vs_Ant",    "sum"),
                    Total_Adicional  = ("Pts_Total_Sem", "sum"),
                ).reset_index())
            # Semáforo total
            max_posible = df_pts_sem_show["Total_Adicional"].max() or 1
            df_pts_sem_show[""] = df_pts_sem_show["Total_Adicional"].apply(
                lambda x: "🟢" if x >= max_posible * 0.7 else ("🟡" if x >= max_posible * 0.4 else "🔴"))
            cols_order = ["","Gestor","Producto",
                          "Días_Sobre_Cuota","Pts_Semanales","Pts_vs_MesAnt","Total_Adicional"]
            st.dataframe(df_pts_sem_show[[c for c in cols_order if c in df_pts_sem_show.columns]],
                         use_container_width=True, hide_index=True)
    else:
        st.info("Sin datos diarios para calcular semanas. Carga datos en la hoja Diario o usa la pestaña Registro Diario.")

# ============================================================================
# TAB 4 — REGISTRO DIARIO DE VENTAS
# ============================================================================
with tab4:
    # ── Header banner ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2A5E 0%,#0B5ED7 100%);
                border-radius:12px; padding:18px 30px 14px 30px; margin-bottom:20px;
                box-shadow:0 4px 16px rgba(31,56,100,0.25);">
        <p style="color:#FFFFFF; margin:0; font-size:22px; font-weight:800;">📝 Registro Diario de Ventas</p>
        <p style="color:#FFFFFF; margin:4px 0 0 0; font-size:13px;">
            Registra tus ventas del día · Los datos se guardan automáticamente y
            se integran al motor de puntos
        </p>
    </div>""", unsafe_allow_html=True)

    # ── Identificación por DNI (fuera del form para reactividad) ────────────
    subheader("🪪 Identificación")
    dni_col, info_col = st.columns([2, 3])

    with dni_col:
        dni_input = st.text_input(
            "Ingresa tu DNI",
            max_chars=15,
            placeholder="Ej: 12345678",
            key="dni_ingreso",
        )

    gestor_activo = None
    depto_activo  = ""

    if dni_input:
        gestor_activo, depto_activo = buscar_por_dni(dni_input.strip())
        with info_col:
            if gestor_activo:
                st.markdown(f"""
                <div style="background:#E8F5E9; border-radius:8px; padding:12px 16px;
                            border-left:5px solid #27AE60; margin-top:26px;">
                    <span style="font-size:11px; color:#1B7A3E; font-weight:700;
                                 text-transform:uppercase;">✅ DNI verificado</span><br>
                    <span style="font-size:22px; color:#1F3864; font-weight:800;">
                        {gestor_activo}</span><br>
                    <span style="font-size:12px; color:#7A8DA8;">{depto_activo}</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#FFF3CD; border-radius:8px; padding:12px 16px;
                            border-left:5px solid #F4C430; margin-top:26px;">
                    <span style="font-size:11px; color:#856404; font-weight:700;
                                 text-transform:uppercase;">⚠️ DNI no encontrado</span><br>
                    <span style="font-size:13px; color:#555;">
                        Contacta al administrador para registrar tu DNI.</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    col_form, col_hoy = st.columns([3, 2])

    # ── Formulario de carga ───────────────────────────────────────────────────────────────────
    with col_form:
        subheader("📋 Nueva Venta")

        if not gestor_activo:
            st.info("👆 Ingresa tu DNI arriba para habilitar el formulario de registro.")
        else:
            with st.form("form_registro_diario", clear_on_submit=True):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0A2A5E 0%,#0B5ED7 100%);
                            border-radius:6px; padding:8px 14px; margin-bottom:10px;
                            border-left:4px solid #C9982A;">
                    <span style="font-size:14px; color:#FFFFFF; font-weight:700;">
                        👤 {gestor_activo}</span>
                    <span style="color:rgba(255,255,255,0.65); font-size:12px;"> · {depto_activo}</span>
                </div>""", unsafe_allow_html=True)

                r1c1, r1c2 = st.columns(2)
                producto_sel_f = r1c1.selectbox("📦 Producto *", PRODUCTOS_ORDEN)
                fecha_f        = r1c2.date_input("📅 Fecha", value=date.today())
                ventas_f       = st.number_input(
                    "🛒 Unidades vendidas *", min_value=0, step=1, value=0)

                submitted_f = st.form_submit_button(
                    "💾  Guardar Registro", use_container_width=True, type="primary")

                if submitted_f:
                    if ventas_f == 0:
                        st.warning("⚠️ Ingresaste 0 ventas. ¿Seguro que quieres guardar?")
                    else:
                        cuota_d_f = 0.0
                        if "Gestor" in df_raw.columns:
                            mask_c = ((df_raw["Gestor"] == gestor_activo) &
                                      (df_raw["Producto"] == producto_sel_f))
                            if mask_c.any():
                                row_c = df_raw[mask_c].iloc[0]
                                if "CuotaDiaria" in row_c and pd.notna(row_c["CuotaDiaria"]):
                                    cuota_d_f = float(row_c["CuotaDiaria"])
                                elif "Cuota" in row_c:
                                    cuota_d_f = float(row_c["Cuota"]) / 22

                        es_dup = existe_registro_db(gestor_activo, producto_sel_f, str(fecha_f))
                        insertar_registro_db(
                            gestor=gestor_activo, departamento=depto_activo,
                            producto=producto_sel_f, fecha=str(fecha_f),
                            venta_dia=float(ventas_f), cuota_diaria=cuota_d_f,
                            dni=dni_input.strip(),
                        )
                        if es_dup:
                            st.info(
                                f"🔄 Registro actualizado · **{producto_sel_f}** · "
                                f"{int(ventas_f)} unidades · {fecha_f} (reemplazó el anterior)")
                        else:
                            st.success(
                                f"✅ Guardado · {producto_sel_f} · "
                                f"{int(ventas_f)} unidades · {fecha_f}")
                        st.rerun()

    with col_hoy:
        subheader(f"📊 Hoy — {date.today().strftime('%d/%m/%Y')}")
        df_db_hoy = cargar_registros_db()
        hoy_str   = str(date.today())

        if not df_db_hoy.empty:
            hoy_rows = df_db_hoy[df_db_hoy["fecha"] == hoy_str].copy()
            if gestor_activo:
                hoy_rows = hoy_rows[hoy_rows["gestor"] == gestor_activo]
            if not hoy_rows.empty:
                hoy_grp = (hoy_rows.groupby("producto")["venta_dia"]
                                   .sum().reset_index().sort_values("producto"))
                for _, row in hoy_grp.iterrows():
                    color = PALETA[PRODUCTOS_ORDEN.index(row["producto"]) % len(PALETA)]
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#0A2A5E 0%,{color} 100%);
                                border-radius:8px; padding:10px 16px; margin-bottom:8px;
                                border-left:4px solid #C9982A;
                                box-shadow:0 3px 10px rgba(0,33,71,0.20);">
                        <span style="font-size:11px; color:rgba(255,255,255,0.65);
                                     font-weight:700; text-transform:uppercase;">{row['producto']}</span><br>
                        <span style="font-size:26px; color:#FFFFFF; font-weight:800;">
                            {int(row['venta_dia'])}</span>
                        <span style="font-size:12px; color:rgba(255,255,255,0.65);"> unidades</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Sin ventas registradas hoy.")
        else:
            st.info("Usa el formulario para empezar.")

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    df_hist_all = cargar_registros_db()

    if gestor_activo:
        subheader(f"📜 Mis Registros — {gestor_activo}")
        df_mis = (df_hist_all[df_hist_all["gestor"] == gestor_activo].copy()
                  if not df_hist_all.empty and "gestor" in df_hist_all.columns
                  else pd.DataFrame())

        if not df_mis.empty:
            df_mis_show = df_mis[["id","fecha","producto","venta_dia","timestamp"]].copy()
            df_mis_show.columns = ["ID","Fecha","Producto","Ventas","Registrado"]
            df_mis_show["Ventas"] = df_mis_show["Ventas"].astype(int)
            st.dataframe(df_mis_show, use_container_width=True, hide_index=True)

            with st.expander("🗑️ Eliminar uno de mis registros"):
                st.caption("Solo puedes eliminar tus propios registros.")
                ids_propios = df_mis["id"].astype(int).tolist()

                def _label(rid):
                    r = df_mis[df_mis["id"] == rid]
                    if r.empty:
                        return str(rid)
                    return (f"#{rid} · {r['producto'].values[0]} · "
                            f"{r['fecha'].values[0]} · {int(r['venta_dia'].values[0])} u.")

                id_a_eliminar = st.selectbox(
                    "Selecciona el registro", ids_propios,
                    format_func=_label, key="del_propio_id")
                if st.button("❌ Eliminar este registro", key="btn_del_propio"):
                    es_mio = ((df_mis["id"] == id_a_eliminar) &
                              (df_mis["gestor"] == gestor_activo)).any()
                    if es_mio:
                        eliminar_registro_db(int(id_a_eliminar))
                        st.success(f"Registro #{id_a_eliminar} eliminado.")
                        st.rerun()
                    else:
                        st.error("No puedes eliminar registros de otros gestores.")
        else:
            st.info("Aún no tienes registros guardados.")
    else:
        subheader("📜 Historial General")
        if not df_hist_all.empty:
            cols_show = [c for c in ["id","timestamp","gestor","producto","fecha","venta_dia"]
                         if c in df_hist_all.columns]
            df_show = df_hist_all[cols_show].head(100).copy()
            rename  = ["ID","Registrado","Gestor","Producto","Fecha","Ventas"]
            df_show.columns = rename[:len(cols_show)]
            if "Ventas" in df_show.columns:
                df_show["Ventas"] = df_show["Ventas"].astype(int)
            st.dataframe(df_show, use_container_width=True, hide_index=True)
            csv_bytes = df_hist_all.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Descargar historial completo (.csv)",
                data=csv_bytes, file_name="historial_ventas.csv",
                mime="text/csv", use_container_width=True,
            )
        else:
            st.info("No hay registros. Ingresa tu DNI para registrar ventas.")
