# ----------------------------------------------------------------------------
# FILTROS (ACTUALIZADO)
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")

deptos_disp = ["Todos"] + sorted(df["Departamento"].unique().tolist())
depto_sel = st.sidebar.selectbox("🏢 Filtrar por departamento", deptos_disp)

gestores_disp = ["Todos"] + sorted(df["Gestor"].unique().tolist())
gestor_sel = st.sidebar.selectbox("👤 Filtrar por gestor", gestores_disp)

df_f = df.copy()

if depto_sel != "Todos":
    df_f = df_f[df_f["Departamento"] == depto_sel]

if gestor_sel != "Todos":
    df_f = df_f[df_f["Gestor"] == gestor_sel]


# ----------------------------------------------------------------------------
# TAB 1 — Ranking (ACTUALIZADO)
# ----------------------------------------------------------------------------
with tab1:
    rank = (
        df_f.groupby("Gestor")["Total_Puntos"]
        .sum()
        .reset_index()
        .sort_values("Total_Puntos", ascending=False)
    )

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
