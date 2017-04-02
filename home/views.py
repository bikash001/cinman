from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine
from django.contrib import auth

def direct(request):
	return redirect('/login')

def login(request, failed=0):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return render(request, 'home/login_page.html', {'failed_login': failed})

def register(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return render(request, 'home/register.html')

def forgot(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return render(request, 'home/forgot_pwd.html')

def messages(request):
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		context={
			'machines':machines, 
		}
		return render(request, 'home/messages.html',context)
	else:
		return redirect('/login')

def messagedetails(request,machine_id):
	if request.user.is_authenticated():
		messages=Messages.objects.filter(machine=machine_id).order_by('-time')
		machines=Machine.objects.all()
		machine_id=int(machine_id)
		context={
			'machines':machines,
			'messages':messages,
			'machine_id':machine_id, 
		}
		return render(request, 'home/messagedetails.html',context)
	else:
		return redirect('/login')

def notifications(request):
	if request.user.is_authenticated():
	   return render(request, 'home/notifications.html')
	else:
		return redirect('/login')

def systemstats(request):
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		context={
			'machines':machines,
		}
		return render(request, 'home/systemstats.html',context)
	else:
		return redirect('/login')


def specificsystemdetails(request,machine_id,info_requested):
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		context={
			'machines':machines,
			'machine_id':machine_id,
		}
		if(info_requested=="geninfo"):
			return render(request, 'home/generalinfo.html',context)

		if(info_requested=="logs"):
			return render(request, 'home/logs.html',context)

		if(info_requested=="softwares"):
			return render(request, 'home/softwares.html',context)

		if(info_requested=="users"):
			return render(request, 'home/systemusers.html',context)

	else:
		return redirect('/login')


def home(request):
	# global validation
	# if(validation==True):
	if request.user.is_authenticated():
	   return render(request, 'home/home.html')
	else:
		return redirect('/login')

def validateUser(request):
	name = request.POST['uname']
	pwd = request.POST['pwd']
	usr = auth.authenticate(username=name, password=pwd)
	
	if usr is not None and usr.is_active:
		# validation=True
		auth.login(request,usr)
		return redirect('/home')
	else:
		global failed
		failed = True
		return redirect('/login/1/')


def logout(request):
	auth.logout(request)
	return redirect('/login')

def getmessages(ip_addr):
	machine_id=Machine.objects.get(ip_address=ip_addr)
	messages=Messages.objects.filter(machine=machine_id).order_by('time')
	return messages

def getip():
	machine=Machine.objects.all()
	return machine.ip_address
