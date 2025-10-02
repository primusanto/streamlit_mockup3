"""
Executive Management Dashboard
KPI Dashboard with Interactive Drill-Downs
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Import utilities
import config
from utils import styling, metrics, data_generator, charts, dialogs

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
styling.apply_custom_css()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = data_generator.generate_historical_data(24)

# Sidebar - Filters
with st.sidebar:
    st.markdown("### Dashboard Filters")
    st.markdown("---")

    # Agency filter
    agencies_list = ["Whole Agency"] + sorted(config.AGENCIES)
    selected_agency = st.selectbox(
        "Agency",
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
        "Portfolio Manager",
        pm_list,
        index=0
    )

    st.markdown("---")

    # Date Selection
    st.markdown("### Date Periods")

    df_dates = st.session_state.df['date']
    min_date = df_dates.min().date()
    max_date = df_dates.max().date()

    # Calendar type toggle - shown first
    calendar_type = st.radio(
        "Calendar Type",
        ["Calendar Year", "Financial Year (AU)"],
        horizontal=True
    )

    # Period Type Selection
    period_type = st.selectbox(
        "Period Type",
        ["Week", "Month", "Quarter", "Year", "Custom Date"]
    )

    # Helper function to generate period options
    def generate_weeks(start_date, end_date):
        """Generate list of weeks with week numbers"""
        weeks = []
        current = start_date
        # Start from the first week of the year containing start_date
        year = current.year
        week_num = 1

        # Find the first Monday of the dataset
        first_monday = current - timedelta(days=current.weekday())
        current = first_monday

        while current <= end_date:
            week_start = current
            week_end = week_start + timedelta(days=6)

            # If we cross into a new year, reset week counter
            if week_start.year != year:
                year = week_start.year
                week_num = 1

            weeks.append((f"Week {week_num} {year}", week_end))
            current = week_end + timedelta(days=1)
            week_num += 1
        return weeks

    def generate_months(start_date, end_date):
        """Generate list of months"""
        months = []
        current = datetime(start_date.year, start_date.month, 1)
        end = datetime(end_date.year, end_date.month, 1)
        while current <= end:
            month_name = current.strftime('%B %Y')
            # Last day of month
            if current.month == 12:
                month_end = datetime(current.year, 12, 31).date()
            else:
                month_end = (datetime(current.year, current.month + 1, 1) - timedelta(days=1)).date()
            months.append((month_name, month_end))
            if current.month == 12:
                current = datetime(current.year + 1, 1, 1)
            else:
                current = datetime(current.year, current.month + 1, 1)
        return months

    def generate_quarters(start_date, end_date):
        """Generate list of quarters"""
        quarters = []
        current_year = start_date.year
        end_year = end_date.year
        for year in range(current_year, end_year + 1):
            for q in range(1, 5):
                q_end_month = q * 3
                q_end = datetime(year, q_end_month, 1)
                if q_end_month == 12:
                    q_end = datetime(year, 12, 31).date()
                else:
                    q_end = (datetime(year, q_end_month + 1, 1) - timedelta(days=1)).date()

                if q_end >= start_date and q_end <= end_date:
                    quarters.append((f"Q{q} {year}", q_end))
        return quarters

    # Current period
    st.markdown("**Current Period**")

    if period_type == "Week":
        weeks = generate_weeks(min_date, max_date)
        selected_week = st.selectbox(
            "Select Week",
            [w[0] for w in weeks],
            index=len(weeks)-1,
            key="current_week"
        )
        current_period = weeks[[w[0] for w in weeks].index(selected_week)][1]

    elif period_type == "Month":
        months = generate_months(min_date, max_date)
        selected_month = st.selectbox(
            "Select Month",
            [m[0] for m in months],
            index=len(months)-1,
            key="current_month"
        )
        current_period = months[[m[0] for m in months].index(selected_month)][1]

    elif period_type == "Quarter":
        quarters = generate_quarters(min_date, max_date)
        selected_quarter = st.selectbox(
            "Select Quarter",
            [q[0] for q in quarters],
            index=len(quarters)-1,
            key="current_quarter"
        )
        current_period = quarters[[q[0] for q in quarters].index(selected_quarter)][1]

    elif period_type == "Year":
        if calendar_type == "Financial Year (AU)":
            # Australian Financial Year: July 1 - June 30
            fy_years = []
            for year in range(min_date.year, max_date.year + 2):
                fy_years.append((f"FY {year}/{year+1}", datetime(year+1, 6, 30).date()))

            selected_fy = st.selectbox(
                "Select Financial Year",
                [fy[0] for fy in fy_years],
                index=len(fy_years)-1,
                key="current_fy"
            )
            current_period = fy_years[[fy[0] for fy in fy_years].index(selected_fy)][1]
        else:  # Calendar Year
            cal_years = [(str(year), datetime(year, 12, 31).date()) for year in range(min_date.year, max_date.year + 1)]
            selected_year = st.selectbox(
                "Select Calendar Year",
                [cy[0] for cy in cal_years],
                index=len(cal_years)-1,
                key="current_cal_year"
            )
            current_period = cal_years[[cy[0] for cy in cal_years].index(selected_year)][1]

    else:  # Custom Date
        current_period = st.date_input(
            "Select current date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="current_period"
        )

    # Ask if user wants to compare
    enable_comparison = st.checkbox("Compare with another period?", value=True)

    # Comparison period (only show if enabled)
    if enable_comparison:
        st.markdown("**Comparison Period**")

    if enable_comparison and period_type == "Week":
        comparison_week = st.selectbox(
            "Select Comparison Week",
            [w[0] for w in weeks],
            index=max(0, len(weeks)-2),
            key="comparison_week"
        )
        comparison_period = weeks[[w[0] for w in weeks].index(comparison_week)][1]

    elif enable_comparison and period_type == "Month":
        comparison_month = st.selectbox(
            "Select Comparison Month",
            [m[0] for m in months],
            index=max(0, len(months)-2),
            key="comparison_month"
        )
        comparison_period = months[[m[0] for m in months].index(comparison_month)][1]

    elif enable_comparison and period_type == "Quarter":
        comparison_quarter = st.selectbox(
            "Select Comparison Quarter",
            [q[0] for q in quarters],
            index=max(0, len(quarters)-2),
            key="comparison_quarter"
        )
        comparison_period = quarters[[q[0] for q in quarters].index(comparison_quarter)][1]

    elif enable_comparison and period_type == "Year":
        if calendar_type == "Financial Year (AU)":
            comparison_fy = st.selectbox(
                "Select Comparison FY",
                [fy[0] for fy in fy_years],
                index=max(0, len(fy_years)-2),
                key="comparison_fy"
            )
            comparison_period = fy_years[[fy[0] for fy in fy_years].index(comparison_fy)][1]
        else:  # Calendar Year
            comparison_year = st.selectbox(
                "Select Comparison Year",
                [cy[0] for cy in cal_years],
                index=max(0, len(cal_years)-2),
                key="comparison_cal_year"
            )
            comparison_period = cal_years[[cy[0] for cy in cal_years].index(comparison_year)][1]

    elif enable_comparison and period_type == "Custom Date":
        default_comparison = max_date - timedelta(days=30)
        if default_comparison < min_date:
            default_comparison = min_date

        comparison_period = st.date_input(
            "Select comparison date",
            value=default_comparison,
            min_value=min_date,
            max_value=max_date,
            key="comparison_period"
        )

    # If comparison is disabled, set comparison_period to current_period
    if not enable_comparison:
        comparison_period = current_period

    st.markdown("---")

    # Info section
    st.info(f"**Data Mode:** {'Mock Data' if config.USE_MOCK_DATA else 'Live Data'}")
    st.caption(f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")

    # Refresh button
    if st.button("↻ Refresh Data"):
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

# Get data for current and comparison periods
current_date = pd.Timestamp(current_period)
comparison_date = pd.Timestamp(comparison_period)

# Find closest dates in dataset
current_date_actual = df['date'][df['date'] <= current_date].max()
comparison_date_actual = df['date'][df['date'] <= comparison_date].max()

current_data = df[df['date'] == current_date_actual]
comparison_data = df[df['date'] == comparison_date_actual]

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

comparison_kpis = {
    'landlords': comparison_data['landlords'].sum() if not comparison_data.empty else kpis['landlords'],
    'properties': comparison_data['properties'].sum() if not comparison_data.empty else kpis['properties'],
    'leases': comparison_data['leases'].sum() if not comparison_data.empty else kpis['leases'],
    'vacancies': comparison_data['vacancies'].sum() if not comparison_data.empty else kpis['vacancies'],
    'avg_occupancy': comparison_data['occupancy_rate'].mean() if not comparison_data.empty else kpis['avg_occupancy'],
    'rent_roll': comparison_data['rent_roll'].sum() if not comparison_data.empty else kpis['rent_roll'],
    'total_revenue': comparison_data['total_revenue'].sum() if not comparison_data.empty else kpis['total_revenue'],
    'total_arrears': comparison_data['total_arrears'].sum() if not comparison_data.empty else kpis['total_arrears'],
}

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Management Fees",
    "Arrears",
    "Critical Dates",
    "Task Management"
])

# Track if a dialog was opened (only allow one per run)
dialog_opened = False

# Initialize session state to track last selection to prevent dialog reopening
if 'last_selection' not in st.session_state:
    st.session_state.last_selection = None

# TAB 1: OVERVIEW
with tab1:
    styling.create_section_header("Key Performance Indicators")
    st.markdown("*Click on any KPI card below to see detailed breakdown*")

    # First row of KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['landlords'], comparison_kpis['landlords'])
        if styling.create_clickable_kpi_button(
            "Total Landlords",
            metrics.format_number(kpis['landlords']),
            delta,
            "vs comparison",
            key="landlord_btn"
        ):
            dialogs.show_landlord_details(current_data, comparison_data)

    with col2:
        delta = metrics.calculate_percent_change(kpis['properties'], comparison_kpis['properties'])
        if styling.create_clickable_kpi_button(
            "Total Properties",
            metrics.format_number(kpis['properties']),
            delta,
            "vs comparison",
            key="property_btn"
        ):
            dialogs.show_property_details(current_data, comparison_data)

    with col3:
        delta = metrics.calculate_percent_change(kpis['leases'], comparison_kpis['leases'])
        if styling.create_clickable_kpi_button(
            "Active Leases",
            metrics.format_number(kpis['leases']),
            delta,
            "vs comparison",
            key="lease_btn"
        ):
            dialogs.show_lease_details(current_data, comparison_data)

    with col4:
        delta = metrics.calculate_percent_change(kpis['vacancies'], comparison_kpis['vacancies'])
        vacancy_rate = metrics.calculate_vacancy_rate(kpis['vacancies'], kpis['properties'])
        if styling.create_clickable_kpi_button(
            f"Vacancies ({vacancy_rate:.1f}%)",
            metrics.format_number(kpis['vacancies']),
            delta,
            "vs comparison",
            inverse=True,
            key="vacancy_btn"
        ):
            dialogs.show_vacancy_details(current_data, comparison_data)

    st.markdown("---")

    # Second row of KPIs
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        delta = metrics.calculate_percent_change(kpis['avg_occupancy'], comparison_kpis['avg_occupancy'])
        if styling.create_clickable_kpi_button(
            "Avg Occupancy Rate",
            f"{kpis['avg_occupancy']:.1f}%",
            delta,
            "vs comparison",
            key="occupancy_btn"
        ):
            dialogs.show_occupancy_details(current_data, comparison_data)

    with col6:
        delta = metrics.calculate_percent_change(kpis['rent_roll'], comparison_kpis['rent_roll'])
        if styling.create_clickable_kpi_button(
            "Total Rent Roll",
            metrics.format_currency(kpis['rent_roll']),
            delta,
            "vs comparison",
            key="rent_roll_btn"
        ):
            dialogs.show_rent_roll_details(current_data, comparison_data, df)

    with col7:
        delta = metrics.calculate_percent_change(kpis['total_arrears'], comparison_kpis['total_arrears'])
        if styling.create_clickable_kpi_button(
            "Total Arrears",
            metrics.format_currency(kpis['total_arrears']),
            delta,
            "vs comparison",
            inverse=True,
            key="arrears_btn"
        ):
            dialogs.show_arrears_details(current_data, comparison_data, df, selected_pm)

    with col8:
        arrears_pct = metrics.calculate_arrears_percentage(kpis['total_arrears'], kpis['rent_roll'])
        comparison_arrears_pct = metrics.calculate_arrears_percentage(comparison_kpis['total_arrears'], comparison_kpis['rent_roll'])
        delta = arrears_pct - comparison_arrears_pct
        if styling.create_clickable_kpi_button(
            "Arrears Ratio",
            f"{arrears_pct:.1f}%",
            delta,
            "vs comparison",
            inverse=True,
            key="arrears_ratio_btn"
        ):
            dialogs.show_arrears_ratio_details(current_data, comparison_data)

    st.markdown("---")

    # Charts section
    styling.create_section_header("Performance Trends & Analytics")

    col1, col2 = st.columns(2)

    with col1:
        pm_properties = current_data.groupby('portfolio_manager')['properties'].sum().reset_index()
        pm_properties.columns = ['Portfolio Manager', 'Properties']
        fig = charts.create_horizontal_bar_chart(
            pm_properties,
            'Properties',
            'Portfolio Manager',
            'Properties by Portfolio Manager'
        )
        properties_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="properties_chart")

        if not dialog_opened and properties_event and len(properties_event.selection.get("points", [])) > 0:
            selected_pm = properties_event.selection["points"][0]["y"]
            selection_key = f"properties_{selected_pm}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm].iloc[0]
                dialogs.show_pm_property_list(pm_data, selected_pm)
                dialog_opened = True

        if not dialog_opened and st.button("📊 View Summary & Download", key="chart_properties_btn", use_container_width=True):
            dialogs.show_property_details(current_data, comparison_data)
            dialog_opened = True

    with col2:
        pm_leases = current_data.groupby('portfolio_manager')['leases'].sum().reset_index()
        pm_leases.columns = ['Portfolio Manager', 'Leases']
        fig = charts.create_horizontal_bar_chart(
            pm_leases,
            'Leases',
            'Portfolio Manager',
            'Active Leases by Portfolio Manager'
        )
        leases_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="leases_chart", selection_mode="points")

        if not dialog_opened and leases_event and len(leases_event.selection.get("points", [])) > 0:
            selected_pm = leases_event.selection["points"][0]["y"]
            selection_key = f"leases_{selected_pm}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm].iloc[0]
                dialogs.show_pm_lease_list(pm_data, selected_pm)
                dialog_opened = True

        if not dialog_opened and st.button("📊 View Summary & Download", key="chart_leases_btn", use_container_width=True):
            dialogs.show_lease_details(current_data, comparison_data)
            dialog_opened = True

    col3, col4 = st.columns(2)

    with col3:
        trend_data = df.groupby('date')['properties'].sum().reset_index()
        fig = charts.create_trend_line_chart(
            trend_data,
            'date',
            'properties',
            'Property Count Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.button("📊 View Details & Download", key="chart_property_trend", use_container_width=True):
            dialogs.show_property_trend_details(df)

    with col4:
        trend_data = df.groupby('date')['occupancy_rate'].mean().reset_index()
        fig = charts.create_trend_line_chart(
            trend_data,
            'date',
            'occupancy_rate',
            'Average Occupancy Rate Trend',
            show_area=True
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.button("📊 View Details & Download", key="chart_occupancy_trend", use_container_width=True):
            dialogs.show_occupancy_trend_details(df)

# TAB 2: MANAGEMENT FEES
with tab2:
    styling.create_section_header("Revenue & Management Fees")

    # Revenue KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['total_revenue'], comparison_kpis['total_revenue'])
        if styling.create_clickable_kpi_button(
            "Total Revenue",
            metrics.format_currency(kpis['total_revenue']),
            delta,
            "vs comparison",
            key="total_revenue_btn"
        ):
            dialogs.show_revenue_details(current_data, comparison_data, df)

    with col2:
        mgmt_fees = current_data['management_fees'].sum()
        comparison_mgmt = comparison_data['management_fees'].sum() if not comparison_data.empty else mgmt_fees
        delta = metrics.calculate_percent_change(mgmt_fees, comparison_mgmt)
        if styling.create_clickable_kpi_button(
            "Management Fees",
            metrics.format_currency(mgmt_fees),
            delta,
            "vs comparison",
            key="mgmt_fees_btn"
        ):
            dialogs.show_management_fees_details(current_data, comparison_data, df)

    with col3:
        leasing_fees = current_data['leasing_fees'].sum()
        comparison_leasing = comparison_data['leasing_fees'].sum() if not comparison_data.empty else leasing_fees
        delta = metrics.calculate_percent_change(leasing_fees, comparison_leasing)
        if styling.create_clickable_kpi_button(
            "Leasing Fees",
            metrics.format_currency(leasing_fees),
            delta,
            "vs comparison",
            key="leasing_fees_btn"
        ):
            dialogs.show_leasing_fees_details(current_data, comparison_data, df)

    with col4:
        avg_fee = kpis['avg_fee']
        comparison_avg_fee = comparison_data['avg_fee_per_tenancy'].mean() if not comparison_data.empty else avg_fee
        delta = metrics.calculate_percent_change(avg_fee, comparison_avg_fee)
        if styling.create_clickable_kpi_button(
            "Avg Fee per Tenancy",
            metrics.format_currency(avg_fee),
            delta,
            "vs comparison",
            key="avg_fee_btn"
        ):
            dialogs.show_avg_fee_details(current_data, comparison_data, df)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
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

    pm_revenue = current_data.groupby('portfolio_manager')['total_revenue'].sum().reset_index()
    pm_revenue.columns = ['Portfolio Manager', 'Revenue']
    fig = charts.create_horizontal_bar_chart(
        pm_revenue,
        'Revenue',
        'Portfolio Manager',
        'Revenue by Portfolio Manager'
    )
    revenue_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="revenue_chart")

    if not dialog_opened and revenue_event and len(revenue_event.selection.get("points", [])) > 0:
        selected_pm = revenue_event.selection["points"][0]["y"]
        selection_key = f"revenue_{selected_pm}"
        if st.session_state.last_selection != selection_key:
            st.session_state.last_selection = selection_key
            pm_data = current_data[current_data['portfolio_manager'] == selected_pm].iloc[0]
            dialogs.show_pm_revenue_details(pm_data, selected_pm)
            dialog_opened = True

    if not dialog_opened and st.button("📊 View Summary & Download", key="chart_revenue_pm_btn", use_container_width=True):
        dialogs.show_revenue_details(current_data, comparison_data, df)
        dialog_opened = True

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta = metrics.calculate_percent_change(kpis['total_arrears'], comparison_kpis['total_arrears'])
        if styling.create_clickable_kpi_button(
            "Total Arrears",
            metrics.format_currency(kpis['total_arrears']),
            delta,
            "vs comparison",
            inverse=True,
            key="total_arrears_btn"
        ):
            dialogs.show_arrears_details(current_data, comparison_data, df, None)

    with col2:
        arrears_0_30 = current_data['arrears_0_30'].sum()
        comparison_arrears_0_30 = comparison_data['arrears_0_30'].sum() if not comparison_data.empty else arrears_0_30
        delta = metrics.calculate_percent_change(arrears_0_30, comparison_arrears_0_30)
        if styling.create_clickable_kpi_button(
            "0-30 Days",
            metrics.format_currency(arrears_0_30),
            delta,
            "vs comparison",
            key="arrears_0_30_btn"
        ):
            dialogs.show_arrears_0_30_details(current_data, comparison_data)

    with col3:
        arrears_31_60 = current_data['arrears_31_60'].sum()
        comparison_arrears_31_60 = comparison_data['arrears_31_60'].sum() if not comparison_data.empty else arrears_31_60
        delta = metrics.calculate_percent_change(arrears_31_60, comparison_arrears_31_60)
        if styling.create_clickable_kpi_button(
            "31-60 Days",
            metrics.format_currency(arrears_31_60),
            delta,
            "vs comparison",
            key="arrears_31_60_btn"
        ):
            dialogs.show_arrears_31_60_details(current_data, comparison_data)

    with col4:
        arrears_90_plus = current_data['arrears_90_plus'].sum()
        comparison_arrears_90_plus = comparison_data['arrears_90_plus'].sum() if not comparison_data.empty else arrears_90_plus
        delta = metrics.calculate_percent_change(arrears_90_plus, comparison_arrears_90_plus)
        if styling.create_clickable_kpi_button(
            "90+ Days",
            metrics.format_currency(arrears_90_plus),
            delta,
            "vs comparison",
            inverse=True,
            key="arrears_90_plus_btn"
        ):
            dialogs.show_arrears_90_plus_details(current_data, comparison_data)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
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
        arrears_bar_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="arrears_bucket_chart")

        if not dialog_opened and arrears_bar_event and len(arrears_bar_event.selection.get("points", [])) > 0:
            selected_bucket = arrears_bar_event.selection["points"][0]["x"]
            selection_key = f"arrears_bar_{selected_bucket}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                dialogs.show_arrears_bucket_list(df, selected_bucket, selected_pm)
                dialog_opened = True

    with col2:
        arrears_buckets['Percentage'] = (arrears_buckets['Amount'] / arrears_buckets['Amount'].sum() * 100).round(1)
        fig = charts.create_donut_chart(
            arrears_buckets,
            'Amount',
            'Bucket',
            'Arrears Distribution'
        )
        arrears_donut_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="arrears_donut_chart")

        if not dialog_opened and arrears_donut_event and len(arrears_donut_event.selection.get("points", [])) > 0:
            selected_bucket = arrears_donut_event.selection["points"][0]["label"]
            selection_key = f"arrears_donut_{selected_bucket}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                dialogs.show_arrears_bucket_list(df, selected_bucket, selected_pm)
                dialog_opened = True

    arrears_trend = df.groupby('date')['total_arrears'].sum().reset_index()
    fig = charts.create_trend_line_chart(
        arrears_trend,
        'date',
        'total_arrears',
        'Total Arrears Trend',
        show_area=True
    )
    st.plotly_chart(fig, use_container_width=True)

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rent_reviews = current_data['rent_reviews_upcoming'].sum()
        comparison_rent_reviews = comparison_data['rent_reviews_upcoming'].sum() if not comparison_data.empty else rent_reviews
        delta = metrics.calculate_percent_change(rent_reviews, comparison_rent_reviews)
        if styling.create_clickable_kpi_button(
            "Rent Reviews",
            metrics.format_number(rent_reviews),
            delta,
            "vs comparison",
            key="rent_reviews_btn"
        ):
            dialogs.show_rent_reviews_details(current_data, comparison_data)

    with col2:
        lease_expiries = current_data['lease_expiries_upcoming'].sum()
        comparison_lease_expiries = comparison_data['lease_expiries_upcoming'].sum() if not comparison_data.empty else lease_expiries
        delta = metrics.calculate_percent_change(lease_expiries, comparison_lease_expiries)
        if styling.create_clickable_kpi_button(
            "Lease Expiries",
            metrics.format_number(lease_expiries),
            delta,
            "vs comparison",
            key="lease_expiries_btn"
        ):
            dialogs.show_lease_expiries_details(current_data, comparison_data)

    with col3:
        next_month_reviews = int(rent_reviews / 12 * 1.2)
        comparison_next_month_reviews = int(comparison_rent_reviews / 12 * 1.2) if not comparison_data.empty else next_month_reviews
        delta = metrics.calculate_percent_change(next_month_reviews, comparison_next_month_reviews)
        if styling.create_clickable_kpi_button(
            "Next Month Reviews",
            metrics.format_number(next_month_reviews),
            delta,
            "vs comparison",
            key="next_month_reviews_btn"
        ):
            dialogs.show_rent_reviews_details(current_data, comparison_data)

    with col4:
        next_month_expiries = int(lease_expiries / 12 * 1.1)
        comparison_next_month_expiries = int(comparison_lease_expiries / 12 * 1.1) if not comparison_data.empty else next_month_expiries
        delta = metrics.calculate_percent_change(next_month_expiries, comparison_next_month_expiries)
        if styling.create_clickable_kpi_button(
            "Next Month Expiries",
            metrics.format_number(next_month_expiries),
            delta,
            "vs comparison",
            key="next_month_expiries_btn"
        ):
            dialogs.show_lease_expiries_details(current_data, comparison_data)

    st.markdown("---")
    styling.create_section_header("Breakdown by Portfolio Manager")

    col1, col2 = st.columns(2)

    with col1:
        pm_rent_reviews = current_data.groupby('portfolio_manager')['rent_reviews_upcoming'].sum().reset_index()
        pm_rent_reviews.columns = ['Portfolio Manager', 'Rent Reviews']
        fig = charts.create_horizontal_bar_chart(
            pm_rent_reviews,
            'Rent Reviews',
            'Portfolio Manager',
            'Rent Reviews by Portfolio Manager'
        )
        rent_reviews_pm_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="rent_reviews_pm_chart")

        if not dialog_opened and rent_reviews_pm_event and len(rent_reviews_pm_event.selection.get("points", [])) > 0:
            selected_pm_name = rent_reviews_pm_event.selection["points"][0]["y"]
            selection_key = f"rent_reviews_pm_{selected_pm_name}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm_name].iloc[0]
                dialogs.show_pm_rent_reviews_list(pm_data, selected_pm_name)
                dialog_opened = True

    with col2:
        pm_lease_expiries = current_data.groupby('portfolio_manager')['lease_expiries_upcoming'].sum().reset_index()
        pm_lease_expiries.columns = ['Portfolio Manager', 'Lease Expiries']
        fig = charts.create_horizontal_bar_chart(
            pm_lease_expiries,
            'Lease Expiries',
            'Portfolio Manager',
            'Lease Expiries by Portfolio Manager'
        )
        lease_expiries_pm_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="lease_expiries_pm_chart")

        if not dialog_opened and lease_expiries_pm_event and len(lease_expiries_pm_event.selection.get("points", [])) > 0:
            selected_pm_name = lease_expiries_pm_event.selection["points"][0]["y"]
            selection_key = f"lease_expiries_pm_{selected_pm_name}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm_name].iloc[0]
                dialogs.show_pm_lease_expiries_list(pm_data, selected_pm_name)
                dialog_opened = True

    st.markdown("---")
    styling.create_section_header("Trend Analysis")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        overdue_items = current_data['overdue_diary_items'].sum()
        comparison_overdue = comparison_data['overdue_diary_items'].sum() if not comparison_data.empty else overdue_items
        delta = metrics.calculate_percent_change(overdue_items, comparison_overdue)
        if styling.create_clickable_kpi_button(
            "Overdue Items",
            metrics.format_number(overdue_items),
            delta,
            "vs comparison",
            inverse=True,
            key="overdue_items_btn"
        ):
            dialogs.show_overdue_items_details(current_data, comparison_data)

    with col2:
        completed_items = current_data['completed_diary_items'].sum()
        comparison_completed = comparison_data['completed_diary_items'].sum() if not comparison_data.empty else completed_items
        delta = metrics.calculate_percent_change(completed_items, comparison_completed)
        if styling.create_clickable_kpi_button(
            "Completed Items",
            metrics.format_number(completed_items),
            delta,
            "vs comparison",
            key="completed_items_btn"
        ):
            dialogs.show_completed_items_details(current_data, comparison_data)

    with col3:
        completion_rate = (completed_items / (completed_items + overdue_items) * 100) if (completed_items + overdue_items) > 0 else 0
        comparison_completion_rate = (comparison_completed / (comparison_completed + comparison_overdue) * 100) if (comparison_completed + comparison_overdue) > 0 else 0
        delta = completion_rate - comparison_completion_rate
        if styling.create_clickable_kpi_button(
            "Completion Rate",
            f"{completion_rate:.1f}%",
            delta,
            "vs comparison",
            key="completion_rate_btn"
        ):
            dialogs.show_completed_items_details(current_data, comparison_data)

    with col4:
        avg_overdue_per_pm = overdue_items / len(current_data) if len(current_data) > 0 else 0
        comparison_avg_overdue_per_pm = comparison_overdue / len(comparison_data) if len(comparison_data) > 0 else avg_overdue_per_pm
        delta = metrics.calculate_percent_change(avg_overdue_per_pm, comparison_avg_overdue_per_pm)
        if styling.create_clickable_kpi_button(
            "Avg per PM",
            metrics.format_number(avg_overdue_per_pm, decimals=1),
            delta,
            "vs comparison",
            inverse=True,
            key="avg_per_pm_btn"
        ):
            dialogs.show_overdue_items_details(current_data, comparison_data)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        pm_overdue = current_data.groupby('portfolio_manager')['overdue_diary_items'].sum().reset_index()
        pm_overdue.columns = ['Portfolio Manager', 'Overdue Items']
        fig = charts.create_horizontal_bar_chart(
            pm_overdue,
            'Overdue Items',
            'Portfolio Manager',
            'Overdue Diary Items by Portfolio Manager'
        )
        overdue_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="overdue_chart")

        if not dialog_opened and overdue_event and len(overdue_event.selection.get("points", [])) > 0:
            selected_pm = overdue_event.selection["points"][0]["y"]
            selection_key = f"overdue_{selected_pm}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm].iloc[0]
                dialogs.show_pm_overdue_items_list(pm_data, selected_pm)
                dialog_opened = True

        if not dialog_opened and st.button("📊 View Summary & Download", key="chart_overdue_btn", use_container_width=True):
            pm_current = current_data
            pm_comparison = comparison_data if not comparison_data.empty else current_data
            dialogs.show_overdue_items_details(pm_current, pm_comparison)
            dialog_opened = True

    with col2:
        pm_completed = current_data.groupby('portfolio_manager')['completed_diary_items'].sum().reset_index()
        pm_completed.columns = ['Portfolio Manager', 'Completed Items']
        fig = charts.create_horizontal_bar_chart(
            pm_completed,
            'Completed Items',
            'Portfolio Manager',
            'Completed Diary Items by Portfolio Manager'
        )
        completed_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="completed_chart")

        if not dialog_opened and completed_event and len(completed_event.selection.get("points", [])) > 0:
            selected_pm = completed_event.selection["points"][0]["y"]
            selection_key = f"completed_{selected_pm}"
            if st.session_state.last_selection != selection_key:
                st.session_state.last_selection = selection_key
                pm_data = current_data[current_data['portfolio_manager'] == selected_pm].iloc[0]
                dialogs.show_pm_completed_items_list(pm_data, selected_pm)
                dialog_opened = True

        if not dialog_opened and st.button("📊 View Summary & Download", key="chart_completed_btn", use_container_width=True):
            pm_current = current_data
            pm_comparison = comparison_data if not comparison_data.empty else current_data
            dialogs.show_completed_items_details(pm_current, pm_comparison)
            dialog_opened = True

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
