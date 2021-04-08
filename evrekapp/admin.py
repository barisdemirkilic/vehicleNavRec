from django.contrib import admin

from .models import Vehicle, NavigationRecord, Bin, Operation, BinOperation

admin.site.register(Vehicle)
admin.site.register(NavigationRecord)
admin.site.register(Bin)
admin.site.register(Operation)
admin.site.register(BinOperation)
