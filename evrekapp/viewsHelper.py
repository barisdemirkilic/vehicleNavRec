from django.db import connection

from .models import Vehicle, NavigationRecord
from random import randint, uniform
from string import ascii_uppercase

import datetime
import json


class LastPointsPerVehicle:
    def __init__(self, plate, latitude, longitude, datetime):
        self.plate = plate
        self.latitude = latitude
        self.longitude = longitude
        self.datetime = datetime

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        '''
        if isinstance(obj, Decimal):
            return float(obj)
        '''
        return obj.__dict__

def getLastPointsPerVehicleHelper():
    sqlQuery = "select plate, latitude, longitude, datetime" \
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

def generateRandomDatetime():
    randYear = randint(1990, 2021)
    randMonth = randint(1, 12)
    randDay = randint(1, 28) # For the 29th, 30th, 31st day need to check month
    randHour = randint(0, 23)
    randMin = randint(0, 59)
    #randSec = randint(0, 59)
    return datetime.datetime(randYear, randMonth, randDay, randHour, randMin)

def addRandomDataHelper(vehicleCount, navRecCount):
    newAddedVehicleIDList = []
    for i in range(vehicleCount):
        curPlate = generateRandomPlateNo()
        newVehicle = Vehicle(plate = curPlate)
        newVehicle.save()
        newAddedVehicleIDList.append(newVehicle.id)
    vehicleIDListLen = len(newAddedVehicleIDList)
    for i in range(navRecCount):
        curVehicleIDIdx = randint(0, vehicleIDListLen - 1)
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
    cursor = connection.cursor()
    cursor.execute("select id from evrekapp_vehicle where plate = %s", [plate])
    queryResTuple = cursor.fetchone()
    newNavRec = NavigationRecord(vehicle_id = queryResTuple[0], \
    latitude = latitude, longitude = longitude, datetime = datetime)
    newNavRec.save()

def clearDatabaseHelper():
    cursor = connection.cursor()
    cursor.execute("delete from evrekapp_navigationrecord")
    cursor.execute("delete from evrekapp_vehicle")
    cursor.execute("alter table evrekapp_navigationrecord auto_increment = 1")
    cursor.execute("alter table evrekapp_vehicle auto_increment = 1")
