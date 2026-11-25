@echo off
echo ============================================================
echo  MediMind AI - Test Suite (18 tests)
echo ============================================================
set PATH=C:\Users\dines\AppData\Local\Programs\Python\Python311;C:\Users\dines\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
set PYTHONPATH=%~dp0;%~dp0backend
cd /d "%~dp0"
python -m pytest tests/ -v --tb=short
pause
