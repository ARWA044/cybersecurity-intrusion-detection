@echo off
echo Installing Cybersecurity Intrusion Detection System...
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the dashboard: streamlit run streamlit_dashboard.py
echo 3. Open your browser to: http://localhost:8501
echo.
pause
