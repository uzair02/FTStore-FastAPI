# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class FtcrawlerPipeline:
#     def process_item(self, item, spider):
#         return item


import requests
from loguru import logger

class FastAPIProductsPipeline:
    """
    Pipeline for sending scraped items to FastAPI.

    Attributes:
        api_url (str): The URL of the FastAPI endpoint to send the items.
    """

    def __init__(self):
        """
        Initialize the pipeline with the FastAPI endpoint URL.
        """
        self.api_url = "http://localhost:8000/products/"

    def process_item(self, item: dict, spider) -> dict:
        """
        Process each scraped item and send it to FastAPI.

        Args:
            item (dict): The scraped item to send.
            spider (scrapy.Spider): The spider instance that scraped the item.

        Returns:
            dict: The processed item.
        """
        try:
            response = requests.post(self.api_url, json=item, timeout=10)  # Set a timeout
            response.raise_for_status()
            logger.info(f"Successfully sent item to FastAPI: {item}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending item to FastAPI: {e}")
        return item
