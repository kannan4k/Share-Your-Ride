from django.conf.urls import patterns, url

from rides import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name = "register"),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/', views.user_logout, name='user logout'),
        url(r'^profile/', views.profile, name='profile'),
        url(r'^postride/', views.postride, name='post new ride'),
        url(r'^search/', views.search, name='search'),
        url(r'^ridedetails/(?P<ride_id>\w+)$', views.ridedetails, name='ride details'),
        url(r'^ridematches/(?P<ride_id>\w+)$', views.ridematches, name='ride matches'),
        )