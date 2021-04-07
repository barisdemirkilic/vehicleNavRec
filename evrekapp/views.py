from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from datetime import datetime

from .viewsHelper import getLastPointsPerVehicleHelper, \
addRandomDataHelper, clearDatabaseHelper, \
addCustomVehicleDataHelper, addCustomNavRecDataHelper

class IndexView(generic.TemplateView):
    template_name = "evrekapp/index.html"

def getLastPointsPerVehicle(request):
    getLastPointsPerVehicleHelper()
    return HttpResponseRedirect(reverse('evrekapp:index'))

def addRandomData(request):
    vehicleCount = int(request.POST["vehicleCount"])
    navRecCount = int(request.POST["navRecCount"])
    addRandomDataHelper(vehicleCount, navRecCount)
    return HttpResponseRedirect(reverse('evrekapp:index'))

def addCustomVehicleData(request):
    plate = str(request.POST["plate"])
    addCustomVehicleDataHelper(plate)
    return HttpResponseRedirect(reverse('evrekapp:index'))

def addCustomNavRecData(request):
    plate = str(request.POST["plateNav"])
    latitude = float(request.POST["latitude"])
    longitude = float(request.POST["longitude"])
    dateReq = request.POST["datetime"]
    datetimeObj = datetime.strptime(dateReq, "%Y-%m-%dT%H:%M")
    addCustomNavRecDataHelper(plate, latitude, longitude, datetimeObj)
    return HttpResponseRedirect(reverse('evrekapp:index'))

def clearDatabase(request):
    clearDatabaseHelper()
    return HttpResponseRedirect(reverse('evrekapp:index'))
