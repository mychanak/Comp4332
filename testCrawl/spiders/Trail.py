#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating how to perform data crawling on one single webpage,
#  to save this webpage to the working directory of our computer, 
#  to obtain a list of all links found in "href" of the "a" HTML tags
#  and save the list in a file called "listOfLink.txt"
#
import scrapy
import json
import os

class OneWebpageSpider(scrapy.Spider):
	name = "Trial"
	start_urls = [ "http://comp4332.com/trial" ]
	
	# Constructor (which is called at the beginning)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("This is called at the beginning.")
		
	# Closed (which is called at the end)
	def closed(self, reason):
		print("This is called at the end.")

	def parse(self, response):
		# We perform the following operations
		global dictionary 
		#dictionary={}

		# Operation 1: Save the HTML file to the working directory of our computer
		crawlFilename = response.url
		#print(crawlFilename)

		listOfLink = response.xpath("//a[@href]/@href").extract()

		for word in listOfLink:
			print(word)
			yield response.follow(word, callback=self.parseMethod1)

	def parseMethod1(self, response):
		listOfLink = response.xpath("//a[@href]/@href").extract()

		for word in listOfLink:
			yield response.follow(word, callback=self.parseMethod2)




	def parseMethod2(self, response):
		# Step (a): Obtain the list of records (ID, name, byear)
		print(response.url)
		url = response.url.split("/")
		time = url[4]+"-"+url[6]+"-"+url[7]+"T"+url[8]+":"+url[9]+":00"
		url = url[4]+url[6]+url[7]+url[8]+url[9]
		listOfRecord = response.xpath("//div[@class='course']")
		#recordFilename = "result"+".txt"		
		for records in listOfRecord:
			h2 = records.xpath("./h2/text()").extract_first()
			h2 = h2.split("-",1)
			code = h2[0].split(" ")
			code = code[0]+code[1]
			result={}
			if (os.path.exists("result/"+code+".txt")):
				result = open("result/"+code+".txt","r")
				result= result.readline()
				result = json.loads(result)
			if result :

				sections = records.xpath("./table//tr[position()>1]")
				lastSection=""
				result[code]["listOfSection"][url]={}
				for sectionnum in sections:
					attr = sectionnum.xpath("./@class").extract_first()
					if("newsect" in attr):
						section = sectionnum.xpath("./td[1]/text()").extract()
						section =section[0].split(" ")[0]
						datetime = sectionnum.xpath("./td[2]/text()").extract()
						datetime = str(datetime)
						room = sectionnum.xpath("./td[3]/text()").extract_first()
						room = room.split("(")[0]
						room = str(room)
						instructor = sectionnum.xpath("./td[4]/text()").extract()
						instructor =str(instructor)
						quota = sectionnum.xpath("./td[5]/text()").extract_first()
						if(str(quota)=="None"):
							quota = sectionnum.xpath("./td[5]/span/text()").extract_first()
						enrol = sectionnum.xpath("./td[6]/text()").extract_first()
						avail = sectionnum.xpath("./td[7]/text()").extract_first()
						if(str(avail) == "None"):
							avail = sectionnum.xpath("./td[7]/strong/text()").extract_first()
						wait = sectionnum.xpath("./td[8]/text()").extract_first()
						if(str(wait) == "None"):
							wait = sectionnum.xpath("./td[8]/strong/text()").extract_first()
						remarks = sectionnum.xpath("./td[9]//div[@class='popupdetail']/text()").extract_first()
						dict1={}
						dict1["section"] = section
						dict1["dateTime"] = []
						dict1["dateTime"].append(datetime)
						dict1["room"] = []
						dict1["room"].append(room)
						dict1["instructor"] = []
						dict1["instructor"].append(instructor)
						dict1["quota"] = quota
						dict1["enrol"] = enrol
						dict1["avail"] = avail
						dict1["wait"] = wait
						dict1["remarks"] = remarks
						dict1["timeSlot"] = time
					
						result[code]["listOfSection"][url][section] = dict1
						#print(dic["listOfSection"][url][section])
						lastSection=section
					else:
						datetime = sectionnum.xpath("./td[1]/text()").extract()
						datetime = str(datetime)
						room = sectionnum.xpath("./td[2]/text()").extract_first()
						room = room.split("(")[0]
						room = str(room)
						instructor = sectionnum.xpath("./td[3]/text()").extract()
						instructor =str(instructor)
						result[code]["listOfSection"][url][lastSection]["dateTime"].append(datetime)
						result[code]["listOfSection"][url][lastSection]["room"].append(room)
						result[code]["listOfSection"][url][lastSection]["instructor"].append(instructor)
				with open("result/"+code+".txt", "w") as f:	
					f.write(json.dumps(result))
					f.write("\n")
				self.log("Saved File {} ".format(code+".txt"))

			else:
				h2 = h2[1]
				h2=h2.split("(")
				ctitle = h2[0]
				ctitle = ctitle.lstrip()
				credit = h2[1]
				credit = credit.split(" ")
				credit = credit[0]
				exclusion = records.xpath('.//div[@class="popupdetail"]//tr[th="EXCLUSION"]/td/text()').extract_first()
				prerequisites = records.xpath('.//div[@class="popupdetail"]//tr[th="PRE-REQUISITE"]/td/text()').extract_first()
				description = records.xpath('.//div[@class="popupdetail"]//tr[th="DESCRIPTION"]/td/text()').extract_first()
				colist = records.xpath('.//div[@class="popupdetail"]//tr[th="CO-REQUISITE"]/td/text()').extract_first()
				sections = records.xpath("./table//tr[position()>1]")
				#print(sections)
				dic = {}
				dic["code"] = code
				dic["ctitle"] = ctitle
				dic["credit"] = credit
				dic["prerequisites"] = prerequisites
				dic["exclusion"] = exclusion
				dic["description"] = description
				dic["colist"] = colist
				dic["listOfSection"] = {}
				dic["listOfSection"][url]={}
				lastSection=""
				for sectionnum in sections:
					attr = sectionnum.xpath("./@class").extract_first()
					if("newsect" in attr):
						section = sectionnum.xpath("./td[1]/text()").extract()
						section =section[0].split(" ")[0]
						datetime = sectionnum.xpath("./td[2]/text()").extract()
						datetime = str(datetime)
						room = sectionnum.xpath("./td[3]/text()").extract_first()
						room = room.split("(")[0]
						room = str(room)
						instructor = sectionnum.xpath("./td[4]/text()").extract()
						instructor =str(instructor)
						quota = sectionnum.xpath("./td[5]/text()").extract_first()
						if(str(quota)=="None"):
							quota = sectionnum.xpath("./td[5]/span/text()").extract_first()
						enrol = sectionnum.xpath("./td[6]/text()").extract_first()
						avail = sectionnum.xpath("./td[7]/text()").extract_first()
						if(str(avail) == "None"):
							avail = sectionnum.xpath("./td[7]/strong/text()").extract_first()
						wait = sectionnum.xpath("./td[8]/text()").extract_first()
						if(str(wait) == "None"):
							wait = sectionnum.xpath("./td[8]/strong/text()").extract_first()
						remarks = sectionnum.xpath("./td[9]//div[@class='popupdetail']/text()").extract_first()
						dict1={}
						dict1["section"] = section
						dict1["dateTime"] = []
						dict1["dateTime"].append(datetime)
						dict1["room"] = []
						dict1["room"].append(room)
						dict1["instructor"] = []
						dict1["instructor"].append(instructor)
						dict1["quota"] = quota
						dict1["enrol"] = enrol
						dict1["avail"] = avail
						dict1["wait"] = wait
						dict1["remarks"] = remarks
						dict1["timeSlot"] = time
						dic["listOfSection"][url][section] = dict1
						result[code] = dic
						# dic["listOfSection"][url]= {}
						# dic["listOfSection"][url][section] = dict1
						# dictionary[code] = dic	
						#print(dic["listOfSection"][url][section])
						lastSection=section
						# if(code=="HUMA2400"):
						# 	print(dictionary[code]["listOfSection"])
					else:
						datetime = sectionnum.xpath("./td[1]/text()").extract()
						datetime = str(datetime)
						room = sectionnum.xpath("./td[2]/text()").extract_first()
						room = room.split("(")[0]
						room = str(room)
						instructor = sectionnum.xpath("./td[3]/text()").extract()
						instructor =str(instructor)
						result[code]["listOfSection"][url][lastSection]["dateTime"].append(datetime)
						result[code]["listOfSection"][url][lastSection]["room"].append(room)
						result[code]["listOfSection"][url][lastSection]["instructor"].append(instructor)
				
						#print(dictionary[code]["listOfSection"][url])
				with open("result/"+code+".txt", "w") as f:	
					f.write(json.dumps(result))
					f.write("\n")
				self.log("Saved File {} ".format(code+".txt"))

		# with open("result.txt", "w") as f:	
		# 	#print(dictionary)
		# 	f.write(json.dumps(dictionary))
		# 	f.write("\n")
		# self.log("Saved File {} ".format("reuslt.txt"))


		
