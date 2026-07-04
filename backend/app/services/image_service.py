import uuid
from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from PIL import Image

from app.database import BASE_DIR
from app.services.exceptions import InvalidImageError

UPLOADS_DIR = BASE_DIR / "uploads"

FORMAT_EXTENSIONS: dict[str, str] = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "WEBP": ".webp",
    "BMP": ".bmp",
}


def ensure_uploads_directory() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def _extension_for_image(content: bytes) -> str:
    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()

        with Image.open(BytesIO(content)) as image:
            image_format = image.format
    except Exception as exc:
        raise InvalidImageError("Uploaded file is not a valid image") from exc

    if image_format is None:
        raise InvalidImageError("Uploaded file is not a valid image")

    extension = FORMAT_EXTENSIONS.get(image_format)
    if extension is None:
        raise InvalidImageError("Unsupported image format")

    return extension


async def save_product_image(image: UploadFile) -> str:
    content = await image.read()
    if not content:
        raise InvalidImageError("Uploaded file is empty")

    extension = _extension_for_image(content)
    filename = f"{uuid.uuid4()}{extension}"
    destination = UPLOADS_DIR / filename
    destination.write_bytes(content)

    return f"uploads/{filename}"
