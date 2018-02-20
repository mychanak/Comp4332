# 5.1 Collection Dropping and Empty Collection Creating
def display_message():
    print("Collection dropping and empty colecction creating are successful")
    return


# 5.2 Data Crawling
def crawling(str):
    if str == "default":
        print("Data Crawling is successful and all data are inserted into database")
    else:
        print("Data Crawling is successful and all data are inserted into database")


# 5.3 Course Search
# 5.3.1 Course Search by Keyword
def search_by_keyword(word):
    if word == "match":
        print ("extracted from database")
        return "success"
    else:
        return


# 5.3.2 Course Search by Waiting List Size
def search_by_list_szie(num, start_ts, end_ts):
    if num == 0 and start_ts == 0 and end_ts == 0:
        print ("extracted from database")
        return "success"
    else:
        return


# 5.4 Waiting List Size Prediction
def predict(course_code, lecture_no, time_slot):
    print ("Search course that match " + course_code + ", " + str(lecture_no) + " and " + str(time_slot))
    predict_list = [0, 0, 0, 0, 0]
    return predict_list


# 5.5
def training():
    print ("Waiting list size training is successful")


# to display the interface
def main():
    # display the menu
    choice = 0
    while choice != 6:
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
        if choice == 1:
            display_message()
        elif choice == 2:
            url = raw_input("Enter a URL or 'default' for crawling: ")
            crawling(url)
        elif choice == 3:
            option = 0
            while option != 3:
                print("")
                print("   Course Search")
                print("=======================")
                print("1. Course Search by Keyword")
                print("2. Course Search by Waiting List Size")
                print("3. Exit")
                print("")

                option = input("Please input your option (1-3): ")
                if option == 1:
                    keyword = raw_input("Please input your keyword: ")
                    course_list = search_by_keyword(keyword)
                    if course_list is not None:
                        print(
                            "Course Code    Course Title    No. of Units/Credits      Section     Date & Time     "
                            "Quota   Enrol   Avail   Wait")
                    else:
                        print("No Courses Match the " + keyword)
                elif option == 2:
                    multiplier = -1
                    while multiplier < 0:
                        multiplier = input("Please input a multiplier: ")
                    start_ts = input("Please input the starting time slot: ")
                    end_ts = input("Please input the ending time slot: ")
                    course_list = search_by_list_szie(multiplier, start_ts, end_ts)
                    if course_list is not None:
                        print(
                            "Course Code    Course Title    No. of Units/Credits      Section     Date & Time     "
                            "Quota   Enrol   Avail   Wait   Satisified")
                    else:
                        print("No Courses Matches")
                elif option == 3:
                    print("")
                else:
                    print ("Invalid Input")
        elif choice == 4:
            course_code = raw_input("Please input the course code: ")
            lecture_no = input("Please input the lecture no.:")
            time_slot = input("Please input the time slot: ")
            predict_list = predict(course_code, lecture_no, time_slot)
            print ("The prediction of the course: " + str(predict_list))

        elif choice == 5:
            training()
        elif choice == 6:
            exit()
        else:
            print("Invalid Input!")


main()
