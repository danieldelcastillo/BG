@echo off
setlocal
cd /d "%~dp0"

echo ==========================================================
echo    BG FUTBOL - Informe de equilibrio por atributos
echo ==========================================================
echo.
set /p BG_MATCHES="Partidos por nivel [100]: "
if "%BG_MATCHES%"=="" set BG_MATCHES=100

set /p BG_BOT_DEF="DEF del bot [15]: "
if "%BG_BOT_DEF%"=="" set BG_BOT_DEF=15
set /p BG_BOT_MED="MED del bot [15]: "
if "%BG_BOT_MED%"=="" set BG_BOT_MED=15
set /p BG_BOT_AT="AT del bot [15]: "
if "%BG_BOT_AT%"=="" set BG_BOT_AT=15

set /p BG_LEVELS="Niveles del jugador separados por espacio [12 13 14 15 16 17 18]: "
if "%BG_LEVELS%"=="" set BG_LEVELS=12 13 14 15 16 17 18

set "BG_ARGS=--matches %BG_MATCHES% --bot %BG_BOT_DEF% %BG_BOT_MED% %BG_BOT_AT% --player-levels %BG_LEVELS%"

rem Prioridad: el Python incluido con Codex; después, cualquier Python instalado.
set "BG_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BG_PYTHON%" (
    "%BG_PYTHON%" -m bg_futbol_simulator.balance_report %BG_ARGS%
    goto :end
)

where py >nul 2>&1
if not errorlevel 1 (
    py -3 -m bg_futbol_simulator.balance_report %BG_ARGS%
    goto :end
)

where python >nul 2>&1
if not errorlevel 1 (
    python -m bg_futbol_simulator.balance_report %BG_ARGS%
    goto :end
)

echo.
echo No se ha encontrado Python 3. Instala Python 3 y vuelve a abrir este archivo.

:end
echo.
pause
