#!/usr/bin/python
#
#  The program was written by Juliana KO.
#  The program is used for illustrating how to write a program with stubs using the "bank" application
#

# 5.1 Collection Dropping And Empty Collection Creating
def dropCollection():
        print ("Collection dropping and empty collection creating are successful")

#5.2 Data Crawling
def crawlData():
        data = input("Please input the URL/Keywords: ")
        if (data == "default"):
                choice = "keyword"
        else:
                choice = "url"
        print ("Data Crawling is successful and all data are inserted into the database")


#5.3.0 Print Course
# For each distinct course, show “Course Code”, “Course Title”, “No. of Units/Credits”, “Matched Time Slot”
# For the list of sections (including both lecture sections and non-lecture sections) of the course, show “Section”, “Date & Time”, “Quota”, “Enrol”, “Avail”, “Wait” and “Satisfied”
# Condition 1 is for display "Matched Time Slot" in course, only needed for 5.3.2
# Condition 2 is for display "Satisfied" in section, only needed for 5.3.2

def printSection (section, condition2):
        print ("Section: ", section[0])
        print ("Date & Time: ", section[1])
        print ("Quota: ", section[2])
        print ("Enroll: ", section[3])
        print ("Avail: ", section[4])
        print ("Wait: ", section[5])
        if (condition2 != ""):
                print ("Satisfied: ", condition2)
        print ("")


def printCourse (course, condition1, condition2):
        print ("Course Code: ", course[0])
        print ("Course Title: ", course[1])
        print ("No. of Units/Credits: ", course[2], "credits")
        if (condition1 != ""):
                print ("Matched Time Slot", condition1)
        print ("")

        section = ("L1", "Tue 10:30", 40, 30, 10, 8)
        printSection (section, condition2)


#5.3.1 Course Search by Keyword
def searchByKeyword():
        keywords = input("Please input the Keyword(s): ")

        course = ("COMP4332", "Big Data Mining", 3, "Satisfied")
        printCourse(course, "", "") 


#5.3.2 Course Search by Waiting List Size
def searchBySize():
        size = input("Please input the Maximum Waiting List Size: ")
        start_ts = input("Please input the Starting Time Slot: ")
        end_ts = input("Please input the Ending Time Slot: ")

        course = ("COMP4332", "Big Data Mining", 3, "Satisfied")
        printCourse(course, "10:30", "Yes") 


# 5.3 Course Search
def courseSearch():
        choice3 = "0"
        while (choice3 != "3"):
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
                        searchByKeyword()
                elif (choice3 == "2"):
                        searchBySize()
                elif (choice3 == "3"):
                        print("")
                else:
                        print("Invalid Input!")

#5.4 Waiting List Size Prediction
def prediction():
        cc = input("Please input the Course Code: ")
        ln = input("Please input the Lecture Number (e.g. the input should be “1” denoting “L1”): ")
        ts = input("Please input the Time Slot: ")
        N1 = 10
        N2 = 20
        N3 = 30
        N4 = 40
        N5 = 50
        print (N1, ", ", N2, ", ", N3, ", ", N4, ", ", N5)


#5.5 Waiting List Size Training
def training():
        print ("Waiting list size training is successful")


# 5.0 to display the bank interface
def main():

        # here, we need to implement for the flow
        # display the menu
        choice = "0"
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
                        courseSearch()
                elif (choice == "4"):
                        prediction()
                elif (choice == "5"):
                        training()
                elif (choice == "6"):
                        print("")
                else:
                        print("Invalid Input!")

main()
