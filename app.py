import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
import os

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Smart City Data Analyzer",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS Design System
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --primary: #6C63FF;
    --primary-light: #8B83FF;
    --secondary: #00D2FF;
    --accent-green: #00E676;
    --accent-orange: #FF9100;
    --accent-red: #FF5252;
    --bg-dark: #0E1117;
    --bg-card: #1A1D29;
    --bg-card-hover: #22263A;
    --text-primary: #EAEAEA;
    --text-secondary: #9CA3AF;
    --border-subtle: rgba(108, 99, 255, 0.15);
    --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.25);
    --shadow-glow: 0 0 30px rgba(108, 99, 255, 0.12);
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
}

/* ── Global Overrides ── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(145deg, #0E1117 0%, #131620 50%, #0E1117 100%);
}

/* ── Hero Header ── */
.hero-container {
    background: linear-gradient(135deg, rgba(108, 99, 255, 0.12) 0%, rgba(0, 210, 255, 0.08) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(108, 99, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #EAEAEA 0%, #6C63FF 50%, #00D2FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
    font-weight: 400;
    margin: 0 0 1rem 0;
}
.hero-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(108, 99, 255, 0.12);
    border: 1px solid rgba(108, 99, 255, 0.25);
    color: var(--primary-light);
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
}

/* ── KPI Metric Cards ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
}
.kpi-card.traffic::before { background: linear-gradient(90deg, #6C63FF, #8B83FF); }
.kpi-card.pollution::before { background: linear-gradient(90deg, #FF5252, #FF9100); }
.kpi-card.energy::before { background: linear-gradient(90deg, #00D2FF, #00E676); }
.kpi-card.zones::before { background: linear-gradient(90deg, #FF9100, #FFD600); }

.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}
.kpi-label {
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.25rem;
}
.kpi-value {
    color: var(--text-primary);
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.2;
}
.kpi-detail {
    color: var(--text-secondary);
    font-size: 0.75rem;
    margin-top: 0.3rem;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border-subtle);
}
.section-header h3 {
    color: var(--text-primary);
    font-size: 1.15rem;
    font-weight: 600;
    margin: 0;
}
.section-badge {
    background: rgba(108, 99, 255, 0.15);
    color: var(--primary-light);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Chart Container ── */
.chart-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s ease;
}
.chart-container:hover {
    box-shadow: var(--shadow-glow);
}
.chart-title {
    color: var(--text-primary);
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Data Table Styling ── */
.dataframe-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1rem;
    overflow: hidden;
}

/* ── Correlation Card ── */
.corr-insight {
    background: linear-gradient(135deg, rgba(108, 99, 255, 0.08) 0%, rgba(0, 210, 255, 0.05) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    font-size: 0.85rem;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13151F 0%, #0E1117 100%);
    border-right: 1px solid var(--border-subtle);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary);
}

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 0.35rem;
    border: 1px solid var(--border-subtle);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--text-secondary);
    background: transparent;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: rgba(108, 99, 255, 0.18) !important;
    color: var(--primary-light) !important;
    border: none !important;
}

/* ── Streamlit Element Overrides ── */
.stMetric {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 1rem;
}
div[data-testid="stMetricValue"] {
    font-weight: 700;
}

/* ── Upload Area ── */
.stFileUploader > div {
    border-radius: var(--radius-md) !important;
    border-color: var(--border-subtle) !important;
}

/* ── Footer ── */
.footer-container {
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    font-size: 0.78rem;
}
.footer-container a {
    color: var(--primary-light);
    text-decoration: none;
}

/* ── Responsive Tweaks ── */
@media (max-width: 768px) {
    .hero-title { font-size: 1.5rem; }
    .kpi-row { grid-template-columns: 1fr 1fr; }
    .hero-container { padding: 1.25rem; }
}
@media (max-width: 480px) {
    .kpi-row { grid-template-columns: 1fr; }
    .hero-title { font-size: 1.3rem; }
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Color Palette for Charts
# ──────────────────────────────────────────────
CHART_COLORS = {
    "traffic": ["#6C63FF", "#8B83FF", "#ABA4FF", "#CBC7FF"],
    "pollution": ["#FF5252", "#FF7B7B", "#FF9100", "#FFB74D"],
    "energy": ["#00D2FF", "#4DE8FF", "#00E676", "#69F0AE"],
    "multi": ["#6C63FF", "#FF5252", "#00D2FF", "#FF9100", "#00E676", "#FFD600"],
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#EAEAEA", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(
        gridcolor="rgba(108, 99, 255, 0.08)",
        zerolinecolor="rgba(108, 99, 255, 0.12)",
    ),
    yaxis=dict(
        gridcolor="rgba(108, 99, 255, 0.08)",
        zerolinecolor="rgba(108, 99, 255, 0.12)",
    ),
    hoverlabel=dict(
        bgcolor="#1A1D29",
        font_size=13,
        font_family="Inter, sans-serif",
        bordercolor="#6C63FF",
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(108, 99, 255, 0.15)",
        borderwidth=1,
        font=dict(size=11),
    ),
)


# ──────────────────────────────────────────────
# Sidebar – Dataset Controls
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏙️ Smart City Analyzer")
    st.markdown("---")
    st.markdown("### 📁 Dataset")

    data_source = st.radio(
        "Choose data source",
        ["📦 Default Dataset", "📤 Upload CSV"],
        index=0,
        help="Load the bundled city_data.csv or upload your own.",
    )

    data = None

    if data_source == "📤 Upload CSV":
        uploaded_file = st.file_uploader("Upload City Dataset", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
    else:
        csv_path = os.path.join(os.path.dirname(__file__), "city_data.csv")
        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path)
        else:
            st.error("Default dataset `city_data.csv` not found.")

    if data is not None:
        st.markdown("---")
        st.markdown("### 🔍 Filters")

        all_areas = data["Area"].unique().tolist()
        selected_areas = st.multiselect(
            "Select Areas / Zones",
            options=all_areas,
            default=all_areas,
            help="Filter dashboard data by area.",
        )
        data = data[data["Area"].isin(selected_areas)]

        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Zones", len(data))
        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        st.metric("Metrics Tracked", len(numeric_cols))
        st.metric("Total Records", len(data))

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;color:#9CA3AF;font-size:0.7rem;">'
        "Built with Streamlit & Plotly<br>© 2026 Smart City Analyzer"
        "</div>",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🏙️ Smart City Data Analyzer</div>
        <p class="hero-subtitle">
            Explore and analyze city-related datasets through interactive visualizations,
            statistical insights, and correlation analysis.
        </p>
        <div class="hero-pills">
            <span class="hero-pill">🚦 Traffic</span>
            <span class="hero-pill">🏭 Pollution</span>
            <span class="hero-pill">⚡ Energy</span>
            <span class="hero-pill">📊 Analytics</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Main Dashboard (data loaded)
# ──────────────────────────────────────────────
if data is not None and not data.empty:

    # Compute key insights
    max_traffic = data.loc[data["Traffic"].idxmax()]
    max_pollution = data.loc[data["Pollution"].idxmax()]
    max_energy = data.loc[data["Energy"].idxmax()]

    # ── KPI Cards ──
    st.markdown(
        f"""
        <div class="kpi-row">
            <div class="kpi-card zones">
                <div class="kpi-icon">🗺️</div>
                <div class="kpi-label">Zones Analyzed</div>
                <div class="kpi-value">{len(data)}</div>
                <div class="kpi-detail">Active city zones in dataset</div>
            </div>
            <div class="kpi-card traffic">
                <div class="kpi-icon">🚦</div>
                <div class="kpi-label">Peak Traffic</div>
                <div class="kpi-value">{int(max_traffic['Traffic']):,}</div>
                <div class="kpi-detail">{max_traffic['Area']}</div>
            </div>
            <div class="kpi-card pollution">
                <div class="kpi-icon">🏭</div>
                <div class="kpi-label">Highest Pollution</div>
                <div class="kpi-value">{int(max_pollution['Pollution']):,}</div>
                <div class="kpi-detail">{max_pollution['Area']}</div>
            </div>
            <div class="kpi-card energy">
                <div class="kpi-icon">⚡</div>
                <div class="kpi-label">Peak Energy Usage</div>
                <div class="kpi-value">{int(max_energy['Energy']):,}</div>
                <div class="kpi-detail">{max_energy['Area']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ──────────────────────────────────────────
    # Tabbed Dashboard
    # ──────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard Overview", "📈 In-Depth Analysis", "📋 Data Explorer", "🔗 Correlations"]
    )

    # ═══════════════════════════════════════════
    # TAB 1 – Dashboard Overview
    # ═══════════════════════════════════════════
    with tab1:
        st.markdown(
            '<div class="section-header"><h3>Overview Charts</h3>'
            '<span class="section-badge">Live</span></div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        # Traffic Bar Chart
        with col1:
            st.markdown(
                '<div class="chart-container">'
                '<div class="chart-title">🚦 Traffic by Area</div>',
                unsafe_allow_html=True,
            )
            fig_traffic = px.bar(
                data,
                x="Area",
                y="Traffic",
                color="Traffic",
                color_continuous_scale=["#6C63FF", "#00D2FF"],
                text="Traffic",
            )
            fig_traffic.update_traces(
                textposition="outside",
                textfont_size=12,
                marker_line_width=0,
                marker_cornerradius=6,
            )
            fig_traffic.update_layout(
                **PLOTLY_LAYOUT,
                coloraxis_showscale=False,
                height=350,
                showlegend=False,
            )
            st.plotly_chart(fig_traffic, width="stretch", key="overview_traffic")
            st.markdown("</div>", unsafe_allow_html=True)

        # Pollution Bar Chart
        with col2:
            st.markdown(
                '<div class="chart-container">'
                '<div class="chart-title">🏭 Pollution Levels</div>',
                unsafe_allow_html=True,
            )
            fig_pollution = px.bar(
                data,
                x="Area",
                y="Pollution",
                color="Pollution",
                color_continuous_scale=["#FF9100", "#FF5252"],
                text="Pollution",
            )
            fig_pollution.update_traces(
                textposition="outside",
                textfont_size=12,
                marker_line_width=0,
                marker_cornerradius=6,
            )
            fig_pollution.update_layout(
                **PLOTLY_LAYOUT,
                coloraxis_showscale=False,
                height=350,
                showlegend=False,
            )
            st.plotly_chart(fig_pollution, width="stretch", key="overview_pollution")
            st.markdown("</div>", unsafe_allow_html=True)

        # Energy Area Chart (full width)
        st.markdown(
            '<div class="chart-container">'
            '<div class="chart-title">⚡ Energy Consumption Trend</div>',
            unsafe_allow_html=True,
        )
        fig_energy = px.area(
            data,
            x="Area",
            y="Energy",
            markers=True,
            color_discrete_sequence=["#00D2FF"],
        )
        fig_energy.update_traces(
            fill="tozeroy",
            fillcolor="rgba(0, 210, 255, 0.12)",
            line=dict(width=3, color="#00D2FF"),
            marker=dict(size=8, color="#00E676", line=dict(width=2, color="#00D2FF")),
        )
        fig_energy.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig_energy, width="stretch", key="overview_energy")
        st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # TAB 2 – In-Depth Analysis
    # ═══════════════════════════════════════════
    with tab2:
        st.markdown(
            '<div class="section-header"><h3>Comparative Analysis</h3>'
            '<span class="section-badge">Detailed</span></div>',
            unsafe_allow_html=True,
        )

        # Multi-metric grouped bar chart
        st.markdown(
            '<div class="chart-container">'
            '<div class="chart-title">📊 Multi-Metric Comparison</div>',
            unsafe_allow_html=True,
        )
        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        data_melted = data.melt(id_vars=["Area"], value_vars=numeric_cols, var_name="Metric", value_name="Value")
        fig_multi = px.bar(
            data_melted,
            x="Area",
            y="Value",
            color="Metric",
            barmode="group",
            color_discrete_sequence=["#6C63FF", "#FF5252", "#00D2FF"],
            text="Value",
        )
        fig_multi.update_traces(textposition="outside", textfont_size=11, marker_cornerradius=5)
        fig_multi.update_layout(**PLOTLY_LAYOUT, height=420)
        st.plotly_chart(fig_multi, width="stretch", key="analysis_multi")
        st.markdown("</div>", unsafe_allow_html=True)

        # Individual detailed charts
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown(
                '<div class="chart-container">'
                '<div class="chart-title">🚦 Traffic Breakdown</div>',
                unsafe_allow_html=True,
            )
            fig_t_pie = px.pie(
                data,
                names="Area",
                values="Traffic",
                color_discrete_sequence=CHART_COLORS["traffic"],
                hole=0.45,
            )
            fig_t_pie.update_traces(textinfo="label+percent", textfont_size=11)
            fig_t_pie.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
            st.plotly_chart(fig_t_pie, width="stretch", key="analysis_traffic_pie")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown(
                '<div class="chart-container">'
                '<div class="chart-title">🏭 Pollution Breakdown</div>',
                unsafe_allow_html=True,
            )
            fig_p_pie = px.pie(
                data,
                names="Area",
                values="Pollution",
                color_discrete_sequence=CHART_COLORS["pollution"],
                hole=0.45,
            )
            fig_p_pie.update_traces(textinfo="label+percent", textfont_size=11)
            fig_p_pie.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
            st.plotly_chart(fig_p_pie, width="stretch", key="analysis_pollution_pie")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_c:
            st.markdown(
                '<div class="chart-container">'
                '<div class="chart-title">⚡ Energy Breakdown</div>',
                unsafe_allow_html=True,
            )
            fig_e_pie = px.pie(
                data,
                names="Area",
                values="Energy",
                color_discrete_sequence=CHART_COLORS["energy"],
                hole=0.45,
            )
            fig_e_pie.update_traces(textinfo="label+percent", textfont_size=11)
            fig_e_pie.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
            st.plotly_chart(fig_e_pie, width="stretch", key="analysis_energy_pie")
            st.markdown("</div>", unsafe_allow_html=True)

        # Key Insights section
        st.markdown(
            '<div class="section-header"><h3>Key Insights</h3>'
            '<span class="section-badge">AI Summary</span></div>',
            unsafe_allow_html=True,
        )

        insight_col1, insight_col2, insight_col3 = st.columns(3)
        with insight_col1:
            st.markdown(
                f'<div class="corr-insight">'
                f"🚦 <strong>Highest Traffic:</strong> {max_traffic['Area']} "
                f"with <strong>{int(max_traffic['Traffic']):,}</strong> vehicles"
                f"</div>",
                unsafe_allow_html=True,
            )
        with insight_col2:
            st.markdown(
                f'<div class="corr-insight">'
                f"🏭 <strong>Highest Pollution:</strong> {max_pollution['Area']} "
                f"with index <strong>{int(max_pollution['Pollution']):,}</strong>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with insight_col3:
            st.markdown(
                f'<div class="corr-insight">'
                f"⚡ <strong>Peak Energy:</strong> {max_energy['Area']} "
                f"consuming <strong>{int(max_energy['Energy']):,}</strong> units"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ═══════════════════════════════════════════
    # TAB 3 – Data Explorer & Statistics
    # ═══════════════════════════════════════════
    with tab3:
        st.markdown(
            '<div class="section-header"><h3>Dataset Preview</h3>'
            '<span class="section-badge">Interactive</span></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            data,
            width="stretch",
            hide_index=True,
            column_config={
                "Area": st.column_config.TextColumn("🗺️ Area"),
                "Traffic": st.column_config.ProgressColumn(
                    "🚦 Traffic",
                    min_value=0,
                    max_value=int(data["Traffic"].max() * 1.2),
                    format="%d",
                ),
                "Pollution": st.column_config.ProgressColumn(
                    "🏭 Pollution",
                    min_value=0,
                    max_value=int(data["Pollution"].max() * 1.2),
                    format="%d",
                ),
                "Energy": st.column_config.ProgressColumn(
                    "⚡ Energy",
                    min_value=0,
                    max_value=int(data["Energy"].max() * 1.2),
                    format="%d",
                ),
            },
        )

        st.markdown(
            '<div class="section-header"><h3>Basic Statistics</h3>'
            '<span class="section-badge">Summary</span></div>',
            unsafe_allow_html=True,
        )
        desc = data.describe()
        st.dataframe(
            desc.style.format("{:.1f}").set_properties(**{"text-align": "center"}),
            width="stretch",
        )

    # ═══════════════════════════════════════════
    # TAB 4 – Correlation Analysis
    # ═══════════════════════════════════════════
    with tab4:
        st.markdown(
            '<div class="section-header"><h3>Feature Correlations</h3>'
            '<span class="section-badge">Heatmap</span></div>',
            unsafe_allow_html=True,
        )

        correlation = data.corr(numeric_only=True)

        # Heatmap
        st.markdown(
            '<div class="chart-container">'
            '<div class="chart-title">🔗 Correlation Heatmap</div>',
            unsafe_allow_html=True,
        )
        fig_heatmap = go.Figure(
            data=go.Heatmap(
                z=correlation.values,
                x=correlation.columns.tolist(),
                y=correlation.columns.tolist(),
                colorscale=[
                    [0.0, "#FF5252"],
                    [0.25, "#FF9100"],
                    [0.5, "#1A1D29"],
                    [0.75, "#6C63FF"],
                    [1.0, "#00D2FF"],
                ],
                text=correlation.values.round(3),
                texttemplate="%{text}",
                textfont=dict(size=14, color="#EAEAEA"),
                hoverongaps=False,
                colorbar=dict(
                    title=dict(text="Correlation", font=dict(color="#EAEAEA")),
                    tickfont=dict(color="#9CA3AF"),
                ),
            )
        )
        fig_heatmap.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#EAEAEA", size=12),
            margin=dict(l=40, r=20, t=40, b=40),
            hoverlabel=dict(
                bgcolor="#1A1D29",
                font_size=13,
                font_family="Inter, sans-serif",
                bordercolor="#6C63FF",
            ),
            height=400,
            xaxis=dict(
                side="bottom",
                tickfont=dict(color="#EAEAEA", size=13),
                gridcolor="rgba(0,0,0,0)",
            ),
            yaxis=dict(
                tickfont=dict(color="#EAEAEA", size=13),
                gridcolor="rgba(0,0,0,0)",
                autorange="reversed",
            ),
        )
        st.plotly_chart(fig_heatmap, width="stretch", key="corr_heatmap")
        st.markdown("</div>", unsafe_allow_html=True)

        # Correlation table
        st.markdown(
            '<div class="section-header"><h3>Correlation Matrix</h3>'
            '<span class="section-badge">Raw Values</span></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            correlation.style.format("{:.4f}")
            .background_gradient(cmap="coolwarm", axis=None)
            .set_properties(**{"text-align": "center"}),
            width="stretch",
        )

        # Correlation insights
        st.markdown(
            '<div class="section-header"><h3>Correlation Insights</h3></div>',
            unsafe_allow_html=True,
        )

        for i in range(len(correlation.columns)):
            for j in range(i + 1, len(correlation.columns)):
                col_a_name = correlation.columns[i]
                col_b_name = correlation.columns[j]
                corr_val = correlation.iloc[i, j]
                if abs(corr_val) >= 0.7:
                    strength = "Strong positive" if corr_val > 0 else "Strong negative"
                    emoji = "🟢" if corr_val > 0 else "🔴"
                elif abs(corr_val) >= 0.4:
                    strength = "Moderate positive" if corr_val > 0 else "Moderate negative"
                    emoji = "🟡"
                else:
                    strength = "Weak"
                    emoji = "⚪"
                st.markdown(
                    f'<div class="corr-insight">'
                    f"{emoji} <strong>{col_a_name}</strong> ↔ <strong>{col_b_name}</strong>: "
                    f"{strength} correlation ({corr_val:.4f})"
                    f"</div>",
                    unsafe_allow_html=True,
                )

elif data is not None and data.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your area selection in the sidebar.")
else:
    st.info("👈 Please upload a CSV dataset or select the default dataset from the sidebar to get started.")


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    '<div class="footer-container">'
    "Smart City Data Analyzer • Built with ❤️ by <strong>Nidhi Palandurkar</strong> • "
    "Powered by Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True,
)