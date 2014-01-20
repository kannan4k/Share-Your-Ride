from django.contrib import admin
from rides.models import UserProfile, Ride, Address, Driver , Rider
admin.site.register(UserProfile)
admin.site.register(Ride)
admin.site.register(Address)
admin.site.register(Driver)
admin.site.register(Rider)
