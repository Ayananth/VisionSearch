import json
from decimal import Decimal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import ValidationError

from app.api.deps import get_product_service
from app.schemas.product import ProductResponse
from app.services.exceptions import InvalidImageError, ProductNotFoundError
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    name: str = Form(...),
    price: Decimal = Form(...),
    description: str | None = Form(None),
    image: UploadFile = File(...),
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    try:
        product = await service.create_product(
            name=name,
            price=price,
            description=description,
            image=image,
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=json.loads(exc.json()),
        ) from exc
    except InvalidImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ProductResponse.model_validate(product)


@router.get("", response_model=list[ProductResponse])
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    products = service.list_products()
    return [ProductResponse.model_validate(product) for product in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    try:
        product = service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ProductResponse.model_validate(product)
