from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class UserProfile (models.Model):
    user  = models.OneToOneField(User)
    phone_num = models.TextField(blank=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __unicode__(self):
        return self.user.username
    
class Address(models.Model):
    add_address = models.TextField(max_length=80,blank=True)
    add_city = models.TextField(max_length=50,blank=True)
    add_state = models.TextField(max_length=30,blank=True)
    add_zip = models.TextField(max_length=6,blank=True)
    add_lat = models.FloatField(default=0.0)
    add_lng = models.FloatField(default=0.0)
    add_type = models.TextField(max_length=30,blank=True)
    def __unicode__(self):
        return self.add_address
    
class Ride(models.Model):
    add_source = models.ForeignKey(Address, related_name='source')
    add_destination = models.ForeignKey(Address, related_name='destination')
    ride_starttime = models.DateTimeField(default= datetime.datetime.now, blank=True)
    ride_endtime = models.DateTimeField(default= datetime.datetime.now, blank=True)
    ride_comment = models.TextField(max_length=140,blank=True)
    def __unicode__(self):
        return self.add_source
    
class Driver(models.Model):
    ride_id = models.ForeignKey(Ride)
    user_id = models.ForeignKey(User)
    drv_carseats = models.SmallIntegerField(blank=False)
    drv_expiration = models.DateTimeField(blank=True)
    def __unicode__(self):
        return self.ride_id
    
class Rider(models.Model):
    ride_id = models.ForeignKey(Ride)
    user_id = models.ForeignKey(User)
    add_pickup = models.ForeignKey(Address)
    def __unicode__(self):
        return self.ride_id
    