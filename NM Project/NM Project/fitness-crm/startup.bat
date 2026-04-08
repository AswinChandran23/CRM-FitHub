@echo off
REM FitHub CRM - Startup Script for Windows
REM This script sets up the environment and starts the FitHub CRM application

echo.
echo ================================================
echo   FitHub CRM - Fitness Center Management
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo [2/4] Installing dependencies...
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo [3/4] Checking database...
if not exist "fitness_crm.db" (
    echo Database not found. It will be created on startup.
)

echo [4/4] Starting FitHub CRM Server...
echo.
echo ================================================
echo   Server starting...
echo   Open: http://localhost:5000
echo ================================================
echo.

python run.py

pause
