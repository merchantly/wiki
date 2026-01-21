# Скрипт для сбора данных с форума Kiiiosk

Этот скрипт автоматически собирает статистику со всех статей форума Kiiiosk.

## Установка

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установка зависимостей
pip install playwright beautifulsoup4

# Установка браузера Chromium
playwright install chromium
```

## Запуск

```bash
source venv/bin/activate
python scrape_forum.py
```

## Что делает скрипт

1. Собирает все статьи с 3 страниц форума:
   - https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles
   - https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles?page=2
   - https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles?page=3

2. Для каждой статьи получает:
   - Название
   - URL
   - Количество просмотров
   - Количество "Полезно"

3. Создает таблицу в формате Markdown, отсортированную по просмотрам (по убыванию)

4. Добавляет рейтинг популярности:
   - **Высокая**: >500 просмотров
   - **Средняя**: 200-500 просмотров
   - **Низкая**: <200 просмотров

5. Сохраняет результат в файлы:
   - `LEGACY-INDEX.md` - Markdown таблица
   - `forum_data.json` - Сырые данные в JSON

## Время работы
Сбор данных занимает ~3-5 минуты (для 103 статей).

## Требования

- Python 3.12+
- Playwright
- Chromium browser