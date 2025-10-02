"""
Chart creation utilities using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional
import config

def create_comparison_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_current: str,
    y_previous: str,
    title: str,
    current_label: str = "Current",
    previous_label: str = "Previous"
) -> go.Figure:
    """Create a grouped bar chart comparing current vs previous period"""

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name=previous_label,
        x=df[x_col],
        y=df[y_previous],
        marker_color='#d4d4d0',
        hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name=current_label,
        x=df[x_col],
        y=df[y_current],
        marker_color=config.PRIMARY_COLOR,
        hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>'
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        hovermode='x unified',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig

def create_trend_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    group_col: Optional[str] = None,
    show_area: bool = False
) -> go.Figure:
    """Create a line chart showing trends over time"""

    if group_col:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=group_col,
            title=title,
            markers=True
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )
    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            fill='tozeroy' if show_area else None,
            line=dict(color=config.PRIMARY_COLOR, width=3),
            marker=dict(size=8, color=config.PRIMARY_COLOR),
            hovertemplate='%{x}<br>%{y:,}<extra></extra>'
        ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        hovermode='x unified',
        height=400,
        legend=dict(
            title="",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig

def create_horizontal_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color_col: Optional[str] = None
) -> go.Figure:
    """Create a horizontal bar chart (useful for rankings)"""

    # Sort by value
    df_sorted = df.sort_values(x_col, ascending=True)

    if color_col:
        fig = px.bar(
            df_sorted,
            x=x_col,
            y=y_col,
            orientation='h',
            color=color_col,
            title=title,
            color_continuous_scale='RdYlGn'
        )
    else:
        fig = go.Figure(go.Bar(
            x=df_sorted[x_col],
            y=df_sorted[y_col],
            orientation='h',
            marker_color=config.PRIMARY_COLOR,
            text=df_sorted[x_col],
            textposition='outside',
            texttemplate='%{text:,}',
            hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>'
        ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        height=max(400, len(df) * 40),
        showlegend=False if not color_col else True,
        margin=dict(l=150, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=False)

    return fig

def create_donut_chart(
    df: pd.DataFrame,
    values_col: str,
    names_col: str,
    title: str
) -> go.Figure:
    """Create a donut chart"""

    fig = go.Figure(data=[go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=0.4,
        marker=dict(
            colors=config.CHART_COLORS,
            line=dict(color='white', width=2)
        ),
        textposition='outside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=40, r=120, t=60, b=40)
    )

    return fig

def create_stacked_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str,
    title: str
) -> go.Figure:
    """Create a stacked bar chart"""

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        title=title,
        barmode='stack',
        color_discrete_sequence=config.CHART_COLORS
    )

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        hovermode='x unified',
        height=400,
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig

def create_heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    title: str
) -> go.Figure:
    """Create a heatmap"""

    pivot_data = df.pivot_table(
        values=value_col,
        index=y_col,
        columns=x_col,
        aggfunc='mean'
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn',
        text=np.round(pivot_data.values, 1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        hovertemplate='%{y}<br>%{x}<br>Value: %{z:.1f}%<extra></extra>',
        colorbar=dict(title="Value")
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        height=400,
        xaxis={'side': 'bottom'},
        margin=dict(l=150, r=40, t=60, b=80)
    )

    return fig

def create_waterfall_chart(
    categories: List[str],
    values: List[float],
    title: str
) -> go.Figure:
    """Create a waterfall chart"""

    # Determine measure type for each value
    measures = []
    for i, val in enumerate(values):
        if i == 0:
            measures.append("absolute")
        elif i == len(values) - 1:
            measures.append("total")
        else:
            measures.append("relative")

    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=measures,
        x=categories,
        textposition="outside",
        text=[f"${x:,.0f}" for x in values],
        y=values,
        connector={"line": {"color": config.NEUTRAL_COLOR}},
        increasing={"marker": {"color": config.SUCCESS_COLOR}},
        decreasing={"marker": {"color": config.DANGER_COLOR}},
        totals={"marker": {"color": config.PRIMARY_COLOR}}
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        height=450,
        margin=dict(l=40, r=40, t=60, b=80)
    )

    return fig

def create_arrears_bucket_chart(
    df: pd.DataFrame,
    title: str = "Arrears by Days Overdue"
) -> go.Figure:
    """Create a specialized chart for arrears buckets with color coding"""

    colors = [config.SUCCESS_COLOR, config.WARNING_COLOR, "#d47300", config.DANGER_COLOR]

    fig = go.Figure(go.Bar(
        x=df.iloc[:, 0],  # Bucket names
        y=df.iloc[:, 1],  # Amounts
        marker_color=colors[:len(df)],
        text=df.iloc[:, 1],
        texttemplate='$%{text:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        showlegend=False,
        height=400,
        xaxis_title="Days Overdue",
        yaxis_title="Amount ($)",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig

def create_multi_metric_chart(
    df: pd.DataFrame,
    x_col: str,
    metrics: List[str],
    title: str
) -> go.Figure:
    """Create a chart with multiple metrics"""

    fig = go.Figure()

    for i, metric in enumerate(metrics):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[metric],
            mode='lines+markers',
            name=metric,
            line=dict(width=3, color=config.CHART_COLORS[i % len(config.CHART_COLORS)]),
            marker=dict(size=8),
            hovertemplate=f'<b>{metric}</b><br>%{{x}}<br>%{{y:,}}<extra></extra>'
        ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        hovermode='x unified',
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig

def create_scatter_matrix(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: str,
    color_col: str,
    hover_name_col: str,
    title: str
) -> go.Figure:
    """Create a scatter plot with size and color dimensions"""

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        hover_name=hover_name_col,
        title=title,
        color_continuous_scale='RdYlGn',
        labels={x_col: x_col, y_col: y_col, color_col: color_col}
    )

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'weight': 700}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Lato, sans-serif", size=12, color="#595959"),
        title_font=dict(family="Playfair Display, serif"),
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')

    return fig
