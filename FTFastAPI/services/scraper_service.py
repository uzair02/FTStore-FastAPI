from typing import List
from sqlalchemy.orm import Session
from models.scraper_model import Product
from schemas.scraper_schema import ProductCreate
from utils.logging_config import logger

def is_product_exists(db: Session, title: str) -> bool:
    """
    Check if a product with the given title already exists in the database.

    Args:
        db (Session): The database session.
        title (str): The title of the product to check.

    Returns:
        bool: True if a product with the given title exists, False otherwise.
    """
    return db.query(Product).filter(Product.title == title).first() is not None

def add_product(db: Session, product: ProductCreate) -> Product:
    """
    Add a new product to the database.

    Args:
        db (Session): The database session.
        product (ProductCreate): The product data to be added.

    Returns:
        Product: The added product.
    """
    logger.info(f"Adding new product: {product.title}")
    try:
        if is_product_exists(db, product.title):
            logger.error(f"Product with title '{product.title}' already exists.")
            raise ValueError(f"Product with title '{product.title}' already exists.")

        db_model = Product(
            title=product.title,
            description=product.description,
            image_url=str(product.image_url),
            product_page_url=str(product.product_page_url),
            blend_file_url=str(product.blend_file_url) if product.blend_file_url else None
        )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        logger.info(f"Product added successfully: {product.title}")
        return db_model
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add product: {e}")
        raise

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    """
    Retrieve a list of products from the database.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of products to skip. Defaults to 0.
        limit (int, optional): The maximum number of products to return. Defaults to 10.

    Returns:
        list[Product]: A list of retrieved products.
    """
    logger.info("Fetching products with skip=%d, limit=%d", skip, limit)
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        logger.info("Products fetched successfully: %d products found", len(products))
        return products
    except Exception as e:
        logger.error(f"Failed to fetch products: {e}")
        raise


def clear_products(db: Session) -> None:
    """
    Clear all products from the database.

    Args:
        db (Session): The database session.
    """
    try:
        db.query(Product).delete()
        db.commit()
        logger.info("All products cleared from the database.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clear products: {e}")
        raise
