# 🚀 Запуск на localhost

## Быстрый запуск

Я создал скрипты для запуска:

### Вариант 1: Использовать скрипты

1. **Backend:**
   - Двойной клик на `start_backend.ps1`
   - Или в PowerShell: `.\start_backend.ps1`

2. **Frontend:**
   - Двойной клик на `start_frontend.ps1`
   - Или в PowerShell: `.\start_frontend.ps1`

### Вариант 2: Вручную

**Backend:**
```powershell
cd C:\Users\User\Documents\PCHMI\backend
.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend (в другом окне):**
```powershell
cd C:\Users\User\Documents\PCHMI\frontend
npm run dev
```

## Доступ

После запуска:
- **Backend:** http://localhost:8000
- **Backend API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:8080

## Тестовые данные

- Email: `alice@example.com`
- Password: `password123`

## Остановка

Нажмите `Ctrl+C` в каждом окне PowerShell для остановки сервисов.

