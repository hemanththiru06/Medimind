@echo off
echo ============================================================
echo  MediMind AI - Frontend Dev Server
echo  React + Vite + TypeScript + Tailwind
echo  App URL: http://localhost:5173
echo ============================================================
set PATH=C:\Users\dines\AppData\Local\Programs\node-portable;%PATH%
cd /d "%~dp0frontend"
echo Starting frontend on http://localhost:5173 ...
node_modules\.bin\vite.cmd
pause
