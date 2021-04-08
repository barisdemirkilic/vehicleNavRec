from django.urls import path

from . import views

app_name = "evrekapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),

    # Below url configurations are for the first assignment
    path('firstAssignment/', views.FirstAssignmentView.as_view(), name="firstAssignment"),
    path('addFirstRandomData/', views.addFirstRandomData, name="addFirstRandomData"),
    path('addCustomVehicleData/', views.addCustomVehicleData, name="addCustomVehicleData"),
    path('addCustomNavRecData/', views.addCustomNavRecData, name="addCustomNavRecData"),
    path('getLastPointsPerVehicle/', views.getLastPointsPerVehicle, name="getLastPointsPerVehicle"),
    path('clearFirstDatabase/', views.clearFirstDatabase, name="clearFirstDatabase"),

    # Below url configurations are for the second assignment
    path('secondAssignment/', views.SecondAssignmentView.as_view(), name="secondAssignment"),
    path('addSecondRandomData/', views.addSecondRandomData, name="addSecondRandomData"),
    path('addCustomBinData/', views.addCustomBinData, name="addCustomBinData"),
    path('addCustomOperationData/', views.addCustomOperationData, name="addCustomOperationData"),
    path('addCustomBinOperationData/', views.addCustomBinOperationData, name="addCustomBinOperationData"),
    path('getCollectionFrequency/', views.getCollectionFrequency, name="getCollectionFrequency"),
    path('clearSecondDatabase/', views.clearSecondDatabase, name="clearSecondDatabase"),
]
