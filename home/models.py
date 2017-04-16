from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class Machine(models.Model):
    ip_address=models.CharField(max_length=20)
    mac_address=models.CharField(max_length=40)
    ram_available_memory=models.CharField(max_length=20)
    ram_total_memory=models.CharField(max_length=20)
    disk_available=models.CharField(max_length=20)
    disk_used=models.CharField(max_length=20)
    disk_size=models.CharField(max_length=20)
    no_of_processors=models.CharField(max_length=20)
    cpu_speed=models.CharField(max_length=20)
    cores_per_processor=models.CharField(max_length=20)
    cpu_model_name=models.CharField(max_length=100)
    vendor_id=models.CharField(max_length=40)
    cache_size=models.CharField(max_length=20)
    hardware_platform=models.CharField(max_length=30)
    kernel_release=models.CharField(max_length=30)
    operating_system=models.CharField(max_length=30)
    machine_hardware=models.CharField(max_length=30)
    node_hostname=models.CharField(max_length=30)
    processor=models.CharField(max_length=30)
    kernel_name=models.CharField(max_length=30)
    ramusagehigh=models.BooleanField(default=False)
    diskusagehigh=models.BooleanField(default=False)

    def __str__(self):
        return self.mac_address

class Softwaresinstalled(models.Model):
    machine=models.ForeignKey(Machine, null=False, blank=False, related_name="softwares_installed",on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    #update_available=models.BooleanField(default=False)
    version=models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.name


class MachineUser(models.Model):
    username=models.CharField(max_length=30)
    #last_login_time=models.DateTimeField()

    def __str__(self):
        return self.username

class Peripherals(models.Model):
    machine = models.ForeignKey(Machine, null=False, blank=False, related_name="peripherals",on_delete=models.CASCADE)
    username=models.ForeignKey(MachineUser, null=False, blank=False, related_name="peripherals_user",on_delete=models.CASCADE)
    device_type=models.CharField(max_length=20)
    connected=models.CharField(max_length=50)
    disconnected=models.CharField(max_length=50,default="Not Yet")
    device_number=models.CharField(max_length=10)


class UsersActiveOn(models.Model):
    username=models.ForeignKey(MachineUser,related_name="active_users")
    machine=models.ForeignKey(Machine,related_name="active_machines")
    time=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.username)+" "+str(self.machine)

class Logs(models.Model):
    TYPE_CHOICES=(
            (1,"General message and system related logs"),
            (2,"Authentication Logs"),
            (3,"Login Records"),
            (4,"MySQL database server log file"),
            (5,"Kernal Logs"),
            (6,"System boot Log"),
            (7,"dpkg"),
            (8,"Mail Server Logs")

    )
    machine=models.ForeignKey(Machine,related_name="machinelogs",on_delete=models.CASCADE,null=False,blank=False)
    content=models.CharField(max_length=500)
    #type=models.IntegerField(choices=TYPE_CHOICES)
    
    def __str__(self):
        return self.content



class Messages(models.Model):
    #session=models.ForeignKey(Session,related_name="message_session")#fill
    username=models.ForeignKey(MachineUser,related_name="user_messages",null=False,blank=False,on_delete=models.CASCADE)
    machine=models.ForeignKey(Machine,related_name="machine_messages",null=False,blank=False,on_delete=models.CASCADE)
    content=models.CharField(max_length=100)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username) + " "+str(self.time) +"\n"+str(self.content) 

class TempUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=100)
    phone_number=models.CharField(max_length=14)


class Administrator(AbstractUser):

	phone_number=models.CharField(max_length=14)

    # username=models.CharField(max_length=30)
    # email=models.CharField(max_length=60)
    # password=models.CharField(max_length=15)

	def __str__(self):
		return self.username
