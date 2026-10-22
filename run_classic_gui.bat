@echo off
title ExamOpt — Classic GUI
cd /d "%~dp0"

echo ===================================================
echo Starting ExamOpt (Classic University Portal)...
echo Theme: Classic Blue ^& Clam
echo ===================================================

py main.py --theme classic
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running ExamOpt Classic GUI.
    pause
)
