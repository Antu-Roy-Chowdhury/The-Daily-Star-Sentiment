import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

# client = MongoClient("mongodb+srv://antu_roy_chow:ryZ2rxvRg1eXKI3r@anturoychowdhur.87lt0.mongodb.net/")
# db = client.scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["www.thedailystar.net"]
    start_urls = ["https://www.thedailystar.net/"]

    def start_requests(self):
        urls = [
            "https://www.thedailystar.net/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"news-{page}.html"
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        
        cards = response.css(".title")
        for card in cards:
            newsDetails = {}
            newsDetails["title"] = card.css("a::text").get()
            newsDetails["Link"] = card.css("a").attrib["href"]
            yield newsDetails
