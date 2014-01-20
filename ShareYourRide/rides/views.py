from django.template import RequestContext
from django.shortcuts import render_to_response
from rides.models import UserProfile, Rider, Address, Ride, Driver
from rides.forms import UserForm, UserProfileForm, RideForm, DriverForm, AddressForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
import time
from datetime import timedelta

def index(request):
    context = RequestContext(request)
    #Get the top five categories        
    context_dict = {'categories':'Hello'}
    context_dict['pages'] = 'Hi'
    
    return render_to_response('rides/index.html', context_dict, context)


def register(request):
    context = RequestContext(request)
    registered=False
    if request.method == 'POST': # Checks POST Request
        user_form = UserForm(data=request.POST) 
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # TO set the Hashed Password
            user.save()
            profile = profile_form.save(commit=False) #To set the picture and website 
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered= True
        else: 
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form':user_form, 'profile_form': profile_form, 'registered': registered}
    return render_to_response('rides/register.html', context_dict, context)



def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rides/')
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            print "Invalid login Details:{0}, {1} ".format(username,password)
            return HttpResponse("Invalid Login Details Supplied ")
        
    else: 
        return render_to_response('rides/login.html', {}, context)

@login_required            
def profile(request):
    context = RequestContext(request)
    u = User.objects.get(username = request.user)
    try:
        up = UserProfile.objects.get(user = u)
    except:
        up = None
    return render_to_response('rides/profile.html',{'up':up}, context )

def processDatetime(strDate, strTime):
    strDateTime = str(strDate) + ' ' + str(strTime)
    time_format = '%Y-%m-%d %I:%M %p'
    from datetime import datetime
    dateTime = datetime.strptime(strDateTime, time_format)
    return dateTime
    

@login_required
def postride(request):
    context = RequestContext(request)
    if request.method == 'POST':
        #To Load the Form data in necessary Form Objects
        sourceAddressForm = AddressForm(data=request.POST, prefix='source')
        destinationAddressForm = AddressForm(data=request.POST, prefix='destination')
        rideForm = RideForm(data=request.POST,prefix='ride')            
        driverForm = DriverForm(data=request.POST, prefix = 'driver')
        
        if rideForm.is_valid() and sourceAddressForm.is_valid() and destinationAddressForm.is_valid():
            #Crate model instances for the model objects
            ride = rideForm.save(commit=False)
            
            #Process the date and time
            startTime = rideForm.cleaned_data['rideStartTime']
            if startTime == 'anytime' or startTime == 'early' or startTime == 'morning' or startTime == 'afternoon' or startTime == 'evening' or  startTime == 'night':    
                ride.ride_startDateTime = processDatetime(rideForm.cleaned_data['rideStartDate'], '12:00 AM')
                ride.ride_startPref = str(startTime)
            else:
                ride.ride_startDateTime = processDatetime(rideForm.cleaned_data['rideStartDate'], startTime)
            returnTime = rideForm.cleaned_data['rideReturnTime']
            if returnTime == 'anytime' or returnTime == 'early' or returnTime == 'morning' or returnTime == 'afternoon' or returnTime == 'evening' or  returnTime == 'night':    
                ride.ride_returnDateTime = processDatetime(rideForm.cleaned_data['rideReturnDate'], '12:00 AM')
                ride.ride_returnPref = str(returnTime)
            else:
                ride.ride_returnDateTime = processDatetime(rideForm.cleaned_data['rideReturnDate'], returnTime)
            
            source,dummy = Address.objects.get_or_create(add_address=sourceAddressForm.cleaned_data['add_address'])
            destination, dummy = Address.objects.get_or_create(add_address=destinationAddressForm.cleaned_data['add_address'])
            
            ride.add_source = source
            ride.add_destination = destination
            ride.save()
            
            who = request.POST.get('ride-type', 'False');
            if who == 'True':
                if driverForm.is_valid():
                    driver = driverForm.save(commit=False)
                    driver.ride_id = ride
                    driver.user_id = request.user
                    driver.save()
                else:
                    driverForm.errors  
            else:
                rider = Rider(ride_id=ride, user_id=request.user)
                rider.save()
            return HttpResponseRedirect('/rides/ridematches/'+ str(ride.pk))                      
        else:
            print rideForm.errors, sourceAddressForm.errors, destinationAddressForm.errors
    else:
        rideForm = RideForm(prefix='ride')
        sourceAddressForm = AddressForm(prefix='source')
        destinationAddressForm = AddressForm(prefix='destination')
        driverForm = DriverForm(prefix='driver')
    
    form_list =  {'rideForm': rideForm,
                           'sourceAddressForm' : sourceAddressForm,
                           'destinationAddressForm':destinationAddressForm,
                           'driverForm' : driverForm,
                          }
    return render_to_response('rides/postride.html',form_list,context)
    
@login_required
def ridedetails(request, ride_id):
    # REquest our context from the request passed to us
    context = RequestContext(request)
    context_dict = dict()
    try: 
        ride = Ride.objects.get(pk=ride_id)
        context_dict['ride'] = ride   #Adding the pages to the dict
    except Ride.DoesNotExist:
        pass    
    return render_to_response('rides/ridedetails.html', context_dict, context)

def run_query(strFrom, strTo, startDate):    
    if strFrom or strTo or startDate:
        print '#Log 1',strFrom, strTo, startDate
        day_min = datetime.datetime.combine(startDate, datetime.time.min)
        day_max = datetime.datetime.combine(startDate, datetime.time.max)
        objFrom = Address.objects.filter(add_address = strFrom)
        objTo = Address.objects.filter(add_address = strTo)
        result_list = Ride.objects.filter(Q(add_source = objFrom) | Q(add_destination = objTo) | Q(ride_startDateTime__range=(day_min, day_max)) )
    else:
        result_list = Ride.objects.all()
    return result_list
    

    
@login_required
def search(request):
    context = RequestContext(request)
    result_list = []
    userList = {}
    if request.method == 'POST':
        strFrom = request.POST['from'].strip()
        strTo = request.POST['to'].strip()
        strDate = request.POST['date']
        print '#Log', strFrom, strTo, strDate
        
        if strDate:
            timeObj = time.strptime(strDate, '%m/%d/%Y')
            startDate = datetime.datetime.fromtimestamp(time.mktime(timeObj))
        else:
            startDate = datetime.datetime.now()
            print datetime.datetime.now()
            print startDate
        result_list = run_query(strFrom, strTo, startDate)     
        
        for ride in result_list:
            if ride.type:
                driver = Driver.objects.get(ride_id = ride)
                userList[ride.pk] = driver.user_id.username
                print 'driver', driver.user_id.username, userList[ride.pk]
            else:
                rider = Rider.objects.get(ride_id = ride)
                userList[ride.pk] = rider.user_id.username
                print 'rider', rider.user_id.username, userList[ride.pk]
        return render_to_response('rides/search.html', {'result_list':result_list,'userList':userList}, context )
    else:
        return render_to_response('rides/search.html', {'result_list':result_list,'userList':userList}, context )

def returnMinMaxTime(ride):
            startTime = ride.ride_startDateTime
            pref = ride.ride_startPref
            if pref == 'None':
                time_min = startTime - timedelta(hours=2)
                time_max = startTime - timedelta(hours=-2)
                print 'Log: Ride Preference is Time'
            elif pref == 'anytime':
                time_min = datetime.datetime.combine(startTime, datetime.time.min)
                time_max = datetime.datetime.combine(startTime, datetime.time.max)
                print 'Log: Ride Preference is anytime'
            elif pref == 'early':
                time_min = startTime - timedelta(hours=0)
                time_max = startTime - timedelta(hours=-8)
                print 'Log: Ride Preference is early'
            elif pref == 'morning':
                time_min = startTime - timedelta(hours=-8)
                time_max = startTime - timedelta(hours=-12)
                print 'Log: Ride Preference is morning'
            elif pref == 'afternoon':
                time_min = startTime - timedelta(hours=-12)
                time_max = startTime - timedelta(hours=-17)
                print 'Log: Ride Preference is afternoon'
            elif pref == 'evening':
                time_min = startTime - timedelta(hours=-17)
                time_max = startTime - timedelta(hours=-21)
                print 'Log: Ride Preference is evening'
            elif pref == 'night':
                time_min = startTime - timedelta(hours=-21)
                time_max = startTime - timedelta(hours=-24)
                print 'Log: Ride Preference is night'
            #print time_min, time_max
            return (time_min, time_max)
        
def getTiming(hour):
    var = ''
    if hour <= 8:
        var = 'early'
    elif hour >=9 and hour <12:
        var = 'morning'
    elif hour >=12 and hour <17:
        var = 'afternoon'
    elif hour >=17 and hour <21:
        var = 'evening'
    elif hour >=21 and hour <24:
        var = 'night'
    return var
    
@login_required
def ridematches(request, ride_id):
    # REquest our context from the request passed to us
    context = RequestContext(request)
    context_dict = dict()
    result_list = []

    try: 
        ride = Ride.objects.get(pk=ride_id)
        minMaxList = returnMinMaxTime(ride)
        print minMaxList[0], minMaxList[1]
        time_min = datetime.datetime.combine(ride.ride_startDateTime, datetime.time.min)
        time_max = datetime.datetime.combine(ride.ride_startDateTime, datetime.time.max)
        q0 = Ride.objects.filter(ride_startDateTime__range=(time_min, time_max))
        q1 = q0.filter(add_source=ride.add_source, add_destination=ride.add_destination)
        print q1
        if ride.ride_startPref == 'None':
            print 'Log: None '
            rideTiming = getTiming(ride.ride_startDateTime.hour)
            result_list = q1.filter (Q(ride_startDateTime__range=(minMaxList[0], minMaxList[1])) | Q(ride_startPref = rideTiming ) | Q(ride_startPref = 'anytime' ) ).exclude(pk= ride.pk)
        elif ride.ride_startPref == 'anytime':
            print 'Log: Anytime'
            result_list = q1.exclude(pk= ride.pk)
        else:
            print 'Log: Morning, Night'
            result_list = q1.filter(Q(ride_startDateTime__range=(minMaxList[0], minMaxList[1])) | Q(ride_startPref = ride.ride_startPref ) | Q(ride_startPref = 'anytime' ) ).exclude(pk= ride.pk)
        context_dict['ride'] = ride   #Adding the pages to the dict
        return render_to_response('rides/ridematches.html', {'result_list':result_list,'ride':ride}, context )
    except Ride.DoesNotExist:
        pass    
    return render_to_response('rides/ridematches.html', {'result_list':result_list,'ride':ride}, context )

    
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect('/rides/')

