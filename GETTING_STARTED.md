# Getting Started with Ray White Property Management Dashboard

## Quick Start

### Option 1: Using the run script (Recommended)
```bash
cd /Users/primusanto/Documents/Code/de/rw_dashboard_3
./run.sh
```

This script will:
- Create a virtual environment if it doesn't exist
- Install all dependencies
- Start the Streamlit dashboard

### Option 2: Manual setup
```bash
cd /Users/primusanto/Documents/Code/de/rw_dashboard_3

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Dashboard Features

The dashboard opens with 5 main tabs:

### 1. 📊 Overview
Your executive summary with all key metrics:
- Total Landlords, Properties, Leases, Vacancies
- Occupancy rates and rent roll
- Arrears tracking
- Interactive drill-downs for each KPI
- Trend charts and performance analytics

### 2. 💰 Management Fees
Revenue tracking and analysis:
- Total revenue breakdown
- Management, leasing, and other fees
- Revenue trends over time
- Revenue by account code (donut chart)
- Top 10 landlords by revenue

### 3. ⚠️ Arrears
Comprehensive arrears management:
- Total arrears with ratio to rent roll
- Aging analysis (0-30, 31-60, 61-90, 90+ days)
- Color-coded visualizations
- Tenant-level drill-down with property details
- Arrears trends over time

### 4. 📅 Critical Dates
Plan ahead with upcoming events:
- Rent reviews over next 12 months
- Lease expiries over next 12 months
- Monthly breakdown charts
- Detailed tables for planning

### 5. ✅ Task Management
Track diary items and tasks:
- Overdue vs completed items
- Completion rates by portfolio manager
- Task trends over time
- Detailed item lists with due dates
- Filter by status (overdue/completed)

## Using Filters

The sidebar provides powerful filtering options:

### Agency Filter
- Select "Whole Agency" to see all data
- Choose a specific agency to focus on that portfolio

### Portfolio Manager Filter
- Select "All Managers" for agency-wide view
- Choose a specific PM to see their performance

### Date Range
- Use the date picker to select custom date ranges
- Analyze historical trends
- Compare different time periods

## Interactive Features

### KPI Drill-downs
Click "📊 View Breakdown" under any KPI card to see:
- Breakdown by portfolio manager
- Detailed data tables
- Quick visualizations

### Charts
All charts are interactive:
- Hover for detailed tooltips
- Click legend items to show/hide data
- Pan and zoom on time-series charts
- Download as PNG images

### Data Export
Data tables can be exported:
- Copy individual cells
- Download full datasets
- Use for further analysis in Excel

## Tips for Best Experience

1. **Start with Overview**: Get familiar with your key metrics
2. **Use Filters**: Focus on specific agencies or PMs
3. **Explore Drill-downs**: Click expanders under KPI cards
4. **Compare Periods**: Note the month-over-month changes
5. **Monitor Trends**: Use the trend charts to spot patterns
6. **Plan Ahead**: Use Critical Dates tab for resource planning
7. **Track Performance**: Use Task Management to monitor completion rates

## Data Refresh

The dashboard currently uses mock data for demonstration. The "🔄 Refresh Data" button in the sidebar will regenerate the mock data.

To connect to real data:
1. Edit `config.py` and set `USE_MOCK_DATA = False`
2. Configure your database connection settings in `config.py`
3. Implement the database queries in `utils/data_generator.py`

## Performance

- Data is cached for fast performance
- Charts render smoothly
- Responsive to filter changes
- Optimized for desktop viewing

## Troubleshooting

### Dashboard won't start
```bash
# Make sure you're in the right directory
cd /Users/primusanto/Documents/Code/de/rw_dashboard_3

# Check Python version (needs 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use
If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Charts not displaying
- Check internet connection (required for Google Fonts)
- Try a different browser
- Clear browser cache

## Browser Compatibility

Tested and optimized for:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Next Steps

1. **Explore all tabs**: Familiarize yourself with each section
2. **Try filters**: See how data changes with different selections
3. **Test drill-downs**: Click on expanders under KPI cards
4. **Review trends**: Look at historical data patterns
5. **Plan integration**: Consider how to connect to real data

## Support

For questions or issues:
- Check the README.md for detailed documentation
- Review the code comments in each file
- Contact the development team

## Keyboard Shortcuts

- **Ctrl+R** / **Cmd+R**: Refresh the dashboard
- **Ctrl+C** in terminal: Stop the dashboard

---

**Welcome to your new Property Management Dashboard!** 🎉
