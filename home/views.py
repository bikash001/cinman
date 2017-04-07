from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine,Softwaresinstalled,MachineUser,UsersActiveOn,Logs
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime

ram_ip = []
disk_ip = []
double_login = {}

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
		machine_id=int(machine_id)
		messages=Messages.objects.filter(machine=machine_id).order_by('-time')
		machines=Machine.objects.all()
		specmachine = Machine.objects.get(id=machine_id)
		context={
			'machines':machines,
			'messages':messages,
			'machine_id':machine_id,
			'specmachine':specmachine,
		}
		return render(request, 'home/messagedetails.html',context)
	else:
		return redirect('/login')

def notifications(request):
	if request.user.is_authenticated():
		# ram_ip.append("aaa")
		# disk_ip.append("bbb")
		context={
		'ram_ip':ram_ip,
		'disk_ip':disk_ip,
		}
		return render(request, 'home/notifications.html',context)
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
		if(info_requested=="geninfo"):
			context={
				'machines':machines,
				'machine_id':machine_id,
				'specmachine': specmachine,
			}
			return render(request, 'home/generalinfo.html',context)

		if(info_requested=="logs"):
			log_details = Logs.objects.all()
			context={
				'machines':machines,
				'machine_id':machine_id,
				'specmachine': specmachine,
				'log_details': log_details,
			}
			return render(request, 'home/logs.html',context)

		if(info_requested=="softwares"):
			softwares = Softwaresinstalled.objects.filter(machine=specmachine)
			half_len = softwares.count() / 2
			context={
				'machines':machines,
				'machine_id':machine_id,
				'specmachine': specmachine,
				'softwares':softwares,
				'half_len': half_len,
			}
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
	global ram_ip, disk_ip, double_login
	request.POST=request.POST.copy()
	x=request.body
	myDict = json.loads(x)
	users=myDict['user list']
	softwares=myDict['softwares']
	del myDict['user list']
	del myDict['softwares']
	i=Machine(**myDict)
	available_ram = float(i.ram_available_memory[:-2])
	total_ram = float(i.ram_total_memory[:-2])
	if i.ip_address in ram_ip:
		if available_ram/total_ram < 0.2:
			ram_ip.remove(i)
	else:
		if available_ram/total_ram > 0.2:
			ram_ip.append(i)

	available_disk = float(i.disk_available[:-1])
	total_disk = float(i.disk_size[:-1])
	if i in disk_ip:
		if available_disk/total_disk > 0.2:
			disk_ip.remove(i)
	else:
		if available_disk/total_disk < 0.2:
			disk_ip.append(i)

	try:
		machine=Machine.objects.get(mac_address=i.mac_address)
		Machine.objects.filter(mac_address=i.mac_address).update(**myDict)
		UsersActiveOn.objects.filter(machine=machine).delete()
	except ObjectDoesNotExist :
		i.save()
	machine=Machine.objects.get(mac_address=i.mac_address)
	for software in softwares:
		p=Softwaresinstalled(machine=machine,name=software)
		p.save()	
	for user in users:
		udict={'username':user}
		machine_ac=Machine.objects.get(mac_address=i.mac_address)
		try:
			machineuser=MachineUser.objects.get(username=user)
			flag = UsersActiveOn.objects.filter(username=machineuser)
			if flag is not None:
				double_login[machineuser.username]= datetime.now()
			z=UsersActiveOn(machine=machine_ac,username=machineuser)
			z.save()
		except ObjectDoesNotExist :
			i=MachineUser(**udict)
			i.save()
			machineuser=MachineUser.objects.get(username=user)
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

@csrf_exempt
def postlogs(request):
	request.POST=request.POST.copy()
	x=request.body
	myDict = json.loads(x)
	machine_mac=Machine.objects.get(mac_address=myDict['mac'])
	for log in myDict['log']:
		i=Logs(machine=machine_mac,content=log)
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
