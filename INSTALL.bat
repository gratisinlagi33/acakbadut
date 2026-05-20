@echo off
title INTERBANK — System Install
echo.
echo   ╔══════════════════════════════════════════════════════════╗
echo   ║       INSTALLING INTERBANK TERMINAL TO SYSTEM           ║
echo   ╚══════════════════════════════════════════════════════════╝
echo.
echo   This will add this folder to your system PATH so you can
echo   run "interbank-connect" from ANY directory in CMD.
echo.
pause

setx PATH "%PATH%;%~dp0" >nul 2>&1

echo.
echo   [OK] Installation complete!
echo.
echo   Now you can open CMD from ANYWHERE and type:
echo.
echo       interbank-connect
echo.
echo   to launch the terminal.
echo.
pause
