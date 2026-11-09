@echo off
title AI Hand Gesture Recognition - Installer

echo ==========================================
echo   AI HAND GESTURE RECOGNITION INSTALLER
echo ==========================================
echo.

echo Checking Python...
python --version

if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH.
    echo Install Python 3.13 and try again.
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo.

python -m pip install --upgrade pip

python -m pip install --upgrade opencv-python mediapipe requests

if errorlevel 1 (
    echo.
    echo ==========================================
    echo INSTALLATION FAILED
    echo ==========================================
    pause
    exit /b 1
)

echo.
echo ==========================================
echo INSTALLATION COMPLETE!
echo ==========================================
echo.
echo You can now run:
echo Hand gesture recognition.py
echo.

pause