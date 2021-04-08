from django.db import connection
from django.utils import timezone

from .models import Vehicle, NavigationRecord, \
Bin, Operation, BinOperation

from datetime import datetime
from random import randint, uniform
from string import ascii_uppercase

import json

class LastPointsPerVehicle:
    def __init__(self, latitude, longitude, plate, datetime):
        self.latitude = latitude
        self.longitude = longitude
        self.plate = plate
        self.datetime = datetime

# This class is defined to ensure objects can be saved as JSON
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        '''
        if isinstance(obj, Decimal):
            return float(obj)
        '''
        return obj.__dict__

# Get the last (last 48 hours) points per vehicle and save it as JSON file
# Currently if a future date is present in navigation records it will be counted as well
# This can easily be fixed by adding less than check with respect to timezone.now()
# Or not allowing future datetime to be an input
def getLastPointsPerVehicleHelper():
    queryResSet = NavigationRecord.objects.select_related("vehicle").filter(datetime__gt = timezone.now() - timezone.timedelta(hours=48))
    #print(str(deneme.query)) # To check what query is being done
    lastPointsPerVehicleList = []
    for navRecObj in queryResSet:
        curLatitude = navRecObj.latitude
        curLongitude = navRecObj.longitude
        curPlate = navRecObj.vehicle.plate
        curDatetime = navRecObj.datetime
        curLastPointsPerVehicle = LastPointsPerVehicle(curLatitude, curLongitude, curPlate, curDatetime)
        lastPointsPerVehicleList.append(curLastPointsPerVehicle)
    jsonFilePath = "evrekapp/jsonFiles/LastPointsPerVehicle.json"
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
        json.dump(lastPointsPerVehicleList, jsonFile, ensure_ascii=False, indent=4, cls=JsonEncoder)

    # With Raw SQL (MySQL)
    '''
    sqlQuery = "select latitude, longitude, plate, datetime" \
    " from (evrekapp_navigationrecord inner join evrekapp_vehicle on" \
    " evrekapp_vehicle.id = evrekapp_navigationrecord.vehicle_id)" \
    " where datetime > date_sub(now(), interval 48 hour)"
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    queryResList = cursor.fetchall()
    lastPointsPerVehicleList = []
    for row in queryResList:
        curLastPointsPerVehicle = LastPointsPerVehicle(row[0], row[1], row[2], row[3])
        lastPointsPerVehicleList.append(curLastPointsPerVehicle)
    jsonFilePath = "evrekapp/jsonFiles/LastPointsPerVehicle.json"
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
        json.dump(lastPointsPerVehicleList, jsonFile, ensure_ascii=False, indent=4, cls=JsonEncoder)
    '''

# Generate random plate number according to the Turkish plate number regulations
def generateRandomPlateNo():
    plateStr = ""
    cityNo = randint(1, 81) # Maximum Turkish plate city number is 81
    if cityNo // 10 == 0: # 1 digit (True div = Integer division is used)
        plateStr += "0"
    plateStr += str(cityNo)
    plateStr += " "
    letterCount = randint(1, 3)
    uppercaseAsciiLen = len(ascii_uppercase)
    for i in range(letterCount):
        randAsciiIdx = randint(0, uppercaseAsciiLen - 1)
        plateStr += ascii_uppercase[randAsciiIdx]
    plateStr += " "
    letterPlusLastNo = randint(5, 6)
    lastNoCount = letterPlusLastNo - letterCount
    for i in range(lastNoCount):
        curLastNoDigit = randint(0, 9)
        plateStr += str(curLastNoDigit)
    return plateStr

# Generating random datetime objects
# Didn't implement it fully (Month-days need a fix)
# Future dates may be disabled but for now I allowed it
def generateRandomDatetime():
    randYear = randint(1990, 2021)
    randMonth = randint(1, 12)
    randDay = randint(1, 28) # For the 29th, 30th, 31st day need to check month
    randHour = randint(0, 23)
    randMin = randint(0, 59)
    #randSec = randint(0, 59)
    return datetime(randYear, randMonth, randDay, randHour, randMin)

def addFirstRandomDataHelper(vehicleCount, navRecCount):
    newAddedVehicleIDList = []

    for i in range(vehicleCount):
        curPlate = generateRandomPlateNo()
        newVehicle = Vehicle(plate = curPlate)
        newVehicle.save()
        newAddedVehicleIDList.append(newVehicle.id)

    # Add navigation records to vehicles that are added just now
    for i in range(navRecCount):
        curVehicleIDIdx = randint(0, vehicleCount - 1)
        curVehicleID = newAddedVehicleIDList[curVehicleIDIdx]
        curLatitude = uniform(-90.0, 90.0)
        curLongitude = uniform(-180.0, 180.0)
        curDatetime = generateRandomDatetime()
        newNavRec = NavigationRecord(vehicle_id = curVehicleID, \
        latitude = curLatitude, longitude = curLongitude, datetime = curDatetime)
        newNavRec.save()

def addCustomVehicleDataHelper(plate):
    newVehicle = Vehicle(plate = plate)
    newVehicle.save()

def addCustomNavRecDataHelper(plate, latitude, longitude, datetime):
    try:
        vehicleObj = Vehicle.objects.get(plate = plate)
    except:
        print("\nVehicle object with this plate doesn't exist\n")
        return
    newNavRec = NavigationRecord(vehicle_id = vehicleObj.id, \
    latitude = latitude, longitude = longitude, datetime = datetime)
    newNavRec.save()

    # With Raw SQL query (MySQL)
    '''
    cursor = connection.cursor()
    cursor.execute("select id from evrekapp_vehicle where plate = %s", [plate])
    queryResTuple = cursor.fetchone()
    newNavRec = NavigationRecord(vehicle_id = queryResTuple[0], \
    latitude = latitude, longitude = longitude, datetime = datetime)
    newNavRec.save()
    '''

# Truncate tables related to the first assignment
def clearFirstDatabaseHelper():
    # Couldn't find how to reset auto_increment PK within this code
    '''
    NavigationRecord.objects.all().delete()
    Vehicle.objects.all().delete()
    '''

    # With Raw SQL (MySQL)
    cursor = connection.cursor()

    # First delete the dependent tables (Tables with foreign keys)
    cursor.execute("delete from evrekapp_navigationrecord")
    cursor.execute("delete from evrekapp_vehicle")

    # Reset auto_increment value to 1, otherwise IDs keep increasing
    cursor.execute("alter table evrekapp_navigationrecord auto_increment = 1")
    cursor.execute("alter table evrekapp_vehicle auto_increment = 1")

def addSecondRandomDataHelper(binCount, operationCount, binOperationCount):
    newAddedBinIDList = []
    for i in range(binCount):
        curLatitude = uniform(-90.0, 90.0)
        curLongitude = uniform(-180.0, 180.0)
        newBin = Bin(latitude = curLatitude, longitude = curLongitude)
        newBin.save()
        newAddedBinIDList.append(newBin.id)
    newAddedOperationIDList = []
    for i in range(operationCount):
        randOpNameIdx = randint(1, 50)
        randOperationName = "RandOpName" + str(randOpNameIdx)
        newOperation = Operation(name = randOperationName)
        newOperation.save()
        newAddedOperationIDList.append(newOperation.id)
    maxAvailableIDPairCount = min(binOperationCount, binCount * operationCount)
    for i in range(binCount):
        curBinID = newAddedBinIDList[i]
        bMaxedUniqueConstraint = False
        for j in range(operationCount):
            if i*operationCount + j >= maxAvailableIDPairCount:
                print("\nNo more unique pair id for bin and operation can be created.\n")
                bMaxedUniqueConstraint = True
                break
            curOpID = newAddedOperationIDList[j]
            curCollectionFreq = randint(0, 100)
            curLastCollection = generateRandomDatetime()
            newBinOperation = BinOperation(bin_id = curBinID, operation_id = curOpID, \
            collection_frequency = curCollectionFreq, last_collection = curLastCollection)
            newBinOperation.save()
        if bMaxedUniqueConstraint:
            break

    #This random ID assignment can break UniqueConstraint
    '''
    for i in range(binOperationCount):
        curBinIDIdx = randint(0, binCount - 1)
        curBinID = newAddedBinIDList[curBinIDIdx]
        curOpIDIdx = randint(0, operationCount - 1)
        curOpID = newAddedOperationIDList[curOpIDIdx]

        curCollectionFreq = randint(0, 100)
        curLastCollection = generateRandomDatetime()
        newBinOperation = BinOperation(bin_id = curBinID, operation_id = curOpID, \
        collection_frequency = curCollectionFreq, last_collection = curLastCollection)
        newBinOperation.save()
    '''

def addCustomBinDataHelper(latitude, longitude):
    newBin = Bin(latitude = latitude, longitude = longitude)
    newBin.save()

def addCustomOperationDataHelper(opName):
    newOperation = Operation(name = opName)
    newOperation.save()

def addCustomBinOperationDataHelper(binID, opID, collectionFreq, lastCollection):
    try:
        binObj = Bin.objects.get(id = binID)
    except:
        print("\nBin object with this binID doesn't exist\n")
        return
    try:
        opObj = Operation.objects.get(id = opID)
    except:
        print("\nOperation object with this operationID doesn't exist\n")
        return
    try:
        binOpObj = BinOperation.objects.get(bin_id = binID, operation_id = opID)
    except:
        pass # Bin operation object can be created without a problem
    else:
        print("\nBin-Operation object with these given binID and operationID pair exists already\n")
        return
    newBinOperation = BinOperation(bin_id = binID, operation_id = opID, \
    collection_frequency = collectionFreq, last_collection = lastCollection)
    newBinOperation.save()

def getCollectionFrequencyHelper():
    collectionFreqList = [obj.collection_frequency for obj in BinOperation.objects.all()]
    jsonFilePath = "evrekapp/jsonFiles/CollectionFrequencyList.json"
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
        json.dump(collectionFreqList, jsonFile, ensure_ascii=False, indent=4, cls=JsonEncoder)

# Truncate tables related to the second assignment
def clearSecondDatabaseHelper():
    # Couldn't find how to reset auto_increment PK within this code
    '''
    BinOperation.objects.all().delete()
    Operation.objects.all().delete()
    Bin.objects.all().delete()
    '''

    # With Raw SQL (MySQL)
    cursor = connection.cursor()

    # First delete the dependent tables (Tables with foreign keys)
    cursor.execute("delete from evrekapp_binoperation")
    cursor.execute("delete from evrekapp_operation")
    cursor.execute("delete from evrekapp_bin")

    # Reset auto_increment value to 1, otherwise IDs keep increasing
    cursor.execute("alter table evrekapp_binoperation auto_increment = 1")
    cursor.execute("alter table evrekapp_operation auto_increment = 1")
    cursor.execute("alter table evrekapp_bin auto_increment = 1")
