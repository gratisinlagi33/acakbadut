@echo off
title INTERBANK TRANSFER TRANSACTION — Secure Terminal
color 0A
echo.
echo   ╔══════════════════════════════════════════════════════════╗
echo   ║     INTERBANK SETTLEMENT TERMINAL — CONNECTING...       ║
echo   ╚══════════════════════════════════════════════════════════╝
echo.
python "C:\Users\Asus\Desktop\acakbadut\interbank_terminal.py" %*
if errorlevel 1 (
    echo.
    echo   [ERROR] Python is not installed or not in PATH.
    pause
)
