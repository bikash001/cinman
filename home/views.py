from django.shortcuts import render, redirect
from .models import Administrator
validation=False
def direct(request):
	return redirect('/login')	
def login(request):
     return render(request, 'home/login_page.html', {'failed_login': False})

def register(request):
	return render(request, 'home/register.html')

def forgot(request):
	return render(request, 'home/forgot_pwd.html')

def home(request):
	global validation
	if(validation==True):
	   return render(request, 'home/home.html')
	else:
		return redirect('/login')

def validateUser(request):
	name = request.POST['uname']
	pwd = request.POST['pwd']
	usr = None
	global validation
	try:
		usr = Administrator.objects.get(username=name)
	except Administrator.DoesNotExist:
		pass

	if usr is not None and usr.password == pwd:
		validation=True
		return redirect('/home')
	else:
		return render(request, 'home/login_page.html', {'failed_login': True})


def logout(request):
	global validation
	validation=False
	redirect('/login')