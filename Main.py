# coding=utf-8
# The program was written by Juliana KO and Alice Chan.
# The program is used for illustrating how to write a program with stubs using the "bank" application
#
from pymongo import MongoClient
from pprint import pprint
from tabulate import tabulate

def dropCollection():
    print ("Collection dropping and empty collection creating are successful")


# 5.2 Data Crawling
def crawlData():
    data = raw_input("Please input the URL/Keywords: ")
    if (data == "default"):
        choice = "keyword"
    else:
        choice = "url"
    print ("Data Crawling is successful and all data are inserted into the database")


# 5.3.0 Print Course
# For each distinct course, show “Course Code”, “Course Title”, “No. of Units/Credits”, “Matched Time Slot”
# For the list of sections (including both lecture sections and non-lecture sections) of the course, show “Section”, “Date & Time”, “Quota”, “Enrol”, “Avail”, “Wait” and “Satisfied”

def printSection(sections, condition3):

    if condition3 == "":

        table=[]
        for section in sections:
            temp=[section["section"], section["dateTime"], section["quota"], section["enrol"], section["avail"], section["wait"]]
            table.append(temp)

        print (tabulate(table, headers={"Section":"", "Date & Time":"", "Quota":"","Enroll":"","Avail":"","Wait":""}))
        print("")

    else:
        title_list = ["Section", "Date & Time", "Quota", "Enroll", "Avail", "Wait", "Satisfied"]
        row_format = "{:>10} {:>15} {:>10} {:>10} {:>10} {:>10} {:>10} "
        print (row_format.format(title_list[0], title_list[1], title_list[2], title_list[3], title_list[4], title_list[5], title_list[6]))
        print("   ----------------------------------------------------------------------------------")
        print  (row_format.format(section[0], section[1], section[2], section[3], section[4], section[5], section[6]))


# for
def printCourse(course,condition3):

    table= [course["code"],course["ctitle"],course["credit"]]
    print (tabulate([table], headers={'Course Code':"", 'Course Title': " ","No. of Credit":""}))
    print("")

    if condition3 =="":
        print ('{:>42}'.format("Sections"))
    else:
        print ('{:>44}'.format("Matched Time Slot "))
        course[3].append("Yes")
    printSection(course["listOfSections"], condition3)


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
            listOfCourse=listCourse = db.course.aggregate([{ "$match": { "$or": query } },\
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
            {"$project":{"code":"$_id.code","ctitle":"$_id.ctitle","credit":"$_id.credit", "listOfSections":"$listOfSections","_id":0}},\
            { "$sort": { "code": 1 } }])
        
        for course in listOfCourse: 
            printCourse(course, "")

        

    except pymongo.errors.ConnectionFailure as error: 
        print("Document Querying Failed! Error Message: \"{}\"".format(error))


# 5.3.2 Course Search by Waiting List Size
# only extract course from database which statisfy the match_ts
def searchBySize():
    size = input("Please input the Maximum Waiting List Size: ")
    start_ts = input("Please input the Starting Time Slot: ")
    end_ts = input("Please input the Ending Time Slot: ")

    section = ["L1", "Tue 10:30", 40, 30, 10, 8]
    course = ("COMP4332", "Big Data Mining", 3 ,section )

    printCourse(course, size)


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
            searchBySize()
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
    N1 = 10
    N2 = 20
    N3 = 30
    N4 = 40
    N5 = 50
    print ("Prediction: "+str(N1) +", " + str(N2) + ", "+ str(N3) +", " +str(N4) +", " + str(N5))


# 5.5 Waiting List Size Training
def training():
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
                dropCollection()
            elif (choice == "2"):
                crawlData()
            elif (choice == "3"):
                courseSearch(db)
            elif (choice == "4"):
                prediction()
            elif (choice == "5"):
                training()
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
