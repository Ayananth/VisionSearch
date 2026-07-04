from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.products import router as products_router
from app.database import Base, engine
from app.models import Product  # noqa: F401
from app.services.image_service import ensure_uploads_directory


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_uploads_directory()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="VisionSearch API",
    description="Visual Product Search - Product Inventory",
    lifespan=lifespan,
)

app.include_router(products_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
