"""
This module defines the API endpoints for product management, including
creating and retrieving products.
"""
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.scraper_schema import ProductCreate, Product
from schemas.error_schema import ErrorResponse
from services.scraper_service import add_product, get_products
from utils.database import get_db
from utils.logging_config import logger
from utils.error_messages import ErrorMessages

router = APIRouter()

@router.post("/products/", response_model=Product, responses={500: {"model": ErrorResponse}})
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.

    Args:
        product (ProductCreate): The product data to create.
        db (Session, optional): The database session dependency.

    Returns:
        Product: The created product.

    Raises:
        HTTPException: If an error occurs during product creation.
    """
    logger.info("Received request to create a product with title: {}", product.title)
    try:
        db_product = add_product(db=db, product=product)
        logger.info("Product created successfully with ID: {}", db_product.id)
        return db_product
    except Exception as e:
        logger.error("Error creating product: {}", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.INTERNAL_SERVER_ERROR.value,
            headers={"X-Error": "There goes my error"}
        ) from e

@router.get("/products/", response_model=list[Product], responses={500: {"model": ErrorResponse}})
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of products.

    Args:
        skip (int, optional): The number of products to skip. Defaults to 0.
        limit (int, optional): The maximum number of products to return. Defaults to 10.
        db (Session, optional): The database session dependency.

    Returns:
        list[Product]: A list of retrieved products.

    Raises:
        HTTPException: If an error occurs during product retrieval.
    """
    logger.info("Received request to retrieve products with skip: {} and limit: {}", skip, limit)
    try:
        products = get_products(db, skip=skip, limit=limit)
        logger.info("Retrieved {} products", len(products))
        return products
    except Exception as e:
        logger.error("Error retrieving products: {}", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.INTERNAL_SERVER_ERROR.value,
            headers={"X-Error": "There goes my error"}
        ) from e
