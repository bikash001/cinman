from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
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
		machine = Machine.objects.get(ip_address=ip)
		obj = {}
		
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
