# Ray White Property Management Dashboard

An elegant, interactive executive dashboard for property management analytics built with Streamlit.

## Features

### 📊 Overview
- **Key Performance Indicators**: Total landlords, properties, leases, vacancies with month-over-month comparisons
- **Interactive Drill-downs**: Click to expand any KPI for detailed breakdowns by portfolio manager
- **Performance Analytics**: Visual charts showing trends and comparisons
- **Occupancy Metrics**: Real-time occupancy rates and vacancy tracking

### 💰 Management Fees
- **Revenue Tracking**: Total revenue, management fees, leasing fees with period comparisons
- **Revenue Breakdown**: Visual breakdown by account codes (Management, Leasing, Other fees)
- **Revenue Trends**: Historical revenue tracking over time
- **Top Landlords**: Top 10 landlords by revenue with property counts

### ⚠️ Arrears
- **Arrears Analysis**: Total arrears with arrears-to-rent-roll ratio
- **Aging Buckets**: Breakdown by days overdue (0-30, 31-60, 61-90, 90+ days)
- **Visual Analytics**: Color-coded charts showing arrears distribution
- **Detailed Drill-down**: Tenant-level details with property addresses and amounts

### 📅 Critical Dates
- **Rent Reviews**: Upcoming rent reviews over the next 12 months
- **Lease Expiries**: Upcoming lease expiries with monthly breakdown
- **Monthly Planning**: Visual timeline of critical events
- **Detailed Breakdown**: Monthly counts for planning and resource allocation

### ✅ Task Management
- **Diary Items**: Track overdue and completed diary items
- **Portfolio Manager Performance**: Compare completion rates across PMs
- **Task Trends**: Historical tracking of task completion
- **Item Details**: Full list of diary items with property addresses and due dates

## Filtering Capabilities

- **Agency Filter**: View data for specific agencies or whole portfolio
- **Portfolio Manager Filter**: Focus on individual PM performance or view agency-wide
- **Date Range**: Select custom date ranges for historical analysis
- **Interactive Drill-downs**: Click to expand any metric for detailed breakdowns

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rw_dashboard_3
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure

```
rw_dashboard_3/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── utils/
    ├── __init__.py
    ├── styling.py         # CSS and UI components
    ├── metrics.py         # Calculation utilities
    ├── data_generator.py  # Mock data generation
    └── charts.py          # Chart creation functions
```

## Configuration

Edit `config.py` to customize:

- **App Title and Icon**: Branding and appearance
- **Database Settings**: Connection strings for real data integration
- **Portfolio Managers**: List of PMs to track
- **Agencies**: Agency names
- **Revenue Codes**: Account code categories
- **Arrears Buckets**: Aging period definitions
- **Colors**: Theme colors and chart color schemes

## Data Integration

Currently using mock data for demonstration. To connect to real data:

1. Set `USE_MOCK_DATA = False` in `config.py`
2. Update database connection settings in `config.py`
3. Implement database queries in `utils/data_generator.py`

## Features Highlights

### Interactive Design
- **Single Page Application**: All features accessible without navigation
- **Tab-based Organization**: Clean separation of different analytics sections
- **Responsive Layout**: Optimized for desktop viewing
- **Professional Styling**: Modern design with Inter font and custom CSS

### Data Visualization
- **Plotly Charts**: Interactive, high-quality visualizations
- **Color Coding**: Intuitive color schemes (green for positive, red for negative)
- **Multiple Chart Types**: Bar, line, donut, horizontal bar, heatmap, and more
- **Hover Details**: Rich tooltips with formatted data

### Executive Experience
- **KPI Cards**: Large, prominent metrics with delta indicators
- **Comparison Views**: Current vs previous period analytics
- **Drill-down Capability**: Expandable sections for detailed analysis
- **Export Ready**: Data formatted for easy export and reporting

## Technical Stack

- **Streamlit**: Web application framework
- **Plotly**: Interactive charting library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

## Requirements

- Python 3.8+
- Streamlit 1.28+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Performance

- **Caching**: Efficient data caching for fast load times
- **Responsive**: Optimized rendering for smooth interactions
- **Scalable**: Handles large datasets efficiently

## Support

For issues or questions, please contact the development team or create an issue in the repository.

## License

© 2025 Ray White Commercial. All rights reserved.
