"""
Schemas for representing products in the database and API requests/responses.

This module defines the Pydantic schemas used for validating and serializing product data.
"""

from uuid import UUID
from typing import Optional
from pydantic import BaseModel, HttpUrl

class ProductBase(BaseModel):
    """
    Base schema for a product, including the common attributes for product data.

    Attributes:
        title (str): The title of the product.
        description (str): A detailed description of the product.
        image_url (HttpUrl): The URL of the product image.
        product_page_url (HttpUrl): The URL of the product's page.
        blend_file_url (Optional[HttpUrl]): The URL of the blend file, if available.
    """
    title: str
    description: str
    image_url: HttpUrl
    product_page_url: HttpUrl
    blend_file_url: Optional[HttpUrl] = None

class ProductCreate(ProductBase):
    """
    Schema for creating a new product.

    This schema inherits from ProductBase and does not add any additional fields.
    It is used for validating data when creating a new product.
    """

class Product(ProductBase):
    """
    Schema for representing a product as returned by the API.

    This schema includes an ID field in addition to the fields from ProductBase.

    Attributes:
        id (UUID): The unique identifier for the product.
    """
    id: UUID

    class Config:
        """
        Configurations for Pydantic to allow ORM models to be used with the schema.
        This enables the automatic conversion of ORM models to Pydantic models.
        """
        orm_mode = True
