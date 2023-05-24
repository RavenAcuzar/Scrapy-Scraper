import scrapy
from pgscraper.services.proxy_api import generate_proxy_url
from pgscraper.services.azure_blob import save
from dotenv import load_dotenv
import os
from scrapy.exceptions import CloseSpider
load_dotenv()


class PgspiderSpider(scrapy.Spider):
    name = "pgspider"
    max_scrape_count=int(os.environ.get('MAX_SCRAPE_DATA_COUNT'))
    current_scrape_count=0
    
    def start_requests(self):
        yield scrapy.Request(url=generate_proxy_url(os.environ.get('WEB_START_URL')), callback=self.parse)

    def parse(self, response, curr_page=1,curr_count=current_scrape_count):
        urls_to_scrape=response.css(os.environ.get('WEB_CSS_ITEM_TO_SCRAPE_SELECTOR')).getall()
        count=curr_count
        page=curr_page
        for property_url in urls_to_scrape:
            count +=1
            if count <= self.max_scrape_count:
                yield scrapy.Request(url=generate_proxy_url(property_url), callback=self.download_html)
            else:
                raise CloseSpider("Reached the maximum scrape count!")
        
        # follow pagination links
        page += 1
        next_page_url = os.environ.get('WEB_PAGINATION_LINK').replace("{page}", str(page))    
        yield scrapy.Request(url=generate_proxy_url(next_page_url), callback=self.parse, cb_kwargs=dict(curr_page=page, curr_count=count),)
            
    def download_html(self, response):
        save(response)
