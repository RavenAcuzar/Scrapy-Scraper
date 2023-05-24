import scrapy
from pgscraper.services.proxy_api import generate_proxy_url
from pgscraper.services.azure_blob import save
from dotenv import load_dotenv
import os
from scrapy.exceptions import CloseSpider
load_dotenv()


class PgspiderSpider(scrapy.Spider):
    name = "pgspider"
    
    def start_requests(self):
        yield scrapy.Request(url=generate_proxy_url(os.environ.get('WEB_START_URL')), callback=self.parse)

    def parse(self, response, curr_page=1):
        urls_to_scrape=response.css(os.environ.get('WEB_CSS_ITEM_TO_SCRAPE_SELECTOR')).getall()
        page=curr_page
        for property_url in urls_to_scrape:
            yield scrapy.Request(url=generate_proxy_url(property_url), callback=self.download_html)

        # follow pagination links
        page += 1
        next_page_url = os.environ.get('WEB_PAGINATION_LINK').replace("{page}", str(page))    
        yield scrapy.Request(url=generate_proxy_url(next_page_url), callback=self.parse, cb_kwargs=dict(curr_page=page),)
            
    def download_html(self, response):
        yield save(response)
