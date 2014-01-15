from django import forms
from rides.models import UserProfile, Ride, Address, Driver, Rider
from django.contrib.auth.models import User
from django.contrib.admin import widgets 
import datetime

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    phone_num = forms.CharField(help_text="Please enter a Mobile Number.")
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    
    class Meta:
        model = UserProfile
        fields = ['phone_num','website', 'picture']

class AddressForm(forms.ModelForm):
    add_address = forms.CharField(help_text="Address")
    class Meta:
        model = Address
        fields = ['add_address']
        
        
class RideForm(forms.ModelForm):
    ride_starttime = forms.DateTimeField(widget=forms.DateInput(attrs={'class':'timepicker'}), help_text="Depart")
    ride_endtime = forms.DateTimeField(widget=forms.DateInput(attrs={'class':'timepicker'}), help_text="Return")
    ride_comment = forms.CharField( help_text="Comment.")
    class Meta:
        model = Ride
        fields = ['ride_starttime','ride_endtime', 'ride_comment']

        
class DriverForm(forms.ModelForm):
    drv_carseats = forms.IntegerField(help_text="Number of available seats")
    class Meta:
        model = Driver
        fields = ['drv_carseats']
        

