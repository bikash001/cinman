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

    def __str__(self):
        return self.mac_address

class Softwaresinstalled(models.Model):
    machine=models.ForeignKey(Machine, null=False, blank=False, related_name="softwares_installed",on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    #update_available=models.BooleanField(default=False)
    version=models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.name

class Peripherals(models.Model):
    PERIPHERAL_CHOICES=(
        (1,"Keyboard"),
        (2,"Mouse"),
        (3,"Speaker")
    )
    machine = models.ForeignKey(Machine, null=False, blank=False, related_name="peripherals",on_delete=models.CASCADE)
    type=models.IntegerField(choices=PERIPHERAL_CHOICES)
    presence=models.BooleanField(default=True)

class MachineUser(models.Model):
    username=models.CharField(max_length=30)
    #last_login_time=models.DateTimeField()

    def __str__(self):
        return self.username

class UsersActiveOn(models.Model):
    username=models.ForeignKey(MachineUser,related_name="active_users")
    machine=models.ForeignKey(Machine,related_name="active_machines")
   
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

class Messages(models.Model):
    #session=models.ForeignKey(Session,related_name="message_session")#fill
    username=models.ForeignKey(MachineUser,related_name="user_messages",null=False,blank=False,on_delete=models.CASCADE)
    machine=models.ForeignKey(Machine,related_name="machine_messages",null=False,blank=False,on_delete=models.CASCADE)
    content=models.CharField(max_length=100)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username) + " "+str(self.time) +"\n"+str(self.content) 

class Administrator(AbstractUser):

	phone_number=models.CharField(max_length=14)

    # username=models.CharField(max_length=30)
    # email=models.CharField(max_length=60)
    # password=models.CharField(max_length=15)

	def __str__(self):
		return self.username
