"""
Metrics calculation utilities
"""
from typing import Union, Dict, Any
import pandas as pd

def calculate_percent_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def calculate_mom_change(current: float, last_month: float) -> float:
    """Calculate month-over-month percentage change"""
    return calculate_percent_change(current, last_month)

def calculate_yoy_change(current: float, last_year: float) -> float:
    """Calculate year-over-year percentage change"""
    return calculate_percent_change(current, last_year)

def format_number(value: Union[int, float], decimals: int = 0) -> str:
    """Format number with thousand separators"""
    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"

def format_currency(value: Union[int, float], symbol: str = "$", decimals: int = 0) -> str:
    """Format value as currency"""
    if decimals == 0:
        return f"{symbol}{value:,.0f}"
    return f"{symbol}{value:,.{decimals}f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"

def calculate_vacancy_rate(vacancies: int, total_properties: int) -> float:
    """Calculate vacancy rate as percentage"""
    if total_properties == 0:
        return 0.0
    return (vacancies / total_properties) * 100

def calculate_occupancy_rate(occupied: int, total_properties: int) -> float:
    """Calculate occupancy rate as percentage"""
    if total_properties == 0:
        return 0.0
    return (occupied / total_properties) * 100

def calculate_arrears_percentage(arrears_amount: float, total_rent_roll: float) -> float:
    """Calculate arrears as percentage of rent roll"""
    if total_rent_roll == 0:
        return 0.0
    return (arrears_amount / total_rent_roll) * 100

def calculate_avg_fee_per_tenancy(total_fees: float, total_leases: int) -> float:
    """Calculate average fee per tenancy"""
    if total_leases == 0:
        return 0.0
    return total_fees / total_leases

def aggregate_by_pm(df: pd.DataFrame, pm_column: str, value_columns: list) -> pd.DataFrame:
    """Aggregate data by portfolio manager"""
    return df.groupby(pm_column)[value_columns].sum().reset_index()

def aggregate_by_agency(df: pd.DataFrame, agency_column: str, value_columns: list) -> pd.DataFrame:
    """Aggregate data by agency"""
    return df.groupby(agency_column)[value_columns].sum().reset_index()

def get_period_comparison(df: pd.DataFrame, date_column: str, current_date, last_month_date, last_year_date) -> Dict[str, Any]:
    """Get data for current period, last month, and last year"""
    current_data = df[df[date_column] == current_date]
    last_month_data = df[df[date_column] == last_month_date]
    last_year_data = df[df[date_column] == last_year_date]

    return {
        "current": current_data,
        "last_month": last_month_data,
        "last_year": last_year_data
    }

def calculate_growth_rate(values: list) -> float:
    """Calculate average growth rate from a list of values"""
    if len(values) < 2:
        return 0.0

    total_growth = 0.0
    count = 0

    for i in range(1, len(values)):
        if values[i-1] != 0:
            growth = ((values[i] - values[i-1]) / values[i-1]) * 100
            total_growth += growth
            count += 1

    return total_growth / count if count > 0 else 0.0

def rank_by_value(df: pd.DataFrame, value_column: str, ascending: bool = False) -> pd.DataFrame:
    """Rank dataframe by a value column"""
    df_sorted = df.sort_values(value_column, ascending=ascending).reset_index(drop=True)
    df_sorted['rank'] = range(1, len(df_sorted) + 1)
    return df_sorted

def calculate_kpi_summary(df: pd.DataFrame, kpi_configs: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Calculate multiple KPIs from dataframe

    Args:
        df: Input dataframe
        kpi_configs: Dictionary of KPI configurations
            Example: {
                'total_properties': {'column': 'properties', 'operation': 'sum'},
                'avg_occupancy': {'column': 'occupancy_rate', 'operation': 'mean'}
            }

    Returns:
        Dictionary of calculated KPIs
    """
    results = {}

    for kpi_name, config in kpi_configs.items():
        column = config.get('column')
        operation = config.get('operation', 'sum')

        if operation == 'sum':
            results[kpi_name] = df[column].sum()
        elif operation == 'mean':
            results[kpi_name] = df[column].mean()
        elif operation == 'count':
            results[kpi_name] = df[column].count()
        elif operation == 'nunique':
            results[kpi_name] = df[column].nunique()
        elif operation == 'min':
            results[kpi_name] = df[column].min()
        elif operation == 'max':
            results[kpi_name] = df[column].max()

    return results
