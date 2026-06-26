# ----------------------------------------------------------------------------
# FILTROS PRO
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")

deptos_disp = ["Todos"] + sorted(df["Departamento"].unique().tolist())
depto_sel = st.sidebar.selectbox("🏢 Departamento", deptos_disp)

gestores_disp = ["Todos"] + sorted(df["Gestor"].unique().tolist())
gestor_sel = st.sidebar.selectbox("👤 Gestor", gestores_disp)

df_f = df.copy()

if depto_sel != "Todos":
    df_f = df_f[df_f["Departamento"] == depto_sel]

if gestor_sel != "Todos":
    df_f = df_f[df_f["Gestor"] == gestor_sel]


# ----------------------------------------------------------------------------
# KPIs GERENCIALES
# ----------------------------------------------------------------------------
st.markdown("## 📊 Resumen Ejecutivo")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Gestores", df_f["Gestor"].nunique())

col2.metric("📈 Cumplimiento Promedio",
            f"{df_f['Cumplimiento_%'].mean():.1f}%")

col3.metric("🏆 Total Puntos",
            int(df_f["Total_Puntos"].sum()))

# comparación vs mes anterior
venta_actual = df_f["Venta"].sum()
venta_anterior = df_f["VentaMesAnterior"].sum()

variacion = ((venta_actual - venta_anterior) / venta_anterior * 100) if venta_anterior != 0 else 0

col4.metric("🚀 Variación vs mes anterior",
            f"{variacion:.1f}%",
            delta=f"{variacion:.1f}%")


st.markdown("---")


# ----------------------------------------------------------------------------
# TOP 3 PODIO
# ----------------------------------------------------------------------------
st.markdown("## 🥇 Top Performers")

rank = (
    df_f.groupby("Gestor")["Total_Puntos"]
    .sum()
    .reset_index()
    .sort_values("Total_Puntos", ascending=False)
)

top3 = rank.head(3)

cols = st.columns(3)

for i, row in enumerate(top3.itertuples()):
    emoji = ["🥇", "🥈", "🥉"][i]
    cols[i].metric(f"{emoji} {row.Gestor}", int(row.Total_Puntos))


# ----------------------------------------------------------------------------
# RANKING PRINCIPAL
# ----------------------------------------------------------------------------
st.markdown("## 🏆 Ranking General")

rank.insert(0, "Puesto", range(1, len(rank) + 1))

colA, colB = st.columns([2, 1])

with colA:
    fig = px.bar(
        rank.sort_values("Total_Puntos"),
        x="Total_Puntos",
        y="Gestor",
        orientation="h",
        text="Total_Puntos",
        title="Ranking de puntos acumulados",
    )
    st.plotly_chart(fig, use_container_width=True)

with colB:
    st.subheader("🏆 Puntos obtenidos")
    st.dataframe(
        rank[["Puesto", "Gestor", "Total_Puntos"]],
        hide_index=True,
        use_container_width=True,
    )


# ----------------------------------------------------------------------------
# EVOLUCIÓN
# ----------------------------------------------------------------------------
st.markdown("## 📈 Evolución de desempeño")

evo = df_f.groupby("Mes")["Cumplimiento_%"].mean().reset_index()

fig2 = px.line(
    evo,
    x="Mes",
    y="Cumplimiento_%",
    markers=True,
    title="Cumplimiento promedio mensual",
)

fig2.add_hline(y=100, line_dash="dash")

st.plotly_chart(fig2, use_container_width=True)


# ----------------------------------------------------------------------------
# SEMÁFORO GERENCIAL
# ----------------------------------------------------------------------------
st.markdown("## 🚦 Estado de cumplimiento")

sem = df_f["Semaforo"].value_counts().reset_index()
sem.columns = ["Estado", "Cantidad"]

fig3 = px.pie(
    sem,
    names="Estado",
    values="Cantidad",
    color="Estado",
    color_discrete_map={
        "🟢 Verde": "green",
        "🟡 Amarillo": "gold",
        "🔴 Rojo": "red"
    }
)

st.plotly_chart(fig3, use_container_width=True)


# ----------------------------------------------------------------------------
# TABLA FINAL LIMPIA
# ----------------------------------------------------------------------------
st.markdown("## 📋 Detalle ejecutivo")

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
