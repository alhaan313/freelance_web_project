@echo off
setlocal

set "PORT=%~1"
if "%PORT%"=="" set "PORT=5000"

echo Checking for any process using port %PORT%...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":%PORT% .*LISTENING"') do (
    echo Stopping PID %%P on port %PORT%...
    taskkill /PID %%P /F >nul 2>&1
)

echo Starting Flask app on http://127.0.0.1:%PORT%/
start "" "http://127.0.0.1:%PORT%/"
cd /d "%~dp0"
set "PORT=%PORT%"
python app.py

endlocal
