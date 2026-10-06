@echo off
setlocal
title MovieMate Recommendation System

echo ==========================================
echo        MovieMate Recommendation System
echo ==========================================
echo.

set "PY_CMD=py"
py -3.14 --version >nul 2>&1
if not errorlevel 1 set "PY_CMD=py -3.14"

%PY_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found.
    echo Install Python, then run this file again.
    pause
    exit /b 1
)

echo Python detected.
echo.
echo Installing/checking required packages...
%PY_CMD% -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo Starting MovieMate...
echo.
echo Open this address in your browser:
echo http://127.0.0.1:5000
echo.
%PY_CMD% app.py

pause
