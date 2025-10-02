"""
Ray White Property Management Dashboard
Executive KPI Dashboard with Interactive Analytics
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Import utilities
import config
from utils import styling, metrics, data_generator, charts

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
styling.apply_custom_css()

# Initialize session state for filters
if 'df' not in st.session_state:
    st.session_state.df = data_generator.generate_historical_data(24)

# Sidebar - Filters
with st.sidebar:
    st.markdown("### 📊 Dashboard Filters")
    st.markdown("---")

    # Agency filter
    agencies_list = ["Whole Agency"] + sorted(config.AGENCIES)
    selected_agency = st.selectbox(
        "🏢 Agency",
        agencies_list,
        index=0
    )

    # Portfolio Manager filter
    if selected_agency == "Whole Agency":
        pm_list = ["All Managers"] + sorted(config.PORTFOLIO_MANAGERS)
    else:
        filtered_pms = st.session_state.df[
            st.session_state.df['agency'] == selected_agency
        ]['portfolio_manager'].unique()
        pm_list = ["All Managers"] + sorted(filtered_pms.tolist())

    selected_pm = st.selectbox(
        "👤 Portfolio Manager",
        pm_list,
        index=0
    )

    # Date range
    st.markdown("### 📅 Date Range")
    df_dates = st.session_state.df['date']
    date_range = st.date_input(
        "Select Range",
        value=(df_dates.min().date(), df_dates.max().date()),
        min_value=df_dates.min().date(),
        max_value=df_dates.max().date()
    )

    st.markdown("---")

    # Info section
    st.info(f"**Data Mode:** {'Mock Data' if config.USE_MOCK_DATA else 'Live Data'}")
    st.caption(f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")

    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.session_state.df = data_generator.generate_historical_data(24)
        st.rerun()

# Main content
styling.create_header(config.APP_TITLE, config.APP_SUBTITLE)

# Filter data based on selections
df = st.session_state.df.copy()

if selected_agency != "Whole Agency":
    df = df[df['agency'] == selected_agency]

if selected_pm != "All Managers":
    df = df[df['portfolio_manager'] == selected_pm]

if len(date_range) == 2:
    df = df[
        (df['date'].dt.date >= date_range[0]) &
        (df['date'].dt.date <= date_range[1])
    ]

# Get current, last month, and last year data
current_date = df['date'].max()
last_month_date = current_date - pd.DateOffset(months=1)
last_year_date = current_date - pd.DateOffset(months=12)

current_data = df[df['date'] == current_date]
last_month_data = df[df['date'] == last_month_date]
last_year_data = df[df['date'] == last_year_date]

# Calculate KPIs
kpis = {
    'landlords': current_data['landlords'].sum(),
    'properties': current_data['properties'].sum(),
    'leases': current_data['leases'].sum(),
    'vacancies': current_data['vacancies'].sum(),
    'avg_occupancy': current_data['occupancy_rate'].mean(),
    'rent_roll': current_data['rent_roll'].sum(),
    'total_revenue': current_data['total_revenue'].sum(),
    'total_arrears': current_data['total_arrears'].sum(),
    'avg_fee': current_data['avg_fee_per_tenancy'].mean(),
}

last_month_kpis = {
    'landlords': last_month_data['landlords'].sum() if not last_month_data.empty else kpis['landlords'],
    'properties': last_month_data['properties'].sum() if not last_month_data.empty else kpis['properties'],
    'leases': last_month_data['leases'].sum() if not last_month_data.empty else kpis['leases'],
    'vacancies': last_month_data['vacancies'].sum() if not last_month_data.empty else kpis['vacancies'],
    'avg_occupancy': last_month_data['occupancy_rate'].mean() if not last_month_data.empty else kpis['avg_occupancy'],
    'rent_roll': last_month_data['rent_roll'].sum() if not last_month_data.empty else kpis['rent_roll'],
    'total_revenue': last_month_data['total_revenue'].sum() if not last_month_data.empty else kpis['total_revenue'],
    'total_arrears': last_month_data['total_arrears'].sum() if not last_month_data.empty else kpis['total_arrears'],
}

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "💰 Management Fees",
    "⚠️ Arrears",
    "📅 Critical Dates",
    "✅ Task Management"
])

# TAB 1: OVERVIEW
with tab1:
    styling.create_section_header("Key Performance Indicators")

    # First row of KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['landlords'], last_month_kpis['landlords'])
        st.markdown(
            styling.create_kpi_card(
                "Total Landlords",
                metrics.format_number(kpis['landlords']),
                delta,
                "vs last month"
            ),
            unsafe_allow_html=True
        )

    with col2:
        delta = metrics.calculate_percent_change(kpis['properties'], last_month_kpis['properties'])
        st.markdown(
            styling.create_kpi_card(
                "Total Properties",
                metrics.format_number(kpis['properties']),
                delta,
                "vs last month"
            ),
            unsafe_allow_html=True
        )

    with col3:
        delta = metrics.calculate_percent_change(kpis['leases'], last_month_kpis['leases'])
        st.markdown(
            styling.create_kpi_card(
                "Active Leases",
                metrics.format_number(kpis['leases']),
                delta,
                "vs last month"
            ),
            unsafe_allow_html=True
        )

    with col4:
        delta = metrics.calculate_percent_change(kpis['vacancies'], last_month_kpis['vacancies'])
        vacancy_rate = metrics.calculate_vacancy_rate(kpis['vacancies'], kpis['properties'])
        st.markdown(
            styling.create_kpi_card(
                f"Vacancies ({vacancy_rate:.1f}%)",
                metrics.format_number(kpis['vacancies']),
                delta,
                "vs last month",
                inverse=True
            ),
            unsafe_allow_html=True
        )

    # Drill-down expanders for first row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.expander("📊 View Breakdown"):
            breakdown = current_data.groupby('portfolio_manager')['landlords'].sum().sort_values(ascending=False).reset_index()
            breakdown.columns = ['Portfolio Manager', 'Landlords']
            st.dataframe(breakdown, use_container_width=True, hide_index=True)

    with col2:
        with st.expander("📊 View Breakdown"):
            breakdown = current_data.groupby('portfolio_manager')['properties'].sum().sort_values(ascending=False).reset_index()
            breakdown.columns = ['Portfolio Manager', 'Properties']
            st.dataframe(breakdown, use_container_width=True, hide_index=True)

    with col3:
        with st.expander("📊 View Breakdown"):
            breakdown = current_data.groupby('portfolio_manager')['leases'].sum().sort_values(ascending=False).reset_index()
            breakdown.columns = ['Portfolio Manager', 'Active Leases']
            st.dataframe(breakdown, use_container_width=True, hide_index=True)

    with col4:
        with st.expander("📊 View Breakdown"):
            breakdown = current_data.groupby('portfolio_manager')['vacancies'].sum().sort_values(ascending=False).reset_index()
            breakdown.columns = ['Portfolio Manager', 'Vacancies']
            st.dataframe(breakdown, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Second row of KPIs
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        delta = metrics.calculate_percent_change(kpis['avg_occupancy'], last_month_kpis['avg_occupancy'])
        st.markdown(
            styling.create_kpi_card(
                "Avg Occupancy Rate",
                f"{kpis['avg_occupancy']:.1f}%",
                delta,
                "vs last month"
            ),
            unsafe_allow_html=True
        )

    with col6:
        delta = metrics.calculate_percent_change(kpis['rent_roll'], last_month_kpis['rent_roll'])
        st.markdown(
            styling.create_kpi_card(
                "Total Rent Roll",
                metrics.format_currency(kpis['rent_roll']),
                delta,
                "vs last month",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col7:
        delta = metrics.calculate_percent_change(kpis['total_arrears'], last_month_kpis['total_arrears'])
        st.markdown(
            styling.create_kpi_card(
                "Total Arrears",
                metrics.format_currency(kpis['total_arrears']),
                delta,
                "vs last month",
                is_currency=True,
                inverse=True
            ),
            unsafe_allow_html=True
        )

    with col8:
        arrears_pct = metrics.calculate_arrears_percentage(kpis['total_arrears'], kpis['rent_roll'])
        st.markdown(
            styling.create_kpi_card(
                "Arrears Ratio",
                f"{arrears_pct:.1f}%",
                None,
                "of rent roll"
            ),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Charts section
    styling.create_section_header("Performance Trends & Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Properties by Portfolio Manager
        pm_properties = current_data.groupby('portfolio_manager')['properties'].sum().reset_index()
        pm_properties.columns = ['Portfolio Manager', 'Properties']
        fig = charts.create_horizontal_bar_chart(
            pm_properties,
            'Properties',
            'Portfolio Manager',
            'Properties by Portfolio Manager'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Leases by Portfolio Manager
        pm_leases = current_data.groupby('portfolio_manager')['leases'].sum().reset_index()
        pm_leases.columns = ['Portfolio Manager', 'Leases']
        fig = charts.create_horizontal_bar_chart(
            pm_leases,
            'Leases',
            'Portfolio Manager',
            'Active Leases by Portfolio Manager'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Trends over time
    col3, col4 = st.columns(2)

    with col3:
        # Properties trend
        trend_data = df.groupby('date')['properties'].sum().reset_index()
        fig = charts.create_trend_line_chart(
            trend_data,
            'date',
            'properties',
            'Property Count Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Occupancy rate trend
        trend_data = df.groupby('date')['occupancy_rate'].mean().reset_index()
        fig = charts.create_trend_line_chart(
            trend_data,
            'date',
            'occupancy_rate',
            'Average Occupancy Rate Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: MANAGEMENT FEES
with tab2:
    styling.create_section_header("Revenue & Management Fees")

    # Revenue KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['total_revenue'], last_month_kpis['total_revenue'])
        st.markdown(
            styling.create_kpi_card(
                "Total Revenue",
                metrics.format_currency(kpis['total_revenue']),
                delta,
                "vs last month",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col2:
        mgmt_fees = current_data['management_fees'].sum()
        last_month_mgmt = last_month_data['management_fees'].sum() if not last_month_data.empty else mgmt_fees
        delta = metrics.calculate_percent_change(mgmt_fees, last_month_mgmt)
        st.markdown(
            styling.create_kpi_card(
                "Management Fees",
                metrics.format_currency(mgmt_fees),
                delta,
                "vs last month",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col3:
        leasing_fees = current_data['leasing_fees'].sum()
        last_month_leasing = last_month_data['leasing_fees'].sum() if not last_month_data.empty else leasing_fees
        delta = metrics.calculate_percent_change(leasing_fees, last_month_leasing)
        st.markdown(
            styling.create_kpi_card(
                "Leasing Fees",
                metrics.format_currency(leasing_fees),
                delta,
                "vs last month",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            styling.create_kpi_card(
                "Avg Fee per Tenancy",
                metrics.format_currency(kpis['avg_fee']),
                None,
                "current period",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Revenue trends and breakdown
    col1, col2 = st.columns(2)

    with col1:
        # Revenue trend over time
        revenue_trend = df.groupby('date')['total_revenue'].sum().reset_index()
        fig = charts.create_trend_line_chart(
            revenue_trend,
            'date',
            'total_revenue',
            'Total Revenue Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue breakdown by account code
        revenue_breakdown = data_generator.generate_revenue_breakdown(
            df,
            selected_pm if selected_pm != "All Managers" else "Whole Agency"
        )
        fig = charts.create_donut_chart(
            revenue_breakdown,
            'amount',
            'account_code',
            'Revenue Breakdown by Account Code'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Portfolio Manager
    pm_revenue = current_data.groupby('portfolio_manager')['total_revenue'].sum().reset_index()
    pm_revenue.columns = ['Portfolio Manager', 'Revenue']
    fig = charts.create_horizontal_bar_chart(
        pm_revenue,
        'Revenue',
        'Portfolio Manager',
        'Revenue by Portfolio Manager'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top 10 Landlords
    st.markdown("---")
    styling.create_section_header("Top 10 Landlords by Revenue")

    top_landlords = data_generator.generate_top_landlords(
        df,
        selected_pm if selected_pm != "All Managers" else "Whole Agency",
        limit=10
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = charts.create_horizontal_bar_chart(
            top_landlords,
            'revenue',
            'landlord_name',
            'Top 10 Landlords by Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(
            top_landlords.style.format({
                'properties': '{:,.0f}',
                'revenue': '${:,.0f}'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

# TAB 3: ARREARS
with tab3:
    styling.create_section_header("Arrears Analysis")

    # Arrears KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['total_arrears'], last_month_kpis['total_arrears'])
        st.markdown(
            styling.create_kpi_card(
                "Total Arrears",
                metrics.format_currency(kpis['total_arrears']),
                delta,
                "vs last month",
                is_currency=True,
                inverse=True
            ),
            unsafe_allow_html=True
        )

    with col2:
        arrears_0_30 = current_data['arrears_0_30'].sum()
        st.markdown(
            styling.create_kpi_card(
                "0-30 Days",
                metrics.format_currency(arrears_0_30),
                None,
                "current period",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col3:
        arrears_31_60 = current_data['arrears_31_60'].sum()
        st.markdown(
            styling.create_kpi_card(
                "31-60 Days",
                metrics.format_currency(arrears_31_60),
                None,
                "current period",
                is_currency=True
            ),
            unsafe_allow_html=True
        )

    with col4:
        arrears_90_plus = current_data['arrears_90_plus'].sum()
        st.markdown(
            styling.create_kpi_card(
                "90+ Days",
                metrics.format_currency(arrears_90_plus),
                None,
                "current period",
                is_currency=True,
                inverse=True
            ),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Arrears analysis
    col1, col2 = st.columns(2)

    with col1:
        # Arrears by bucket
        arrears_buckets = pd.DataFrame({
            'Bucket': ['0-30 days', '31-60 days', '61-90 days', '90+ days'],
            'Amount': [
                current_data['arrears_0_30'].sum(),
                current_data['arrears_31_60'].sum(),
                current_data['arrears_61_90'].sum(),
                current_data['arrears_90_plus'].sum()
            ]
        })
        fig = charts.create_arrears_bucket_chart(arrears_buckets, 'Arrears by Days Overdue')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Arrears percentage of rent roll
        arrears_buckets['Percentage'] = (arrears_buckets['Amount'] / arrears_buckets['Amount'].sum() * 100).round(1)
        fig = charts.create_donut_chart(
            arrears_buckets,
            'Amount',
            'Bucket',
            'Arrears Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Arrears trend
    arrears_trend = df.groupby('date')['total_arrears'].sum().reset_index()
    fig = charts.create_trend_line_chart(
        arrears_trend,
        'date',
        'total_arrears',
        'Total Arrears Trend',
        show_area=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Drill-down: Arrears details
    st.markdown("---")
    styling.create_section_header("Arrears Details")

    selected_bucket = st.selectbox(
        "Select Bucket for Details",
        ['All', '0-30', '31-60', '61-90', '90+']
    )

    arrears_details = data_generator.generate_arrears_details(
        df,
        selected_pm if selected_pm != "All Managers" else "Whole Agency",
        None if selected_bucket == 'All' else selected_bucket
    )

    st.dataframe(
        arrears_details.style.format({
            'amount_overdue': '${:,.2f}',
            'days_overdue': '{:.0f}'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )

# TAB 4: CRITICAL DATES
with tab4:
    styling.create_section_header("Critical Dates - Upcoming Events")

    # Critical dates KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rent_reviews = current_data['rent_reviews_upcoming'].sum()
        st.markdown(
            styling.create_kpi_card(
                "Rent Reviews",
                metrics.format_number(rent_reviews),
                None,
                "next 12 months"
            ),
            unsafe_allow_html=True
        )

    with col2:
        lease_expiries = current_data['lease_expiries_upcoming'].sum()
        st.markdown(
            styling.create_kpi_card(
                "Lease Expiries",
                metrics.format_number(lease_expiries),
                None,
                "next 12 months"
            ),
            unsafe_allow_html=True
        )

    with col3:
        # Calculate next month
        next_month_reviews = int(rent_reviews / 12 * 1.2)  # Mock calculation
        st.markdown(
            styling.create_kpi_card(
                "Next Month Reviews",
                metrics.format_number(next_month_reviews),
                None,
                "due date"
            ),
            unsafe_allow_html=True
        )

    with col4:
        # Calculate next month expiries
        next_month_expiries = int(lease_expiries / 12 * 1.1)  # Mock calculation
        st.markdown(
            styling.create_kpi_card(
                "Next Month Expiries",
                metrics.format_number(next_month_expiries),
                None,
                "due date"
            ),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Monthly breakdown
    col1, col2 = st.columns(2)

    with col1:
        rent_reviews_details = data_generator.generate_critical_dates_details(
            df,
            selected_pm if selected_pm != "All Managers" else "Whole Agency",
            "rent_reviews"
        )
        fig = charts.create_trend_line_chart(
            rent_reviews_details,
            'month',
            'count',
            'Upcoming Rent Reviews (Next 12 Months)',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        lease_expiries_details = data_generator.generate_critical_dates_details(
            df,
            selected_pm if selected_pm != "All Managers" else "Whole Agency",
            "lease_expiries"
        )
        fig = charts.create_trend_line_chart(
            lease_expiries_details,
            'month',
            'count',
            'Upcoming Lease Expiries (Next 12 Months)',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed tables
    st.markdown("---")
    styling.create_section_header("Detailed Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Rent Reviews by Month**")
        st.dataframe(
            rent_reviews_details[['month', 'count']].rename(columns={'month': 'Month', 'count': 'Count'}),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        st.markdown("**Lease Expiries by Month**")
        st.dataframe(
            lease_expiries_details[['month', 'count']].rename(columns={'month': 'Month', 'count': 'Count'}),
            use_container_width=True,
            hide_index=True,
            height=400
        )

# TAB 5: TASK MANAGEMENT
with tab5:
    styling.create_section_header("Diary Items & Task Management")

    # Task KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        overdue_items = current_data['overdue_diary_items'].sum()
        st.markdown(
            styling.create_kpi_card(
                "Overdue Items",
                metrics.format_number(overdue_items),
                None,
                "current period",
                inverse=True
            ),
            unsafe_allow_html=True
        )

    with col2:
        completed_items = current_data['completed_diary_items'].sum()
        st.markdown(
            styling.create_kpi_card(
                "Completed Items",
                metrics.format_number(completed_items),
                None,
                "current period"
            ),
            unsafe_allow_html=True
        )

    with col3:
        completion_rate = (completed_items / (completed_items + overdue_items) * 100) if (completed_items + overdue_items) > 0 else 0
        st.markdown(
            styling.create_kpi_card(
                "Completion Rate",
                f"{completion_rate:.1f}%",
                None,
                "current period"
            ),
            unsafe_allow_html=True
        )

    with col4:
        avg_overdue_per_pm = overdue_items / len(current_data) if len(current_data) > 0 else 0
        st.markdown(
            styling.create_kpi_card(
                "Avg per PM",
                metrics.format_number(avg_overdue_per_pm, decimals=1),
                None,
                "overdue items"
            ),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Task charts
    col1, col2 = st.columns(2)

    with col1:
        # Overdue items by PM
        pm_overdue = current_data.groupby('portfolio_manager')['overdue_diary_items'].sum().reset_index()
        pm_overdue.columns = ['Portfolio Manager', 'Overdue Items']
        fig = charts.create_horizontal_bar_chart(
            pm_overdue,
            'Overdue Items',
            'Portfolio Manager',
            'Overdue Diary Items by Portfolio Manager'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Completed items by PM
        pm_completed = current_data.groupby('portfolio_manager')['completed_diary_items'].sum().reset_index()
        pm_completed.columns = ['Portfolio Manager', 'Completed Items']
        fig = charts.create_horizontal_bar_chart(
            pm_completed,
            'Completed Items',
            'Portfolio Manager',
            'Completed Diary Items by Portfolio Manager'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Trends over time
    col3, col4 = st.columns(2)

    with col3:
        overdue_trend = df.groupby('date')['overdue_diary_items'].sum().reset_index()
        fig = charts.create_trend_line_chart(
            overdue_trend,
            'date',
            'overdue_diary_items',
            'Overdue Items Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        completed_trend = df.groupby('date')['completed_diary_items'].sum().reset_index()
        fig = charts.create_trend_line_chart(
            completed_trend,
            'date',
            'completed_diary_items',
            'Completed Items Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed diary items
    st.markdown("---")
    styling.create_section_header("Diary Item Details")

    status_filter = st.radio(
        "Select Status",
        ['Overdue', 'Completed'],
        horizontal=True
    )

    diary_items = data_generator.generate_diary_items_details(
        df,
        selected_pm if selected_pm != "All Managers" else "Whole Agency",
        status_filter.lower()
    )

    st.dataframe(
        diary_items.style.format({
            'due_date': lambda x: x.strftime('%Y-%m-%d'),
            'days_overdue': '{:.0f}'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )

# Footer
styling.create_footer()
