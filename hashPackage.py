import datetime

# Custom class package
class Package:
    def __init__(self, package_id, street, city, state, zip_code, deadline, weight, status, notes=None):
        self.package_id = package_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None
        self.deliveryTime = None
    
    def summary(self):
        print(f"ID: {self.package_id}, Address: {self.street}, {self.city}, {self.state} {self.zip_code}, Depart Time: {self.departureTime}, Delivery Time: {self.deliveryTime}, Status: {self.status}")

    def __repr__(self):
        return (f"Package: ({self.package_id}, {self.street}, {self.city}, {self.state}, "
                f"{self.zip_code}, {self.deadline}, {self.weight}, {self.notes})")
    
    def status_update(self, a_timedelta) :
        if self.deliveryTime == None:
            self.status = "At the hub"
        elif a_timedelta < self.departureTime:
            self.status = "At the hub"   
        elif a_timedelta < self.deliveryTime:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        
        # specific outlier edge case code for the one package that has the wrong address
        if self.package_id == 9:         
            if a_timedelta > datetime.timedelta(hours=10, minutes=10):
                self.street = "410 S State St"  
                self.zip = "84111"  
            else:
                self.street = "300 State St"
                self.zip = "84103"  


# Custom class hash table
class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for _ in range(size)]  # Array of lists to handle collisions

    def _hash(self, key):
        # hash function base on size of table
        return key % self.size

    # insert function
    def insert(self, package):
        # index from the hash function
        index = self._hash(package.package_id)
        
        # insert package at index 
        for i, item in enumerate(self.table[index]):
            # if package id already exists then this will update it
            if item.package_id == package.package_id:
                self.table[index][i] = package 
                return

        # if package id does not exist then add a new package
        self.table[index].append(package)

    # get function
    def get(self, package_id):
        # Compute the index using the hash function
        index = self._hash(package_id)
        
        # Search for the package in the list at the computed index
        for package in self.table[index]:
            if package.package_id == package_id:
                return package
        return None  # Return None if the package is not found
    
    # look up search function
    def lookup_package(self, package_id):
        package = self.get(package_id)
        if package:
            return package
            
        else:
            print(f"Package ID {package_id} not found.")
            return None
    
    # remove item from hash table function
    def remove(self, package_id):
        # compute the hash using package id
        index = self._hash(package_id)
        
        # search for the package in the list and remove it
        for i, package in enumerate(self.table[index]):
            if package.package_id == package_id:
                del self.table[index][i]
                print(f"Package ID {package_id} has been removed.")
                return True
        # if package not found
        print(f"Package ID {package_id} not found.")
        return False 

    def __repr__(self):
        return "\n".join(f"Index {i}: {bucket}" for i, bucket in enumerate(self.table))