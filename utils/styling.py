"""
Styling and UI components for the dashboard
Brand-inspired design with clean, premium aesthetic
"""
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling with brand-inspired design language"""
    st.markdown("""
    <style>
        /* Import brand-inspired fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Lato:wght@300;400;700;900&display=swap');

        /* Global styling */
        * {
            font-family: 'Lato', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Main container - clean ecru background */
        .main {
            background: #FAF9F2;
            padding: 0rem 1rem;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        /* Header styling - elegant and clean */
        .dashboard-header {
            background: #ffffff;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(89, 89, 89, 0.12);
            border-bottom: 3px solid #ffe512;
        }

        .dashboard-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #595959;
            margin: 0;
            letter-spacing: -0.3px;
        }

        .dashboard-subtitle {
            font-family: 'Lato', sans-serif;
            font-size: 0.875rem;
            color: #7a7a7a;
            margin-top: 0.25rem;
            font-weight: 400;
            letter-spacing: 0.3px;
        }

        /* KPI Card styling - clean and minimal */
        .kpi-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(89, 89, 89, 0.12);
            border-top: 3px solid #ffe512;
            margin-bottom: 1rem;
            transition: all 0.2s ease;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .kpi-card:hover {
            box-shadow: 0 4px 12px rgba(89, 89, 89, 0.15);
            transform: translateY(-2px);
        }

        .kpi-label {
            font-family: 'Lato', sans-serif;
            font-size: 0.75rem;
            color: #7a7a7a;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.75rem;
        }

        .kpi-value {
            font-family: 'Playfair Display', serif;
            font-size: 2.25rem;
            font-weight: 700;
            color: #595959;
            margin: 0.5rem 0;
            line-height: 1.1;
        }

        .kpi-delta {
            font-family: 'Lato', sans-serif;
            font-size: 0.8125rem;
            font-weight: 600;
            margin-top: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .kpi-delta-positive {
            color: #2d5f3f;
        }

        .kpi-delta-negative {
            color: #8b3a3a;
        }

        .kpi-delta-neutral {
            color: #7a7a7a;
        }

        /* Sidebar styling - clean and professional */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e5e0;
        }

        section[data-testid="stSidebar"] > div {
            background: transparent;
        }

        section[data-testid="stSidebar"] .stMarkdown h3,
        section[data-testid="stSidebar"] .stMarkdown h2,
        section[data-testid="stSidebar"] .stMarkdown h1 {
            font-family: 'Playfair Display', serif;
            color: #595959 !important;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] label {
            font-family: 'Lato', sans-serif;
            color: #595959 !important;
            font-weight: 600;
            font-size: 0.875rem;
        }

        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stDateInput label {
            color: #7a7a7a !important;
            font-weight: 600;
        }

        /* Section headers - elegant typography */
        .section-header {
            font-family: 'Playfair Display', serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: #595959;
            margin: 2rem 0 1.25rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #ffe512;
        }

        /* Chart container - clean white cards */
        .chart-container {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(89, 89, 89, 0.12);
            margin-bottom: 1.5rem;
        }

        /* Tabs styling - minimal and clean */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            border-bottom: 1px solid #e5e5e0;
        }

        .stTabs [data-baseweb="tab"] {
            font-family: 'Lato', sans-serif;
            height: 48px;
            background-color: transparent;
            border-radius: 0;
            padding: 0 24px;
            font-weight: 600;
            font-size: 0.9375rem;
            border: none;
            border-bottom: 3px solid transparent;
            color: #7a7a7a;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #595959;
            border-bottom-color: #d4b000;
        }

        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: #595959 !important;
            border-bottom-color: #ffe512;
        }

        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 700;
            color: #595959;
        }

        [data-testid="stMetricLabel"] {
            font-family: 'Lato', sans-serif;
            font-size: 0.875rem;
            color: #7a7a7a;
        }

        /* Dataframe styling */
        .stDataFrame {
            border-radius: 4px;
            overflow: hidden;
            font-family: 'Lato', sans-serif;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            font-family: 'Lato', sans-serif;
            background-color: #ffffff;
            border: 1px solid #e5e5e0;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.875rem;
            color: #595959;
            padding: 0.75rem 1rem;
        }

        .streamlit-expanderHeader:hover {
            background-color: #FAF9F2;
            border-color: #ffe512;
        }

        /* Button styling - yellow accent */
        .stButton > button {
            font-family: 'Lato', sans-serif;
            background: #ffe512;
            color: #595959;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 2rem;
            font-weight: 700;
            font-size: 0.9375rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: #d4b000;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(255, 229, 18, 0.3);
        }

        /* KPI Button - make invisible, positioned over card */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            height: 180px !important;
            margin-top: -180px !important;
            margin-bottom: 0 !important;
            position: relative !important;
            z-index: 10 !important;
            cursor: pointer !important;
            font-size: 0 !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
        }

        .stButton > button[kind="secondary"]:active {
            transform: none !important;
        }

        .stButton > button[kind="secondary"]:focus {
            box-shadow: none !important;
        }

        .stButton > button[kind="secondary"] p {
            display: none !important;
        }

        /* Info/Warning/Success boxes */
        .stAlert {
            font-family: 'Lato', sans-serif;
            border-radius: 4px;
            border-left-width: 4px;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif;
            color: #595959;
            font-weight: 700;
        }

        /* Body text */
        p, div, span, label {
            font-family: 'Lato', sans-serif;
            color: #595959;
        }

        /* Footer */
        .dashboard-footer {
            text-align: center;
            color: #7a7a7a;
            padding: 2rem 0 1rem 0;
            font-size: 0.875rem;
            border-top: 1px solid #e5e5e0;
            margin-top: 3rem;
            font-family: 'Lato', sans-serif;
        }

        /* Clean scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #FAF9F2;
        }

        ::-webkit-scrollbar-thumb {
            background: #d4b000;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #ffe512;
        }

        /* Plotly chart styling */
        .js-plotly-plot {
            border-radius: 4px;
        }

        /* Remove default streamlit branding colors */
        .stApp header {
            background-color: transparent;
        }

        /* Select box styling */
        .stSelectbox > div > div {
            background-color: #ffffff;
            border: 1px solid #e5e5e0;
            border-radius: 4px;
        }

        /* Date input styling */
        .stDateInput > div > div {
            background-color: #ffffff;
            border: 1px solid #e5e5e0;
            border-radius: 4px;
        }

        /* Radio button styling */
        .stRadio > div {
            gap: 1rem;
        }

        .stRadio label {
            font-family: 'Lato', sans-serif;
            font-weight: 500;
            color: #595959;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header(title: str, subtitle: str):
    """Create clean, elegant dashboard header"""
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">{title}</h1>
        <p class="dashboard-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_kpi_card(label: str, value: str, delta: float = None, delta_label: str = "vs comparison", is_currency: bool = False, inverse: bool = False):
    """
    Create a clean KPI card with brand-inspired styling

    Args:
        label: KPI label
        value: Current value (formatted string)
        delta: Percentage change (can be None)
        delta_label: Label for delta (default: "vs comparison")
        is_currency: If True, formats as currency
        inverse: If True, negative delta is good (e.g., for arrears, vacancies)
    """
    if delta is not None:
        if inverse:
            delta_class = "kpi-delta-positive" if delta < 0 else "kpi-delta-negative" if delta > 0 else "kpi-delta-neutral"
        else:
            delta_class = "kpi-delta-positive" if delta > 0 else "kpi-delta-negative" if delta < 0 else "kpi-delta-neutral"

        delta_icon = "▲" if delta > 0 else "▼" if delta < 0 else "●"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {abs(delta):.1f}% {delta_label}</div>'
    else:
        delta_html = ""

    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    return card_html

def create_clickable_kpi_button(label: str, value: str, delta: float = None, delta_label: str = "vs comparison", inverse: bool = False, key: str = None):
    """
    Create a clickable KPI button that looks like a card

    Args:
        label: KPI label
        value: Current value (formatted string)
        delta: Percentage change (can be None)
        delta_label: Label for delta
        inverse: If True, negative delta is good
        key: Unique key for the button

    Returns:
        bool: True if button was clicked
    """
    if delta is not None:
        if inverse:
            delta_class = "kpi-delta-positive" if delta < 0 else "kpi-delta-negative" if delta > 0 else "kpi-delta-neutral"
            delta_color = "#2d5f3f" if delta < 0 else "#8b3a3a" if delta > 0 else "#7a7a7a"
        else:
            delta_class = "kpi-delta-positive" if delta > 0 else "kpi-delta-negative" if delta < 0 else "kpi-delta-neutral"
            delta_color = "#2d5f3f" if delta > 0 else "#8b3a3a" if delta < 0 else "#7a7a7a"

        delta_symbol = "▲" if delta > 0 else "▼" if delta < 0 else "●"
        delta_html = f'<div style="font-size: 0.8125rem; font-weight: 600; color: {delta_color}; margin-top: 0.75rem;">{delta_symbol} {abs(delta):.1f}% {delta_label}</div>'
    else:
        delta_html = '<div style="height: 1.5rem;"></div>'  # Placeholder for spacing

    # Create the full card as HTML
    card_html = f"""
    <style>
        .clickable-kpi-card-{key} {{
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(89, 89, 89, 0.12);
            border-top: 3px solid #ffe512;
            margin-bottom: 0.5rem;
            min-height: 148px;
            transition: all 0.2s ease;
            cursor: pointer;
            pointer-events: none;
        }}
        .clickable-kpi-card-{key}:hover {{
            box-shadow: 0 4px 12px rgba(89, 89, 89, 0.15);
            transform: translateY(-2px);
        }}
    </style>
    <div class="clickable-kpi-card-{key}">
        <div style="font-size: 0.75rem; color: #7a7a7a; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
        <div style="font-family: 'Playfair Display', serif; font-size: 2.25rem; font-weight: 700; color: #595959; margin: 0.5rem 0;">{value}</div>
        {delta_html}
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)

    # Use invisible button to capture click (overlaid on card)
    clicked = st.button(
        "",  # Empty string
        key=key,
        use_container_width=True,
        type="secondary"
    )

    return clicked

def create_clickable_kpi_card(label: str, value: str, delta: float = None, delta_label: str = "vs comparison", inverse: bool = False, click_hint: str = "Click for details"):
    """
    Create a clickable KPI card that shows a click hint

    Args:
        label: KPI label
        value: Current value (formatted string)
        delta: Percentage change (can be None)
        delta_label: Label for delta
        inverse: If True, negative delta is good
        click_hint: Hint text to show on hover
    """
    if delta is not None:
        if inverse:
            delta_class = "kpi-delta-positive" if delta < 0 else "kpi-delta-negative" if delta > 0 else "kpi-delta-neutral"
        else:
            delta_class = "kpi-delta-positive" if delta > 0 else "kpi-delta-negative" if delta < 0 else "kpi-delta-neutral"

        delta_icon = "▲" if delta > 0 else "▼" if delta < 0 else "●"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {abs(delta):.1f}% {delta_label}</div>'
    else:
        delta_html = f'<div class="kpi-delta kpi-delta-neutral" style="opacity: 0;">● 0.0% {delta_label}</div>'

    card_html = f"""
    <div class="kpi-card" style="cursor: pointer;" title="{click_hint}">
        <div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        <div style="margin-top: 0.75rem; font-size: 0.75rem; color: #7a7a7a;">
            ▸ {click_hint}
        </div>
    </div>
    """
    return card_html

def create_section_header(text: str):
    """Create an elegant section header"""
    st.markdown(f'<h2 class="section-header">{text}</h2>', unsafe_allow_html=True)

def create_footer():
    """Create clean dashboard footer"""
    from datetime import datetime
    st.markdown(f"""
    <div class="dashboard-footer">
        <p>Executive Management Dashboard | Last Updated: {datetime.now().strftime("%d %b %Y, %H:%M")}</p>
        <p style="margin-top: 0.5rem; font-size: 0.75rem; color: #9a9a9a;">© {datetime.now().year} Commercial Property Management</p>
    </div>
    """, unsafe_allow_html=True)
