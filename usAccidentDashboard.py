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
    print("\t[1] Retrieving data for a particular accident ID.")
    print("\t[2] Report new accidents: insert new accident data into database.")
    print("\t[3] Update Severity(s) of an Accident.")
    print("\t[4] Delete wrongly/falsely reported accident.")
    print("\t[q] Quit.")

    return input("What would you like to do? ")



choice = 1

while choice != 'q':

    choice = get_choice()

    if choice == '1':
        acc_ID = input("\tPlease enter Accident ID : ")
       
        print("\tAccident Details for ID = ",acc_ID)
        flag=False
        for x in mycol.find({ "ID":acc_ID} ,{"ID":1, "Start_Time": 1, "State": 1,"Zipcode":1 }):
            print("\t",x)
            flag=True
        if flag==False :
            print("DATA NOT FOUND")
       
        
    elif choice == '2':
        print("Recording new Accident ")
        #find the max id
        #record = db.usAccident.find({},{ "ID": 1}).sort({"_id": -1}).limit(1)
        #ranNum = random.random()   #random.seed(a=int)
        acc_ID = "NE" + str(random.random()*1000000)[0:6]
        state = input("\tPlease enter State : ")
        zipcode = input("\tPlease enter Zipcode : ")
        description = input("\tPlease enter Description: ")
        
        mydict = { "ID": acc_ID, "State":state,"Zipcode":zipcode,"description":description }
        x = mycol.insert_one(mydict)
        print(x.inserted_id)
        print("The following record was inserted :")
        print(mycol.find_one({ "ID":acc_ID} ,{"ID":1,"State": 1,"Zipcode":1,"description":1 }))
        
    elif choice == '3':
           acc_ID = input("\tPlease enter which Accident data to update based on accident id: ")
           x = mycol.find_one({ "ID":acc_ID} ,{"ID":1, "Severity":1, "State": 1,"Zipcode":1 })
           print("\t", x)
           print("Updating Accident DB ")
           newSeverityID=input("\tPlease enter new Severity value : ")
           
           #myquery = { "ID": acc_ID}
           newvalues = { "$set": { "Severity": newSeverityID } }
           mycol.update_one(x, newvalues)

           #print  updated data
           print(mycol.find_one({ "ID":acc_ID} ,{"ID":1, "Severity":1, "State": 1,"Zipcode":1 }))
          
    elif choice == '4':
        acc_ID = input("\tPlease enter Accident ID : ")
        print("Deleting:")
        myquery = { "ID": acc_ID}
        x = mycol.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")
        
        
    elif choice == 'q':
        print("\n Exiting! Bye!")
    else:
        print("\n Selection Invalid. Please select only from given choices.\n")
    

print("\t**********************************************")

'''
#mydb = client["ctestdb"]
#mycol = mydb["ctestcol"]
#mydict = { "name": "Charu", "address": "37S" }
#x = mycol.insert_one(mydict)
#print(x.inserted_id)

#collist = mydb.list_collection_names()

cursor = collection.find({})
for document in cursor:
  print(document)
'''

