#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating 
#  1. how to perform data crawling on one single webpage,
#     to save this webpage to the working directory of our computer,
#  2. to obtain a list of all links found in "href" of the "a" HTML tags,
#     and to perform data crawling on the webpage of each of the links
#     where each link contains keywords "Table.html"
#
import scrapy

class LinkWebpageSpider(scrapy.Spider):
	name = "LinkWebpage"
	start_urls = [ "http://www.cse.ust.hk/~raywong/temp/SimpleWebpage.html" ]
	
	# Constructor (which is called at the beginning)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("This is called at the beginning.")
		
	# Closed (which is called at the end)
	def closed(self, reason):
		print("This is called at the end.")	
			
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

