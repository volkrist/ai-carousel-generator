# AI Carousel Generator

Backend MVP для генерации Instagram-каруселей из текста.

## Стек

- FastAPI
- PostgreSQL
- MinIO (S3)
- OpenAI
- Playwright
- Docker

## Архитектура

- `backend/` — API, сервисы, БД
- `frontend/` — Nuxt (Vue)
- `docker-compose.yml` — API, Postgres, MinIO

## Запуск

```bash
docker compose up --build
```

**Swagger:** http://localhost:8000/docs

## Основные endpoints

| Действие | Метод | Endpoint |
|----------|--------|----------|
| Create carousel | POST | `/carousels` |
| Generate slides | POST | `/generations` |
| Edit slides | PATCH | `/carousels/{id}/slides/{slide_id}` |
| Design settings | GET / PATCH | `/carousels/{id}/design` |
| Upload assets | POST | `/assets/upload` |
| Export carousel | POST / GET | `/exports`, `/exports/{id}` |

## Export

Карусель экспортируется как **PNG 1080×1350** и собирается в **ZIP archive**. В ответе `GET /exports/{id}` при `status=done` возвращается `download_url` — прямая ссылка на скачивание ZIP (MinIO).
