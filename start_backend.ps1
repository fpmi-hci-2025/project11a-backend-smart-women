# Скрипт для запуска бэкенда
cd C:\Users\User\Documents\PCHMI\backend
if (Test-Path .venv\Scripts\Activate.ps1) {
    .venv\Scripts\Activate.ps1
}
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

