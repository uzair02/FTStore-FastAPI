import time
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

class Free3dSpider(scrapy.Spider):
    name = 'free3d'
    allowed_domains = ['free3d.com']
    start_urls = ['https://free3d.com/3d-models/blender']

    def __init__(self, *args, **kwargs):
        super(Free3dSpider, self).__init__(*args, **kwargs)
        options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)

        page_source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'
        }

        for item in response.css('div.search-result__info-wrapper'):
            title = item.css('div.search-result__title a::text').get()
            item_url = response.urljoin(item.css('div.search-result__title a::attr(href)').get())
            is_free = item.css('span.search-result__price.free::text').get()

            if is_free:
                yield scrapy.Request(item_url, callback=self.parse_item, meta={'title': title}, headers=headers)

        next_page = response.css('a.paging-link.paging-link__next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse, headers=headers)

    def parse_item(self, response):
        title = response.meta['title']
        
        description_parts = response.css('div.product-description__text.desc_english *::text').getall()
        description = ' '.join(description_parts).strip()
        image_url = response.css('img.large-image::attr(src)').get()
        product_page_url = response.url

        self.driver.get(response.url)
        try:
            wait = WebDriverWait(self.driver, 10)
            download_button = wait.until(EC.element_to_be_clickable((By.ID, 'download-prod')))
            download_button.click()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to click download button: {e}")
            yield {
                'title': title,
                'description': description,
                'image_url': image_url,
                'product_page_url': product_page_url,
                'blend_file_url': None
            }
            return

        page_source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        files = response.css('div.vault-cont div.files a.file')
        blend_file_url = None
        for file in files:
            format_span = file.css('span.formats::text').get()
            if format_span and '.blend' in format_span:
                blend_file_url = file.css('::attr(href)').get()
                break

        if blend_file_url:
            blend_file_url = response.urljoin(blend_file_url)

        yield {
            'title': title,
            'description': description,
            'image_url': image_url,
            'product_page_url': product_page_url,
            'blend_file_url': blend_file_url
        }

    def closed(self, reason):
        if self.driver:
            self.driver.quit()
            logger.info(f"Spider closed due to: {reason}")
