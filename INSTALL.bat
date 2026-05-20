@echo off
title INTERBANK — System Install
echo.
echo   Adding interbank-connect to system PATH...
echo.

:: Get the folder where this bat file lives
set "INSTALL_DIR=%~dp0"

:: Add to user PATH permanently
setx PATH "%PATH%;%INSTALL_DIR%" >nul 2>&1

echo   [OK] Done! Close this CMD, open a NEW CMD, then type:
echo.
echo       interbank-connect
echo.
pause
