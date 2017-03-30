from django.contrib import admin
from .models import Administrator,Machine,Messages,MachineUser

admin.site.register(Administrator)
admin.site.register(Machine)
admin.site.register(Messages)
admin.site.register(MachineUser)
# Register your models here.
