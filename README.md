# AI Carousel Generator

## Overview

AI-инструмент для генерации Instagram каруселей из текста с использованием LLM.

Проект реализует полный pipeline:

**text → AI generation → slide editor → design → PNG export → ZIP archive**

## Features

### Carousel creation

- создание карусели из текста
- настройка количества слайдов
- выбор языка
- style hint для LLM

### AI slide generation

Используется **OpenAI API**.

LLM возвращает структуру:

- `slides`: order, title, body, footer

JSON валидируется через Pydantic schema.

### Slide editor

Можно редактировать:

- **title**
- **body**
- **footer**

Редактор сохраняет изменения через API.

### Design settings

Поддерживается настройка:

- template
- background
- overlay
- padding
- alignment
- header
- footer

Шаблоны: **classic**, **bold**, **minimal**.

### Asset upload

Можно загружать:

- background images
- resources
- design assets

Файлы хранятся в **MinIO** (S3 compatible storage).

### Export

Карусель экспортируется в:

- **PNG 1080×1350**

Каждый слайд рендерится через **Playwright (Chromium)**.

После этого: **PNG → ZIP archive**

API возвращает: **download_url**

## Architecture

```
Frontend (Nuxt)
       ↓
FastAPI Backend
       ↓
 ┌───────────────┬──────────────┬──────────────┐
PostgreSQL     MinIO          OpenAI API
Database       Storage        LLM
       ↓
Playwright Renderer
       ↓
PNG Export
```

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **AI** | OpenAI API, gpt-4o-mini |
| **Storage** | MinIO, boto3 |
| **Rendering** | Playwright, Chromium |
| **Infrastructure** | Docker, Docker Compose |
| **Frontend** | Nuxt, Vue, TypeScript |

## Project Structure

```
ai-carousel-generator
│
├── backend
│   ├── api
│   ├── models
│   ├── schemas
│   ├── services
│   └── core
│
├── frontend
│
├── docker-compose.yml
├── README.md
└── .env.example
```

## Setup

### Clone repository

```bash
git clone https://github.com/volkrist/ai-carousel-generator.git
cd ai-carousel-generator
```

### Create environment variables

Создать `.env`:

```
OPENAI_API_KEY=your_api_key
```

### Start project

```bash
docker compose up --build
```

### Swagger API

http://localhost:8000/docs

### MinIO Console

http://localhost:9101

- login: `minio`
- password: `minio123`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

http://localhost:3000

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for slide generation |
| `DATABASE_URL` | PostgreSQL connection string (set in docker-compose) |
| `S3_ENDPOINT` | MinIO endpoint (set in docker-compose) |
| `S3_ACCESS_KEY` | MinIO access key |
| `S3_SECRET_KEY` | MinIO secret key |
| `S3_BUCKET` | MinIO bucket name |

## API Endpoints

| Group | Method | Endpoint |
|-------|--------|----------|
| **Carousels** | POST | `/carousels` |
| | GET | `/carousels` |
| | GET | `/carousels/{id}` |
| | PATCH | `/carousels/{id}` |
| **Generation** | POST | `/generations` |
| | GET | `/generations/{id}` |
| **Slides** | GET | `/carousels/{id}/slides` |
| | PATCH | `/carousels/{id}/slides/{slide_id}` |
| **Design** | GET | `/carousels/{id}/design` |
| | PATCH | `/carousels/{id}/design` |
| **Assets** | POST | `/assets/upload` |
| **Export** | POST | `/exports` |
| | GET | `/exports/{id}` |

## Workflow

```
Create carousel
        ↓
Generate slides (LLM)
        ↓
Edit slides
        ↓
Apply design
        ↓
Export PNG
        ↓
Download ZIP
```

## Export

### Example Export

ZIP архив содержит:

- `slide_01.png`
- `slide_02.png`
- `slide_03.png`
- `slide_04.png`
- `slide_05.png`
- `slide_06.png`
- `slide_07.png`
- `slide_08.png`

Размер: **1080 × 1350**

## Limitations

MVP версия имеет упрощения:

- нет авторизации
- нет очереди задач
- BackgroundTasks вместо worker queue
- нет live обновления статусов

## Future Improvements

- WebSocket status updates
- Redis queue
- Celery workers
- presigned S3 URLs
- drag-and-drop editor
- video source parsing
- multi-template engine

## Development Notes

**Использованы AI-инструменты:**

- ChatGPT
- Cursor
- OpenAI API

**Время разработки:** ~10–12 часов

**Средний расход токенов:** ≈ $0.01 за генерацию карусели

## Author

**Alexander Shvetsov**

- **GitHub:** https://github.com/volkrist
- **Repository:** https://github.com/volkrist/ai-carousel-generator
