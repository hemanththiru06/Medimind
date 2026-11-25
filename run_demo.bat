@echo off
echo ============================================================
echo  MediMind AI - Viva Demo Script
echo  Runs all 7 acceptance scenarios automatically
echo ============================================================
set PATH=C:\Users\dines\AppData\Local\Programs\Python\Python311;C:\Users\dines\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
set PYTHONPATH=%~dp0;%~dp0backend
cd /d "%~dp0"
python run_demo.py
pause
