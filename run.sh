#!/bin/bash

# Run the Ray White Property Management Dashboard

echo "Starting Ray White Property Management Dashboard..."
echo "=================================================="
echo ""
echo "The dashboard will open in your default browser at http://localhost:8501"
echo ""
echo "To stop the dashboard, press Ctrl+C"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run Streamlit
streamlit run app.py
