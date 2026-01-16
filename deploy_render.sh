#!/bin/bash
# Скрипт для деплоя на Render.com
# Использование: ./deploy_render.sh

echo "=== Деплой на Render.com ==="
echo ""
echo "Этот скрипт поможет вам задеплоить приложение на Render.com"
echo ""
echo "Шаги:"
echo "1. Убедитесь, что код закоммичен в Git"
echo "2. Зайдите на https://render.com"
echo "3. Создайте новый Web Service"
echo "4. Используйте следующие настройки:"
echo ""
echo "   Name: onlearn-backend"
echo "   Root Directory: backend"
echo "   Environment: Python 3"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "5. Добавьте переменные окружения:"
echo "   PYTHON_VERSION = 3.11.0"
echo "   FRONTEND_URL = https://your-frontend.vercel.app"
echo ""
echo "Готово! Render автоматически задеплоит приложение."

