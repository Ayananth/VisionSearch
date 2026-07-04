from decimal import Decimal

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate
from app.services.exceptions import ProductNotFoundError
from app.services.image_service import save_product_image


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_product(
        self,
        name: str,
        price: Decimal,
        description: str | None,
        image: UploadFile,
    ) -> Product:
        product_data = ProductCreate(
            name=name,
            price=price,
            description=description,
        )

        image_path = await save_product_image(image)

        product = Product(
            name=product_data.name,
            price=product_data.price,
            description=product_data.description,
            image_path=image_path,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def list_products(self) -> list[Product]:
        statement = select(Product).order_by(Product.created_at.desc())
        return list(self.db.scalars(statement).all())

    def get_product(self, product_id: int) -> Product:
        product = self.db.get(Product, product_id)
        if product is None:
            raise ProductNotFoundError(f"Product with id {product_id} not found")
        return product
