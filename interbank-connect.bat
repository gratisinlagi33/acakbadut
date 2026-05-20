@echo off
title INTERBANK TRANSFER TRANSACTION — Secure Terminal
color 0A
echo.
echo   ╔══════════════════════════════════════════════════════════╗
echo   ║     INTERBANK SETTLEMENT TERMINAL — CONNECTING...       ║
echo   ╚══════════════════════════════════════════════════════════╝
echo.
python "%~dp0interbank_terminal.py" %*
if errorlevel 1 (
    echo.
    echo   [ERROR] Python is not installed or not in PATH.
    echo   Please install Python 3.8+ from https://python.org
    pause
)
