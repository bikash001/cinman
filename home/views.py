from django.shortcuts import render, redirect
from .models import Administrator

def login(request):
     return render(request, 'home/login_page.html', {'failed_login': False})

def success(request):
     return render(request, 'home/success.html')

def register(request):
	return render(request, 'home/register.html')

def forgot(request):
	return render(request, 'home/forgot_pwd.html')

def home(request):
	return render(request, 'home/home.html')

def validateUser(request):
	name = request.POST['uname']
	pwd = request.POST['pwd']
	usr = None
	try:
		usr = Administrator.objects.get(username=name)
	except Administrator.DoesNotExist:
		pass

	if usr is not None and usr.password == pwd:
		return redirect('/home')
	else:
		return render(request, 'home/login_page.html', {'failed_login': True})