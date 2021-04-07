from django.db import models
from django.utils import timezone

# Django adds this default id if pk is not defined => id = models.AutoField(primary_key=True)

class Vehicle(models.Model):
    plate = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return "Vehicle's ID = " + str(self.id) + ", Plate = " + self.plate

class NavigationRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    datetime = models.DateTimeField(blank=False, default=timezone.now)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    def __str__(self):
        return "NavigationRecord's ID = " + str(self.id) \
            + ", VehicleID = " + str(self.vehicle_id) \
            + ", Datetime = " + str(self.datetime) \
            + ", Latitude = " + str(self.latitude) \
            + ", Longitude = " + str(self.longitude)
