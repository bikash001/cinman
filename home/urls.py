from django.conf.urls import url
from . import views

app_name = "home"

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^login/?(?P<failed>[0-1])/$',views.login,name='login'),
    #url(r'^success/',views.success,name='success'),
    url(r'^register/$', views.register, name='register'),
    url(r'^forgot_pwd/$', views.forgot, name='forgot'),
    url(r'^validateUser/', views.validateUser),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/messages$', views.messages, name='messages'),
    url(r'^logout/$', views.logout),
    url(r'^home/messages/(?P<machine_id>[0-9]+)/$',views.messagedetails,name='messagedetails'),
    url(r'^home/notifications$', views.notifications, name='notifications'),
    url(r'^home/systemstats$', views.systemstats, name='systemstats'),
    url(r'^home/systemstats/(?P<machine_id>[0-9]+)/(?P<info_requested>[a-z]+)$',views.specificsystemdetails,name='specificsystemdetails'),
    url(r'^$', views.home, name='home'),
]
