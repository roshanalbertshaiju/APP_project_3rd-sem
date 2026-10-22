@echo off
title ExamOpt — Modern Studio GUI
cd /d "%~dp0"

echo ===================================================
echo Starting ExamOpt (Modern Minimalist Studio)...
echo Theme: Obsidian Slate ^& Electric Indigo
echo ===================================================

py main.py --theme modern
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running ExamOpt Modern GUI.
    pause
)
