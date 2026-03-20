@echo off
REM E-Commerce Analytics Pro - Installation Script for Windows

echo.
echo 🚀 Installing E-Commerce Analytics Pro...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Installation complete!
echo.
echo 🎯 To run the dashboard:
echo    1. Activate the virtual environment: venv\Scripts\activate.bat
echo    2. Run the app: streamlit run app.py
echo.
echo 📖 For more information, see QUICKSTART.md
echo.
pause
