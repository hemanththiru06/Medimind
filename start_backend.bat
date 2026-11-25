@echo off
echo ============================================================
echo  MediMind AI - Backend Server
echo  FastAPI + SQLAlchemy + SQLite
echo  API Docs: http://localhost:8000/docs
echo ============================================================
set PATH=C:\Users\dines\AppData\Local\Programs\Python\Python311;C:\Users\dines\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
set PYTHONPATH=%~dp0;%~dp0backend
cd /d "%~dp0backend"
echo Starting backend on http://localhost:8000 ...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
