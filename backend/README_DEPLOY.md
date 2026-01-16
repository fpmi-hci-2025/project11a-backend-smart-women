# Деплой приложения

## Локальный запуск с Docker

### Требования
- Docker
- Docker Compose

### Запуск

```bash
# Сборка и запуск контейнера
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build

# Остановка
docker-compose down
```

Приложение будет доступно по адресу: http://localhost:8000

## Деплой на Render.com (Backend)

### Шаги:

1. Создайте аккаунт на https://render.com
2. Подключите ваш GitHub репозиторий
3. Создайте новый Web Service
4. Настройки:
   - **Name**: onlearn-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

5. Добавьте переменные окружения (если нужны)
6. Нажмите "Create Web Service"

Render автоматически определит порт из переменной `$PORT`.

### CORS настройка

После деплоя обновите CORS в `main.py`:
```python
allow_origins=[
    "http://localhost:8080",
    "https://your-frontend-domain.vercel.app"
]
```

## Деплой на Vercel.com (Frontend)

### Шаги:

1. Установите Vercel CLI:
```bash
npm i -g vercel
```

2. В директории frontend:
```bash
cd frontend
vercel
```

3. Или через веб-интерфейс:
   - Создайте аккаунт на https://vercel.com
   - Подключите GitHub репозиторий
   - Выберите директорию `frontend`
   - Vercel автоматически определит настройки

4. Добавьте переменную окружения:
   - `VITE_API_URL` = URL вашего бэкенда на Render.com

### Конфигурация Vercel

Создайте файл `vercel.json` в корне frontend:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

## Проверка деплоя

1. Backend: https://your-backend.onrender.com/
2. Frontend: https://your-frontend.vercel.app
3. Проверьте, что API работает: https://your-backend.onrender.com/test

