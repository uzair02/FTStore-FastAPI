import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from utils.database import Base

class Product(Base):
    """Represents a product in the database.

    Attributes:
        id (UUID): The unique identifier for the product.
        title (str): The title of the product.
        description (str): A detailed description of the product.
        image_url (str): The URL of the product image.
        product_page_url (str): The URL of the product's page.
    """

    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(Text)
    image_url = Column(String)
    product_page_url = Column(String)
    blend_file_url = Column(String, nullable=True)
