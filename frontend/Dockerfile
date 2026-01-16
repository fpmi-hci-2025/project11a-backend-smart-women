# Dockerfile для фронтенда (опционально, для локального запуска)
FROM node:20-alpine

WORKDIR /app

# Копирование package файлов
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование исходного кода
COPY . .

# Открытие порта
EXPOSE 8080

# Команда запуска
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "8080"]

