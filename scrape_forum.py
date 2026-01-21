#!/usr/bin/env python3
"""
Скрипт для сбора данных со всех статей форума kiiioskforum.userecho.ru
Использует Playwright для браузерной автоматизации
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Список URL страниц с статьями
PAGES = [
    "https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles",
    "https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles?page=2",
    "https://kiiioskforum.userecho.ru/knowledge-bases/4-obschie-voprosyi/articles?page=3"
]

async def get_article_links(page):
    """Получение списка всех ссылок на статьи со страницы"""
    all_articles = []
    
    for page_url in PAGES:
        print(f"Обработка страницы: {page_url}")
        try:
            await page.goto(page_url, wait_until="networkidle")
            
            # Ждем загрузки списка статей
            await page.wait_for_selector("a[href*='knowledge-bases/4/articles/']")
            
            # Получаем HTML и парсим с помощью BeautifulSoup
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Ищем все ссылки на статьи
            article_links = soup.find_all('a', href=re.compile(r'/knowledge-bases/4/articles/\d+'))
            print(f"Найдено {len(article_links)} ссылок на статьи")
            
            for link in article_links:
                title = link.get_text(strip=True)
                href = link.get('href')
                if href and not href.startswith('http'):
                    href = f"https://kiiioskforum.userecho.ru{href}"
                
                # Проверяем, что это не дубликат
                if not any(a['url'] == href for a in all_articles):
                    all_articles.append({
                        'title': title,
                        'url': href
                    })
            
            print(f"Всего уникальных статей собрано: {len(all_articles)}")
        except Exception as e:
            print(f"  Ошибка при обработке страницы {page_url}: {e}")
    
    return all_articles

async def get_article_stats(page, article_url):
    """Получение статистики для конкретной статьи"""
    print(f"  Получение данных для: {article_url}")
    
    try:
        await page.goto(article_url, wait_until="networkidle")
        
        # Ждем загрузки контента
        await page.wait_for_selector(".topic-header")
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ищем метрики
        views = 0
        likes = 0
        
        # Поиск просмотров - ищем элементы списка с иконкой глаза
        list_items = soup.find_all('li')
        for li in list_items:
            # Проверяем, есть ли иконка глаза (просмотры)
            eye_icon = li.find('i', class_='fa-eye')
            if eye_icon:
                badge = li.find('span', class_='badge')
                if badge:
                    views_text = badge.get_text(strip=True)
                    # Удаляем пробелы и неразрывные пробелы, оставляем только цифры
                    views = int(''.join(filter(str.isdigit, views_text.replace('\xa0', ''))))
            
            # Проверяем, есть ли иконка лайка (полезно)
            thumbs_icon = li.find('i', class_='fa-thumbs-up')
            if thumbs_icon:
                badge = li.find('span', class_='badge')
                if badge:
                    likes_text = badge.get_text(strip=True)
                    likes = int(''.join(filter(str.isdigit, likes_text.replace('\xa0', ''))))
        
        return {
            'views': views,
            'likes': likes
        }
    except Exception as e:
        print(f"  Ошибка при обработке {article_url}: {e}")
        return {
            'views': 0,
            'likes': 0
        }

def calculate_popularity_rating(views):
    """Определение рейтинга популярности по количеству просмотров"""
    if views > 500:
        return "Высокая"
    elif views >= 200:
        return "Средняя"
    else:
        return "Низкая"

async def generate_markdown_table(articles):
    """Генерация Markdown таблицы со статьями"""
    # Заголовок таблицы
    markdown = """# Legacy Index - Статистика статей форума Kiiiosk

Данные собраны: {datetime}
Всего статей: {total}

Степень популярности/востребованности определена по количеству просмотров:
- **Высокая**: >500 просмотров
- **Средняя**: 200-500 просмотров
- **Низкая**: <200 просмотров

| # | Название статьи | URL | Просмотры | Полезно | Рейтинг популярности |
|---|-----------------|-----|-----------|---------|---------------------|
""".format(
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=len(articles)
    )
    
    # Добавляем строки
    for i, article in enumerate(articles, 1):
        markdown += f"| {i} | {article['title']} | {article['url']} | {article['views']} | {article['likes']} | {article['rating']} |\n"
    
    return markdown

async def main():
    """Основная функция"""
    print("Запуск сбора данных с форума Kiiiosk...")
    
    async with async_playwright() as p:
        print("Запуск браузера...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 1. Получаем список всех статей
            print("\n=== Шаг 1: Сбор ссылок на статьи ===")
            articles = await get_article_links(page)
            print(f"Всего найдено {len(articles)} статей")
            
            if not articles:
                print("Ошибка: не удалось найти ни одной статьи!")
                return
            
            # 2. Получаем статистику для каждой статьи
            print("\n=== Шаг 2: Сбор статистики по статьям ===")
            for i, article in enumerate(articles):
                stats = await get_article_stats(page, article['url'])
                article.update(stats)
                article['rating'] = calculate_popularity_rating(stats['views'])
                
                if (i + 1) % 10 == 0 or (i + 1) == len(articles):
                    print(f"Обработано {i + 1}/{len(articles)} статей")
            
            # 3. Сортируем по просмотрам (по убыванию)
            articles.sort(key=lambda x: x['views'], reverse=True)
            
            # 4. Генерируем Markdown таблицу
            print("\n=== Шаг 3: Генерация Markdown таблицы ===")
            markdown_content = await generate_markdown_table(articles)
            
            # 5. Сохраняем в файл
            output_file = "LEGACY-INDEX.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Результат сохранен в файл: {output_file}")
            
            # 6. Выводим краткую статистику
            print("\n=== Статистика ===")
            total_views = sum(a['views'] for a in articles)
            total_likes = sum(a['likes'] for a in articles)
            high_rating = sum(1 for a in articles if a['rating'] == 'Высокая')
            medium_rating = sum(1 for a in articles if a['rating'] == 'Средняя')
            low_rating = sum(1 for a in articles if a['rating'] == 'Низкая')
            
            print(f"Общее количество просмотров: {total_views}")
            print(f"Общее количество 'Полезно': {total_likes}")
            print(f"Статьи с высоким рейтингом: {high_rating}")
            print(f"Статьи со средним рейтингом: {medium_rating}")
            print(f"Статьи с низким рейтингом: {low_rating}")
            
            # Сохраняем также JSON для отладки
            with open('forum_data.json', 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print("Данные также сохранены в forum_data.json")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())