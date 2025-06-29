@echo off
cd /d %~dp0

start cmd /k "python server.py"
timeout /t 2 >nul
start cmd /k "python -m http.server"
start http://localhost:8000/index.html
