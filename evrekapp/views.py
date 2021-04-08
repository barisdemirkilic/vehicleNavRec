from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from datetime import datetime

from .viewsHelper import getLastPointsPerVehicleHelper, \
addFirstRandomDataHelper, clearFirstDatabaseHelper, \
addCustomVehicleDataHelper, addCustomNavRecDataHelper, \
addCustomBinDataHelper, addCustomOperationDataHelper, \
addCustomBinOperationDataHelper, addSecondRandomDataHelper, \
getCollectionFrequencyHelper, clearSecondDatabaseHelper

class IndexView(generic.TemplateView):
    template_name = "evrekapp/index.html"

class FirstAssignmentView(generic.TemplateView):
    template_name = "evrekapp/firstAssignment.html"

class SecondAssignmentView(generic.TemplateView):
    template_name = "evrekapp/secondAssignment.html"

def getLastPointsPerVehicle(request):
    getLastPointsPerVehicleHelper()
    return HttpResponseRedirect(reverse('evrekapp:firstAssignment'))

def addFirstRandomData(request):
    vehicleCount = int(request.POST["vehicleCount"])
    navRecCount = int(request.POST["navRecCount"])
    addFirstRandomDataHelper(vehicleCount, navRecCount)
    return HttpResponseRedirect(reverse('evrekapp:firstAssignment'))

def addCustomVehicleData(request):
    plate = str(request.POST["plate"])
    addCustomVehicleDataHelper(plate)
    return HttpResponseRedirect(reverse('evrekapp:firstAssignment'))

def addCustomNavRecData(request):
    plate = str(request.POST["plateNav"])
    latitude = float(request.POST["latitude"])
    longitude = float(request.POST["longitude"])
    dateReq = request.POST["datetime"]
    datetimeObj = datetime.strptime(dateReq, "%Y-%m-%dT%H:%M")
    addCustomNavRecDataHelper(plate, latitude, longitude, datetimeObj)
    return HttpResponseRedirect(reverse('evrekapp:firstAssignment'))

def clearFirstDatabase(request):
    clearFirstDatabaseHelper()
    return HttpResponseRedirect(reverse('evrekapp:firstAssignment'))

def addSecondRandomData(request):
    binCount = int(request.POST["binCount"])
    operationCount = int(request.POST["operationCount"])
    binOperationCount = int(request.POST["binOperationCount"])
    addSecondRandomDataHelper(binCount, operationCount, binOperationCount)
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))

def addCustomBinData(request):
    latitude = float(request.POST["binLatitude"])
    longitude = float(request.POST["binLongitude"])
    addCustomBinDataHelper(latitude, longitude)
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))

def addCustomOperationData(request):
    opName = str(request.POST["operationName"])
    addCustomOperationDataHelper(opName)
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))

def addCustomBinOperationData(request):
    binID = int(request.POST["binID"])
    opID = int(request.POST["operationID"])
    collectionFreq = int(request.POST["collectionFrequency"])
    dateReq = request.POST["lastCollection"]
    datetimeObj = datetime.strptime(dateReq, "%Y-%m-%dT%H:%M")
    addCustomBinOperationDataHelper(binID, opID, collectionFreq, datetimeObj)
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))

def getCollectionFrequency(request):
    getCollectionFrequencyHelper()
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))

def clearSecondDatabase(request):
    clearSecondDatabaseHelper()
    return HttpResponseRedirect(reverse('evrekapp:secondAssignment'))
