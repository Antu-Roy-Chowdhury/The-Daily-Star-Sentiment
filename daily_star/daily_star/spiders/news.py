import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime
import csv

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
        
        cards = response.css(".title")
        news_items = []

        for card in cards:
            pref = "https://www.thedailystar.net"
            newsDetails = {}
            newsDetails["title"] = card.css("a::text").get()
            suff = card.css("a").attrib["href"]
            newsDetails["Link"] = pref + suff
            news_items.append(newsDetails)

        if news_items:
            filename = "1st_page.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["title", "Link"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for item in news_items:
                    writer.writerow(item)

            self.log(f"Saved data to {filename}")