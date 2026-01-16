# Скрипт для исправления проблемы с входом
Write-Host "=== Исправление проблемы с входом ===" -ForegroundColor Yellow
Write-Host ""

# Остановить все процессы Python
Write-Host "1. Остановка старых процессов..." -ForegroundColor Cyan
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Удалить старую базу данных
Write-Host "2. Удаление старой базы данных..." -ForegroundColor Cyan
if (Test-Path app.db) {
    try {
        Remove-Item app.db -Force
        Write-Host "   [OK] База данных удалена" -ForegroundColor Green
    } catch {
        Write-Host "   [WARNING] Не удалось удалить БД (может быть заблокирована)" -ForegroundColor Yellow
        Write-Host "   Попробуйте удалить вручную: app.db" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [OK] База данных не найдена" -ForegroundColor Green
}

Write-Host ""
Write-Host "3. Запуск бэкенда..." -ForegroundColor Cyan
Write-Host "   Выполните вручную:" -ForegroundColor Yellow
Write-Host "   .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python -m uvicorn main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "=== Готово ===" -ForegroundColor Green
Write-Host ""
Write-Host "После запуска бэкенда:" -ForegroundColor Cyan
Write-Host "  - Откройте http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - Попробуйте войти: alice@example.com / password123" -ForegroundColor White


