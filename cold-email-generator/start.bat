@echo off
cd /d "%~dp0"
title ReachFlow
echo.
echo  Starting ReachFlow...
echo.
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 ( echo. & echo  ERROR: Could not install packages. Is Python installed? & echo  Download Python at https://python.org & pause & exit /b 1 )
python app.py
pause
