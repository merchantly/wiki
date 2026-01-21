#!/bin/bash
# Скрипт для запуска сбора данных с форума Kiiiosk

echo "Запуск сбора данных с форума Kiiiosk..."

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    echo "Активация виртуального окружения..."
    source venv/bin/activate
else
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Установка зависимостей..."
    pip install playwright beautifulsoup4
    echo "Установка браузера..."
    playwright install chromium
fi

# Запуск скрипта
echo "Запуск scraper..."
python scrape_forum.py

echo "Сбор данных завершен!"
echo "Результат сохранен в LEGACY-INDEX.md"