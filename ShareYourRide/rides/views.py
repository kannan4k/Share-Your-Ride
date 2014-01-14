from django.template import RequestContext
from django.shortcuts import render_to_response
from rides.models import UserProfile
from rides.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User

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

          
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect('/rides/')

