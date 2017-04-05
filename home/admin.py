from django.contrib import admin
from .models import Administrator,Machine,Messages,MachineUser,UsersActiveOn

admin.site.register(Administrator)
admin.site.register(Machine)
admin.site.register(Messages)
admin.site.register(MachineUser)
admin.site.register(UsersActiveOn)
# Register your models here.
