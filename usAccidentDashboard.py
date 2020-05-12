import pymongo
from pymongo import MongoClient
from pprint import pprint
import os
import random

'''
__author__ = "Charulata Lodha"
__versionPython__= 2.7
'''

client = MongoClient('mongodb://127.0.0.1:27017/')

db = client.accidentDB
mycol=db.usAccident
print(client.list_database_names())
print(mycol.name)

os.system('clear')
print("\t**********************************************")
print("\t*** US Accident Dashboard  ***")
print("\t**********************************************")

def get_choice():
# Let users know what they can do.
    print("\n\nAvailable Use-Cases : ")
    print("\t[1] Retrieving only key data (public view) for a particular accident ID.")
    print("\t[2] Report new accidents: insert new accident data into database.")
    print("\t[3] Update Severity(s) of an Accident.")
    print("\t[4] Delete wrongly/falsely reported accident.")
    print("\t[5] Retrieve number of accidents each year.")
    print("\t[6] Top 10 states with the most total accidents for a specific year or from entire data set.")
    print("\t[7] Top 10 states with the least total accidents for a specific year (or from entire data set).")
    print("\t[8] Retrieve top 8 frequent weather conditions of accidents in a particular state.")
    print("\t[9] Average severity of accident based on time of day.")
    print("\t[10] View the top zip codes with the most accidents in a specific state or in a specific city")
    print("\t[11] Accident Analysis report based on Visibility, Weather_Condition, Wind_Speed & Temperature.")
    print("\t[12] Analyse Most Accident Prone Road Type for a State")
    print("\t[13] Retrieve total accidents during the day time and night time in a particular state.")
    print("\t[14] Retrieve number of accidents corresponding to the amount of rain.")
    print("\t[15] Retrieving average severity of a city, zip code, state.")
    print("\t[16] Retrieving average length of the road extent affected by accident.")
    print("\t[17] Retrieving detailed data for a particular accident ID.")
    print("\t[q] Quit.")

    return input("What would you like to do? ")

choice = 1

while choice != 'q':
    choice = get_choice()
   
    if choice == '1':
        acc_ID = input("\tPlease enter Accident ID : ")
       
        print("\tAccident Details for ID = ",acc_ID)
        flag=False
        for x in mycol.find({ "ID":acc_ID} ,{"ID":1, "Start_Time": 1, "Severity":1, "State": 1,"Zipcode":1}):
            print("\t",x)
            flag=True
        if flag==False :
            print("DATA NOT FOUND")
       
        
    elif choice == '2':
        print("Recording new Accident ")
        #find the max id
        #record = db.usAccident.find({},{ "ID": 1}).sort({"_id": -1}).limit(1)
        #ranNum = random.random()   #random.seed(a=int)
        acc_ID = "NEW" + str(random.random()*1000000)[0:6]
        state = input("\tPlease enter State : ")
        zipcode = input("\tPlease enter Zipcode : ")
        description = input("\tPlease enter Description: ")
        
        mydict = { "ID": acc_ID, "State":state,"Zipcode":zipcode,"description":description }
        x = mycol.insert_one(mydict)
        print(x.inserted_id)
        print("The following record was inserted :")
        print(mycol.find_one({ "ID":acc_ID} ,{"ID":1,"State": 1,"Zipcode":1,"description":1 }))
        
    elif choice == '3':
           acc_ID = input("\tWhich accident's severity you want to update? Enter Accident-ID: ")
           x = mycol.find_one({ "ID":acc_ID} ,{"ID":1, "Severity":1, "State": 1,"Zipcode":1 })
           print("\t", x)
           print("Updating Accident ",acc_ID)
           newSeverityID=input("\tPlease enter the new Severity value : ")
           
           newvalues = { "$set": { "Severity": newSeverityID } }
           mycol.update_one(x, newvalues)

           #print  updated data
           print(mycol.find_one({ "ID":acc_ID} ,{"ID":1, "Severity":1, "State": 1,"Zipcode":1 }))
    
    #delete an accident record
    elif choice == '4':
        acc_ID = input("\tPlease enter Accident ID : ")
        
        myquery = { "ID": acc_ID}
        x = mycol.delete_many(myquery)
        if x.deleted_count == 0 :
            print("\t No records found");
        else:
            print(x.deleted_count, " documents deleted.")
            
    #Receive the number of accidents for each year.
    elif choice == '5':
        print("\tNumber of accidents each year: ")
        flag = False
        for x in mycol.aggregate([{"$group": {"_id": {"$arrayElemAt": [{"$split":["$Start_Time", "-"]}, 0]},"count":{"$sum": 1 }}}, {"$sort": {"_id": 1}}]):
            print("\t", x)
            flag = True
        if flag == False:
            print("DATA NOT FOUND")
    
    #Top 10 states with the most total accidents for a specific year or from entire data set.
    elif choice == '6':
           year = input("\tPlease input Year for which you want to view top 10 states : ")
           print("Top 10 States with most accidents reported in year : " +year)
           print("\t States | Frequency of Accident")
           
           colNameStr = 'TotalAccident' + year
           colName = db[colNameStr]
           for x in colName.find().sort([("value",-1)]).limit(10) :
                print("\t",x)
      
    
    #Top 10 states with least total accidents for a specific year or from entire data set.
    elif choice == '7':
         year = input("\tPlease input Year for which you want to view bottom 10 states : ")
         print("Top 10 States with least accidents reported in year : " +year)
         print("\t States | Frequency of Accident")
         
         colNameStr = 'TotalAccident' + year
         colName = db[colNameStr]
         for x in colName.find().sort([("value", 1)]).limit(10) :
              print("\t",x)
              
    #View the top 8 frequent weather conditions in which accidents most occur of a specific state.
    elif choice == '8':
           state = input("\tPlease enter state : ")
           print("\tTop 8 frequent weather conditions of accidents in " + state + ':')
           flag = False
           for x in mycol.aggregate([{"$group": {"_id": {"Weather":"$Weather_Condition", "State":state}, "count": {"$sum":1}}},{"$sort": {"count":-1}},{"$limit": 8}]):
               print("\t", x)
               flag = True
           if flag == False:
               print("DATA NOT FOUND")
   
    #Average severity of accident based on time of day.
    elif choice == '9':
           time = input("\tPlease enter time of the day (0->23) : ")
           while int(time) < 0 or int(time) > 23:
               time = input("\tPlease enter time of the day (0->23) : ")
           if int(time) <=9:
               time_regex = ' 0'+time+':'
           else:
               time_regex = ' '+time +':'
           
           print("\tAverage severity level of accidents from timestamp ",
                 time,":00 to ", time , ":59")
           flag = False
           pipeline = [ {"$match":{"Start_Time":{"$regex": time_regex}}},
                        {"$group":
                             {"_id": "null",
                             "Average_Severity":{"$avg": "$Severity"}}
                        }]
           
           for x in mycol.aggregate(pipeline):
               print("\t", x)
               flag = True
           if flag == False:
               print("DATA NOT FOUND")

    #View the top zip codes with the most accidents in a specific state or in a specific city
    elif choice == '10':
           print("1. Retrieve top zip codes with the most accidents in a specific state")
           print("2. Retrieve top zip codes with the most accidents in a specific city")
           option = input("\tPlease enter a choice : ")
           flag = False

           if option == "1":
               state = input("\tPlease enter the state: ")
               amount = int(input("\tPlease enter the amount of zip codes to view: "))
               for x in mycol.aggregate([{"$match":{"State":state}},{"$group": {"_id": {"City":"$City", "Zipcode":"$Zipcode"}, "count": {"$sum":1}}},{"$sort": {"count":-1}},{"$limit":amount}]):
                   print("\t", x)
                   flag = True
           elif option == "2":
               state = input("\tPlease enter the state: ")
               city = input("\tPlease enter the city: ")
               amount = int(input("\tPlease enter the amount of zip codes to view: "))
               for x in mycol.aggregate([{"$match":{"State":state, "City":city}},{"$group": {"_id": {"Zipcode":"$Zipcode"}, "count": {"$sum":1}}},{"$sort": {"count":-1}},{"$limit":amount}]):
                   print("\t", x)
                   flag = True

           if flag == False:
               print("DATA NOT FOUND")

    #Accident Analysis report based on Visibility, Weather_Condition, Wind_Speed & Temperature.
    elif choice == '11':
           print("\t[1] The average visibility in miles when accidents occur by states.")
           print("\t[2] The average wind speed in mph when accidents occur by states.")
           print("\t[3] The average temperature in Fahrenheit when "
                 "accidents occur by states.")
           print("\t[4] The most common weather condition when accidents occur by states.")
           condition = input("\tPlease enter your choice : ")
           while condition not in ['1','2','3','4']:
               print(
                   "\n Selection Invalid. Please select only from given choices.\n")
               print(
                   "\t[1] The average visibility in miles when accidents occur by states.")
               print(
                   "\t[2] The average wind speed in mph when accidents occur by states.")
               print("\t[3] The average temperature in Fahrenheit when "
                     "accidents occur by states.")
               print(
                   "\t[4] The most common weather condition when accidents occur by states.")
               condition = input("\tPlease enter your choice : ")

           if condition == '1':
               pipeline = [{"$group":
                                {"_id": {"State": "$State"},
                                 "Average_Visibility": { "$avg": "$Visibility(mi)" }}
                            },
                            {"$sort": {"_id":1}}]
               print("\tAverage visibility in miles by state: ")
               flag = False
               for x in mycol.aggregate(pipeline):
                   print("\t", x)
                   flag = True
               if flag == False:
                   print("DATA NOT FOUND")
           elif condition == '2':
               pipeline = [{"$group":
                                {"_id": {"State": "$State"},
                                 "Average_Wind_Speed": { "$avg": "$Wind_Speed("
                                                                 "mph)" }}
                            },
                           {"$sort": {"_id":1}}]
               print("\tAverage Wind_Speed in Fahrenheit by state: ")
               flag = False
               for x in mycol.aggregate(pipeline):
                   print("\t", x)
                   flag = True
               if flag == False:
                   print("DATA NOT FOUND")
           elif condition == '3':
               pipeline = [{"$group":
                                {"_id": {"State": "$State"},
                                 "Average_Temperature": { "$avg": "$Temperature(F)" }}
                            },
                           {"$sort": {"_id":1}}]
               print("\tAverage temperature in Fahrenheit by state: ")
               flag = False
               for x in mycol.aggregate(pipeline):
                   print("\t", x)
                   flag = True
               if flag == False:
                   print("DATA NOT FOUND")
           elif condition == '4':
               pipeline = [
                   { "$group":
                       {
                       "_id": {"State": "$State", "Weather_Condition": "$Weather_Condition"},
                       "count": { "$sum": 1 },
                       }
                   },
                   { "$sort": { "count": -1 } },
                   { "$group":
                       {
                           "_id" : "$_id.State",
                           "mostWeather":  { "$first": "$_id.Weather_Condition" },
                       }
                   },
                   { "$sort": {"_id" : 1}},
                   { "$project":
                       { "_id": 0,
                           "state": "$_id",
                           "mostWeather":  { "name": "$mostWeather"}
                       }
                   }
                   ]
               print("\tMost common weather condition when accidents occur by "
                     "state: ")
               flag = False
               for x in mycol.aggregate(pipeline):
                   print("\t", x)
                   flag = True
               if flag == False:
                   print("DATA NOT FOUND")
    
    #Find the count of accidents reflecting most accident prone road type for a State
    elif choice == '12':
        state = input("\tPlease enter state : ")
        print("\t Road Types most prone to accidents in " + state + ':')
        
        print('\tCrossing =',db.usAccident.count_documents( { "$and" : [{"State":state},{"Crossing": "True"}] } ) )
        print('\tStop = ', db.usAccident.count_documents( { "$and" : [{"State":state},{"Stop": "True"}] } ) )
        print('\tTraffic_Signal = ', db.usAccident.count_documents( { "$and" : [{"State":state},{"Traffic_Signal": "True"}] } ) )
        print('\tTurning_Loop = ',db.usAccident.count_documents( { "$and" : [{"State":state},{"Traffic_Signal": "True"}] } ) )
        print('\tRoundabout = ',db.usAccident.count_documents( { "$and" : [{"State":state},{"Roundabout": "True"}] } ) )
        print('\tCrossing = ', db.usAccident.count_documents( { "$and" : [{"State":state},{"Crossing": "True"}] } ) )
        print('\tBump = ', db.usAccident.count_documents( { "$and" : [{"State":state},{"Bump": "True"}] } ) )
        print('\tJunction = ', db.usAccident.count_documents( { "$and" : [{"State":state},{"Junction": "True"}] } ) )

        
        
    #Receive the total number of accidents within a particular state during the day and night time using the entire dataset.
    elif choice == '13':
       state = input("\tPlease enter state : ")
       print("\tTotal accidents during the day time and night time in " + state + ':')
       flag = False
       for x in mycol.aggregate([{"$group": {"_id": {"DayOrNight":"$Sunrise_Sunset", "State":state}, "count": {"$sum":1}}},{"$sort": {"count":-1}},{"$limit": 2}]):
           print("\t", x)
           flag = True
       if flag == False:
           print("DATA NOT FOUND")

    #Receive the number of accidents for each rain amount to draw a correlation between the two.
    elif choice == '14':
       print("\tNumber of accidents corresponding to the amount of rain: ")
       flag = False
       for x in mycol.aggregate([{"$group": {"_id":"$Precipitation(in)", "count": {"$sum":1}}},{"$sort":{"_id": 1}},{"$limit":20}]):
           print("\t", x)
           flag = True
       if flag == False:
           print("DATA NOT FOUND")
   
    #Retrieving average severity of a city, zip code, state
    elif choice == '15':
       print(
           "\t[1] The average severity of accident in each state.")
       print(
           "\t[2] The average severity of accident in each city.")
       print("\t[3] The average severity of accident in each zip code.")
       condition = input("\tPlease enter your choice : ")
       while condition not in ['1', '2', '3']:
           print(
               "\n Selection Invalid. Please select only from given choices.\n")
           print(
               "\t[1] The average severity of accident in each state.")
           print(
               "\t[2] The average severity of accident in each city.")
           print("\t[3] The average severity of accident in each zip code.")
           condition = input("\tPlease enter your choice : ")
       if condition == '1':
           pipeline = [{ "$group":
                             { "_id": {"State": "$State"},
                               "Average_Severity": { "$avg": "$Severity" } } },
                       {"$sort": {"_id":1}}
                       ]
           print("\tAverage severity of accident in each state: ")
           flag = False
           for x in mycol.aggregate(pipeline):
               print("\t", x)
               flag = True
           if flag == False:
               print("DATA NOT FOUND")
       elif condition == '2':
           state = input("\tPlease enter state of choice : ")
           pipeline = [ {"$match": {"State": state}},
                        {"$group":
                            {"_id": {"City": "$City",
                             "State": "$State"},
                             "Average_Severity": {"$avg": "$Severity"}}},
                        {"$sort": {"_id":1}}
                       ]
           print("\tAverage severity of accident in each city: ")
           flag = False
           for x in mycol.aggregate(pipeline):
               print("\t", x)
               flag = True
           if flag == False:
               print("DATA NOT FOUND")
       elif condition == '3':
           state = input("\tPlease enter state of choice : ")
           city = input("\tPlease enter city of choice : ")
           pipeline = [
                       {"$match": {"State": state, "City": city}},
                       {"$group":
                            {"_id": {"Zipcode": "$Zipcode","City": "$City",
                             "State": "$State"},
                             "Average_Severity": {"$avg": "$Severity"}}},
                       {"$sort": {"_id":1}}
                       ]
           print("\tAverage severity of accident in each zip code: ")
           flag = False
           for x in mycol.aggregate(pipeline):
               print("\t", x)
               flag = True
           if flag == False:
               print("DATA NOT FOUND")
   
    #Retrieving average length of the road extent affected
    elif choice == '16':
       print("\tAverage length of the road extent affected by the "
             "accident in each state: ")
       flag = False
       pipeline = [
                   {
                   "$group": { "_id": {"State": "$State"},
                               "Average_Distance": { "$avg": "$Distance(mi)" } }
                   },
                   {"$sort": {"_id":1}}
                   ]
       for x in mycol.aggregate(pipeline):
           print("\t", x)
           flag = True
       if flag == False:
           print("DATA NOT FOUND")
   
   
    #get complete details about an accident
    elif choice == '17':
          acc_ID = input("\tPlease enter Accident ID : ")
             
          print("\n\tComplete Accident Details for Accidnet Number = ",acc_ID)
          flag=False
          for x in mycol.find({ "ID":acc_ID},{"_id":0 }):   #// to hide Object ID
              flag=True
              for i in x :
                print("\t", i, x[i])
          if flag==False :
              print("DATA NOT FOUND")
    
    elif choice == 'q':
        print("\n Exiting! Bye!")
    

    else:
        print("\n Selection Invalid. Please select only from given choices.\n")
    print("\t*************************************************************************************************")


