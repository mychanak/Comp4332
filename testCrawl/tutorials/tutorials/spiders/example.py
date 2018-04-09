# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'Spider'
    allowed_domains = ['ust.hk']
    start_urls = ['http://comp4332.com/trial']

    def parse(self, response):
        # Operation 1: Save the HTML file to the working directory of our computer
        crawlFilename = response.url.split("/")[-1]
        with open(crawlFilename, "wb") as f:
            f.write(response.body)
        self.log("Saved File %s " % crawlFilename)
        
        # Operation 2:
        # Step (a): Find a list of all links found in "href" of the "a" HTML tags
        listOfLink = response.xpath("//a[@href]/@href").extract()
        
        # Step (b): To perform data crawling on the webpage of each of the links
        #          where each link contains keyword "Table.html"
        for link in listOfLink:
            if ("Table.html" in link):
                yield response.follow(link, callback=self.parse)


        pass
