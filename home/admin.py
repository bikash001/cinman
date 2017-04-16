from django.contrib import admin
from .models import Administrator,Machine,Messages,MachineUser,Softwaresinstalled,UsersActiveOn,Logs,Peripherals
admin.site.register(Administrator)
admin.site.register(Machine)
admin.site.register(Messages)
admin.site.register(MachineUser)
admin.site.register(UsersActiveOn)
admin.site.register(Softwaresinstalled)
admin.site.register(Logs)
admin.site.register(Peripherals)
# Register your models here.
