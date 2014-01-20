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
    add_address = forms.CharField(help_text="Address", required=True)
    class Meta:
        model = Address
        fields = ['add_address']
        

class RideForm(forms.ModelForm):
    CHOICES=[(False,'Passenger'),(True,'Driver')]
    NO_OF_HRS = (
                 ('anytime','anytime'),
                 ('early','early (12a-8a)'),
                 ('morning','morning (8a-12p)'),
                 ('afternoon','afternoon (12p-5p)'),
                 ('evening','evening (5p-9p)'),
                 ('night','night (9p-12a)'),
                 ('1:00 AM','1:00am'),
                 ('2:00 AM','2:00am'),
                 ('3:00 AM','3:00am'),
                 ('4:00 AM','4:00am'),
                 ('5:00 AM','5:00am'),
                 ('6:00 AM','6:00am'),
                 ('7:00 AM','7:00am'),
                 ('8:00 AM','8:00am'),
                 ('9:00 AM','9:00am'),
                 ('10:00 AM','10:00am'),
                 ('11:00 AM','11:00am'),
                 ('12:00 AM','noon'),
                 ('1:00 PM','1:00pm'),
                 ('2:00 PM','2:00pm'),
                 ('3:00 PM','3:00pm'),
                 ('4:00 PM','4:00pm'),
                 ('5:00 PM','5:00pm'),
                 ('6:00 PM','6:00pm'),
                 ('7:00 PM','7:00pm'),
                 ('8:00 PM','8:00pm'),
                 ('9:00 PM','9:00pm'),
                 ('10:00 PM','10:00pm'),
                 ('11:00 PM','11:00pm'),
                 ('12:00 PM','midnight')                 
                 )
    
    type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    
    rideStartDate = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}), help_text="Depart Date",required=True)
    rideStartTime = forms.ChoiceField(choices=NO_OF_HRS,help_text="Depart Time")
    
    rideReturnDate = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}), help_text="Return Date", required=True)
    rideReturnTime = forms.ChoiceField(choices=NO_OF_HRS,help_text="Return Time")
    
    ride_comment = forms.CharField( help_text="Comment.", required=True)
    class Meta:
        model = Ride
        fields = ['type','rideStartDate','rideStartTime','rideReturnDate', 'rideReturnTime','ride_comment']

        
class DriverForm(forms.ModelForm):
    drv_carseats = forms.IntegerField(help_text="Number of available seats", required=True)
    class Meta:
        model = Driver
        fields = ['drv_carseats']


