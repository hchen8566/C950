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
    if distance_value == "":
        distance_value = distance_csv[position_y][position_x]
        
    distance_value = float(distance_value)
    return distance_value

# the first truck will be responsible for the package with wrong address which will get corrected at 10:20 and remaining packaages left from second/third truck
truck_1 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# the second truck will take the packages that have to be delivered on truck 2
# the second truck will take packages that wont arrive until 9:05
# the second truck will fill up on packages that are remaining until the load has been met
truck_2 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# the third truck will take packages 13, 15, 19, 14, 16, 20 which have to be delivered together
# the third truck will then take packages without special notes until it has reached 16 packages
truck_3 = truck.Truck(16, 18, None, None, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))

# loading truck 3 first (highlighted in green in the xlsx document)
truck_3.packages = [15, 13, 14, 19, 16, 20, 1, 2, 4, 5, 7, 8, 10, 11, 12, 17]

# loading truck 2 (highlighted in yellow in the xlsx document)
truck_2.packages = [3, 6, 18, 25, 28, 32, 36, 38, 21, 22, 23, 24, 26, 27]

# loading truck 1 (highlighted in blue in the xlsx document)
truck_1.packages = [9, 29, 30, 31, 33, 34, 35, 37, 39, 40]

# function to get the address id of an address from addressCSV.csv (this will be used when using the table to find distance)
def get_address_int(address):
    for row in address_csv:
        if address in row[2]:
            x = row[0]
            return int(x)
        


# delivery algorithm
def package_delivery(truck):

    # make a list of packages that are not delivered
    unfinished_delivery = []
    # load it with the trucks packages
    for x in truck.packages:
            package = hashTable_package.lookup_package(x)
            unfinished_delivery.append(package)

    truck.packages.clear()

    # loops until unfinished_delivery is empty
    while unfinished_delivery:
        # variable for temp address and temp mileage
        target_address = None
        target_distance = 100000
        tempPackage = None

        for package in unfinished_delivery:
            if (distance_calculator(get_address_int(truck.address), get_address_int(package.street)) <= target_distance):
                
                target_distance = distance_calculator(get_address_int(truck.address), get_address_int(package.street))
                
                target_address = package.street
              
                tempPackage = package
        
        #print(tempPackage)
        truck.mileage = truck.mileage + target_distance
        #print("Mileage: ", truck.mileage)
        truck.address = target_address
        #print("Current Address: ", truck.address)
        truck.time = truck.time + datetime.timedelta(hours = target_distance / 18)
        
        unfinished_delivery.remove(tempPackage)
        #print("NEW LIST", unfinished_delivery)
        #print("Target Distance", target_distance)
        tempPackage.deliveryTime = truck.time
        tempPackage.departureTime = truck.time
        truck.packages.append(tempPackage.package_id)


# send trucks 3 and 2 out first to deliver packages
package_delivery(truck_3)
package_delivery(truck_2)

# whichever truck comes back first, truck 1 will then go out
if (truck_2.time > truck_3.time):
    truck_1.depart_time = truck_3.time
else :
    truck_1.depart_time = truck_2.time