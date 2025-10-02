"""
Configuration file for Ray White Property Management Dashboard
"""
import os
from typing import List

# App Configuration
APP_TITLE = "Executive Management Dashboard"
APP_ICON = "■"  # Simple monochrome square
APP_SUBTITLE = "KPI Dashboard & Analytics"

# Database Configuration (for future real data integration)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "property_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Use mock data for development
USE_MOCK_DATA = True

# Cache configuration (TTL in seconds)
CACHE_TTL = 3600  # 1 hour

# Comparison periods
COMPARISON_PERIODS = {
    "last_month": 1,
    "last_year": 12,
}

# Agencies
AGENCIES = [
    "Commercial CBD",
    "Commercial North",
    "Commercial South",
    "Commercial West",
]

# Portfolio Managers
PORTFOLIO_MANAGERS = [
    "Jamie Mills",
    "Allison Dumbrell",
    "Holly Davidson",
    "Joanne Patamisi",
    "Nash Eli",
    "Sarah Chen",
    "Michael Roberts",
    "Emma Wilson",
]

# Revenue account codes
REVENUE_CODES = [
    "Management Fees",
    "Leasing Fees",
    "Letting Fees",
    "Property Administration",
    "Marketing Fees",
    "Inspection Fees",
    "Other Fees",
]

# Arrears buckets (days overdue)
ARREARS_BUCKETS = {
    "0-30": "0-30 days",
    "31-60": "31-60 days",
    "61-90": "61-90 days",
    "90+": "90+ days",
}

# Diary item types
DIARY_ITEM_TYPES = [
    "All Types",
    "Inspection Due",
    "Call Owner",
    "Rent Review Due",
    "Lease Expiry",
    "Fire Safety Check",
    "End of Lease Charge Advised",
    "Property Maintenance",
    "Tenant Follow-up",
]

# Property types
PROPERTY_TYPES = [
    "Office",
    "Retail",
    "Industrial",
    "Warehouse",
    "Mixed Use",
    "Medical",
]

# Export settings
EXPORT_PDF_ORIENTATION = "landscape"
EXPORT_EXCEL_SHEET_NAME = "Dashboard Export"

# Styling - Brand-inspired color palette
PRIMARY_COLOR = "#ffe512"  # Broom Yellow (brand accent)
DARK_COLOR = "#595959"  # Scorpion Gray (text and dark elements)
LIGHT_COLOR = "#FAF9F2"  # Ecru White (backgrounds)
SECONDARY_COLOR = "#d4b000"  # Darker yellow for variety
ACCENT_COLOR = "#ffe512"  # Yellow accent
SUCCESS_COLOR = "#2d5f3f"  # Deep green
WARNING_COLOR = "#e8a317"  # Amber
DANGER_COLOR = "#8b3a3a"  # Deep red
NEUTRAL_COLOR = "#7a7a7a"  # Medium gray

CHART_COLORS = ["#ffe512", "#d4b000", "#b89f00", "#9e8700", "#856f00", "#6b5800"]

# Date format
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%d %b %Y"
