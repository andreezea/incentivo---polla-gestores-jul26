st.markdown("""
<style>

/* ══════════════════════════════════════════════════
   PALETA GERENCIAL PRO — NIVEL CORPORATIVO (Power BI)
   ══════════════════════════════════════════════════ */

/* 🎯 COLORES BASE */
:root {
    --azul-primario: #0A2A5E;
    --azul-secundario: #0B5ED7;
    --azul-claro: #E9F1FB;
    --dorado: #C9982A;
    --verde: #1F9D55;
    --amarillo: #F2C94C;
    --rojo: #D64545;
    --gris-texto: #5A6A85;
}

/* ── Fondo general más limpio ── */
.stApp { 
    background: linear-gradient(180deg, #EEF3FB 0%, #F7FAFF 100%);
}

/* ── Sidebar ULTRA PRO ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081F4D 0%, #0A2A5E 50%, #0D3C84 100%);
    border-right: 2px solid var(--dorado);
}

/* ── Tabs estilo Power BI real ── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    padding: 6px;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

.stTabs [data-baseweb="tab"] {
    color: var(--gris-texto) !important;
    font-weight: 700 !important;
}

.stTabs [aria-selected="true"] {
    background: var(--azul-primario) !important;
    color: #FFFFFF !important;
    border-radius: 8px;
}

/* ── KPI CARDS NIVEL GERENCIAL ── */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-top: 4px solid var(--azul-primario);
}

/* TEXTO KPI */
[data-testid="metric-label"] {
    color: var(--gris-texto) !important;
    font-weight: 700;
}

[data-testid="metric-value"] {
    color: var(--azul-primario) !important;
    font-size: 32px !important;
    font-weight: 900;
}

/* DELTAS (COLORES DE PERFORMANCE) */
[data-testid="metric-delta"] {
    font-weight: 700;
}

/* ── BOTONES ── */
.stButton > button {
    background: var(--azul-primario);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 700;
}

.stButton > button:hover {
    background: var(--azul-secundario);
}

/* ── HEADERS ── */
h1 {
    color: var(--azul-primario);
    font-weight: 900;
}

h2, h3 {
    color: #1B2A4A;
    font-weight: 800;
}

/* ── TARJETAS / CONTENEDORES ── */
.block-container {
    padding-top: 1rem;
}

/* ── SCROLL limpio ── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #C1C9D6;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
