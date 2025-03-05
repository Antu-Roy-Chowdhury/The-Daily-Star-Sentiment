import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime
import csv

client = MongoClient("mongodb+srv://antu_roy_chow:ryZ2rxvRg1eXKI3r@anturoychowdhur.87lt0.mongodb.net/")
db = client.scrapy
news_items = []

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["www.thedailystar.net"]
    start_urls = ["https://www.thedailystar.net/"]

    def parse(self, response):
        
        cards = response.css(".title")
        
        for card in cards:
            pref = "https://www.thedailystar.net"
            suff = card.css("a").attrib["href"]
            link = pref + suff
            
            yield response.follow(link, callback=self.parse_article)


        
    def parse_article(self, response):

        article_title = response.css("h1::text").get()
        article_strong = response.css("strong::text").getall()
        article_strong = " ".join(article_strong)
        article_body = response.css("p::text").getall()
        article_body = " ".join(article_body)

        newsDetails = {}
        newsDetails["title"] = article_title
        newsDetails["Link"] = response.url
        newsDetails["strong"] = article_strong
        newsDetails["body"] = article_body
        news_items.append(newsDetails)
        
        db.news.insert_one(newsDetails)
        self.log(f"Inserted item into MongoDB: {newsDetails['title']}")

        if news_items:
            filename = "home_page.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["title", "Link", "strong", "body"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in news_items:
                    writer.writerow(item)

            self.log(f"Saved data to {filename}")





