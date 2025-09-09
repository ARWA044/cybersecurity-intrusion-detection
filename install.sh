#!/bin/bash

echo "Installing Cybersecurity Intrusion Detection System..."
echo

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Installation complete!"
echo
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the dashboard: streamlit run streamlit_dashboard.py"
echo "3. Open your browser to: http://localhost:8501"
echo
