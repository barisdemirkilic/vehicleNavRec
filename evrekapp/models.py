from django.db import models
from django.utils import timezone

# Django adds this default id if pk is not defined => id = models.AutoField(primary_key=True)

class Vehicle(models.Model):
    plate = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return "Vehicle's ID = " + str(self.id) + ", Plate = " + self.plate

class NavigationRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    def __str__(self):
        return "NavigationRecord's ID = " + str(self.id) \
            + ", VehicleID = " + str(self.vehicle_id) \
            + ", Datetime = " + str(self.datetime) \
            + ", Latitude = " + str(self.latitude) \
            + ", Longitude = " + str(self.longitude)

class Bin(models.Model):
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    def __str__(self):
        return "Bin's ID = " + str(self.id) \
            + ", Latitude = " + str(self.latitude) \
            + ", Longitude = " + str(self.longitude)

class Operation(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return "Operation's ID = " + str(self.id) \
            + ", Name = " + self.name

class BinOperation(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, blank=False, null=False)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, blank=False, null=False)
    collection_frequency = models.IntegerField(blank=False, null=False)
    last_collection = models.DateTimeField(default=timezone.now, blank=False, null=False)

    # This is defined to ensure unique pair of binID and operationID
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["bin", "operation"], name="BinOperationConstraint")
        ]

    def __str__(self):
        return "BinOperation's ID = " + str(self.id) \
            + ", BinID = " + str(self.bin_id) \
            + ", OperationID = " + str(self.operation_id) \
            + ", CollectionFrequency = " + str(self.collection_frequency) \
            + ", LastCollection = " + str(self.last_collection)
