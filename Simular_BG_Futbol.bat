@echo off
setlocal
cd /d "%~dp0"

rem Prioridad: el Python incluido con Codex; después, cualquier Python instalado.
set "BG_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BG_PYTHON%" (
    "%BG_PYTHON%" -m bg_futbol_simulator.interactive
    goto :end
)

where py >nul 2>&1
if not errorlevel 1 (
    py -3 -m bg_futbol_simulator.interactive
    goto :end
)

where python >nul 2>&1
if not errorlevel 1 (
    python -m bg_futbol_simulator.interactive
    goto :end
)

echo.
echo No se ha encontrado Python 3. Instala Python 3 y vuelve a abrir este archivo.

:end
echo.
pause
