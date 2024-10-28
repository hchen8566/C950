# Hao Chen
# Student ID: 010771133
# C950 Data Structures and Algorithms II 

import csv
import datetime
import truck
from hashPackage import HashTable
from hashPackage import Package

# reading the csv files
with open("addressCSV.csv") as file1:
    address_csv = csv.reader(file1)
    address_csv = list(address_csv)

with open("distanceCSV.csv") as file2:
    distance_csv = csv.reader(file2)
    distance_csv = list(distance_csv)

with open("packageCSV.csv") as file3:
    package_csv = csv.reader(file3)
    package_csv = list(package_csv)

# create hash table for package
hashTable_package = HashTable() 

# load the hash table
with open("packageCSV.csv") as package_file:
    package_data = csv.reader(package_file)
    for package in package_data:
        
        packageID = int(package[0])
        packageAddress = package[1]
        packageCity = package[2]
        packageState = package[3]
        packageZipcode = package[4]
        packageDeadline_time = package[5]
        packageWeight = package[6]
        packageStatus = "At the Delivery Depot"
        packageNotes = package[7]

        # turning the data into a package object 
        tempPackage = Package(packageID, packageAddress, packageCity, packageState, packageZipcode, packageDeadline_time, packageWeight, packageStatus, packageNotes)

        # inserting the package object into the hash table
        hashTable_package.insert(tempPackage)


# distance finder
def distance_calculator(position_x, position_y):
    distance_value = distance_csv[position_x][position_y]

    # flips x and y if its empty so the inverse on the csv file
    if distance_value == " ":
        distance_value = distance_csv[position_y][position_x]

    distance_value = float(distance_value)
    return distance_value

# the first truck will be responsible for the package with wrong address which will get corrected at 10:20 and remaining packaages left from second/third truck
truck_1 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# the second truck will take the packages that have to be delivered on truck 2
# the second truck will take packagaes 13, 15, 19 which have to be delivered together
# the second truck will take packages that wont arrive until 9:05
# the second truck will fill up on packages that are remaining until the load has been met
truck_2 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# the third truck will take the first 16 packages without a special note
truck_3 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))


