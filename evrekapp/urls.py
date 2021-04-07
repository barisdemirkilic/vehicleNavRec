from django.urls import path

from . import views

app_name = "evrekapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('getLastPointsPerVehicle/', views.getLastPointsPerVehicle, name="getLastPointsPerVehicle"),
    path('addRandomData/', views.addRandomData, name="addRandomData"),
    path('clearDatabase/', views.clearDatabase, name="clearDatabase"),
    path('addCustomVehicleData/', views.addCustomVehicleData, name="addCustomVehicleData"),
    path('addCustomNavRecData/', views.addCustomNavRecData, name="addCustomNavRecData"),
]
