# coding=utf-8
# The program was written by Juliana KO and Alice Chan.
# The program is used for illustrating how to write a program with stubs using the "bank" application
#
from pymongo import MongoClient
from pprint import pprint
from tabulate import tabulate
import datetime
import subprocess
import json 
import glob, os
import csv
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import time
import re

def dropCollection(db):
    db.course.drop()
    dire=os.getcwd()
    os.chdir(dire+"/result")
    for file in glob.glob("*.txt"):
        os.remove(file)
    print ("Collection dropping and empty collection creating are successful")
    os.chdir(dire)


# 5.2 Data Crawling
def crawlData(db):

    try:
        data = input("Please input the URL/Keywords: ")
        if (data == "default"):
            strCommand = "scrapy crawl Realistic"
            subprocess.run(strCommand, shell=True)  
            print("inserting")

        else:
            url=""
            with open("testCrawl/spiders/Spider.py","r") as f:
                url=f.read()
                #print(url)
                f.close()
            url = url.replace("http://comp4332.com/realistic/",data)
            url=url.replace("Realistic","Temp")
            with open("testCrawl/spiders/Temp.py","w") as f:
                f.write(url)
                f.close()
            strCommand = "scrapy crawl Temp"
            subprocess.run(strCommand, shell=True)  



        dire=os.getcwd()
        os.chdir(dire+"/result")
        for file in glob.glob("*.txt"):
            fileopened  = open (file,"r")
            dic = fileopened.readline()
            dic = json.loads(dic)
            for key in dic:

                query=[]
                for section in dic[key]["listOfSection"]:
                    for sub in dic[key]["listOfSection"][section]:
                        time = datetime.datetime.strptime(dic[key]["listOfSection"][section][sub]["timeSlot"] , "%Y-%m-%dT%H:%M:%S")
                        query.append({"section": dic[key]["listOfSection"][section][sub]["section"],\
                        'dateTime': dic[key]["listOfSection"][section][sub]["dateTime"] ,\
                        'room': dic[key]["listOfSection"][section][sub]["room"],\
                        'instructor': dic[key]["listOfSection"][section][sub]["instructor"],\
                        'quota': dic[key]["listOfSection"][section][sub]["quota"],\
                        'enrol': dic[key]["listOfSection"][section][sub]["enrol"],\
                        'avail': dic[key]["listOfSection"][section][sub]["avail"],\
                        'wait': dic[key]["listOfSection"][section][sub]["wait"],\
                        'timeSlot': time ,\
                        'remarks': dic[key]["listOfSection"][section][sub]["remarks"] })

                db.course.insert({\
                    "code": dic[key]["code"],\
                    "ctitle": dic[key]["ctitle"],\
                    "credit": dic[key]["credit"],\
                    "prerequisite": dic[key]["prerequisites"],\
                    "colist": dic[key]["colist"],\
                    "exclusion": dic[key]["exclusion"],\
                    "description": dic[key]["description"],\
                    "listOfSections": query\
                })

        os.chdir(dire)
        print ("Data Crawling is successful and all data are inserted into the database")
    except pymongo.errors.ConnectionFailure as error: 
            print("Document Querying Failed! Error Message: \"{}\"".format(error))


# 5.3.0 Print Course
# For each distinct course, show “Course Code”, “Course Title”, “No. of Units/Credits”, “Matched Time Slot”
# For the list of sections (including both lecture sections and non-lecture sections) of the course, show “Section”, “Date & Time”, “Quota”, “Enrol”, “Avail”, “Wait” and “Satisfied”

def printSection(sections, size):

    if size == "":
        table=[]
        for section in sections:
            dateTime=""
            for i in section["dateTime"]:
                dateTime = dateTime+str(i) +"\n"
            temp=[section["section"], dateTime, section["quota"], section["enrol"], section["avail"], section["wait"]]
            table.append(temp)
            #pprint(sections[section]["section"])
            #for each in section["dateTime"]:
                #print(each)

        print (tabulate(table, headers={"Section":"", "Date & Time":"", "Quota":"","Enroll":"","Avail":"","Wait":""}))
        print("")

    else:
        table=[]
        for section in sections:
            wait = float(section["wait"])
            enrol = float(section["enrol"])
            size = float(size)
            dateTime=""
            for i in section["dateTime"]:
                dateTime = dateTime+str(i) +"\n"
            condition= wait >= (enrol*size)
            if(condition):
                temp=[section["section"], dateTime, section["quota"], section["enrol"], section["avail"], section["wait"],"Yes"]
                table.append(temp)
            else:
                temp=[section["section"], dateTime, section["quota"], section["enrol"], section["avail"], section["wait"],"No"]
                table.append(temp)

        print (tabulate(table, headers={"Section":"", "Date & Time":"", "Quota":"","Enroll":"","Avail":"","Wait":"","Satisfied":""}))
        print("")
        


# for
def printCourse(course,size):


    if size=="":
        table= [course["code"],course["ctitle"],course["credit"]]
        print (tabulate([table], headers={'Course Code':"", 'Course Title': " ","No. of Credit":""}))
        print("")
        print ('{:>42}'.format("Sections"))
        printSection(course["listOfSections"], size)
    else:
        for temp in course["listOfSections"]:
            temp2  = temp["section"]
            pattern = re.compile("^L\d")
            if not (pattern.match(temp2)):
                return
        table= [course["code"],course["ctitle"],course["credit"],course["match_ts"]]
        print (tabulate([table], headers={'Course Code':"", 'Course Title': " ","No. of Credit":"","Matched Time slot":""}))
        print("")
        print ('{:>44}'.format("Matched Time Slot "))
        printSection(course["listOfSections"], size)


# 5.3.1 Course Search by Keyword
def searchByKeyword(db):
    try:

        keywords = input("Please input the Keyword(s): ")
        db.course.aggregate([ {"$unwind": "$listOfSections"},\
            {"$group": {"_id":"$code","maxDate":{"$max": "$listOfSections.timeSlot"}}},\
            {"$out": "R1"}\
        ])

        query = []
        listOfKeywords = keywords.split(" ")

        for word in listOfKeywords:
            reg =".*"+word+".*"
            query.append({'ctitle': {'$regex':reg }})
            query.append({'description': {'$regex':reg }})
            query.append({'listOfSections.remarks': {'$regex':reg }})

        listOfCourse = db.course.aggregate([{ "$match": { "$or": query } },\
        {"$lookup":{ \
        "localField": "code",\
        "from": "R1",\
        "foreignField": "_id",\
        "as": "R3"\
        }},\
        {"$unwind": "$R3"},\
        {"$unwind": "$listOfSections"},\
        { "$project": { '_id': 0, 'code': 1, 'ctitle': 1, 'credit': 1, "listOfSections.section": 1, \
        "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1,\
        "listOfSections.avail": 1, "listOfSections.wait": 1 ,"compareResult": {"$eq": ["$listOfSections.timeSlot", "$R3.maxDate"]}} },\
        {"$match": {"compareResult": True}},\
        { "$group": {"_id": { "code": "$code","ctitle": "$ctitle" ,"credit":"$credit"}, "listOfSections":{"$addToSet": "$listOfSections"}}},\
        {"$unwind":"$listOfSections"},\
        {"$sort":{"listOfSections.section":1}},\
        {"$group": {"_id": {  "code": "$_id.code","ctitle": "$_id.ctitle" ,"credit":"$_id.credit"}, "listOfSections":{"$push": "$listOfSections"}}},\
        {"$project":{"code":"$_id.code","ctitle":"$_id.ctitle","credit":"$_id.credit", "listOfSections":"$listOfSections","_id":0}},\
        { "$sort": { "code": 1 } }])
        
        for course in listOfCourse: 
            printCourse(course, "")

        db.R1.drop()

        

    except pymongo.errors.ConnectionFailure as error: 
        print("Document Querying Failed! Error Message: \"{}\"".format(error))


# 5.3.2 Course Search by Waiting List Size
# only extract course from database which statisfy the match_ts
def searchBySize(db):
    
    try:
        size = input("Please input the Maximum Waiting List Size: ")
        start_ts = input("Please input the Starting Time Slot in YYYY-mm-ddTHH:MM:SS Format: ")
        end_ts = input("Please input the Ending Time Slot in YYYY-mm-ddTHH:MM:SS Format: ")

        dateTime1 = datetime.datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%S")
        dateTime2 = datetime.datetime.strptime(end_ts, "%Y-%m-%dT%H:%M:%S")
        
        db.course.aggregate([ {"$unwind": "$listOfSections"},\
            {"$match": {\
            "$and": [{ "listOfSections.timeSlot": { "$gte": dateTime1 } }, \
                { "listOfSections.timeSlot": { "$lte": dateTime2 } }\
            ]}},\
            {"$group": {"_id":"$code","maxDate":{"$max": "$listOfSections.timeSlot"}}},\
            {"$out": "R1"}\
        ])



        listOfCourse = db.course.aggregate([\
        {"$lookup":{\
            "localField": "code",\
            "from": "R1",\
            "foreignField": "_id",\
            "as": "R3"\
        }},\
        {"$unwind": "$R3"},\
        {"$project":{"_id": 0, "code":1, "ctitle":1, "credit":1, "listOfSections.section": 1, "listOfSections.dateTime": 1,\
         "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1, "R3.maxDate":1}},\
        {"$unwind": "$listOfSections"},\
        {"$project":{"_id": 0, "code":1, "ctitle":1, "credit":1, "listOfSections.section": 1, "listOfSections.dateTime": 1, \
        "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1,
         "R3.maxDate":1, "compareResult": {"$eq": ["$listOfSections.timeSlot", "$R3.maxDate"]} }},\
        {"$match": {"compareResult": True}},\
        {"$project":{"_id": 0, "code":1, "ctitle":1, "credit":1, "listOfSections.section": 1, "listOfSections.dateTime": 1,\
         "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "match_ts":"$R3.maxDate" }},\
        { "$group": {"_id": { "code": "$code","ctitle": "$ctitle" ,"credit":"$credit" ,"match_ts":"$match_ts"}, "listOfSections":{"$addToSet": "$listOfSections"}}},\
        {"$unwind":"$listOfSections"},\
        {"$sort":{"listOfSections.section":1}},\
        {"$group": {"_id": {  "code": "$_id.code","ctitle": "$_id.ctitle" ,"credit":"$_id.credit","match_ts":"$_id.match_ts"}, "listOfSections":{"$push": "$listOfSections"}}},\
        {"$project":{"code":"$_id.code","ctitle":"$_id.ctitle","credit":"$_id.credit","match_ts":"$_id.match_ts" ,"listOfSections":"$listOfSections","_id":0}},\
        { "$sort": { "code": 1 } }\
        ])

        # courseWithLecture = db.course.aggregate([\
        #     { "$unwind": "$listOfSections"},\
        #     { "$match":{ "listOfSections.section":{'$regex': "^L\d" }}},\
        #     { "$group":{"_id":{"code":"$code"},"listOfSections":{"$push": "$listOfSections"}}},\
        #     { "$project":{"_id":0,"code":"$_id.code"}}\
        # ])
        # courseWithLecturelist=[]
        # for course in courseWithLecture:
        #     courseWithLecturelist.append(course["code"])


        for course in listOfCourse: 
            # if(course["code"] in courseWithLecturelist):
            printCourse(course,size)

        db.R1.drop()


    except pymongo.errors.ConnectionFailure as error: 
        print("Document Querying Failed! Error Message: \"{}\"".format(error))

    #printCourse(course, size)


# 5.3 Course Search
def courseSearch(db):
    choice3 = 0
    while (choice3 != 3):
        print("")
        print("   Course Search Menu")
        print("=======================")
        print("1. Course Search by Keyword")
        print("2. Course Search by Waiting List Size")
        print("3. Exit")
        print("")

        # allow the user to choose one of the functions in the menu
        choice3 = input("Please input your choice (1-3): ")

        print("")

        # check the input and call the correspondence function
        if (choice3 == "1"):
            searchByKeyword(db)
        elif (choice3 == "2"):
            searchBySize(db)
        elif (choice3 == "3"):
            print("")
            return
        else:
            print("Invalid Input!")


# 5.4 Waiting List Size Prediction
def prediction():



    cc = input("Please input the Course Code: ")
    ln = input("Please input the Lecture Number (e.g. the input should be “1” denoting “L1”): ")
    ts = input("Please input the Time Slot: ")
    print ("Training for course " + cc + ", " + str(ln) + " and " + str(ts))
    ts = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
    ts = str(ts)
    filename = "timeSeries/"+str(cc)+"L"+str(ln)+".csv"
    try:
        newX = numpy.loadtxt(filename, delimiter=",",usecols=range(0, 5),dtype="str")
    except:
        print("There is no lecture section and thus there is no prediction result.")
        return
    result = numpy.where(newX == ts)
    if (len(result[0])!=0):
        result = newX[result[0]][result[1]][4]
        result = result.astype(int)
        N1 = result
        N2 = result
        N3 = result
        N4 = result
        N5 = result
        print ("Prediction: "+str(N1) +", " + str(N2) + ", "+ str(N3) +", " +str(N4) +", " + str(N5))
    else:
        time = numpy.loadtxt(filename, delimiter=",",usecols=[0],dtype="str")
        
        small= numpy.where(time< ts)
        small1 = numpy.array(small)
        if (small1.size ==0):
            small = 0
        else:
            small = numpy.max(small)
        
        big= numpy.where(time> ts)
        big1 = numpy.array(big)
        if (big1.size ==0):
            big = len(newX)-1
        else:
            big = numpy.min(big)
        # print(newX[small])
        # print(newX[big])
        result = []
        result.append(int((int(newX[small][1]) +int(newX[big][1]))/2))
        result.append(int((int(newX[small][2]) +int(newX[big][2]))/2))
        result.append(int((int(newX[small][3]) +int(newX[big][3]))/2))
        result.append(int((int(newX[small][4]) +int(newX[big][4]))/2))
        result = numpy.array(result)
        result = result.reshape(1,4)
        #target = numpy.loadtxt("timeSeries/COMP4332.csv", delimiter=",",usecols=[4])
        with open("M1/"+cc+"L"+ln+".json", "r") as f:
            model_json = f.read()
            model = model_from_json(model_json)
            model.load_weights("M1/"+cc+"L"+ln+".h1")
        newY = model.predict(result, batch_size=4)
        newY = numpy.around(newY)
        N1 = int(newY)
        with open("M2/"+cc+"L"+ln+".json", "r") as f:
            model_json = f.read()
            model = model_from_json(model_json)
            model.load_weights("M2/"+cc+"L"+ln+".h2")
        newY = model.predict(result, batch_size=4)
        newY = numpy.around(newY)
        N2 = int(newY)
        with open("M3/"+cc+"L"+ln+".json", "r") as f:
            model_json = f.read()
            model = model_from_json(model_json)
            model.load_weights("M3/"+cc+"L"+ln+".h2")
        newY = model.predict(result, batch_size=4)
        newY = numpy.around(newY)
        N3 = int(newY)
        if (big1.size ==0):
            small = small-1
            big = int(len(newX)-1)
        if (small1.size ==0):
            big = big+1
        result = [] 
        result.append(int((int(newX[small][1]) +int(newX[big][1]))/2))
        result.append(int((int(newX[small][2]) +int(newX[big][2]))/2))
        result.append(int((int(newX[small][4]) +int(newX[big][4]))/2))
        result.append(int((int(newX[small][1]) +int(newX[big][1]))/2))
        result.append(int((int(newX[small][2]) +int(newX[big][2]))/2))
        result.append(int((int(newX[small][4]) +int(newX[big][4]))/2))
        result = numpy.array(result)
        result = result.reshape(1,6)
        with open("M4/"+cc+"L"+ln+".json", "r") as f:
            model_json = f.read()
            model = model_from_json(model_json)
            model.load_weights("M4/"+cc+"L"+ln+".h1")
        newY = model.predict(result, batch_size=4)
        newY = numpy.around(newY)
        N4 = int(newY)

        with open("M5/"+cc+"L"+ln+".json", "r") as f:
            model_json = f.read()
            model = model_from_json(model_json)
            model.load_weights("M5/"+cc+"L"+ln+".h1")
        newY = model.predict(result, batch_size=4)
        newY = numpy.around(newY)
        N5 = int(newY)
        print ("Prediction: "+str(N1) +", " + str(N2) + ", "+ str(N3) +", " +str(N4) +", " + str(N5))
    # newY= numpy.insert(newY, 1, target, axis=1)
    # numpy.savetxt("output-NN.csv", newY, delimiter=",", fmt="%.1f")

    #print ("Prediction: "+str(N1) +", " + str(N2) + ", "+ str(N3) +", " +str(N4) +", " + str(N5))


# 5.5 Waiting List Size Training
def training(db):
    try:

        listOfCourse=db.course.aggregate([\
        { "$match": { "$or":[{"code": "COMP1942" } ,{"code":{'$regex': "^COMP42" }},{"code":{'$regex': "^COMP43" }},{"code":{'$regex': "^RMBI" }}]}},\
        { "$project": {"_id":0,"code":1,"listOfSections":1}},\
        { "$unwind": "$listOfSections"},\
        { "$match":{ "listOfSections.section":{'$regex': "^L\d" }}},\
        { "$sort":{"code":1,"listOfSections.section":1,"listOfSections.timeSlot":1}},\
        { "$group":{"_id":{"code":"$code"},"listOfSections":{"$push": "$listOfSections"}}},\
        { "$project":{"_id":0,"code":"$_id.code","listOfSections.section":1,"listOfSections.timeSlot":1,"listOfSections.quota":1,"listOfSections.avail":1,"listOfSections.enrol":1,"listOfSections.wait":1}}
        ])
        dire=os.getcwd()
        os.chdir(dire+"/timeSeries")
        for file in glob.glob("*.csv"):
            os.remove(file)

        for course in listOfCourse: 
            for i in course["listOfSections"]:   
                with open(course["code"]+i["section"]+".csv","a") as csvfile:
                    fieldnames = ['TimeSlots', 'Quota','Enrol','Avail','Wait']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   
                    writer.writerow({'TimeSlots': str(i["timeSlot"]), 'Quota': str(i["quota"]),'Enrol':str(i["enrol"]),'Avail':str(i["avail"]),'Wait':str(i["wait"])})
        

        for file in glob.glob("*.csv"):
            file= file.split(".")[0]
            print(file)
            dataset = numpy.loadtxt(file+".csv", delimiter=",",usecols=range(1, 5))
            target = numpy.loadtxt(file+".csv", delimiter=",",usecols=[4])
            dataset = dataset.astype(int)
            target = target.astype(int)
            numpy.random.seed(seed=int(time.time())+1)
            

            model = Sequential()
            model.add(Dense(4, input_dim=4, activation='relu'))
            model.add(Dense(1, activation='relu'))
            model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
            
            # Step 3: to compile the model
            print("  Step 3: to compile the model...")
            #model.compile(loss="mean_squared_error", optimizer="adam")
            
            # Step 4: To fit the model
            print("  Step 4: to fit the model...")
            model.fit(dataset, target, epochs=50, batch_size=1)
            # Step 5: To evaluate the model
            print("  Step 5: to evaluate the model...")
            trainScores = model.evaluate(dataset, target)
            print("")
            print(" Scores --- {}: {}".format(model.metrics_names[0], trainScores))
            with open("../M1/"+file+"Score.txt", "w") as f:
                f.write("{} {}".format(model.metrics_names[0], trainScores))
            model_json = model.to_json()
            with open("../M1/"+file+".json", "w") as f:
                f.write(model_json)
            model.save_weights("../M1/"+file+".h1")

        for file in glob.glob("*.csv"):
            file= file.split(".")[0]
            dataset = numpy.loadtxt(file+".csv", delimiter=",",usecols=range(1, 5))
            target = numpy.loadtxt(file+".csv", delimiter=",",usecols=[4])
            dataset = dataset.astype(int)
            target = target.astype(int)
            numpy.random.seed(seed=int(time.time())+1)
            

            model = Sequential()
            model.add(Dense(4, input_dim=4))
            model.add(Dense(5, activation='linear'))
            model.add(Dense(1, activation='relu'))
            model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])
            
            # Step 3: to compile the model
            print("  Step 3: to compile the model...")
            #model.compile(loss="mean_squared_error", optimizer="adam")
            
            # Step 4: To fit the model
            print("  Step 4: to fit the model...")
            model.fit(dataset, target, epochs=50, batch_size=10,validation_split=0.2)
            # Step 5: To evaluate the model
            print("  Step 5: to evaluate the model...")
            trainScores = model.evaluate(dataset, target)
            print("")
            print(" Scores --- {}: {}".format(model.metrics_names[0], trainScores))
            with open("../M2/"+file+"Score.txt", "w") as f:
                f.write("{} {}".format(model.metrics_names[0], trainScores))
            model_json = model.to_json()
            with open("../M2/"+file+".json", "w") as f:
                f.write(model_json)
            model.save_weights("../M2/"+file+".h2")
        for file in glob.glob("*.csv"):
            file= file.split(".")[0]
            dataset = numpy.loadtxt(file+".csv", delimiter=",",usecols=range(1, 5))
            target = numpy.loadtxt(file+".csv", delimiter=",",usecols=[4])
            dataset = dataset.astype(int)
            target = target.astype(int)
            numpy.random.seed(seed=int(time.time())+1)
            

            model = Sequential()
            model.add(Dense(4, input_dim=4,activation='linear'))
            model.add(Dense(1, activation='linear'))
            model.compile(loss="mae", optimizer="adam", metrics=["accuracy"])
            
            # Step 3: to compile the model
            print("  Step 3: to compile the model...")
            #model.compile(loss="mean_squared_error", optimizer="adam")
            
            # Step 4: To fit the model
            print("  Step 4: to fit the model...")
            model.fit(dataset, target, epochs=100, batch_size=10,validation_split=0.2)
            # Step 5: To evaluate the model
            print("  Step 5: to evaluate the model...")
            trainScores = model.evaluate(dataset, target)
            print("")
            print(" Scores --- {}: {}".format(model.metrics_names[0], trainScores))
            with open("../M3/"+file+"Score.txt", "w") as f:
                f.write("{} {}".format(model.metrics_names[0], trainScores))
            model_json = model.to_json()
            with open("../M3/"+file+".json", "w") as f:
                f.write(model_json)
            model.save_weights("../M3/"+file+".h2")


        for file in glob.glob("*.csv"):
            file= file.split(".")[0]
            print(file)
            dataset = numpy.loadtxt(file+".csv", delimiter=",",usecols=range(1, 5))
            target = numpy.loadtxt(file+".csv", delimiter=",",usecols=[4])
            dataset = dataset.astype(int)
            target = target.astype(int)
            numpy.random.seed(seed=int(time.time())+1)
            newDataset = []
            target= numpy.delete(target, len(target)-1, axis=0)
            for i in range(len(dataset)-1):
                newDataset.append([dataset[i][0],dataset[i][1],dataset[i][3],dataset[i+1][0],dataset[i+1][1],dataset[i+1][3]])
                #result = numpy.insert(result, 6, temp, axis=0)
            newDataset = numpy.array(newDataset)
            model = Sequential()
            model.add(Dense(6, input_dim=6))
            model.add(Dense(9, activation='relu'))
            model.add(Dense(1, activation='linear'))
            model.compile(loss="mae", optimizer="adam", metrics=["accuracy"])
            
            # Step 3: to compile the model
            print("  Step 3: to compile the model...")
            #model.compile(loss="mean_squared_error", optimizer="adam")
            
            # Step 4: To fit the model
            print("  Step 4: to fit the model...")
            model.fit(newDataset, target, epochs=100, batch_size=2,validation_split=0.2)
            # Step 5: To evaluate the model
            print("  Step 5: to evaluate the model...")
            trainScores = model.evaluate(newDataset, target)
            print("")
            print(" Scores --- {}: {}".format(model.metrics_names[0], trainScores))
            with open("../M4/"+file+"Score.txt", "w") as f:
                f.write("{} {}".format(model.metrics_names[0], trainScores))
            model_json = model.to_json()
            with open("../M4/"+file+".json", "w") as f:
                f.write(model_json)
            model.save_weights("../M4/"+file+".h1")

        for file in glob.glob("*.csv"):
            file= file.split(".")[0]
            print(file)
            dataset = numpy.loadtxt(file+".csv", delimiter=",",usecols=range(1, 5))
            target = numpy.loadtxt(file+".csv", delimiter=",",usecols=[4])
            dataset = dataset.astype(int)
            target = target.astype(int)
            numpy.random.seed(seed=int(time.time())+1)
            newDataset = []
            target= numpy.delete(target, 0, axis=0)
            target= numpy.delete(target, 0, axis=0)
            for i in range(len(dataset)-2):
                newDataset.append([dataset[i][0],dataset[i][1],dataset[i][3],dataset[i+1][0],dataset[i+1][1],dataset[i+1][3]])
                #result = numpy.insert(result, 6, temp, axis=0)
            newDataset = numpy.array(newDataset)
            model = Sequential()
            model.add(Dense(6, input_dim=6,activation='sigmoid'))
            model.add(Dense(12, activation='sigmoid'))
            model.add(Dense(1))
            model.compile(loss="mae", optimizer="rmsprop", metrics=["accuracy"])
            
            # Step 3: to compile the model
            print("  Step 3: to compile the model...")
            #model.compile(loss="mean_squared_error", optimizer="adam")
            
            # Step 4: To fit the model
            print("  Step 4: to fit the model...")
            model.fit(newDataset, target, epochs=200, batch_size=3,validation_split=0.2)
            # Step 5: To evaluate the model
            print("  Step 5: to evaluate the model...")
            trainScores = model.evaluate(newDataset, target)
            print("")
            print(" Scores --- {}: {}".format(model.metrics_names[0], trainScores))
            with open("../M5/"+file+"Score.txt", "w") as f:
                f.write("{} {}".format(model.metrics_names[0], trainScores))
            model_json = model.to_json()
            with open("../M5/"+file+".json", "w") as f:
                f.write(model_json)
            model.save_weights("../M5/"+file+".h1")
            os.chdir(dire)

    except pymongo.errors.ConnectionFailure as error: 
        print("Document Querying Failed! Error Message: \"{}\"".format(error))

    print ("Waiting list size training is successful")


# 5.0 to display the interface
def main():
    # here, we need to implement for the flow
    # display the menu
    try:
        print("Making a MongoDB connection...")
        client = MongoClient("mongodb://localhost:27017")
            
        # Getting a Database named "university"
        print("Getting a database named \"comp4332\"")
        db = client["comp4332"]

        choice = 0
        while (choice != "6"):
            print("")
            print("   Main Menu")
            print("=======================")
            print("1. Collection Dropping and Empty Collection Creating")
            print("2. Data Crawling")
            print("3. Course Search")
            print("4. Waiting List Size Prediction")
            print("5. Waiting List Size Training")
            print("6. Exit")
            print("")

            # allow the user to choose one of the functions in the menu
            choice = input("Please input your choice (1-6): ")

            print("")

            # check the input and call the correspondence function
            if (choice == "1"):
                dropCollection(db)
            elif (choice == "2"):
                crawlData(db)
            elif (choice == "3"):
                courseSearch(db)
            elif (choice == "4"):
                prediction()
            elif (choice == "5"):
                training(db)
            elif (choice == "6"):
                print("")
            else:
                print("Invalid Input!")

                # Closing a DB connection
        print("Closing a DB connection...") 
        client.close()
        
    except pymongo.errors.ConnectionFailure as error: 
        print("DB Connection Failed! Error Message: \"{}\"".format(error))  



main()
