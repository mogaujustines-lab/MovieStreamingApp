@echo off
title MovieMate Recommendation System

echo ==========================================
echo        MovieMate Recommendation System
echo ==========================================
echo.

REM Check that Python is installed
py --version >nul 2>&1

if errorlevel 1 (
    echo Python was not found.
    echo.
    echo Please install Python first from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python detected.
echo.

REM Install project dependencies
echo Checking required Python packages...
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install project dependencies.
    pause
    exit /b 1
)

echo.
echo Dependencies are ready.
echo.
echo Starting MovieMate...
echo.
echo Open your browser at:
echo http://127.0.0.1:5000
echo.

py app.py

pause