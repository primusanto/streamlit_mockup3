"""
Dialog/Modal components for interactive drill-downs
"""
import streamlit as st
import pandas as pd
from utils import charts, metrics, data_generator

def create_download_button(data: pd.DataFrame, filename: str, label: str = "📥 Download CSV"):
    """Helper function to create a download button for dataframe"""
    csv = data.to_csv(index=False)
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )

@st.dialog("Landlord Details", width="large")
def show_landlord_details(current_data, comparison_data):
    """Show detailed landlord breakdown"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Landlords by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['landlords'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['landlords'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button
    with col_download:
        create_download_button(breakdown, "landlords_by_pm.csv")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        # Create grouped bar chart
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Landlords by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Period comparison summary
    st.markdown("---")
    st.markdown("### Period Comparison Summary")

    current_total = current_data['landlords'].sum()
    comparison_total = comparison_data['landlords'].sum() if not comparison_data.empty else current_total

    comparison_df = pd.DataFrame({
        'Period': ['Comparison Period', 'Current Period'],
        'Landlords': [comparison_total, current_total]
    })

    fig = charts.create_horizontal_bar_chart(
        comparison_df,
        'Landlords',
        'Period',
        'Landlords - Period Comparison'
    )
    st.plotly_chart(fig, use_container_width=True)

@st.dialog("Property Details", width="large")
def show_property_details(current_data, comparison_data):
    """Show detailed property breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Properties by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['properties'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['properties'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "properties_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Properties by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Lease Details", width="large")
def show_lease_details(current_data, comparison_data):
    """Show detailed lease breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Active Leases by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['leases'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['leases'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "leases_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Active Leases by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Vacancy Details", width="large")
def show_vacancy_details(current_data, comparison_data):
    """Show detailed vacancy breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Vacancies by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['vacancies'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['vacancies'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "vacancies_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Vacancies by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Occupancy Rate Details", width="large")
def show_occupancy_details(current_data, comparison_data):
    """Show detailed occupancy breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Occupancy Rate by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['occupancy_rate'].mean().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']
    current_breakdown['Current Period'] = current_breakdown['Current Period'].round(1)

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['occupancy_rate'].mean().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']
    comparison_breakdown['Comparison Period'] = comparison_breakdown['Comparison Period'].round(1)

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "occupancy_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.1f}%',
                'Comparison Period': '{:.1f}%',
                'Change': '{:+.1f}%',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Occupancy Rate by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Occupancy Rate (%)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Rent Roll Details", width="large")
def show_rent_roll_details(current_data, comparison_data, df):
    """Show detailed rent roll breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Rent Roll by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['rent_roll'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['rent_roll'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "rent_roll_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Rent Roll by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Rent Roll ($)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Trend chart
    st.markdown("---")
    st.markdown("### Rent Roll Trend")
    rent_trend = df.groupby(['date', 'portfolio_manager'])['rent_roll'].sum().reset_index()
    fig = charts.create_trend_line_chart(
        rent_trend,
        'date',
        'rent_roll',
        'Rent Roll Trend Over Time',
        group_col='portfolio_manager'
    )
    st.plotly_chart(fig, use_container_width=True)

@st.dialog("Arrears Details", width="large")
def show_arrears_details(current_data, comparison_data, df, selected_pm):
    """Show detailed arrears breakdown"""
    from utils import data_generator

    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Arrears Analysis")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['total_arrears'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['total_arrears'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "arrears_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Arrears by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Arrears ($)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Arrears aging breakdown
    st.markdown("---")
    st.markdown("### Arrears by Age")

    aging_data = pd.DataFrame({
        'Age Range': ['0-30 days', '31-60 days', '61-90 days', '90+ days'],
        'Amount': [
            current_data['arrears_0_30'].sum(),
            current_data['arrears_31_60'].sum(),
            current_data['arrears_61_90'].sum(),
            current_data['arrears_90_plus'].sum()
        ]
    })

    fig = charts.create_arrears_bucket_chart(aging_data, 'Arrears by Days Overdue')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed drill-down
    st.markdown("---")
    st.markdown("### Tenant Details")

    selected_bucket = st.selectbox(
        "Select Arrears Bucket",
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

@st.dialog("Total Revenue Details", width="large")
def show_revenue_details(current_data, comparison_data, df):
    """Show detailed revenue breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Total Revenue by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['total_revenue'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['total_revenue'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "revenue_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Total Revenue by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Management Fees Details", width="large")
def show_management_fees_details(current_data, comparison_data, df):
    """Show detailed management fees breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Management Fees by Portfolio Manager")

    current_breakdown = current_data.groupby('portfolio_manager')['management_fees'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['management_fees'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "management_fees_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Management Fees by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Leasing Fees Details", width="large")
def show_leasing_fees_details(current_data, comparison_data, df):
    """Show detailed leasing fees breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Leasing Fees by Portfolio Manager")

    current_breakdown = current_data.groupby('portfolio_manager')['leasing_fees'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['leasing_fees'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "leasing_fees_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Leasing Fees by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Avg Fee per Tenancy Details", width="large")
def show_avg_fee_details(current_data, comparison_data, df):
    """Show detailed average fee breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Average Fee per Tenancy by Portfolio Manager")

    current_breakdown = current_data.groupby('portfolio_manager')['avg_fee_per_tenancy'].mean().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['avg_fee_per_tenancy'].mean().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "avg_fee_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Avg Fee per Tenancy by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Arrears Ratio Details", width="large")
def show_arrears_ratio_details(current_data, comparison_data):
    """Show arrears ratio breakdown"""
    st.markdown("### Arrears Ratio by Portfolio Manager")

    arrears_ratio_breakdown = current_data.groupby('portfolio_manager').agg({
        'total_arrears': 'sum',
        'rent_roll': 'sum'
    }).reset_index()
    arrears_ratio_breakdown['Arrears Ratio (%)'] = (
        arrears_ratio_breakdown['total_arrears'] / arrears_ratio_breakdown['rent_roll'] * 100
    ).round(1)
    arrears_ratio_breakdown = arrears_ratio_breakdown[['portfolio_manager', 'Arrears Ratio (%)']].sort_values('Arrears Ratio (%)', ascending=False)
    arrears_ratio_breakdown.columns = ['Portfolio Manager', 'Arrears Ratio (%)']

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            arrears_ratio_breakdown,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = charts.create_horizontal_bar_chart(
            arrears_ratio_breakdown,
            'Arrears Ratio (%)',
            'Portfolio Manager',
            'Arrears Ratio by Portfolio Manager'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Period comparison
    st.markdown("---")
    st.markdown("### Period Comparison")

    current_ratio = (current_data['total_arrears'].sum() / current_data['rent_roll'].sum() * 100) if current_data['rent_roll'].sum() > 0 else 0
    comparison_ratio = (comparison_data['total_arrears'].sum() / comparison_data['rent_roll'].sum() * 100) if not comparison_data.empty and comparison_data['rent_roll'].sum() > 0 else current_ratio

    comparison_df = pd.DataFrame({
        'Period': ['Comparison Period', 'Current Period'],
        'Arrears Ratio (%)': [comparison_ratio, current_ratio]
    })

    fig = charts.create_horizontal_bar_chart(
        comparison_df,
        'Arrears Ratio (%)',
        'Period',
        'Arrears Ratio - Period Comparison'
    )
    st.plotly_chart(fig, use_container_width=True)

@st.dialog("Arrears 0-30 Days Details", width="large")
def show_arrears_0_30_details(current_data, comparison_data):
    """Show detailed 0-30 days arrears breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### 0-30 Days Arrears by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['arrears_0_30'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['arrears_0_30'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "arrears_0_30_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='0-30 Days Arrears by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Amount ($)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Arrears 31-60 Days Details", width="large")
def show_arrears_31_60_details(current_data, comparison_data):
    """Show detailed 31-60 days arrears breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### 31-60 Days Arrears by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['arrears_31_60'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['arrears_31_60'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "arrears_31_60_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='31-60 Days Arrears by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Amount ($)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Arrears 90+ Days Details", width="large")
def show_arrears_90_plus_details(current_data, comparison_data):
    """Show detailed 90+ days arrears breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### 90+ Days Arrears by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['arrears_90_plus'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['arrears_90_plus'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "arrears_90_plus_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '${:,.0f}',
                'Comparison Period': '${:,.0f}',
                'Change': '${:+,.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='90+ Days Arrears by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Amount ($)'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)
@st.dialog("Rent Reviews Details", width="large")
def show_rent_reviews_details(current_data, comparison_data):
    """Show detailed rent reviews breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Upcoming Rent Reviews by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['rent_reviews_upcoming'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['rent_reviews_upcoming'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "rent_reviews_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Rent Reviews by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Count'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Lease Expiries Details", width="large")
def show_lease_expiries_details(current_data, comparison_data):
    """Show detailed lease expiries breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Upcoming Lease Expiries by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['lease_expiries_upcoming'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['lease_expiries_upcoming'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "lease_expiries_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Lease Expiries by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Count'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Overdue Items Details", width="large")
def show_overdue_items_details(current_data, comparison_data):
    """Show detailed overdue items breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Overdue Diary Items by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['overdue_diary_items'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['overdue_diary_items'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "overdue_items_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Overdue Items by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Count'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Completed Items Details", width="large")
def show_completed_items_details(current_data, comparison_data):
    """Show detailed completed items breakdown"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Completed Diary Items by Portfolio Manager")

    # Get data for both periods
    current_breakdown = current_data.groupby('portfolio_manager')['completed_diary_items'].sum().reset_index()
    current_breakdown.columns = ['Portfolio Manager', 'Current Period']

    comparison_breakdown = comparison_data.groupby('portfolio_manager')['completed_diary_items'].sum().reset_index() if not comparison_data.empty else current_breakdown.copy()
    comparison_breakdown.columns = ['Portfolio Manager', 'Comparison Period']

    # Merge both periods
    breakdown = current_breakdown.merge(comparison_breakdown, on='Portfolio Manager', how='outer').fillna(0)
    breakdown['Change'] = breakdown['Current Period'] - breakdown['Comparison Period']
    breakdown['Change %'] = ((breakdown['Current Period'] - breakdown['Comparison Period']) / breakdown['Comparison Period'] * 100).round(1)
    breakdown = breakdown.sort_values('Current Period', ascending=False)

    # Download button

    with col_download:

        create_download_button(breakdown, "completed_items_by_pm.csv")


    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            breakdown.style.format({
                'Current Period': '{:.0f}',
                'Comparison Period': '{:.0f}',
                'Change': '{:+.0f}',
                'Change %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Comparison Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Comparison Period'],
            orientation='h',
            marker=dict(color='#d4b000')
        ))
        fig.add_trace(go.Bar(
            name='Current Period',
            y=breakdown['Portfolio Manager'],
            x=breakdown['Current Period'],
            orientation='h',
            marker=dict(color='#ffe512')
        ))

        fig.update_layout(
            title='Completed Items by Portfolio Manager',
            barmode='group',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Count'),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Property Count Trend", width="large")
def show_property_trend_details(df):
    """Show property count trend data"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Property Count Over Time")

    # Get trend data
    trend_data = df.groupby('date')['properties'].sum().reset_index()
    trend_data.columns = ['Date', 'Properties']
    trend_data = trend_data.sort_values('Date')

    # Download button
    with col_download:
        create_download_button(trend_data, "property_count_trend.csv")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            trend_data.style.format({
                'Date': lambda x: x.strftime('%Y-%m-%d'),
                'Properties': '{:.0f}'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Properties'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='#ffe512', width=2),
            fillcolor='rgba(255, 229, 18, 0.3)'
        ))

        fig.update_layout(
            title='Property Count Trend',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Date'),
            yaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Properties')
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Occupancy Rate Trend", width="large")
def show_occupancy_trend_details(df):
    """Show occupancy rate trend data"""
    import plotly.graph_objects as go

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown("### Average Occupancy Rate Over Time")

    # Get trend data
    trend_data = df.groupby('date')['occupancy_rate'].mean().reset_index()
    trend_data.columns = ['Date', 'Occupancy Rate']
    trend_data = trend_data.sort_values('Date')

    # Download button
    with col_download:
        create_download_button(trend_data, "occupancy_rate_trend.csv")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            trend_data.style.format({
                'Date': lambda x: x.strftime('%Y-%m-%d'),
                'Occupancy Rate': '{:.2f}%'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Occupancy Rate'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='#ffe512', width=2),
            fillcolor='rgba(255, 229, 18, 0.3)'
        ))

        fig.update_layout(
            title='Average Occupancy Rate Trend',
            height=400,
            font=dict(family="Lato, sans-serif", size=12, color="#595959"),
            title_font=dict(family="Playfair Display, serif", size=16, color="#595959"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Date'),
            yaxis=dict(showgrid=True, gridcolor='#e5e5e0', title='Occupancy Rate (%)')
        )

        st.plotly_chart(fig, use_container_width=True)

@st.dialog("Property List", width="large")
def show_pm_property_list(pm_data: pd.Series, pm_name: str):
    """Show detailed property list for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Properties Managed by {pm_name}")

    # Generate property list
    property_list = data_generator.generate_property_list(pm_data, pm_name)

    # Download button
    with col_download:
        create_download_button(property_list, f"properties_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Properties: {len(property_list)} | Leased: {(property_list['Status'] == 'Leased').sum()} | Vacant: {(property_list['Status'] == 'Vacant').sum()}**")

    st.dataframe(
        property_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Lease List", width="large")
def show_pm_lease_list(pm_data: pd.Series, pm_name: str):
    """Show detailed lease list for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Active Leases Managed by {pm_name}")

    # Generate lease list
    lease_list = data_generator.generate_lease_list(pm_data, pm_name)

    # Download button
    with col_download:
        create_download_button(lease_list, f"leases_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Active Leases: {len(lease_list)}**")

    st.dataframe(
        lease_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Overdue Diary Items", width="large")
def show_pm_overdue_items_list(pm_data: pd.Series, pm_name: str):
    """Show detailed overdue diary items list for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Overdue Diary Items - {pm_name}")

    # Generate diary items list
    items_list = data_generator.generate_diary_items_list(pm_data, pm_name, "overdue")

    # Download button
    with col_download:
        create_download_button(items_list, f"overdue_items_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Overdue Items: {len(items_list)}**")

    st.dataframe(
        items_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Completed Diary Items", width="large")
def show_pm_completed_items_list(pm_data: pd.Series, pm_name: str):
    """Show detailed completed diary items list for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Completed Diary Items - {pm_name}")

    # Generate diary items list
    items_list = data_generator.generate_diary_items_list(pm_data, pm_name, "completed")

    # Download button
    with col_download:
        create_download_button(items_list, f"completed_items_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Completed Items: {len(items_list)}**")

    st.dataframe(
        items_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Arrears Bucket Details", width="large")
def show_arrears_bucket_list(df: pd.DataFrame, bucket_name: str, selected_pm: str):
    """Show detailed tenant arrears list for a specific bucket"""
    # Ensure bucket_name is a string
    bucket_name = str(bucket_name)

    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Arrears: {bucket_name}")

    # Map bucket name to bucket parameter
    bucket_map = {
        '0-30 days': '0-30',
        '31-60 days': '31-60',
        '61-90 days': '61-90',
        '90+ days': '90+'
    }
    bucket_param = bucket_map.get(bucket_name)

    # Generate arrears details list
    arrears_list = data_generator.generate_arrears_details(df, selected_pm, bucket_param)

    # Download button - safe filename
    filename = f"arrears_{bucket_name.replace(' ', '_').replace('+', 'plus')}.csv"
    with col_download:
        create_download_button(arrears_list, filename)

    total_amount = arrears_list['amount_overdue'].sum()
    st.markdown(f"**Total Properties: {len(arrears_list)} | Total Amount: ${total_amount:,.2f}**")

    # Format the amount_overdue column as currency
    arrears_list['amount_overdue'] = arrears_list['amount_overdue'].apply(lambda x: f"${x:,.2f}")

    st.dataframe(
        arrears_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Revenue Details", width="large")
def show_pm_revenue_details(pm_data: pd.Series, pm_name: str):
    """Show detailed revenue breakdown for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Revenue Breakdown - {pm_name}")

    # Create revenue breakdown
    revenue_breakdown = pd.DataFrame({
        'Revenue Type': ['Management Fees', 'Leasing Fees', 'Other Fees'],
        'Amount': [
            pm_data['management_fees'],
            pm_data['leasing_fees'],
            pm_data['other_fees']
        ]
    })

    # Download button
    with col_download:
        create_download_button(revenue_breakdown, f"revenue_{pm_name.replace(' ', '_')}.csv")

    total_revenue = revenue_breakdown['Amount'].sum()
    st.markdown(f"**Total Revenue: ${total_revenue:,.2f}**")

    # Show breakdown as table
    revenue_breakdown['Percentage'] = (revenue_breakdown['Amount'] / total_revenue * 100).round(1)
    revenue_breakdown['Amount'] = revenue_breakdown['Amount'].apply(lambda x: f"${x:,.2f}")
    revenue_breakdown['Percentage'] = revenue_breakdown['Percentage'].apply(lambda x: f"{x}%")

    st.dataframe(
        revenue_breakdown,
        use_container_width=True,
        hide_index=True,
        height=200
    )

    st.markdown("---")
    st.markdown("### Property Metrics")

    metrics_data = pd.DataFrame({
        'Metric': ['Total Properties', 'Active Leases', 'Vacancies', 'Occupancy Rate', 'Avg Fee per Tenancy'],
        'Value': [
            f"{int(pm_data['properties'])}",
            f"{int(pm_data['leases'])}",
            f"{int(pm_data['vacancies'])}",
            f"{pm_data['occupancy_rate']:.1f}%",
            f"${pm_data['avg_fee_per_tenancy']:,.2f}"
        ]
    })

    st.dataframe(
        metrics_data,
        use_container_width=True,
        hide_index=True,
        height=250
    )

@st.dialog("Rent Reviews", width="large")
def show_pm_rent_reviews_list(pm_data: pd.Series, pm_name: str):
    """Show list of properties with upcoming rent reviews for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Rent Reviews - {pm_name}")

    # Generate rent reviews list
    reviews_list = data_generator.generate_rent_reviews_list(pm_data, pm_name)

    with col_download:
        create_download_button(reviews_list, f"rent_reviews_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Reviews: {len(reviews_list)}**")

    st.dataframe(
        reviews_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )

@st.dialog("Lease Expiries", width="large")
def show_pm_lease_expiries_list(pm_data: pd.Series, pm_name: str):
    """Show list of leases expiring soon for a portfolio manager"""
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.markdown(f"### Lease Expiries - {pm_name}")

    # Generate lease expiries list
    expiries_list = data_generator.generate_lease_expiries_list(pm_data, pm_name)

    with col_download:
        create_download_button(expiries_list, f"lease_expiries_{pm_name.replace(' ', '_')}.csv")

    st.markdown(f"**Total Expiring Leases: {len(expiries_list)}**")

    st.dataframe(
        expiries_list,
        use_container_width=True,
        hide_index=True,
        height=500
    )
