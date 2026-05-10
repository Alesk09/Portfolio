@echo off
title Proxy Yahoo Finance - Portfolio Dashboard
color 0A

echo =====================================================
echo   Proxy Yahoo Finance - Portfolio Dashboard
echo =====================================================
echo.

:: Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Installez Python depuis https://www.python.org/downloads/
    echo Cochez bien "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

echo [1/2] Installation des dependances...
pip install flask requests --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer les dependances.
    echo Essayez manuellement : pip install flask requests
    pause
    exit /b 1
)

echo [2/2] Demarrage du proxy sur http://localhost:5000 ...
echo.
echo  Gardez cette fenetre ouverte pendant l'utilisation
echo  du dashboard. Fermez-la pour arreter le serveur.
echo.

python "%~dp0proxy.py"

echo.
echo Le serveur s'est arrete.
pause
