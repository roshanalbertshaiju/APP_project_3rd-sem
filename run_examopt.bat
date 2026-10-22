@echo off
title ExamOpt Launcher
cd /d "%~dp0"

echo ===================================================
echo Starting ExamOpt Examination Scheduling System...
echo ===================================================

py main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running ExamOpt.
    pause
)
