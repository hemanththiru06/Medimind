@echo off
echo ============================================================
echo  MediMind AI - Virtual Box Simulator
echo  Simulates ESP32 device (600x time warp for demo)
echo ============================================================
set PATH=C:\Users\dines\AppData\Local\Programs\Python\Python311;C:\Users\dines\AppData\Local\Programs\Python\Python311\Scripts;%PATH%
set PYTHONPATH=%~dp0;%~dp0backend
cd /d "%~dp0"
echo Starting simulator against http://localhost:8000 ...
python simulator\box_sim.py --speed 600 --box-id BOX-001 --server http://localhost:8000
pause
