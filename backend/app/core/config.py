import os
from functools import lru_cache


@lru_cache
def get_settings():
    return {
        "database_url": os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/carousel_db"),
        "s3_endpoint": os.getenv("S3_ENDPOINT", "http://localhost:9000"),
        "s3_access_key": os.getenv("S3_ACCESS_KEY", "minio"),
        "s3_secret_key": os.getenv("S3_SECRET_KEY", "minio123"),
        "s3_bucket": os.getenv("S3_BUCKET", "carousel-assets"),
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    }


def get_openai_api_key() -> str:
    return get_settings()["openai_api_key"]
