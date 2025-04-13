@echo off

set FRIENDLY_MESSAGE="WatsonX Inference Matcher - Ollama Serving"
set INSTALL_MESSAGE="Ollama is not installed. Please install Ollama from the following link:"
set STOP_MESSAGE="Stopping Ollama service..."
set START_MESSAGE="Starting Ollama server (ollama serve)..."
set DONT_CLOSE_MESSAGE="Don't close this window; the Ollama server is running."

echo %FRIENDLY_MESSAGE%

REM Check if Ollama is installed (by checking for the executable)
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo %INSTALL_MESSAGE%
    start "Ollama Installer" https://ollama.com/download/windows
    echo "After installing, please run this script again."
    pause
    exit /b 1
)

echo %FRIENDLY_MESSAGE%
echo %STOP_MESSAGE%

REM Attempt to stop any existing Ollama service. Windows doesn't use systemd, so we use taskkill if ollama is running.
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    taskkill /F /IM ollama.exe
    echo "Ollama service stopped."
) else (
    echo "Ollama service was not running."
)

echo %FRIENDLY_MESSAGE%
echo %START_MESSAGE%

start cmd /k "ollama serve"

echo %FRIENDLY_MESSAGE%
echo %DONT_CLOSE_MESSAGE%

REM Keep the original script running, so the cmd window stays open.
pause