from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine,Softwaresinstalled,MachineUser,UsersActiveOn
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.core.exceptions import ObjectDoesNotExist
import json


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
		machine_id=int(machine_id)
		messages=Messages.objects.filter(machine=machine_id).order_by('-time')
		machines=Machine.objects.all()
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
	machine_id = int(machine_id)
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		specmachine=Machine.objects.get(id=machine_id)
		softwares = Softwaresinstalled.objects.filter(machine=specmachine)
		context={
			'machines':machines,
			'machine_id':machine_id,
			'specmachine': specmachine,
			'softwares':softwares,
		}
		if(info_requested=="geninfo"):
			return render(request, 'home/generalinfo.html',context)

		if(info_requested=="logs"):
			return render(request, 'home/logs.html',context)

		if(info_requested=="softwares"):
			return render(request, 'home/softwares.html',context)

		if(info_requested=="peripherals"):
			return render(request, 'home/peripherals.html',context)

	else:
		return redirect('/login')


def home(request):
	if request.user.is_authenticated():
		userCount = MachineUser.objects.count()
		machineCount = Machine.objects.count()
		userActive = UsersActiveOn.objects.values('username').distinct().count()
		machineActive = UsersActiveOn.objects.values('machine').distinct().count()
		vals = {'actUsers': userActive, 'actMachines': machineActive, 'machines': machineCount, 'users': userCount}
		return render(request, 'home/home.html', context=vals)
	else:
		return redirect('/login')

@csrf_exempt
def postdata(request):
	#CSRF_COOKIE_SECURE=False
	request.POST=request.POST.copy()
	x=request.body
	myDict = json.loads(x)
	users=myDict['user list']
	del myDict['user list']
	i=Machine(**myDict)
	try:
		machine=Machine.objects.get(mac_address=i.mac_address)
		Machine.objects.filter(mac_address=i.mac_address).update(**myDict)
		UsersActiveOn.objects.filter(machine=machine).delete()
	except ObjectDoesNotExist :
		i.save()	
	for user in users:
		udict={'username':user}
		machine_ac=Machine.objects.get(mac_address=i.mac_address)
		try:
			machineuser=MachineUser.objects.get(username=user)
			z=UsersActiveOn(machine=machine_ac,username=machineuser)
			z.save()
		except ObjectDoesNotExist :
			i=MachineUser(**udict)
			i.save()
			z=UsersActiveOn(machine=machine_ac,username=machineuser)
			z.save()
	
	return HttpResponse("success", content_type="text/plain")

@csrf_exempt
def postmessage(request):
	#CSRF_COOKIE_SECURE=False
	request.POST=request.POST.copy()
	x=request.body
	myDict = json.loads(x)
	user_id= myDict['user']
	machine_mac=myDict['mac']
	try:
		user=MachineUser.objects.get(username=user_id)
		myDict['username']=user
		del myDict['user']
	except ObjectDoesNotExist :
		return HttpResponse("fail", content_type="text/plain")
	
	try:
		machine=Machine.objects.get(mac_address=machine_mac)
		myDict['machine']=machine
		del myDict['mac']
	except ObjectDoesNotExist :
		return HttpResponse("fail", content_type="text/plain")	
	i=Messages(**myDict)
	i.save()
	return HttpResponse("success", content_type="text/plain")


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
