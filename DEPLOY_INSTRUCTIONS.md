# 📦 Инструкция по деплою

## 🐳 1. Локальный запуск с Docker

### Запуск всего приложения:
```bash
docker-compose up --build
```

### Запуск только бэкенда:
```bash
cd backend
docker build -t onlearn-backend .
docker run -p 8000:8000 onlearn-backend
```

**Доступ:**
- Frontend: http://localhost:8080
- Backend: http://localhost:8000

---

## ☁️ 2. Деплой на Render.com (Backend)

### Шаги:

1. **Зайдите на https://render.com** → Войдите через GitHub

2. **Создайте Web Service:**
   - New + → Web Service
   - Подключите репозиторий
   - Настройки:
     ```
     Name: onlearn-backend
     Root Directory: backend
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Добавьте переменные окружения:**
   - `PYTHON_VERSION` = `3.11.0`
   - `FRONTEND_URL` = `https://your-frontend.vercel.app` (после деплоя фронтенда)

4. **Нажмите "Create Web Service"**

5. **Дождитесь деплоя** (5-10 минут)

6. **Получите URL:** `https://onlearn-backend.onrender.com`

---

## 🚀 3. Деплой на Vercel.com (Frontend)

### Шаги:

1. **Зайдите на https://vercel.com** → Войдите через GitHub

2. **Импортируйте проект:**
   - Add New → Project
   - Выберите репозиторий

3. **Настройки:**
   ```
   Framework: Vite
   Root Directory: frontend
   Build Command: npm run build (автоматически)
   Output Directory: dist (автоматически)
   ```

4. **Добавьте переменную окружения:**
   - `VITE_API_URL` = `https://your-backend.onrender.com`

5. **Нажмите "Deploy"**

6. **Получите URL:** `https://your-frontend.vercel.app`

---

## ✅ 4. Финальная настройка

После деплоя обоих сервисов:

1. **Обновите CORS на Render:**
   - Settings → Environment
   - Добавьте: `FRONTEND_URL` = URL вашего фронтенда
   - Перезапустите сервис

2. **Проверьте работу:**
   - Откройте фронтенд
   - Попробуйте войти
   - Проверьте все функции

---

## 📝 Файлы для деплоя

- `Dockerfile` - образ бэкенда
- `docker-compose.yml` - локальный запуск
- `render.yaml` - конфигурация Render
- `frontend/vercel.json` - конфигурация Vercel
- `README_DEPLOY.md` - подробная документация

