# Kiiiosk Wiki

Документация и инструкции для пользователей платформы [Kiiiosk](https://kiiiosk.store).

> **Важно:** Этот репозиторий является следующим поколением базы знаний [https://kiiioskforum.userecho.ru/](https://kiiioskforum.userecho.ru/). В него переносятся все статьи из старого форума с современными переработками и улучшениями.

## Технологии

- **[Docusaurus](https://docusaurus.io/)** — генератор статических сайтов от Meta
- **Markdown/MDX** — формат документации
- **GitHub Pages** — хостинг

## Структура проекта

```
wiki/
├── docs/                    # Документация (Markdown файлы)
├── blog/                    # Блог с новостями
├── src/
│   ├── components/          # React компоненты
│   ├── css/                 # Стили
│   └── pages/               # Кастомные страницы
├── static/
│   └── img/                 # Изображения
├── docusaurus.config.js     # Конфигурация сайта
├── sidebars.js              # Навигация документации
└── package.json
```

## Локальная разработка

```bash
# Установка зависимостей
npm install

# Запуск dev-сервера
npm start

# Сборка для продакшена
npm run build

# Деплой на GitHub Pages
npm run deploy
```

## Добавление документации

1. Создайте `.md` файл в папке `docs/`
2. Добавьте frontmatter:
   ```markdown
   ---
   sidebar_position: 1
   title: Название страницы
   ---

   # Заголовок

   Контент...
   ```
3. Изображения кладите в `static/img/` и ссылайтесь как `![](/img/screenshot.png)`

## Публикация

Сайт автоматически публикуется на GitHub Pages при пуше в `main` ветку.

**URL:** https://merchantly.github.io/wiki/

## Ресурсы

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Markdown Features](https://docusaurus.io/docs/markdown-features)
- [Deployment Guide](https://docusaurus.io/docs/deployment)

---

© Kiiiosk — платформа для создания интернет-магазинов
