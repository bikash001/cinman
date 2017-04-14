from django.conf.urls import url
from . import views

app_name = "home"

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$',views.login,name='login'),
    url(r'^register/$', views.registration_handler),
    url(r'^forgot_pwd/$', views.forgot),
    url(r'^validateUser/', views.validateUser),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/messages/$', views.messages, name='messages'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/messages/(?P<machine_id>[0-9]+)/$',views.messagedetails,name='messagedetails'),
    url(r'^home/notifications/$', views.notifications, name='notifications'),
    url(r'^home/systemstats/$', views.systemstats, name='systemstats'),
    url(r'^home/systemstats/(?P<machine_id>[0-9]+)/(?P<info_requested>[a-z]+)$',views.specificsystemdetails,name='specificsystemdetails'),
    url(r'^postdata$',views.postdata,name='postdata'),
    url(r'^postmessage$',views.postmessage,name='postmessage'),
    url(r'^postlogs$',views.postlogs,name='postlogs'),
    url(r'^approve_user$', views.approve_user_registration),
    url(r'^decline_user$', views.decline_user_registration),
]
