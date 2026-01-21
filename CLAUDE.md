# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## О проекте

База знаний для платформы [Kiiiosk](https://kiiiosk.store) на основе Docusaurus 3.x.

- **URL:** https://merchantly.github.io/wiki/
- **Локаль:** ru (русский)
- **baseUrl:** /wiki/

Репозиторий является следующим поколением базы знаний, куда переносятся статьи из старого форума [https://kiiioskforum.userecho.ru/](https://kiiioskforum.userecho.ru/).

## Команды разработки

```bash
npm install         # Установка зависимостей
npm start           # Запуск dev-сервера (localhost:3000)
npm run build       # Сборка для продакшена
npm run serve       # Локальный просмотр сборки
npm run deploy      # Деплой на GitHub Pages
npm run clear       # Очистка кэша Docusaurus
```

## Архитектура

Стандартная структура Docusaurus classic:
- `docs/` — документация в Markdown/MDX
- `blog/` — блог с новостями
- `src/components/` — React компоненты
- `src/css/custom.css` — кастомные стили (CSS variables для цветов)
- `src/pages/` — кастомные страницы
- `static/img/` — статические изображения
- `docusaurus.config.js` — основная конфигурация
- `sidebars.js` — структура навигации документации

## Работа с документацией

Frontmatter для страниц:

```markdown
---
sidebar_position: 1
title: Название страницы
---
```

Изображения: `![Alt](/img/filename.png)` (файлы в `static/img/`).

## CI/CD

GitHub Actions (`.github/workflows/deploy.yml`) автоматически деплоит на GitHub Pages при пуше в `main`.
