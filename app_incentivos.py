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
# PARÁMETROS
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

BANDAS_CRECIMIENTO = [
    (0, 9.999, 0),
    (10, 19.999, 2),
    (20, 29.999, 4),
    (30, 1e12, 6)
]

BONO_CONSISTENCIA = 5
BONO_ELITE = 5

# 🔥 AGREGAMOS DEPARTAMENTO
REQUIRED_COLS = [
    "Departamento", "Gestor", "Mes", "Cuota", "Venta", "VentaMesAnterior",
    "Sem1", "Sem2", "Sem3", "Sem4", "TodosProductos",
]

# ----------------------------------------------------------------------------
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
        (df["Venta"] - df["VentaMesAnterior"]) /
        df["VentaMesAnterior"].replace(0, pd.NA) * 100
    ).fillna(0).round(1)

    df["Bono_Crecimiento"] = df["Crecimiento_%"].apply(bono_crecimiento)

    df["Consistencia"] = df[["Sem1", "Sem2", "Sem3", "Sem4"]].apply(
        lambda r: all(str(v).strip().lower() in ("sí", "si", "yes", "true", "1") for v in r),
        axis=1
    )

    df["Bono_Consistencia"] = df["Consistencia"].map({True: BONO_CONSISTENCIA, False: 0})

    df["Elite"] = df["TodosProductos"].astype(str).str.lower().isin(["sí", "si", "yes", "true", "1"])
    df["Bono_Elite"] = df["Elite"].map({True: BONO_ELITE, False: 0})

    df["Total_Puntos"] = (
        df["Puntos_Base"] +
        df["Bono_Crecimiento"] +
        df["Bono_Consistencia"] +
        df["Bono_Elite"]
    )

    df["Semaforo"] = df["Cumplimiento_%"].apply(
        lambda p: "🟢 Verde" if p >= 100 else ("🟡 Amarillo" if p >= 80 else "🔴 Rojo")
    )

    return df


# ----------------------------------------------------------------------------
def datos_demo():
    import random
    random.seed(7)

    gestores = ["Ana Torres", "Luis Ramírez", "Carla Méndez", "Jorge Salas"]
    departamentos = ["Lima", "Arequipa", "Trujillo"]

    meses = ["Abril 2026", "Mayo 2026", "Junio 2026"]

    rows = []

    for mes in meses:
        for g in gestores:
            depto = random.choice(departamentos)

            cuota = random.randint(40000, 70000)
            venta = cuota * random.uniform(0.7, 1.6)

            venta_ant = venta * random.uniform(0.8, 1.1)

            rows.append([
                depto, g, mes,
                cuota, venta, venta_ant,
                "Sí", "Sí", "Sí", "Sí",
                random.choice(["Sí", "No"])
            ])

    return pd.DataFrame(rows, columns=REQUIRED_COLS)


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Filtros")

archivo = st.sidebar.file_uploader("📂 Cargar Excel o CSV", type=["xlsx", "csv"])

if archivo is not None:
    if archivo.name.endswith(".csv"):
        df_raw = pd.read_csv(archivo)
    else:
        df_raw = pd.read_excel(archivo)
else:
    df_raw = datos_demo()

df = procesar(df_raw)

# ----------------------------------------------------------------------------
# FILTROS JERÁRQUICOS
# ----------------------------------------------------------------------------
meses_disp = ["Todos"] + sorted(df["Mes"].unique().tolist())
mes_sel = st.sidebar.selectbox("📅 Mes", meses_disp)

depto_disp = ["Todos"] + sorted(df["Departamento"].unique().tolist())
depto_sel = st.sidebar.selectbox("🏢 Departamento", depto_disp)

df_f = df.copy()

if mes_sel != "Todos":
    df_f = df_f[df_f["Mes"] == mes_sel]

if depto_sel != "Todos":
    df_f = df_f[df_f["Departamento"] == depto_sel]

gestores_disp = ["Todos"] + sorted(df_f["Gestor"].unique().tolist())
gestor_sel = st.sidebar.selectbox("👤 Gestor", gestores_disp)

if gestor_sel != "Todos":
    df_f = df_f[df_f["Gestor"] == gestor_sel]

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.title("🏆 Sistema de Incentivo de Ventas")

c1, c2, c3 = st.columns(3)

c1.metric("Gestores", df_f["Gestor"].nunique())
c2.metric("Cumplimiento promedio", f"{df_f['Cumplimiento_%'].mean():.1f}%")
c3.metric("Puntos totales", int(df_f["Total_Puntos"].sum()))

st.markdown("---")

# ----------------------------------------------------------------------------
# TABLA FINAL
# ----------------------------------------------------------------------------
st.subheader("📊 Detalle")

cols = [
    "Departamento", "Gestor", "Mes",
    "Cuota", "Venta", "Cumplimiento_%",
    "Puntos_Base", "Bono_Crecimiento",
    "Bono_Consistencia", "Bono_Elite",
    "Total_Puntos", "Semaforo"
]

st.dataframe(df_f[cols], use_container_width=True)

st.download_button(
    "⬇️ Descargar CSV",
    df_f[cols].to_csv(index=False).encode("utf-8-sig"),
    file_name="incentivos.csv",
    mime="text/csv"
)
