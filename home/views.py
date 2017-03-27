from django.shortcuts import render

def login(request):
     return render(request, 'home/login_page.html')

def success(request):
     return render(request, 'home/success.html')

def register(request):
	return render(request, 'home/register.html')

def forgot(request):
	return render(request, 'home/forgot_pwd.html')