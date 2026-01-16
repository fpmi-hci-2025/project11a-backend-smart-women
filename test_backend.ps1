# Скрипт для проверки работы Onlearn API
# Использование: .\test_backend.ps1

$baseUrl = "http://localhost:8000"

Write-Host ""
Write-Host "=== Проверка Onlearn API ===" -ForegroundColor Yellow
Write-Host ""

# Проверка 1: Главная страница
Write-Host "1. Проверка GET / ..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/" -UseBasicParsing -ErrorAction Stop
    if ($response.Content -eq '"Onlearn API"') {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ОШИБКА]" -ForegroundColor Red
    }
} catch {
    Write-Host " [СЕРВЕР НЕ ЗАПУЩЕН!]" -ForegroundColor Red
    Write-Host "   Запустите: python -m uvicorn main:app --reload" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Проверка 2: Список курсов
Write-Host "2. Проверка GET /courses ..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/courses" -UseBasicParsing -ErrorAction Stop
    $courses = $response.Content | ConvertFrom-Json
    if ($courses.Count -gt 0) {
        Write-Host " [OK - найдено $($courses.Count) курсов]" -ForegroundColor Green
    } else {
        Write-Host " [ПРЕДУПРЕЖДЕНИЕ - нет курсов]" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [ОШИБКА]" -ForegroundColor Red
}

# Проверка 3: Конкретный курс
Write-Host "3. Проверка GET /courses/1 ..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/courses/1" -UseBasicParsing -ErrorAction Stop
    $course = $response.Content | ConvertFrom-Json
    if ($course.id -eq 1) {
        Write-Host " [OK - курс: $($course.title)]" -ForegroundColor Green
    } else {
        Write-Host " [ОШИБКА]" -ForegroundColor Red
    }
} catch {
    Write-Host " [ОШИБКА]" -ForegroundColor Red
}

# Проверка 4: Курсы пользователя
Write-Host "4. Проверка GET /users/1/courses ..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/users/1/courses" -UseBasicParsing -ErrorAction Stop
    $enrollments = $response.Content | ConvertFrom-Json
    if ($enrollments.Count -ge 0) {
        Write-Host " [OK - найдено $($enrollments.Count) записей]" -ForegroundColor Green
    } else {
        Write-Host " [ПРЕДУПРЕЖДЕНИЕ - нет записей]" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [ОШИБКА]" -ForegroundColor Red
}

# Проверка 5: Swagger UI
Write-Host "5. Проверка GET /docs ..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/docs" -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [ОШИБКА]" -ForegroundColor Red
    }
} catch {
    Write-Host " [ОШИБКА]" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Проверка завершена ===" -ForegroundColor Green
Write-Host ""
Write-Host "Swagger UI: $baseUrl/docs" -ForegroundColor Cyan
Write-Host "ReDoc: $baseUrl/redoc" -ForegroundColor Cyan
Write-Host ""
