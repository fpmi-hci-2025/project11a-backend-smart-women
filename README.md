# Onlearn API

Educational web platform backend API built with FastAPI.

## Features

- Course catalog management
- User enrollment system
- Progress tracking
- Role-based access (Student, Teacher, Admin)

## Setup

### Windows PowerShell

1. Create virtual environment:
```powershell
python -m venv .venv
```

2. Activate virtual environment:
```powershell
.venv\Scripts\Activate.ps1
```

3. Upgrade pip:
```powershell
python -m pip install --upgrade pip
```

4. Install dependencies:
```powershell
pip install -r requirements.txt
```

5. Run the server:
```powershell
python -m uvicorn main:app --reload
```

Or alternatively:
```powershell
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Проверка работы бэкенда

### Способ 1: Браузер (самый простой)

1. Откройте в браузере: **http://localhost:8000/**
   - Должно отобразиться: `"Onlearn API"`

2. Откройте Swagger UI: **http://localhost:8000/docs**
   - Должен открыться интерактивный интерфейс с документацией API
   - Здесь можно тестировать все эндпоинты прямо в браузере

### Способ 2: PowerShell команды

**Проверка главной страницы:**
```powershell
curl http://localhost:8000/
```

**Проверка списка курсов:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/courses" -UseBasicParsing | Select-Object StatusCode, Content
```

**Проверка конкретного курса:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/courses/1" -UseBasicParsing | Select-Object StatusCode, Content
```

**Проверка курсов пользователя:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/users/1/courses" -UseBasicParsing | Select-Object StatusCode, Content
```

### Способ 3: Автоматический скрипт проверки

Запустите готовый скрипт для проверки всех эндпоинтов:
```powershell
.\test_backend.ps1
```

Скрипт проверит:
- Главную страницу (`GET /`)
- Список курсов (`GET /courses`)
- Детали курса (`GET /courses/1`)
- Курсы пользователя (`GET /users/1/courses`)
- Swagger UI (`GET /docs`)

### Способ 4: Проверка через Swagger UI

1. Откройте http://localhost:8000/docs
2. Разверните любой эндпоинт (например, `GET /courses`)
3. Нажмите "Try it out"
4. Нажмите "Execute"
5. Проверьте ответ (Status 200 и данные)

### Что проверить:

✅ **Сервер запущен:**
- `GET /` → возвращает `"Onlearn API"`

✅ **База данных работает:**
- `GET /courses` → возвращает список из 4 курсов

✅ **Swagger UI доступен:**
- `GET /docs` → открывается интерактивная документация

## API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /` - API welcome message
- `GET /courses` - List all courses (optional query: `?published_only=true/false`)
- `GET /courses/{id}` - Get course details
- `POST /enroll` - Create a new enrollment
- `GET /users/{id}/courses` - Get user's enrolled courses with progress
- `PATCH /enrollments/{id}/progress` - Update enrollment progress

## Data Models

- **User**: id, name, role (student|teacher|admin)
- **Course**: id, title, description, teacher_id, is_published
- **Enrollment**: id, user_id, course_id, progress_percent (0-100)

## Notes

- This is a prototype using SQLite database (app.db)
- Data is seeded on server startup if database is empty
- Database file persists between server restarts
- CORS is enabled for frontend integration (localhost:8080)

## Frontend Integration

The backend is integrated with the React frontend located in `../frontend/`.

- Frontend runs on: http://localhost:8080
- Backend runs on: http://localhost:8000
- CORS is configured to allow requests from the frontend

See `../INTEGRATION.md` for detailed integration instructions.








