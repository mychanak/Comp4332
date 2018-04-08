#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating how to perform data crawling on one single webpage,
#  to obtain the data information using XPath,
#  and to save the information in a file (using two methods)
#  (one file is called "record1.txt" and the other file is called "record2.txt")
#
import scrapy

class TableWebpageSpider(scrapy.Spider):
	name = "TableWebpage"
	start_urls = [ "http://www.cse.ust.hk/~raywong/temp/Table.html" ]
	
	# Constructor (which is called at the beginning)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("This is called at the beginning.")
		
	# Closed (which is called at the end)
	def closed(self, reason):
		print("This is called at the end.")	
			
	def parse(self, response):
		# We perform the following operations
		
		# Operation 1: Using Method 1 to obtain the data information using XPath
		#              and save the information in a file called "record1.txt"
		yield self.parseMethod1(response)
	
		# Operation 2: Using Method 2 to obtain the data information using XPath
		#              and save the information in a file called "record2.txt"
		yield self.parseMethod2(response)

	def parseMethod1(self, response):
		# Step (a): Obtain the list of records (ID, name, byear)
		listOfID = response.xpath("//tr/td[1]/text()").extract()
		listOfName = response.xpath("//tr/td[2]/text()").extract()
		listOfByear = response.xpath("//tr/td[3]/text()").extract()
		
		# Step (b): Save the list of records in a file called "record1.txt"
		recordFilename = "record1.txt"
		no = 0
		with open(recordFilename, "w") as f:
			for id in listOfID:
				id = listOfID[no]
				name = listOfName[no]
				byear = listOfByear[no]
				no = no + 1
				f.write("({}: {}, {}, {})\n".format(no, id, name, byear))
				f.write("\n")
		self.log("Saved File {} ".format(recordFilename))
		
	def parseMethod2(self, response):
		# Step (a): Obtain the list of records (ID, name, byear)
		listOfRecord = response.xpath("//tr[td]")
		
		# Step (b): Save the list of records in a file called "record2.txt"
		recordFilename = "record2.txt"
		no = 0
		with open(recordFilename, "w") as f:
			for record in listOfRecord:
				id = record.xpath("./td[1]/text()").extract_first()
				name = record.xpath("./td[2]/text()").extract_first()
				byear = record.xpath("./td[3]/text()").extract_first()
				no = no + 1
				f.write("({}: {}, {}, {})\n".format(no, id, name, byear))
				f.write("\n")
		self.log("Saved File {} ".format(recordFilename))
