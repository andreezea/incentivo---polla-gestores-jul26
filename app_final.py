# -*- coding: utf-8 -*-
from __future__ import annotations
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
_logo_html = f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:200px;object-fit:contain;" alt="Fanero SAC">'



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
# Puntos por criterio — valores definitivos por producto
# ─────────────────────────────────────────────────────────────────────────────
# 1. Cumple cuota diaria (pts fijos por día que cumple)
PTS_CUOTA_DIARIA = {
    "Prepago":   2,
    "Porta Pre": 5,
    "Postpago":  2,
    "OSS":       5,
}

# 2. Supera cuota diaria (pts fijos por día que SUPERA — no por unidad extra)
PTS_EXTRA_DIARIA = {
    "Prepago":   3,
    "Porta Pre": 6,
    "Postpago":  3,
    "OSS":       6,
}

# 3. Semana >= 100% cuota semanal (pts fijos por semana cumplida)
PTS_CUOTA_SEMANAL = {
    "Prepago":   10,
    "Porta Pre": 15,
    "Postpago":  10,
    "OSS":       15,
}

# 4. Mes >= 100% cuota mensual (pts fijos si cumple el mes)
PTS_CUOTA_MENSUAL = {
    "Prepago":   40,
    "Porta Pre": 50,
    "Postpago":  40,
    "OSS":       50,
}

# 5. Semana > promedio semanal mes anterior (pts fijos por semana que supera)
PTS_MES_ANTERIOR = {
    "Prepago":   15,
    "Porta Pre": 18,
    "Postpago":  15,
    "OSS":       18,
}

PTS_UR    = 15    # 6. UR: Prepago >= 55% de su cuota mensual
UR_UMBRAL = 0.55

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
def calcular_puntos_producto(df_mensual: pd.DataFrame,
                             df_diario: pd.DataFrame,
                             df_sem_ant: pd.DataFrame = None) -> pd.DataFrame:
    """
    Calcula Puntos_Producto por Gestor × Producto.

    Reglas (nombres oficiales del criterio):
      1. Cumple cuota diaria  (PD_Diario)  : pts fijos por día con Venta_Dia >= CuotaDiaria
      2. Supera cuota diaria  (PD_Extra)   : pts fijos por día que supera (no por unidad)
      3. Semana >= 100% cuota (PD_Semanal) : pts si Venta_Semana >= Cuota_Mensual/N_Semanas
      4. Mes >= 100% cuota    (PD_Mensual) : pts si Venta_Mes >= Cuota_Mensual
      5. Semana > semana mes ant(PD_MesAnt): pts por semana N > venta semana N de Semanal_MesAnt
      6. UR Prepago           (PD_UR)      : pts si Prepago >= 55% de su cuota mensual

    df_sem_ant: hoja Semanal_MesAnt con columnas Gestor, Producto, Semana, Venta_Semana
    """
    import calendar as _cal_pts
    _hoy_pts    = date.today()
    _n_dias_mes = _cal_pts.monthrange(_hoy_pts.year, _hoy_pts.month)[1]
    _n_semanas  = (_n_dias_mes - 1) // 7 + 1   # semanas del mes (grupos de 7 días)

    # Construir lookup de Semanal_MesAnt: (gestor, producto, semana_num) → venta
    _sem_ant_map = {}
    if df_sem_ant is not None and not df_sem_ant.empty:
        _sa = df_sem_ant.copy()
        for col in ["Gestor","Producto"]:
            if col in _sa.columns:
                _sa[col] = _sa[col].astype(str).str.strip()
        req = {"Gestor","Producto","Semana","Venta_Semana"}
        if req.issubset(set(_sa.columns)):
            for _, _r in _sa.iterrows():
                try:
                    _k = (str(_r["Gestor"]).strip(),
                          str(_r["Producto"]).strip(),
                          int(_r["Semana"]))
                    _sem_ant_map[_k] = float(_r["Venta_Semana"] or 0)
                except Exception:
                    pass

    # Acumulado real de ventas desde df_diario — SOLO MES ACTUAL
    # Filtramos por mes/año para evitar sumar datos históricos de meses anteriores.
    # Solo se otorga PD_Mensual cuando ventas acumuladas del mes actual >= cuota mensual.
    _venta_real_map = {}
    if not df_diario.empty and "Venta_Dia" in df_diario.columns and "Fecha" in df_diario.columns:
        _d_mes = df_diario.copy()
        _d_mes["Fecha"] = pd.to_datetime(_d_mes["Fecha"], errors="coerce")
        _d_mes = _d_mes[
            (_d_mes["Fecha"].dt.year  == _hoy_pts.year) &
            (_d_mes["Fecha"].dt.month == _hoy_pts.month)
        ]
        if not _d_mes.empty:
            _agg_real = _d_mes.groupby(["Gestor","Producto"])["Venta_Dia"].sum()
            _venta_real_map = _agg_real.to_dict()

    filas = []

    for (gestor, producto), grp_m in df_mensual.groupby(["Gestor", "Producto"]):
        row       = grp_m.iloc[0]
        cuota_m   = float(row["Cuota"])
        venta_m   = float(row["Venta"])
        # Para PD_Mensual: SOLO acumulado real del diario (mes actual).
        # No se usa el valor Excel como fallback porque puede ser una fórmula
        # cacheada con proyección. Si no hay registros diarios, no se otorgan puntos.
        venta_m_real = float(_venta_real_map.get((gestor, producto), 0) or 0)
        venta_ant = float(row.get("VentaMesAnterior", 0) or 0)
        cuota_d   = float(row.get("CuotaDiaria", cuota_m / _n_dias_mes) or cuota_m / _n_dias_mes)

        pts_dia_u   = PTS_CUOTA_DIARIA.get(producto, 2)
        pts_extra_u = PTS_EXTRA_DIARIA.get(producto, 3)
        pts_sem_u   = PTS_CUOTA_SEMANAL.get(producto, 10)
        pts_mes_u   = PTS_CUOTA_MENSUAL.get(producto, 40)
        pts_ant_u   = PTS_MES_ANTERIOR.get(producto, 15)

        # Cuota semanal = cuota mensual / nº semanas del mes
        cuota_sem    = cuota_m / _n_semanas if (_n_semanas > 0 and cuota_m > 0) else 0
        # Promedio semanal del mes anterior (fallback si no hay Semanal_MesAnt)
        prom_sem_ant = venta_ant / _n_semanas if (_n_semanas > 0 and venta_ant > 0) else 0
        # ¿Hay datos en Semanal_MesAnt para este gestor×producto?
        _tiene_sem_ant = any(
            (gestor, producto, s) in _sem_ant_map for s in range(1, _n_semanas + 1)
        )

        pd_diario = pd_extra = pd_semanal = pd_mes_ant = 0

        # ── Datos diarios — SOLO mes actual ──────────────────────────────────
        # IMPORTANTE: filtrar al mes actual para que PD_Diario, PD_Extra y
        # PD_Semanal sean consistentes con PD_Mensual (que ya filtra por mes).
        # Sin este filtro, si df_diario tiene datos de meses anteriores, los
        # puntos diarios se inflarian contando todos los meses históricos.
        if not df_diario.empty and "Gestor" in df_diario.columns:
            mask  = (df_diario["Gestor"] == gestor) & (df_diario["Producto"] == producto)
            grp_d = df_diario[mask].copy()
            # Filtrar al mes actual (Fecha ya es datetime desde calcular_cuota_diaria_historica)
            if "Fecha" in grp_d.columns and not grp_d.empty:
                grp_d = grp_d[
                    (grp_d["Fecha"].dt.year  == _hoy_pts.year) &
                    (grp_d["Fecha"].dt.month == _hoy_pts.month)
                ].copy()  # .copy() evita ChainedAssignmentError en pandas 2.x

            if not grp_d.empty:
                cd_col = grp_d["CuotaDiaria"] if "CuotaDiaria" in grp_d.columns else cuota_d

                # Regla: si el gestor YA llegó al 100% de su cuota mensual,
                # no se otorgan puntos diarios ni extras (ya cumplió su meta).
                # Si aún no llega al 100%, se otorgan normalmente.
                _ya_cumplio_mes = (cuota_m > 0 and venta_m_real >= cuota_m)

                if _ya_cumplio_mes:
                    # Ya alcanzó el 100% mensual → sin puntos diarios ni extras
                    pd_diario = 0
                    pd_extra  = 0
                else:
                    # 1. Cumple cuota diaria: pts fijos por cada día que cumple (venta >= cuota)
                    dias_ok   = grp_d["Venta_Dia"] >= cd_col
                    pd_diario = int(dias_ok.sum()) * pts_dia_u

                    # 2. Supera cuota diaria: pts fijos por cada día que SUPERA (venta > cuota)
                    dias_supera = grp_d["Venta_Dia"] > cd_col
                    pd_extra    = int(dias_supera.sum()) * pts_extra_u

                # Agrupar por semana del mes: día 1-7=sem1, 8-14=sem2, etc.
                grp_d["_semana"] = grp_d["Fecha"].dt.day.apply(lambda d: (d - 1) // 7 + 1)
                ventas_sem = grp_d.groupby("_semana")["Venta_Dia"].sum()

                # 3. Semana >= 100% cuota semanal
                if cuota_sem > 0:
                    semanas_ok = (ventas_sem >= cuota_sem).sum()
                    pd_semanal = int(semanas_ok) * pts_sem_u

                # 5. Semana N > Venta semana N mes anterior (Semanal_MesAnt)
                #    Si no hay datos exactos por semana, usar promedio como fallback
                if _tiene_sem_ant:
                    # Comparación semana-a-semana exacta (semana 1 vs semana 1, etc.)
                    for _s_num, _v_sem in ventas_sem.items():
                        _ref = _sem_ant_map.get((gestor, producto, int(_s_num)), None)
                        if _ref is not None and _v_sem > _ref:
                            pd_mes_ant += pts_ant_u
                elif prom_sem_ant > 0:
                    # Fallback: comparar vs promedio si no hay datos exactos
                    semanas_vs_ant = (ventas_sem > prom_sem_ant).sum()
                    pd_mes_ant     = int(semanas_vs_ant) * pts_ant_u

        # 4. Mes >= 100% cuota mensual — DESHABILITADO por solicitud del cliente.
        #    No se otorga bonus por llegar al 100% del mes.
        pd_mensual = 0

        total = pd_diario + pd_extra + pd_semanal + pd_mensual + pd_mes_ant

        filas.append({
            "Gestor":          gestor,
            "Producto":        producto,
            "PD_Diario":       pd_diario,
            "PD_Extra":        pd_extra,
            "PD_Semanal":      pd_semanal,
            "PD_Mensual":      pd_mensual,
            "PD_MesAnt":       pd_mes_ant,
            "PD_UR":           0,
            "Puntos_Producto": total,
            # Debug: valores usados para PD_Mensual
            "_VentaRealAcum":  round(venta_m_real, 2),
            "_CuotaMes":       round(cuota_m, 2),
        })

    if not filas:
        cols = ["Gestor","Producto","PD_Diario","PD_Extra","PD_Semanal",
                "PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto",
                "_VentaRealAcum","_CuotaMes"]
        return pd.DataFrame(columns=cols)

    df_pts = pd.DataFrame(filas)

    # 6. UR Prepago: cumplimiento >= 55 %
    prepago_m = df_mensual[df_mensual["Producto"] == "Prepago"][["Gestor","Cuota","Venta"]].copy()
    prepago_m["_cumpl_pre"] = (prepago_m["Venta"] /
                                prepago_m["Cuota"].replace(0, float("nan")))
    ur_map = (
        prepago_m.set_index("Gestor")["_cumpl_pre"]
        .apply(lambda x: PTS_UR if pd.notna(x) and x >= UR_UMBRAL else 0)
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

def _semaforo_emoji(pct):
    """Emoji semáforo: 🟢 ≥100%, 🟡 ≥80%, 🔴 <80%."""
    try:
        p = float(pct)
    except Exception:
        return "⚪"
    if p >= 100: return "🟢"
    elif p >= 80: return "🟡"
    else:        return "🔴"

def _pivot_to_html(pv, index_col, prods):
    """Renderiza un DataFrame MultiIndex como tabla HTML con estilo gerencial.
    Espera que (p, 'Proy%') ya esté pre-calculado en pv."""
    CELL = (
        "padding:7px 12px;border:1px solid #BFCDE0;"
        "color:#0A2A5E;font-size:12.5px;text-align:right;"
        "background:#F5F7FB;"
    )
    PROY_CELL = (
        "padding:7px 12px;border:1px solid #BFCDE0;"
        "font-size:13px;text-align:center;"
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
    # Fila 1: productos (span 4 cada uno) + celda índice
    header1 = f'<th style="{HEAD_TOP};text-align:left;" rowspan="2">{index_col}</th>'
    for p in prods:
        if p in [c[0] for c in pv.columns]:
            header1 += f'<th style="{HEAD_TOP}" colspan="4">{p}</th>'
    rows_html.append(f"<tr>{header1}</tr>")

    # Fila 2: sub-columnas
    header2 = ""
    for p in prods:
        if p in [c[0] for c in pv.columns]:
            for m in ["Cuota", "Ventas", "Cumpl%", "Proy%"]:
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
            # Proy% pre-calculado con datos mensuales
            proy_raw = pv.loc[idx, (p,"Proy%")] if (p,"Proy%") in pv.columns else 0
            try:
                cu_n = int(cuota) if pd.notna(cuota) else 0
                ve_n = int(venta)  if pd.notna(venta)  else 0
                cm_n = int(cumpl)  if pd.notna(cumpl)  else 0
                pr_n = int(proy_raw) if pd.notna(proy_raw) else 0
            except Exception:
                cu_n, ve_n, cm_n, pr_n = 0, 0, 0, 0
            sem = _semaforo_emoji(pr_n)
            cols_td += f'<td style="{CELL}">{cu_n if pd.notna(cuota) else "-"}</td>'
            cols_td += f'<td style="{CELL}">{ve_n if pd.notna(venta) else "-"}</td>'
            cols_td += f'<td style="{CELL}">{cm_n if pd.notna(cumpl) else "-"}%</td>'
            cols_td += f'<td style="{PROY_CELL}">{sem} {pr_n}%</td>'
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
    HEAD1  = "padding:7px 12px;background:#0A2A5E;color:#FFF;font-size:11px;font-weight:700;text-align:center;border:1px solid #1565C0;text-transform:uppercase;letter-spacing:0.5px;"
    HEAD2  = "padding:5px 10px;background:#0B5ED7;color:#FFF;font-size:10.5px;font-weight:700;text-align:center;border:1px solid #1976D2;"
    THEAD1 = "padding:7px 12px;background:#7B3F00;color:#FFD97A;font-size:11px;font-weight:800;text-align:center;border:2px solid #C9982A;text-transform:uppercase;letter-spacing:0.5px;"
    THEAD2 = "padding:5px 10px;background:#9B5200;color:#FFD97A;font-size:10.5px;font-weight:700;text-align:center;border:1px solid #C9982A;"
    TCELL  = "padding:7px 11px;border:2px solid #C9982A;font-size:12.5px;text-align:right;background:#FFFBF0;font-weight:700;"

    # Proyección mensual
    import calendar as _cal_reg
    _hoy_reg  = date.today()
    _dia_reg  = max(_hoy_reg.day, 1)
    _nmes_reg = _cal_reg.monthrange(_hoy_reg.year, _hoy_reg.month)[1]

    # Cabecera — columna TOTAL primero, luego productos
    h1 = f'<th style="{HEAD1};text-align:left" rowspan="2">{label_idx.upper()}</th>'
    h2 = ""
    for p in avail:
        h1 += f'<th style="{HEAD1}" colspan="4">{p}</th>'
        for m in ["Cuota", "Ventas", "Cumpl%", "Proy%"]:
            h2 += f'<th style="{HEAD2}">{m}</th>'
    thead = f"<thead><tr>{h1}</tr><tr>{h2}</tr></thead>"

    def _celdas(pv, ix, cel, modo):
        out = ""
        # ── Columnas por producto ────────────────────────────────────────────
        for p in avail:
            cu = pv.loc[ix, (p, "Cuota")]  if (p, "Cuota")  in pv.columns else 0
            ve = pv.loc[ix, (p, "Ventas")] if (p, "Ventas") in pv.columns else 0
            cm = pv.loc[ix, (p, "Cumpl%")] if (p, "Cumpl%") in pv.columns else 0
            try:   cm_n = float(str(cm).replace("%", ""))
            except: cm_n = 0
            try:   cu_n = int(cu) if pd.notna(cu) else 0
            except: cu_n = 0
            try:   ve_n = int(ve) if pd.notna(ve) else 0
            except: ve_n = 0
            proy_pct = round(ve_n * _nmes_reg / _dia_reg * 100 / cu_n) if cu_n > 0 else 0
            sem_p    = _semaforo_emoji(proy_pct)
            out += f'<td style="{cel}">{cu_n if pd.notna(cu) else "-"}</td>'
            out += f'<td style="{cel}">{ve_n if pd.notna(ve) else "-"}</td>'
            out += f'<td style="{cel}">{int(cm_n) if pd.notna(cm) else "-"}%</td>'
            out += f'<td style="{cel}font-size:14px;text-align:center;">{sem_p} {proy_pct}%</td>'
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
            # gestores cuyo departamento pertenece a la región — orden A-Z sin distinción may/min
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
            ], key=lambda x: x.lower())
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
    sem["Pts_Sem"]     = sem.apply(
        lambda r: PTS_CUOTA_SEMANAL.get(r["Producto"], 10) if r["Cumpl_Sem_%"] >= 100 else 0,
        axis=1)

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

    sem["Pts_vs_Ant"]    = sem.apply(
        lambda r: PTS_MES_ANTERIOR.get(r["Producto"], 15) if r["Ventas_Sem"] > r["Venta_Ant_Sem"] else 0,
        axis=1)
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
                    "CuotaDiaria": round(cd, 0),
                })
    df_diario = pd.DataFrame(rows_d)
    return df_mensual, df_diario

# ============================================================================
# PERSISTENCIA CSV + SESSION STATE — Registro Diario
# Compatible con Streamlit Cloud y servidores locales.
# Primario: CSV en disco (persiste entre sesiones en servidores).
# Fallback: st.session_state (persiste en la sesión actual).
# ============================================================================
CSV_PATH      = "ventas_registro.csv"
DNI_PATH      = "gestores_dni.csv"
PDV_PATH      = "pdv_cumplimiento.json"
GITHUB_REPO   = "andreezea/incentivo---polla-gestores-jul26"
GITHUB_BRANCH = "main"

# ── GitHub helpers ────────────────────────────────────────────────────────────
def _gh_headers() -> dict:
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
    except Exception:
        token = ""
    if not token:
        return {}
    return {"Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"}

def _gh_get_file(path: str):
    """Retorna (contenido_str, sha) o (None, None) si falla."""
    import requests, base64
    hdrs = _gh_headers()
    if not hdrs:
        return None, None
    url = (f"https://api.github.com/repos/{GITHUB_REPO}"
           f"/contents/{path}?ref={GITHUB_BRANCH}")
    try:
        r = requests.get(url, headers=hdrs, timeout=8)
        if r.status_code == 200:
            data = r.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content, data.get("sha")
    except Exception:
        pass
    return None, None

def _gh_put_file(path: str, content_str: str, message: str):
    """Crea o actualiza un archivo en el repositorio GitHub."""
    import requests, base64
    hdrs = _gh_headers()
    if not hdrs:
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    encoded = base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
    try:
        r = requests.get(url, headers=hdrs, timeout=8)
        sha = r.json().get("sha") if r.status_code == 200 else None
    except Exception:
        sha = None
    payload = {"message": message, "content": encoded, "branch": GITHUB_BRANCH}
    if sha:
        payload["sha"] = sha
    try:
        requests.put(url, headers=hdrs, json=payload, timeout=15)
    except Exception:
        pass

# ── Excel ↔ GitHub (persistencia permanente del archivo de datos) ─────────────
GITHUB_EXCEL_PATH = "datos_incentivos.xlsx"

def cargar_excel_desde_github() -> bytes | None:
    """Descarga el Excel de datos desde GitHub. Retorna bytes o None."""
    import requests, base64 as _b64
    hdrs = _gh_headers()
    if not hdrs:
        return None
    url = (f"https://api.github.com/repos/{GITHUB_REPO}"
           f"/contents/{GITHUB_EXCEL_PATH}?ref={GITHUB_BRANCH}")
    try:
        r = requests.get(url, headers=hdrs, timeout=20)
        if r.status_code == 200:
            return _b64.b64decode(r.json()["content"])
    except Exception:
        pass
    return None

def guardar_excel_en_github(excel_bytes: bytes) -> bool:
    """Sube el Excel a GitHub. Retorna True si OK."""
    import requests, base64 as _b64
    hdrs = _gh_headers()
    if not hdrs:
        return False
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_EXCEL_PATH}"
    try:
        r   = requests.get(url, headers=hdrs, timeout=10)
        sha = r.json().get("sha") if r.status_code == 200 else None
    except Exception:
        sha = None
    payload = {
        "message": f"Datos incentivo {date.today().isoformat()}",
        "content": _b64.b64encode(excel_bytes).decode(),
        "branch":  GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha
    try:
        rp = requests.put(url, headers=hdrs, json=payload, timeout=60)
        return rp.status_code in (200, 201)
    except Exception:
        return False

def acelerador_pdv(pct: float) -> float:
    """Devuelve el multiplicador de Prepago según % de cumplimiento de PDVs."""
    if pct >= 100: return 1.2
    if pct >= 90:  return 1.1
    if pct >= 85:  return 1.0
    return 0.9

def cargar_pdv_map() -> dict:
    """Devuelve {departamento: {nuevos: pct, captura: pct}}."""
    import json
    # 1. Disco local (caché rápida)
    if os.path.exists(PDV_PATH):
        try:
            with open(PDV_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 2. GitHub (fuente persistente)
    content, _ = _gh_get_file(PDV_PATH)
    if content:
        try:
            mapa = json.loads(content)
            with open(PDV_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            return mapa
        except Exception:
            pass
    return st.session_state.get("_pdv_map", {})

def guardar_pdv_map(mapa: dict):
    """Guarda el mapa PDV en disco y en GitHub."""
    import json
    st.session_state["_pdv_map"] = mapa
    content = json.dumps(mapa, ensure_ascii=False, indent=2)
    try:
        with open(PDV_PATH, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass
    _gh_put_file(PDV_PATH, content, "Update PDV cumplimiento desde app")
_CSV_COLS = ["id","timestamp","dni","gestor","departamento",
             "producto","fecha","venta_dia","cuota_diaria"]
_DNI_COLS = ["dni","gestor","departamento"]

def _df_vacio():
    return pd.DataFrame(columns=_CSV_COLS)

def cargar_registros_db():
    """Carga registros desde CSV local, GitHub o session_state."""
    import io
    df_ss = st.session_state.get("_registros", _df_vacio())

    def _leer_csv_str(text: str):
        return pd.read_csv(io.StringIO(text), dtype={"id": int})

    # 1. Disco local
    if os.path.exists(CSV_PATH):
        try:
            df_csv = pd.read_csv(CSV_PATH, dtype={"id": int})
            if not df_ss.empty and not df_csv.empty:
                df_merged = pd.concat([df_csv, df_ss], ignore_index=True)
                return df_merged.drop_duplicates(subset=["id"]).sort_values(
                    ["fecha","timestamp"], ascending=False)
            return df_csv if not df_csv.empty else df_ss
        except Exception:
            pass

    # 2. GitHub (si el disco no tiene el archivo)
    content, _ = _gh_get_file(CSV_PATH)
    if content:
        try:
            df_gh = _leer_csv_str(content)
            with open(CSV_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            if not df_ss.empty and not df_gh.empty:
                df_merged = pd.concat([df_gh, df_ss], ignore_index=True)
                return df_merged.drop_duplicates(subset=["id"]).sort_values(
                    ["fecha","timestamp"], ascending=False)
            return df_gh if not df_gh.empty else df_ss
        except Exception:
            pass

    return df_ss

def _guardar_csv(df: pd.DataFrame):
    """Escribe el CSV en disco y lo sube a GitHub para persistencia."""
    csv_str = df.to_csv(index=False)
    try:
        with open(CSV_PATH, "w", encoding="utf-8") as f:
            f.write(csv_str)
    except Exception:
        pass
    _gh_put_file(CSV_PATH, csv_str, "Update ventas diarias desde app")

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
    Solo incluye registros del mes en curso para evitar contaminación histórica.
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
    # Filtrar solo registros del mes en curso (evita contaminación de meses anteriores)
    _hoy_dba = date.today()
    agg = agg[(agg["Fecha"].dt.year  == _hoy_dba.year) &
              (agg["Fecha"].dt.month == _hoy_dba.month)]
    return agg

# ============================================================================
# GESTIÓN DNI — mapeo DNI → Gestor
# ============================================================================
def cargar_dni_map() -> dict:
    """Devuelve {dni: {gestor, departamento}} desde disco, GitHub o session_state."""
    def _parse_csv(text: str) -> dict:
        import io
        df = pd.read_csv(io.StringIO(text), dtype=str).fillna("")
        return {str(r["dni"]).strip(): {"gestor": r["gestor"],
                                        "departamento": r["departamento"]}
                for _, r in df.iterrows()}
    # 1. Disco local
    if os.path.exists(DNI_PATH):
        try:
            with open(DNI_PATH, "r", encoding="utf-8") as f:
                text = f.read()
            mapa = _parse_csv(text)
            st.session_state["_dni_map"] = mapa
            return mapa
        except Exception:
            pass
    # 2. GitHub
    content, _ = _gh_get_file(DNI_PATH)
    if content:
        try:
            mapa = _parse_csv(content)
            with open(DNI_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            st.session_state["_dni_map"] = mapa
            return mapa
        except Exception:
            pass
    return st.session_state.get("_dni_map", {})

def guardar_dni_map(mapa: dict):
    """Guarda el mapa DNI en disco, session_state y GitHub."""
    st.session_state["_dni_map"] = mapa
    rows = [{"dni": k, "gestor": v["gestor"], "departamento": v["departamento"]}
            for k, v in mapa.items()]
    df = pd.DataFrame(rows, columns=_DNI_COLS)
    csv_str = df.to_csv(index=False)
    try:
        with open(DNI_PATH, "w", encoding="utf-8") as f:
            f.write(csv_str)
    except Exception:
        pass
    _gh_put_file(DNI_PATH, csv_str, "Update gestores DNI desde app")

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
    """
    Normaliza nombres de columna:
    - Quita asteriscos y espacios extra
    - Si el nombre tiene salto de línea (ej: 'Cuota\n(Julio)'), toma solo la primera línea
      → 'Cuota\n(Julio)' → 'Cuota', 'VentaMesAnterior\n(Junio total)' → 'VentaMesAnterior'
    """
    def _limpiar(c):
        c = str(c).replace("*", "").strip()
        if "\n" in c:
            c = c.split("\n")[0].strip()
        return c
    df.columns = [_limpiar(c) for c in df.columns]
    return df

def _limpiar_texto_gestores(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia tabs y espacios extra en columnas de texto (Gestor, Departamento, Producto)."""
    for col in ["Gestor", "Departamento", "Producto"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace("\t", " ", regex=False).str.strip()
    return df

def leer_hoja(xls, sheet_name):
    """
    Lee una hoja tolerando:
      - Formato simple: encabezados en fila 1
      - Plantilla con título decorativo: encabezados en fila 3, tooltips en fila 4
    También normaliza nombres de columna (quita asteriscos, newlines).
    """
    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
    primera_col = str(df.columns[0]).upper()
    if "GESTOR" not in primera_col and primera_col not in ("GESTOR", "NAN"):
        df = pd.read_excel(xls, sheet_name=sheet_name, header=2).iloc[1:].reset_index(drop=True)
    df = normalizar_columnas(df)
    df = _limpiar_texto_gestores(df)
    return df

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
# ── es_admin desde session_state ─────────────────────────────────────────────
es_admin = st.session_state.get("es_admin", False)

# ── Carga del Excel: disco → session_state → GitHub → demo ───────────────────
# Prioridad: archivo en disco (más reciente) → cache en sesión →
#            descarga desde GitHub (persiste entre reinicios) → datos demo.
_modo_demo = False

if not os.path.exists(DATA_PATH):
    # Intentar session_state primero (rápido, sin red)
    if "excel_bytes_cache" in st.session_state:
        try:
            with open(DATA_PATH, "wb") as _f_cache:
                _f_cache.write(st.session_state["excel_bytes_cache"])
        except Exception:
            pass
    else:
        # Intentar GitHub (recupera datos tras reinicio de Streamlit Cloud)
        with st.spinner("🔄 Recuperando datos desde GitHub…"):
            _gh_bytes = cargar_excel_desde_github()
        if _gh_bytes:
            try:
                with open(DATA_PATH, "wb") as _f_gh:
                    _f_gh.write(_gh_bytes)
                st.session_state["excel_bytes_cache"] = _gh_bytes
            except Exception:
                pass

if os.path.exists(DATA_PATH):
    df_raw, df_diario, df_sem_ant = cargar_excel(DATA_PATH)
else:
    df_raw, df_diario = datos_demo()
    df_sem_ant = pd.DataFrame()
    _modo_demo = True

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

# ── Mapa DNI desde columna "DNI" del Excel Mensual (prioridad sobre GitHub JSON) ──
# Si la hoja Mensual tiene columna DNI, se usa como fuente primaria.
# El admin solo necesita llenar esa columna en el Excel — no necesita el panel GitHub.
_mapa_dni_excel = {}
if not df_raw.empty and "DNI" in df_raw.columns:
    _seen_d = set()
    for _, _r in df_raw.iterrows():
        _gest = str(_r.get("Gestor","")).strip()
        _dept = str(_r.get("Departamento","")).strip()
        _dni  = str(_r.get("DNI","")).strip()
        if _gest and _dni and _dni not in ("nan","None","") and _dni not in _seen_d:
            _mapa_dni_excel[_dni] = {"gestor": _gest, "departamento": _dept}
            _seen_d.add(_dni)

# ── Filtrar filas instrucción / cabeceras coladas en la hoja Diario ───────────
# El template tiene textos de ayuda en el área de datos (ej: "Fecha: DD/MM/YYYY…").
# Se filtran conservando solo filas cuyo Producto esté en PRODUCTOS_ORDEN
# Y cuyo Gestor coincida con alguno de la hoja Mensual.
if not df_diario.empty:
    _mask_prod = df_diario["Producto"].isin(PRODUCTOS_ORDEN)
    if "Gestor" in df_raw.columns:
        _valid_gest = set(df_raw["Gestor"].dropna().unique())
        _mask_prod  = _mask_prod & df_diario["Gestor"].isin(_valid_gest)
    df_diario = df_diario[_mask_prod].reset_index(drop=True)

# ── Merge datos SQLite (Registro Diario) → df_diario ─────────────────────────
# Regla de prioridad: Excel Diario > SQLite (app).
# Si el Excel ya tiene un registro para Gestor+Producto+Fecha, ese gana.
# Solo se usan los registros SQLite para fechas que NO están en el Excel.
df_diario_sqlite = db_a_diario(df_raw)
if not df_diario_sqlite.empty:
    if not df_diario.empty:
        # Normalizar fechas a YYYY-MM-DD para evitar "2026-07-01 00:00:00" vs "2026-07-01"
        excel_keys = set(
            zip(df_diario["Gestor"].astype(str),
                df_diario["Producto"].astype(str),
                pd.to_datetime(df_diario["Fecha"]).dt.strftime("%Y-%m-%d"))
        )
        def _sqlite_key(r):
            try:
                d = pd.Timestamp(r["Fecha"]).strftime("%Y-%m-%d")
            except Exception:
                d = str(r["Fecha"])[:10]
            return (str(r["Gestor"]), str(r["Producto"]), d) in excel_keys
        mask_nuevas = ~df_diario_sqlite.apply(_sqlite_key, axis=1)
        df_diario = pd.concat([df_diario, df_diario_sqlite[mask_nuevas]], ignore_index=True)
    else:
        df_diario = df_diario_sqlite

# ── Cuota diaria dinámica: (Cuota − ventas acumuladas hasta ayer) / días hábiles restantes ──
def calcular_cuota_diaria_historica(df_diario: pd.DataFrame,
                                     df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Asigna a cada fila de df_diario su CuotaDiaria correcta según el día exacto:
        CuotaDiaria_dia_N = (Cuota_mensual - ventas_acum_días_anteriores) / dias_restantes_del_mes
    donde dias_restantes = dias_del_mes - dia_del_mes + 1  (días calendario)
    Esto garantiza que día 1 = cuota/31, día 2 = (cuota-v1)/30, etc.
    """
    import calendar as _cal_hist
    if df_diario.empty or df_raw.empty:
        return df_diario
    cuota_map = (df_raw.drop_duplicates(["Gestor", "Producto"])
                 .set_index(["Gestor", "Producto"])["Cuota"].to_dict())
    df = df_diario.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    grupos = []
    for (gestor, producto), grp in df.groupby(["Gestor", "Producto"]):
        cuota_m = float(cuota_map.get((gestor, producto), 0))
        grp     = grp.sort_values("Fecha").reset_index(drop=True)
        acum    = 0.0
        nuevas  = []
        for _, row in grp.iterrows():
            dia        = int(row["Fecha"].day)
            n_dias_mes = _cal_hist.monthrange(int(row["Fecha"].year),
                                              int(row["Fecha"].month))[1]
            dias_rest   = max(1, n_dias_mes - dia + 1)
            cuota_rest  = max(0.0, cuota_m - acum)
            row         = row.copy()
            row["CuotaDiaria"] = round(cuota_rest / dias_rest, 1)
            nuevas.append(row)
            acum += float(row["Venta_Dia"])
        grupos.append(pd.DataFrame(nuevas))
    if not grupos:
        return df_diario
    return pd.concat(grupos, ignore_index=True)


def calcular_cuota_diaria_dinamica(df_mensual: pd.DataFrame,
                                   df_diario_: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaza CuotaDiaria del Excel (fila Mensual) por el valor de HOY:
        CuotaDiaria = (Cuota − Ventas acumuladas hasta ayer) / días calendario restantes
    Usa días calendario (no hábiles) para ser consistente con la división mensual.
    """
    import calendar as _cal_din
    hoy     = date.today()
    ayer    = hoy - timedelta(days=1)
    if hoy.month < 12:
        fin_mes = date(hoy.year, hoy.month + 1, 1) - timedelta(days=1)
    else:
        fin_mes = date(hoy.year, 12, 31)

    # Días calendario restantes incluyendo hoy
    dias_restantes = max(1, (fin_mes - hoy).days + 1)

    if not df_diario_.empty and "Fecha" in df_diario_.columns:
        acum = (df_diario_[df_diario_["Fecha"] <= pd.Timestamp(ayer)]
                .groupby(["Gestor", "Producto"])["Venta_Dia"]
                .sum().reset_index()
                .rename(columns={"Venta_Dia": "_Acum"}))
    else:
        acum = pd.DataFrame(columns=["Gestor", "Producto", "_Acum"])

    df_m = df_mensual.copy()
    df_m = df_m.merge(acum, on=["Gestor", "Producto"], how="left")
    df_m["_Acum"]       = df_m["_Acum"].fillna(0)
    df_m["CuotaDiaria"] = ((df_m["Cuota"] - df_m["_Acum"]).clip(lower=0)
                           / dias_restantes).round(1)
    return df_m.drop(columns=["_Acum"])

df_raw = calcular_cuota_diaria_dinamica(df_raw, df_diario)

# ── CuotaDiaria histórica: día N = (cuota - acum_anterior) / días_restantes ──
# Cada fila de df_diario recibe la cuota que correspondía ESE día exacto.
# Día 1 = cuota/31, Día 2 = (cuota-v1)/30, etc.  (días calendario)
if not df_diario.empty:
    df_diario = calcular_cuota_diaria_historica(df_diario, df_raw)

# ── Rellenar Venta mensual desde Diario cuando el Mensual trae NaN ───────────
# El Excel usa fórmulas que a veces no se calculan → Venta queda NaN.
# En ese caso usamos el acumulado real de la hoja Diario.
if not df_diario.empty and "Venta_Dia" in df_diario.columns:
    _venta_acum = (df_diario.groupby(["Gestor","Producto"])["Venta_Dia"]
                             .sum().reset_index()
                             .rename(columns={"Venta_Dia": "_VentaAcum"}))
    df_raw = df_raw.merge(_venta_acum, on=["Gestor","Producto"], how="left")
    _mask_v = df_raw["Venta"].isna() | (df_raw["Venta"] == 0)
    df_raw.loc[_mask_v, "Venta"] = df_raw.loc[_mask_v, "_VentaAcum"].fillna(0)
    df_raw = df_raw.drop(columns=["_VentaAcum"])

# ── Agregar gestores del mapa DNI que no están en el Excel ───────────────────
# Permite que aparezcan en "Detalle por Producto" con cuota y ventas en 0
_mapa_dni_base = cargar_dni_map()
if _mapa_dni_base:
    _gestores_excel = set(df_raw["Gestor"].unique()) if "Gestor" in df_raw.columns else set()
    _nuevos = [
        {"Gestor": v["gestor"], "Departamento": v["departamento"],
         "Mes": "", "Producto": p,
         "Cuota": 0, "Venta": 0, "VentaMesAnterior": 0,
         "CuotaDiaria": 0, "VentaDiaria": 0.0}
        for dni, v in _mapa_dni_base.items()
        if v["gestor"] not in _gestores_excel
        for p in PRODUCTOS_ORDEN
    ]
    if _nuevos:
        df_raw = pd.concat([df_raw, pd.DataFrame(_nuevos)], ignore_index=True)

# ── Procesar base ────────────────────────────────────────────────────────────
df = procesar(df_raw)

# ── Calcular nuevo motor por producto ────────────────────────────────────────
df_pts_prod = calcular_puntos_producto(df_raw, df_diario, df_sem_ant)

# ── Merge y actualizar Total_Puntos ──────────────────────────────────────────
COLS_PROD = ["PD_Diario","PD_Extra","PD_Semanal","PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto",
             "_VentaRealAcum","_CuotaMes"]
if not df_pts_prod.empty:
    _merge_cols = [c for c in ["Gestor","Producto"] + COLS_PROD if c in df_pts_prod.columns]
    df = df.merge(df_pts_prod[_merge_cols],
                  on=["Gestor","Producto"], how="left")
else:
    for c in COLS_PROD:
        df[c] = 0

# Columnas de puntos enteros; columnas debug como float
_COLS_INT   = ["PD_Diario","PD_Extra","PD_Semanal","PD_Mensual","PD_MesAnt","PD_UR","Puntos_Producto"]
_COLS_FLOAT = ["_VentaRealAcum","_CuotaMes"]
for c in _COLS_INT:
    if c in df.columns:
        df[c] = df[c].fillna(0).astype(int)
for c in _COLS_FLOAT:
    if c in df.columns:
        df[c] = df[c].fillna(0).astype(float)

# ── Acelerador PDV: multiplica Puntos_Producto de Prepago ────────────────────
_pdv_map_global = cargar_pdv_map()
if _pdv_map_global and "Departamento" in df.columns:
    def _mult_prepago(row):
        if row.get("Producto") != "Prepago":
            return row["Puntos_Producto"]
        dept = row.get("Departamento", "")
        cfg  = _pdv_map_global.get(dept, {})
        mn   = acelerador_pdv(float(cfg.get("nuevos",  0)))
        mc   = acelerador_pdv(float(cfg.get("captura", 0)))
        mult = round((mn + mc) / 2, 3)
        return round(row["Puntos_Producto"] * mult)
    df["Puntos_Producto"] = df.apply(_mult_prepago, axis=1)

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

# Total = exactamente la suma de los 6 criterios del motor (trazable)
df["Total_Puntos"] = df["Puntos_Producto"]

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

# ── Descarga de puntos (solo admin) ────────────────────────────────────────
if st.session_state.get("es_admin"):
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 📥 Descargar Puntos")
    if "_puntos_excel_bytes" not in st.session_state:
        if st.sidebar.button("🔄 Preparar Excel de puntos",
                             key="btn_prep_pts_sb", use_container_width=True):
            import io as _io_sb, calendar as _cal_sb
            _buf_sb    = _io_sb.BytesIO()
            _hoy_sb    = date.today()
            _n_dias_sb = _cal_sb.monthrange(_hoy_sb.year, _hoy_sb.month)[1]
            _n_sem_sb  = (_n_dias_sb - 1) // 7 + 1
            try:
                with pd.ExcelWriter(_buf_sb, engine="openpyxl") as _wr_sb:

                    # ── Hoja 1: Resumen por Gestor ────────────────────────────
                    _res = df.groupby(["Gestor","Departamento"]).agg(**AGG_COLS).reset_index()
                    _res["Cumpl%"] = (_res["Venta"] / _res["Cuota"] * 100).round(1)
                    _res = _res.sort_values("Total_Puntos", ascending=False).reset_index(drop=True)
                    _res.insert(0, "Puesto", range(1, len(_res)+1))
                    _res = _res.rename(columns={
                        "Venta":"Ventas","Cuota":"Meta",
                        "PD_Diario":  "Cumple cuota diaria",
                        "PD_Extra":   "Supera cuota diaria",
                        "PD_Semanal": "Semana>=100% cuota",
                        "PD_Mensual": "Mes>=100% cuota",
                        "PD_MesAnt":  "Semana>prom.mes ant.",
                        "PD_UR":      "UR Prepago",
                        "Total_Puntos":"TOTAL PTS",
                    })
                    _cols_res = ["Puesto","Gestor","Departamento","Meta","Ventas","Cumpl%",
                                 "Cumple cuota diaria","Supera cuota diaria",
                                 "Semana>=100% cuota","Mes>=100% cuota",
                                 "Semana>prom.mes ant.","UR Prepago","TOTAL PTS"]
                    _res[[c for c in _cols_res if c in _res.columns]].to_excel(
                        _wr_sb, sheet_name="Resumen Gestores", index=False)

                    # ── Hoja 2: Detalle Diario ────────────────────────────────
                    if not df_diario.empty:
                        _dd = df_diario.copy()
                        _dd["Fecha"] = pd.to_datetime(_dd["Fecha"]).dt.strftime("%Y-%m-%d")
                        # Cuota diaria desde df_raw
                        _cmap = (df_raw.drop_duplicates(["Gestor","Producto"])
                                 .set_index(["Gestor","Producto"])["CuotaDiaria"].to_dict())
                        _dd["Cuota_Diaria"] = _dd.apply(
                            lambda r: _cmap.get((r["Gestor"], r["Producto"]), 0), axis=1)
                        _dd["Cumpl_Dia%"]   = (_dd["Venta_Dia"] /
                                                _dd["Cuota_Diaria"].replace(0, float("nan")) * 100).round(1).fillna(0)
                        _dd["Cumple"]       = _dd.apply(
                            lambda r: "Sí" if r["Venta_Dia"] >= r["Cuota_Diaria"] else "No", axis=1)
                        # Puntos diarios
                        _pts_dia_map  = PTS_CUOTA_DIARIA
                        _pts_ext_map  = PTS_EXTRA_DIARIA
                        _dd["Pts_Cumple"]  = _dd.apply(
                            lambda r: _pts_dia_map.get(r["Producto"],2) if r["Cumple"]=="Sí" else 0, axis=1)
                        _dd["Extra_Uds"]   = _dd.apply(
                            lambda r: max(0, r["Venta_Dia"] - r["Cuota_Diaria"]) if r["Cumple"]=="Sí" else 0, axis=1)
                        _dd["Pts_Extra"]   = _dd.apply(
                            lambda r: _pts_ext_map.get(r["Producto"], 3) if r["Venta_Real"] > r["Cuota_Diaria"] else 0,
                            axis=1)
                        _dd = _dd.rename(columns={"Venta_Dia":"Venta_Real"})
                        _cols_dd = ["Gestor","Departamento","Producto","Fecha",
                                    "Cuota_Diaria","Venta_Real","Cumpl_Dia%",
                                    "Cumple","Pts_Cumple","Extra_Uds","Pts_Extra"]
                        _dd[[c for c in _cols_dd if c in _dd.columns]].sort_values(
                            ["Gestor","Producto","Fecha"]).to_excel(
                            _wr_sb, sheet_name="Detalle Diario", index=False)

                    # ── Hoja 3: Detalle Semanal ───────────────────────────────
                    if not df_diario.empty:
                        _ds = df_diario.copy()
                        _ds["Semana"] = pd.to_datetime(_ds["Fecha"]).dt.day.apply(
                            lambda d: (d - 1) // 7 + 1)
                        # cuota mensual por gestor×producto
                        _cmes_map = (df_raw.drop_duplicates(["Gestor","Producto"])
                                     .set_index(["Gestor","Producto"])["Cuota"].to_dict())
                        _vant_map = (df_raw.drop_duplicates(["Gestor","Producto"])
                                     .set_index(["Gestor","Producto"])["VentaMesAnterior"].to_dict()
                                     if "VentaMesAnterior" in df_raw.columns else {})
                        _sem_agg = (_ds.groupby(["Gestor","Departamento","Producto","Semana"])
                                    ["Venta_Dia"].sum().reset_index()
                                    .rename(columns={"Venta_Dia":"Venta_Semanal"}))
                        _sem_agg["Cuota_Semanal"] = _sem_agg.apply(
                            lambda r: round(_cmes_map.get((r["Gestor"],r["Producto"]),0)/_n_sem_sb,1)
                            if _n_sem_sb>0 else 0, axis=1)
                        _sem_agg["Cumpl_Sem%"] = (_sem_agg["Venta_Semanal"] /
                            _sem_agg["Cuota_Semanal"].replace(0,float("nan"))*100).round(1).fillna(0)
                        _sem_agg["Cumple_100%"] = _sem_agg.apply(
                            lambda r: "Sí" if r["Venta_Semanal"]>=r["Cuota_Semanal"] else "No", axis=1)
                        _sem_agg["Pts_Semana"] = _sem_agg.apply(
                            lambda r: PTS_CUOTA_SEMANAL.get(r["Producto"], 10) if r["Cumple_100%"]=="Sí" else 0,
                            axis=1)
                        _sem_agg["Prom_Sem_MesAnt"] = _sem_agg.apply(
                            lambda r: round(_vant_map.get((r["Gestor"],r["Producto"]),0)/_n_sem_sb,1)
                            if _n_sem_sb>0 else 0, axis=1)
                        _sem_agg["Supera_Prom_Ant"] = _sem_agg.apply(
                            lambda r: "Sí" if (r["Prom_Sem_MesAnt"]>0 and
                                               r["Venta_Semanal"]>r["Prom_Sem_MesAnt"]) else "No",
                            axis=1)
                        _sem_agg["Pts_Crecimiento"] = _sem_agg.apply(
                            lambda r: PTS_MES_ANTERIOR.get(r["Producto"], 15) if r["Supera_Prom_Ant"]=="Sí" else 0,
                            axis=1)
                        _sem_agg.sort_values(["Gestor","Producto","Semana"]).to_excel(
                            _wr_sb, sheet_name="Detalle Semanal", index=False)

            except Exception as _e_sb:
                pass
            _buf_sb.seek(0)
            st.session_state["_puntos_excel_bytes"] = _buf_sb.read()
            st.rerun()
    else:
        st.sidebar.download_button(
            label="📥 Descargar Excel de puntos",
            data=st.session_state["_puntos_excel_bytes"],
            file_name=f"Puntos_Fanero_{date.today().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="btn_dl_pts_sidebar",
        )
        if st.sidebar.button("🔁 Actualizar datos",
                             key="btn_regen_pts", use_container_width=True):
            del st.session_state["_puntos_excel_bytes"]
            st.rerun()

# ============================================================================
# MENÚ ☰ — esquina superior derecha (Admin · Configuración · Gestores DNI)
# ============================================================================
_col_sp, _col_menu = st.columns([9, 1])
with _col_menu:
    with st.popover("☰", use_container_width=True):

        # ─── Administrador ────────────────────────────────────────────────────
        st.markdown("##### 🔐 Administrador")
        if not st.session_state.get("es_admin"):
            _pwd = st.text_input("Contraseña", type="password", key="admin_pwd_top")
            if st.button("Entrar", key="btn_admin_enter", use_container_width=True):
                if _pwd == ADMIN_PASSWORD:
                    st.session_state["es_admin"] = True
                    st.rerun()
                elif _pwd:
                    st.error("Contraseña incorrecta")
        else:
            st.success("✅ Modo administrador activo")
            if st.button("🔓 Cerrar sesión", key="logout_top", use_container_width=True):
                st.session_state["es_admin"] = False
                st.rerun()

        # ─── Configuración y Gestores DNI (solo admin) ───────────────────────
        if st.session_state.get("es_admin"):
            st.markdown("---")
            st.markdown("##### ⚙️ Configuración")
            _fu = st.file_uploader("Archivo .xlsx", type=["xlsx"], key="fu_hamburger")
            if _fu is not None:
                _fu_bytes = _fu.read()
                st.session_state["excel_bytes_cache"] = _fu_bytes   # persiste en sesión
                with open(DATA_PATH, "wb") as _f:
                    _f.write(_fu_bytes)
                # ── Subir a GitHub para persistir entre reinicios ─────────────
                with st.spinner("Sincronizando con GitHub…"):
                    _gh_ok = guardar_excel_en_github(_fu_bytes)
                if _gh_ok:
                    st.success("✅ Datos guardados y sincronizados con GitHub ✓")
                else:
                    st.warning("⚠️ Guardado local OK · GitHub no disponible (revisa GITHUB_TOKEN en Secrets)")
                st.rerun()
            if os.path.exists(DATA_PATH):
                import time as _time
                _mod = os.path.getmtime(DATA_PATH)
                _fecha_mod = date.fromtimestamp(_mod).strftime("%d/%m/%Y %H:%M")
                st.caption(f"📂 Cargado el {_fecha_mod}")
                if _mapa_dni_excel:
                    st.success(f"✅ {len(_mapa_dni_excel)} DNIs leídos desde columna Excel")

            st.markdown("---")
            st.markdown("##### 👥 Gestores · DNI")
            mapa_dni = cargar_dni_map()
            if mapa_dni:
                df_mapa_sb = pd.DataFrame(
                    [{"DNI": k, "Nombre": v["gestor"], "Depto": v["departamento"]}
                     for k, v in mapa_dni.items()])
                st.dataframe(df_mapa_sb, hide_index=True, use_container_width=True)
            else:
                st.caption("Sin gestores registrados aún.")
            st.markdown("**Agregar gestor**")
            _deptos_validos = sorted([d for deptos in REGIONES.values() for d in deptos])
            sb_dni  = st.text_input("DNI", key="sb_dni_add", max_chars=15)
            sb_gst  = st.text_input("Nombre completo", key="sb_gst_txt")
            sb_dept = st.selectbox("Departamento", _deptos_validos, key="sb_dept_sel")
            _region_preview = DEPTO_A_REGION.get(sb_dept, "—")
            st.caption(f"Región: {_region_preview}")
            if st.button("➕ Agregar gestor", key="btn_add_dni_sb"):
                if sb_dni.strip() and sb_gst.strip():
                    mapa_dni[sb_dni.strip()] = {"gestor": sb_gst.strip(), "departamento": sb_dept}
                    guardar_dni_map(mapa_dni)
                    st.success(f"✅ {sb_gst.strip()} · {sb_dept} · DNI {sb_dni.strip()}")
                    st.rerun()
                else:
                    st.error("Completa DNI y nombre.")
            if mapa_dni:
                st.markdown("**Modificar gestor**")
                dni_editar = st.selectbox(
                    "Selecciona gestor",
                    list(mapa_dni.keys()),
                    format_func=lambda d: f"{d} — {mapa_dni[d]['gestor']}",
                    key="dni_editar_sb")
                _curr = mapa_dni[dni_editar]
                _deptos_validos2 = sorted([d for deptos in REGIONES.values() for d in deptos])
                _idx_dept = (_deptos_validos2.index(_curr["departamento"])
                             if _curr["departamento"] in _deptos_validos2 else 0)
                ed_dni  = st.text_input("Nuevo DNI (deja igual si no cambia)",
                                        value=dni_editar, key="ed_dni_txt", max_chars=15)
                ed_gst  = st.text_input("Nombre completo",
                                        value=_curr["gestor"], key="ed_gst_txt")
                ed_dept = st.selectbox("Departamento", _deptos_validos2,
                                       index=_idx_dept, key="ed_dept_sel")
                st.caption(f"Región: {DEPTO_A_REGION.get(ed_dept, '—')}")
                if st.button("💾 Guardar cambios", key="btn_edit_dni_sb"):
                    if ed_dni.strip() and ed_gst.strip():
                        if ed_dni.strip() != dni_editar:
                            del mapa_dni[dni_editar]
                        mapa_dni[ed_dni.strip()] = {"gestor": ed_gst.strip(),
                                                    "departamento": ed_dept}
                        guardar_dni_map(mapa_dni)
                        st.success(f"✅ Actualizado: {ed_gst.strip()} · {ed_dept}")
                        st.rerun()
                    else:
                        st.error("Completa DNI y nombre.")

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

            # ── Acelerador PDV ─────────────────────────────────────────
            st.markdown("---")
            st.markdown("##### 📈 Acelerador PDV · Prepago")
            st.caption("% de cumplimiento de PDVs por departamento. Aplica multiplicador a Prepago.")
            _pdv_edit = cargar_pdv_map()
            _deptos_all = sorted([d for deptos in REGIONES.values() for d in deptos])
            for _dept in _deptos_all:
                _cfg = _pdv_edit.get(_dept, {"nuevos": 0.0, "captura": 0.0})
                _c1, _c2 = st.columns(2)
                _pn = _c1.number_input(
                    f"{_dept} · Nuevos %",
                    min_value=0.0, max_value=200.0,
                    value=float(_cfg.get("nuevos", 0.0)),
                    step=1.0, key=f"pdv_n_{_dept}"
                )
                _pc = _c2.number_input(
                    f"Captura %",
                    min_value=0.0, max_value=200.0,
                    value=float(_cfg.get("captura", 0.0)),
                    step=1.0, key=f"pdv_c_{_dept}"
                )
                _mn = acelerador_pdv(_pn)
                _mc = acelerador_pdv(_pc)
                _mult = round((_mn + _mc) / 2, 3)
                st.caption(f"×{_mn} · ×{_mc} → **Mult. Prepago: ×{_mult}**")
                _pdv_edit[_dept] = {"nuevos": _pn, "captura": _pc}
            if st.button("💾 Guardar PDV %", key="btn_save_pdv", use_container_width=True):
                guardar_pdv_map(_pdv_edit)
                st.success("✅ PDV guardado — recargando…")
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
    # ── Aviso modo demo / mantenimiento ──────────────────────────────────────
    if _modo_demo:
        from datetime import timezone as _tz, timedelta as _td
        _hora_peru = __import__("datetime").datetime.now(_tz(_td(hours=-5))).hour
        _en_mantenimiento = 0 <= _hora_peru < 7
        if _en_mantenimiento:
            st.info(
                "🔧 **Ventana de mantenimiento (00:00–07:00 hora Perú).**  "
                "Los datos reales estarán disponibles automáticamente a las 07:01 — "
                "el sistema los recupera desde GitHub sin intervención manual."
            )
        else:
            st.warning(
                "⚠️ **Datos de demostración** — El servidor se reinició y no se encontró el Excel. "
                "Esto no debería pasar fuera del horario 00:00–07:00. "
                "Inicia sesión como administrador (menú ≡) y sube el archivo para restaurar. "
                "Una vez subido, el app lo guardará en GitHub y **nunca más necesitarás subirlo de nuevo tras un reinicio.**"
            )
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
        import calendar as _cal_rg2
        _hoy_rg2  = date.today()
        _dia_rg2  = max(_hoy_rg2.day, 1)
        _nmes_rg2 = _cal_rg2.monthrange(_hoy_rg2.year, _hoy_rg2.month)[1]
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
                _proy_r  = round(_ventas * _nmes_rg2 / _dia_rg2 * 100 / _cuota) if _cuota > 0 else 0
                _sem_r   = _semaforo_emoji(_proy_r)
                _color_r = "#0B5ED7" if _region == "Oriente" else "#198754"
                st.markdown(f"""
                <div style="background:{_color_r}; border-radius:12px; padding:18px 20px;
                            box-shadow:0 4px 14px rgba(0,0,0,0.20); margin-bottom:10px;">
                    <div style="color:#FFD97A; font-size:17px; font-weight:800;
                                margin-bottom:10px;">🌎 Región {_region}</div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                        <div style="flex:1; min-width:65px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 10px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Gestores</div>
                            <div style="color:#fff; font-size:20px; font-weight:800;">{_gest}</div>
                        </div>
                        <div style="flex:1; min-width:65px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 10px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Cumpl.%</div>
                            <div style="color:#FFD97A; font-size:20px; font-weight:800;">{_cumpl}%</div>
                        </div>
                        <div style="flex:1; min-width:65px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 10px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Ventas</div>
                            <div style="color:#fff; font-size:20px; font-weight:800;">{_ventas:,}</div>
                        </div>
                        <div style="flex:1; min-width:65px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 10px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Proy%</div>
                            <div style="color:#fff; font-size:18px; font-weight:800;">{_sem_r} {_proy_r}%</div>
                        </div>
                        <div style="flex:1; min-width:65px; background:rgba(255,255,255,0.12);
                                    border-radius:8px; padding:10px 10px; text-align:center;">
                            <div style="color:rgba(255,255,255,0.75); font-size:10px;
                                        font-weight:700; text-transform:uppercase;">Puntos</div>
                            <div style="color:#fff; font-size:20px; font-weight:800;">{_pts:,}</div>
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

    # ── Top 10 Gestores — desglose de puntos por regla ─────────────────────────
    subheader("🎯 Top 10 — Puntos por Gestor")
    _top10 = rank.head(10).copy()

    # Stacked bar chart: desglose visual por regla
    _reglas_def = [
        ("Días cumplidos",  "PD_Diario",  "#2196F3"),
        ("Extra unidades",  "PD_Extra",   "#4CAF50"),
        ("Semana cumplida", "PD_Semanal", "#FF9800"),
        ("Mes cumplido",    "PD_Mensual", "#9C27B0"),
        ("Supera mes ant.", "PD_MesAnt",  "#E91E63"),
        ("UR Prepago",      "PD_UR",      "#009688"),
    ]
    _fig_top = go.Figure()
    for _rn, _rc, _clr in _reglas_def:
        if _rc in _top10.columns:
            _v = _top10[_rc].fillna(0).astype(int)
            _fig_top.add_trace(go.Bar(
                name=_rn,
                y=_top10["Gestor"],
                x=_v,
                orientation="h",
                marker_color=_clr,
                text=_v.apply(lambda v: str(v) if v > 0 else ""),
                textposition="inside",
                textfont=dict(color="white", size=10),
            ))
    _fig_top.update_layout(
        barmode="stack",
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="Puntos acumulados", gridcolor="#EEF2F7"),
        yaxis=dict(title="", autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=11)),
        margin=dict(t=50, b=10, l=10, r=10),
        height=max(320, len(_top10) * 38),
    )
    st.plotly_chart(_fig_top, use_container_width=True)

    # ── Tabla resumen Top 10 — HTML ──────────────────────────────────────────
    _fecha_hoy = date.today()
    _mes_str   = _fecha_hoy.strftime("%B %Y").capitalize()
    _dia_str   = _fecha_hoy.strftime("%d/%m")
    # Colores por criterio (coinciden con el stacked bar)
    _crit_cols = [
        ("Días cumplidos",  "PD_Diario",  "#2196F3"),
        ("Extra unid.",     "PD_Extra",   "#4CAF50"),
        ("Sem. cumplida",   "PD_Semanal", "#FF9800"),
        ("Mes cumplido",    "PD_Mensual", "#9C27B0"),
        ("Sup. mes ant.",   "PD_MesAnt",  "#E91E63"),
        ("UR Prepago",      "PD_UR",      "#009688"),
    ]
    _TH  = "padding:7px 10px;font-size:11px;font-weight:700;text-align:center;white-space:nowrap;border-bottom:2px solid #C8D6E5;"
    _TH2 = "padding:4px 8px;font-size:11px;font-weight:700;text-align:center;white-space:nowrap;border-bottom:2px solid #C8D6E5;"
    _TD  = "padding:6px 10px;font-size:12px;text-align:center;border-bottom:1px solid #E8EFF5;"
    _TDL = "padding:6px 10px;font-size:12px;text-align:left;border-bottom:1px solid #E8EFF5;white-space:nowrap;"
    # Cabecera
    _hdr = (
        f"<tr style='background:#0A2A5E;color:white;'>"
        f"<th style='{_TH}'>#</th>"
        f"<th style='{_TH};text-align:left;'>Gestor</th>"
        f"<th style='{_TH}'>Departamento</th>"
    )
    for _cn, _cc, _clr in _crit_cols:
        _hdr += f"<th style='{_TH2};background:{_clr}20;color:{_clr};border-left:3px solid {_clr};'>{_cn}</th>"
    _hdr += f"<th style='{_TH};background:#0B5ED7;'>TOTAL</th></tr>"
    # Filas
    _rows_html = ""
    for _ri, (_, _rr) in enumerate(_top10.iterrows(), 1):
        _bg = "#F5F8FF" if _ri % 2 == 0 else "white"
        _dep = str(_rr.get("Departamento","")).strip()
        _r = (
            f"<tr style='background:{_bg};'>"
            f"<td style='{_TD};font-weight:700;color:#0A2A5E;'>{_ri}</td>"
            f"<td style='{_TDL};font-weight:600;'>{_rr['Gestor']}</td>"
            f"<td style='{_TD};'>{_dep}</td>"
        )
        for _cn, _cc, _clr in _crit_cols:
            _v = int(_rr.get(_cc, 0) or 0)
            _txt = f"<b>{_v}</b>" if _v > 0 else "<span style='color:#CCC;'>—</span>"
            _r += f"<td style='{_TD};border-left:2px solid {_clr}30;'>{_txt}</td>"
        _tot = int(_rr.get("Total_Puntos", 0) or 0)
        _r += f"<td style='{_TD};font-weight:900;color:#0B5ED7;font-size:14px;'>{_tot}</td></tr>"
        _rows_html += _r
    _html_tbl = (
        f"<div style='margin-top:8px;'>"
        f"<div style='font-weight:700;font-size:13px;color:#0A2A5E;margin-bottom:8px;'>📋 Puntos acumulados al {_dia_str} — {_mes_str}</div>"
        f"<div style='overflow-x:auto;'>"
        f"<table style='width:100%;border-collapse:collapse;font-family:sans-serif;'>"
        f"<thead>{_hdr}</thead><tbody>{_rows_html}</tbody>"
        f"</table></div></div>"
    )
    import streamlit.components.v1 as _stc_top10
    _ht_top10 = len(_top10) * 37 + 90
    _stc_top10.html(
        f"<html><head><style>body{{margin:0;padding:0;font-family:sans-serif;}}"
        f"table{{width:100%;border-collapse:collapse;}}</style></head>"
        f"<body>{_html_tbl}</body></html>",
        height=_ht_top10, scrolling=False)

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

    subheader("🌡️ Mapa de Calor")
    _hc1, _hc2 = st.columns(2)

    # ── Izquierda: Cumplimiento % por Gestor ─────────────────────────────────
    with _hc1:
        st.markdown(
            "<div style='font-weight:700;font-size:13px;color:#0A2A5E;"
            "margin-bottom:6px;text-align:center;'>Cumplimiento % por Gestor</div>",
            unsafe_allow_html=True)
        df_pa = (
            df_f.groupby(["Gestor","Producto"])
            .agg(Venta=("Venta","sum"), Cuota=("Cuota","sum"))
            .reset_index()
        )
        df_pa["Cumplimiento_%"] = (df_pa["Venta"] / df_pa["Cuota"] * 100).round(1)
        pivot_heat = df_pa.pivot(index="Gestor", columns="Producto",
                                 values="Cumplimiento_%").fillna(0)
        cols_ok = [p for p in PRODUCTOS_ORDEN if p in pivot_heat.columns]
        fig_heat = px.imshow(
            pivot_heat[cols_ok], text_auto=".0f",
            color_continuous_scale="RdYlGn", zmin=0, zmax=150, aspect="auto",
            labels=dict(x="Producto", y="Gestor", color="Cumpl%"))
        fig_heat.update_layout(
            margin=dict(t=10, b=10, l=10, r=80),
            coloraxis_colorbar=dict(title="Cumpl%", ticksuffix="%"))
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── Derecha: Ventas absolutas por Gestor, ordenado por Departamento ─────
    with _hc2:
        st.markdown(
            "<div style='font-weight:700;font-size:13px;color:#0A2A5E;"
            "margin-bottom:6px;text-align:center;'>Ventas por Gestor (agrupado por Departamento)</div>",
            unsafe_allow_html=True)
        # Agrupar ventas por gestor × producto
        df_gv = (
            df_f.groupby(["Departamento","Gestor","Producto"])
            .agg(Venta=("Venta","sum"))
            .reset_index()
        )
        # Ordenar por Departamento luego Gestor para que queden agrupados
        _orden_gest = (
            df_gv[["Departamento","Gestor"]]
            .drop_duplicates()
            .sort_values(["Departamento","Gestor"])["Gestor"]
            .tolist()
        )
        pivot_gv = df_gv.pivot_table(
            index="Gestor", columns="Producto", values="Venta",
            aggfunc="sum", fill_value=0
        )
        # Reordenar filas agrupadas por departamento
        pivot_gv = pivot_gv.reindex([g for g in _orden_gest if g in pivot_gv.index])
        cols_gv = [p for p in PRODUCTOS_ORDEN if p in pivot_gv.columns]
        # Etiquetas del eje Y con departamento como prefijo (separador visual)
        _dep_lookup = (
            df_gv[["Gestor","Departamento"]]
            .drop_duplicates()
            .set_index("Gestor")["Departamento"]
            .to_dict()
        )
        _ytick_labels = []
        _prev_dep = None
        for _g in pivot_gv.index:
            _d = _dep_lookup.get(_g, "")
            if _d != _prev_dep:
                _ytick_labels.append(f"[{_d}] {_g}")
                _prev_dep = _d
            else:
                _ytick_labels.append(f"  {_g}")
        fig_gv = px.imshow(
            pivot_gv[cols_gv], text_auto=".0f",
            color_continuous_scale="Blues", aspect="auto",
            labels=dict(x="Producto", y="Gestor", color="Ventas"))
        fig_gv.update_yaxes(ticktext=_ytick_labels, tickvals=list(range(len(pivot_gv))))
        fig_gv.update_layout(
            margin=dict(t=10, b=10, l=10, r=80),
            height=max(350, len(pivot_gv) * 22),
            coloraxis_colorbar=dict(title="Ventas"))
        st.plotly_chart(fig_gv, use_container_width=True)

    # ── Puntos Producto por gestor y producto ────────────────────────────────
    subheader("🆕 Puntos Motor por Gestor y Producto")
    _agg_dict = dict(
        PD_Diario=("PD_Diario","sum"), PD_Extra=("PD_Extra","sum"),
        PD_Semanal=("PD_Semanal","sum"), PD_Mensual=("PD_Mensual","sum"),
        PD_MesAnt=("PD_MesAnt","sum"), PD_UR=("PD_UR","sum"),
        Puntos_Producto=("Puntos_Producto","sum"),
    )
    if "_VentaRealAcum" in df_f.columns:
        _agg_dict["VentaRealAcum_Jul"] = ("_VentaRealAcum", "sum")
    if "_CuotaMes" in df_f.columns:
        _agg_dict["CuotaMes"]          = ("_CuotaMes", "sum")
    df_motor = df_f.groupby(["Gestor","Producto"]).agg(**_agg_dict).reset_index()
    st.dataframe(df_motor, use_container_width=True, hide_index=True)
    st.caption("🔍 VentaRealAcum_Jul = suma Diario julio (usada para PD_Mensual) · CuotaMes = cuota mensual del Excel")

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

    prod_sel = st.selectbox("📦 Producto", ["Todos"] + PRODUCTOS_ORDEN, key="d_prod")

    def _safe_int(s):
        """Convierte a int ignorando NaN e inf."""
        return pd.to_numeric(s, errors="coerce").fillna(0).replace(
            [float("inf"), float("-inf")], 0).round(0).astype(int)

    # ── Base siempre desde df_raw: todos los gestores × productos con cuota ──
    # Así se ven cuotas aunque no haya ventas en Diario.
    _hoy = pd.Timestamp(date.today())
    _base_hoy = df_raw[["Gestor","Departamento","Producto","CuotaDiaria"]].copy()
    _base_hoy = _base_hoy[_base_hoy["CuotaDiaria"] > 0].copy()
    _base_hoy["Fecha"]     = _hoy
    _base_hoy["Venta_Dia"] = 0.0

    # Aplicar filtros de barra lateral
    if gestor_sel != "Todos": _base_hoy = _base_hoy[_base_hoy["Gestor"] == gestor_sel]
    if depto_sel  != "Todos": _base_hoy = _base_hoy[_base_hoy["Departamento"] == depto_sel]
    if prod_sel   != "Todos": _base_hoy = _base_hoy[_base_hoy["Producto"] == prod_sel]

    # Unir ventas reales de hoy si las hay
    if not df_diario.empty and "Fecha" in df_diario.columns:
        _ref_dia = df_diario["Fecha"].max()   # último día con datos
        _ventas_ref = (df_diario[df_diario["Fecha"] == _ref_dia]
                       .groupby(["Gestor","Producto"])["Venta_Dia"].sum()
                       .reset_index().rename(columns={"Venta_Dia":"_V"}))
        _base_hoy = _base_hoy.merge(_ventas_ref, on=["Gestor","Producto"], how="left")
        _base_hoy["Venta_Dia"] = _base_hoy["_V"].fillna(0)
        _base_hoy = _base_hoy.drop(columns=["_V"])
        _label_dia = str(_ref_dia)[:10]
    else:
        _label_dia = _hoy.strftime("%Y-%m-%d")

    # KPIs
    v_hoy  = _base_hoy["Venta_Dia"].sum()
    c_hoy  = _base_hoy["CuotaDiaria"].sum()
    cp_hoy = (v_hoy / c_hoy * 100) if c_hoy else 0
    emoji_hoy = "🟢" if cp_hoy >= 100 else ("🟡" if cp_hoy >= 80 else "🔴")

    render_kpi_row([
        {"label":"📅 Referencia",           "value": _label_dia,         "color":"#0A2A5E"},
        {"label":"Venta Total",             "value": f"{v_hoy:.0f}",     "color":"#0B5ED7"},
        {"label":"Cuota Diaria Prorrateada","value": f"{c_hoy:.0f}",     "color":"#0B5ED7"},
        {"label":f"{emoji_hoy} Cumpl. del Día",
         "value": f"{cp_hoy:.0f}%",
         "color":"#198754" if cp_hoy >= 100 else ("#B45309" if cp_hoy >= 80 else "#DC3545")},
    ])

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    # ── Tabla pivot gestores × productos ─────────────────────────────────────
    subheader(f"📋 Estado por Gestor — {_label_dia}")

    grp_h = (_base_hoy.groupby(["Gestor","Producto"])
                       .agg(Cuota=("CuotaDiaria","sum"), Venta=("Venta_Dia","sum"))
                       .reset_index())
    prods_h = [p for p in PRODUCTOS_ORDEN if p in grp_h["Producto"].unique()] \
              if prod_sel == "Todos" else [prod_sel]

    p_c = grp_h.pivot(index="Gestor", columns="Producto", values="Cuota").reindex(columns=prods_h)
    p_v = grp_h.pivot(index="Gestor", columns="Producto", values="Venta").reindex(columns=prods_h)
    p_k = (p_v / p_c * 100).round(0)

    tuples_h = [(p, m) for p in prods_h for m in ["Cuota","Ventas","Cumpl%","Proy%"]]
    pivot_h  = pd.DataFrame(index=p_c.index, columns=pd.MultiIndex.from_tuples(tuples_h))
    pivot_h.index.name = "Gestor"
    for p in prods_h:
        pivot_h[(p,"Cuota")]  = _safe_int(p_c[p])
        pivot_h[(p,"Ventas")] = _safe_int(p_v[p])
        pivot_h[(p,"Cumpl%")] = _safe_int(p_k[p])

    # Proy% con datos mensuales reales (Cuota y Venta acumulada de df_raw)
    import calendar as _cal3h
    _hoy3h   = date.today()
    _dia3h   = max(_hoy3h.day, 1)
    _nmes3h  = _cal3h.monthrange(_hoy3h.year, _hoy3h.month)[1]
    if not df_raw.empty and "Cuota" in df_raw.columns and "Venta" in df_raw.columns:
        _mens_proy = (df_raw[df_raw["Cuota"] > 0]
                      .groupby(["Gestor","Producto"])
                      .agg(_Cu=("Cuota","first"), _Ve=("Venta","sum"))
                      .reset_index())
        for _pp in prods_h:
            _mp = _mens_proy[_mens_proy["Producto"] == _pp].set_index("Gestor")
            for _gg in pivot_h.index:
                if _gg in _mp.index:
                    _cu3 = float(_mp.loc[_gg, "_Cu"])
                    _ve3 = float(_mp.loc[_gg, "_Ve"])
                    _pv3 = round(_ve3 * _nmes3h / _dia3h * 100 / _cu3) if _cu3 > 0 else 0
                else:
                    _pv3 = 0
                pivot_h.loc[_gg, (_pp, "Proy%")] = _pv3
    else:
        for _pp in prods_h:
            pivot_h[(_pp, "Proy%")] = 0

    st.markdown(_pivot_to_html(pivot_h, "Gestor", prods_h), unsafe_allow_html=True)
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Acumulado mes (solo si hay datos en Diario) ───────────────────────────
    subheader("📈 Acumulado del Mes: Ventas vs Meta")

    if df_diario.empty:
        st.info("Aún no hay ventas registradas en Diario. Las cuotas prorrateadas aparecen arriba.")
    else:
        df_d = df_diario.copy()
        if gestor_sel != "Todos": df_d = df_d[df_d["Gestor"] == gestor_sel]
        if depto_sel  != "Todos": df_d = df_d[df_d["Departamento"] == depto_sel]
        if prod_sel   != "Todos": df_d = df_d[df_d["Producto"] == prod_sel]
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
        df_dia_agg["Cumpl_Dia_%"] = (
            df_dia_agg["Venta_Dia"] / df_dia_agg["CuotaDiaria"].replace(0, float("nan")) * 100
        ).fillna(0).round(1)
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
        # Tabla día a día: cuota vs venta
        if not df_dia_agg.empty:
            _tbl = df_dia_agg.copy()
            
            _cols = [c for c in ["Fecha","Venta_Dia","CuotaDiaria","Cumpl_Dia_%"] if c in _tbl.columns]
            st.dataframe(
                _tbl[_cols].rename(columns={
                    "Venta_Dia":"Venta","CuotaDiaria":"Cuota","Cumpl_Dia_%":"Cumpl%"
                }).reset_index(drop=True),
                use_container_width=True, hide_index=True
            )

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

    # ── Lookup por DNI ────────────────────────────────────────────────────────
    # Excel DNIs tienen prioridad; GitHub JSON sirve como fallback
    mapa_dni_tab4 = {**cargar_dni_map(), **_mapa_dni_excel}
    subheader("🔑 Identificación del Gestor")
    dni_input = st.text_input("📋 Ingresa tu DNI", max_chars=15, key="dni_registro_tab4")
    gestor_activo = ""
    depto_activo  = ""

    if dni_input.strip():
        info_dni = mapa_dni_tab4.get(dni_input.strip())
        if info_dni:
            gestor_activo = info_dni["gestor"]
            depto_activo  = info_dni["departamento"]
            st.markdown(
                f"""<div style="background:#E8F5E9; border-radius:8px; padding:10px 16px;
                               border-left:5px solid #198754; margin-bottom:10px;">
                    <span style="font-size:14px; color:#155724; font-weight:700;">
                        ✅ {gestor_activo}</span>
                    <span style="color:#555; font-size:12px;"> · {depto_activo}</span>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """<div style="background:#FFF8CD; border-radius:8px; padding:10px 16px;
                               border-left:5px solid #F4C430; margin-bottom:10px;">
                    <span style="font-size:11px; color:#856404; font-weight:700;
                                 text-transform:uppercase;">⚠️ DNI no encontrado</span><br>
                    <span style="font-size:13px; color:#555;">
                        Contacta al administrador para registrar tu DNI.</span>
                </div>""",
                unsafe_allow_html=True
            )


    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    col_form, col_hoy = st.columns([3, 2])

    # ── Formulario de carga ───────────────────────────────────────────────────
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

                r2c1, r2c2 = st.columns(2)
                ventas_f       = r2c1.number_input("📊 Ventas del día *", min_value=0, step=1,
                                                    key="ventas_f_input")

                submitted_f = st.form_submit_button("💾 Guardar registro",
                                                     use_container_width=True)
                if submitted_f:
                    insertar_registro_db(
                        gestor=gestor_activo,
                        departamento=depto_activo,
                        producto=producto_sel_f,
                        fecha=fecha_f,
                        venta_dia=int(ventas_f),
                        cuota_diaria=0,
                        dni=str(dni_input).strip()
                    )
                    st.success(
                        f"✅ {int(ventas_f)} unidades de {producto_sel_f} "
                        f"guardadas para {fecha_f}"
                    )
                    st.rerun()

    # ── Panel derecho: registros de hoy ──────────────────────────────────────
    with col_hoy:
        subheader("📅 Registros de hoy")
        _hoy_dt = pd.Timestamp(date.today())
        if not df_diario.empty and "Fecha" in df_diario.columns:
            _df_hoy = df_diario[df_diario["Fecha"] == _hoy_dt]
            if gestor_activo:
                _df_hoy = _df_hoy[_df_hoy["Gestor"] == gestor_activo]
            if _df_hoy.empty:
                st.info("Sin registros para hoy.")
            else:
                _cols_show = ["Gestor","Producto","Venta_Dia","CuotaDiaria"]
                _cols_show = [c for c in _cols_show if c in _df_hoy.columns]
                st.dataframe(
                    _df_hoy[_cols_show].rename(columns={
                        "Venta_Dia":"Ventas","CuotaDiaria":"Cuota Día"
                    }).reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("Sin datos diarios cargados.")
