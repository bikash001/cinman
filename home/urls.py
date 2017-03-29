from django.conf.urls import url
from . import views

app_name = "home"

urlpatterns = [
    url(r'^login$',views.login,name='login'),
    url(r'^success/',views.success,name='success'),
    url(r'^register$', views.register, name='register'),
    url(r'^forgot_pwd$', views.forgot, name='forgot'),
    url(r'^validateUser/', views.validateUser),
    url(r'^$', views.home, name='home'),
    # url(r'^$', views.login, name='login'),
]
