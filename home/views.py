from django.shortcuts import render, redirect
from .models import Administrator,Messages,Machine,Softwaresinstalled,MachineUser,UsersActiveOn,Logs,TempUser,Peripherals
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
import json
from datetime import datetime,timedelta
from django.utils import timezone
import subprocess as sb
from django.core.mail import send_mail


def delete_msg(request):
	if request.user.is_authenticated():
		Messages.objects.filter(id=request.POST['id']).delete()
		return HttpResponse('deleted', status=200)
	else:
		return HttpResponse('unauthorised', status=403)
	
def sendMail(request):
	send_mail('Test', 'hw r u?', 'abc@gmail.com',
		['xxx@gmail.com'])
	return HttpResponse('lol', status=200)

def login(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return render(request, 'home/login_page.html')

def registration_handler(request):
	temp = None
	try:
		temp = Administrator.objects.get(username=request.POST['uname'])
	except Exception as e:
		pass
	if temp:
		return HttpResponse('username already exist', status=403)
	else:
		user = TempUser.objects.create(username=request.POST['uname'],phone_number=request.POST['mobile'],
			email=request.POST['email'], first_name=request.POST['fname'], last_name=request.POST['lname'],
			password=auth.hashers.make_password(request.POST['passwd']))
		return HttpResponse('stored data', status=200)

def approve_user_registration(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		udetails = TempUser.objects.get(id=request.POST['id'])
		user = Administrator.objects.create(username=udetails.username,phone_number=udetails.phone_number,
			email=udetails.email, first_name=udetails.first_name, last_name=udetails.last_name,
			password=udetails.password)
		udetails.delete()
		return HttpResponse('successfully registered', status=202)
	else:
		return HttpResponse('you are not logged in', status=403)

def decline_user_registration(request):
	if request.user.is_authenticated()  and request.user.is_superuser:
		TempUser.objects.filter(id=request.POST['id']).delete()
		return HttpResponse('deleted', status=200)
	else:
		return HttpResponse('you are not logged in', status=403)

def current_status(request):
	if request.user.is_authenticated():
		ipList = Machine.objects.values_list('ip_address', flat=True)
		print ipList
		obj = {}
		for ip in ipList:
			try:
				ret = sb.check_output(['ping','-c 5','-f','-i 0.2', ip])
				obj[ip] = 1
			except Exception as e:
				obj[ip] = 0
		return JsonResponse(obj)
	else:
		return HttpResponse('you are not logged in', status=403)

def forgot(request):
	user = None
	try:
		user = Administrator.objects.get(username=request.POST['uname'])
	except Exception as e:
		pass

	if user != None and user['email'] == request.POST['email']:
		return HttpResponse("new password will be set", status=202)
	else:
		return HttpResponse("user does not exist.", status=403)

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
		obj = {}
		prev = ""
		temp = []
		# print 'hello', userActive[0].username == userActive[1].username
		# print userActive[0].username, userActive[1].username
		userActive = UsersActiveOn.objects.order_by('username')
		print userActive
		for i in range(len(userActive)):
			if (prev == userActive[i].username):
				temp.append(str(userActive[i].machine))
			else:
				prev = userActive[i].username
				if len(temp) > 1:
					obj[str(userActive[i-1].username)] = temp
					# print 'temp',temp
					temp = []
				else:
					# print 'na', userActive[i].username
					temp = [str(userActive[i].machine)]
		if len(temp) > 1:
			obj[str(userActive.last().username)] = temp
			# print temp
		
		users = {}
		if request.user.is_superuser:
			tempuser = TempUser.objects.all()
			for x in tempuser:
				users[str(x.id)] = [str(x.first_name), str(x.last_name), str(x.email), str(x.phone_number)]

		ram_ip=Machine.objects.filter(ramusagehigh=True)
		disk_ip=Machine.objects.filter(diskusagehigh=True)	
		context={
			'ram_ip':ram_ip,
			'disk_ip':disk_ip,
			'double_login': obj,
			'users': users
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
	#machine_req=Machine.object.get(id=machine_id)
	if request.user.is_authenticated():
		machines=Machine.objects.all()
		specmachine=Machine.objects.get(id=machine_id)
		if(info_requested=="geninfo"):
			users_active=UsersActiveOn.objects.filter(machine=specmachine)
			context={
				'machines':machines,
				'machine_id':machine_id,
				'specmachine': specmachine,
				'users': users_active,
			}
			return render(request, 'home/generalinfo.html',context)

		if(info_requested=="logs"):
			log_details = Logs.objects.filter(machine=specmachine).order_by('-id')
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
		now = timezone.now()
		earlier = now - timedelta(minutes=5)
		actusers = UsersActiveOn.objects.values_list('username').filter(time__range=(earlier,now)).distinct()
		userActive = len(actusers)
		macs = UsersActiveOn.objects.values_list('machine').filter(time__range=(earlier,now)).distinct()
		machineActive = macs.count()
		machines = Machine.objects.all()
		ips = []
		usernames=[]
		for actuser in actusers:
			usernames.append(MachineUser.objects.get(id=actuser[0]))

		for mac in macs:
			ips.append(Machine.objects.get(id=mac[0]))

		#print ips
		# print macs
		# for x in macs:
		# 	print str(x.machine), "hello"
			# ips.append(machines.get(mac_address=x.))
		# print users
		# print macs
		# for x in macs

		superuser = {}
		users = []
		admins = Administrator.objects.all()
		for x in admins:
			if x.is_superuser:
				superuser['name'] = x.first_name+" "+x.last_name
				superuser['email'] = x.email
				superuser['mobile'] = x.phone_number
			else:
				users.append({'name': x.first_name+" "+x.last_name, 'email': x.email,
					'mobile': x.phone_number})

		vals = {'actUsers': userActive, 'actMachines': machineActive, 'machines': machineCount,
		'usercount': userCount, 'superuser': superuser, 'users': users, 'ips': ips,'activeusers':usernames}
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
	softwares=myDict['softwares']
	del myDict['user list']
	del myDict['softwares']
	#print myDict
	i=Machine(**myDict)
	available_ram = float(i.ram_available_memory[:-2])
	total_ram = float(i.ram_total_memory[:-2])
	available_disk = float(i.disk_available[:-1])
	total_disk = float(i.disk_size[:-1])
	try:
		machine=Machine.objects.get(mac_address=i.mac_address)
		Machine.objects.filter(mac_address=i.mac_address).update(**myDict)
		UsersActiveOn.objects.filter(machine=machine).delete()
	except ObjectDoesNotExist :
		i.save()
	machine=Machine.objects.get(mac_address=i.mac_address)

	if(available_ram/total_ram<0.7):
		Machine.objects.filter(mac_address=i.mac_address).update(ramusagehigh=True)
	else:	
		Machine.objects.filter(mac_address=i.mac_address).update(ramusagehigh=False)

	if(available_disk/total_disk<0.7):
		Machine.objects.filter(mac_address=i.mac_address).update(diskusagehigh=True)
	else:	
		Machine.objects.filter(mac_address=i.mac_address).update(diskusagehigh=False)

	for software in softwares:
		p=Softwaresinstalled(machine=machine,name=software)
		p.save()	
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

@csrf_exempt
def postperipherals(request):
	request.POST=request.POST.copy()
	x=request.body
	myDict = json.loads(x)
	machine_mac=Machine.objects.get(mac_address=myDict['mac_address'])
	username=MachineUser.objects.get(username=myDict['username'])
	del myDict['mac_address']
	del myDict['username']
	myDict['machine']=machine_mac
	myDict['username']=username
	i=Peripherals(**myDict)
	try:
		x=Peripherals.objects.get(machine=machine_mac,device_number=myDict['device_number'])
		Peripherals.objects.filter(machine=machine_mac,device_number=myDict['device_number']).update(disconnected=myDict['disconnected'])
	except ObjectDoesNotExist:
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
