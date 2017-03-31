from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine
validation=False
def direct(request):
	return redirect('/login')
def login(request):
     return render(request, 'home/login_page.html', {'failed_login': False})

def register(request):
	return render(request, 'home/register.html')

def forgot(request):
	return render(request, 'home/forgot_pwd.html')

def messages(request):
	if(validation==True):
		machines=Machine.objects.all()
		context={
			'machines':machines, 
		}
		return render(request, 'home/messages.html',context)
	else:
		return redirect('/login')

def messagedetails(request,machine_id):
	if(validation==True):
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
	global validation
	if(validation==True):
	   return render(request, 'home/notifications.html')
	else:
		return redirect('/login')

def systemstats(request):
	global validation
	if(validation==True):
		machines=Machine.objects.all()
		context={
			'machines':machines,
		}
		return render(request, 'home/systemstats.html',context)
	else:
		return redirect('/login')


def specificsystemdetails(request,machine_id,info_requested):
	global validation
	if(validation==True):
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
	return redirect('/login')

def getmessages(ip_addr):
	machine_id=Machine.objects.get(ip_address=ip_addr)
	messages=Messages.objects.filter(machine=machine_id).order_by('time')
	return messages

def getip():
	machine=Machine.objects.all()
	return machine.ip_address
