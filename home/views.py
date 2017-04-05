from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine,MachineUser,UsersActiveOn
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.core.exceptions import ObjectDoesNotExist
import json


def direct(request):
	return redirect('/login')

def login(request, failed=0):
	if request.user.is_authenticated():
		print 'success'
		return redirect('/home')
	else:
		print 'failure'
		return render(request, 'home/login_page.html')

def register(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		Administrator.objects.create_user(username=request.POST['uname'], password=request.POST['passwd'], phone_number=request.POST['mobile'])
		return HttpResponse("user will be registered", status=403)

def forgot(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return HttpResponse("new password will be set", status=403)

def messages(request):
	if request.user.is_authenticated():
		messages = Messages.objects.all()
		obj = {'type': 'message', 'data': []}
		arr = []
		for msg in messages:
			val = {}
			val['uname'] = str(msg.username)
			val['ip'] = str(msg.machine)
			val['time'] = str(msg.time)
			val['msg'] = str(msg.content)
			arr.append(val)

		obj['data'] = arr
		return JsonResponse(obj)
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

def systemDetails(request, ip):
	if request.user.is_authenticated():
		machine = Machine.objects.get(id=ip)
		obj = {}
		if (machine is not None):
			obj['cpu'] = [machine.cpu_speed,machine.cores_per_processor,machine.cpu_model_name,machine.processor,machine.no_of_processors]
			obj['ram'] = [machine.ram_available_memory,machine.ram_total_memory]
			obj['hdd'] = [machine.disk_avialble,machine.disk_used,machine.disk_used]
			obj['ni'] = [machine.ip_address,machine.mac_address,machine.node_hostname]
			obj['os'] = [machine.operating_system,machine.kernal_name,machine.kernal_release]
		return JsonResponse(obj)
	else:
		return HttpResponse('access denied', status=403)


def systemstats(request):
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		obj = {'type': 'stats', 'data': []}
		arr = []
		for machine in machines:
			val = {}
			val['id'] = machine.id
			val['ip'] = machine.ip_address
			arr.append(val)

		obj['data'] = arr
		return JsonResponse(obj)
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
	if request.user.is_authenticated():
	   return render(request, 'home/home.html')
	else:
		print 'not logged in'
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
	print myDict
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
		return HttpResponse('success', status=200)
	else:
		return HttpResponse("invalid credentials", status=403)


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
