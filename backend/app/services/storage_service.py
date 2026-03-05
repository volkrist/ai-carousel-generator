import os
import uuid

import boto3
from botocore.config import Config

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")

# MinIO needs path-style addressing
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)


def ensure_bucket() -> None:
    buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]
    if S3_BUCKET not in buckets:
        s3.create_bucket(Bucket=S3_BUCKET)


def upload_file(file_bytes: bytes, filename: str, content_type: str | None) -> dict:
    ensure_bucket()

    ext = filename.split(".")[-1] if "." in filename else "bin"
    key = f"assets/{uuid.uuid4()}.{ext}"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType=content_type or "application/octet-stream",
    )

    url = f"{S3_ENDPOINT}/{S3_BUCKET}/{key}"

    return {"key": key, "url": url}


def get_file_url(key: str) -> str:
    return f"{S3_ENDPOINT}/{S3_BUCKET}/{key}"
