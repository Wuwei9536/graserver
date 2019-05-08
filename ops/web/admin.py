from django.contrib import admin

# Register your models here.
from .models import UserSystem,UserStudent,LoginLog,Software,SoftwareLog,Storage,SysLog,Equipment,Cpu,Disk

admin.site.register(UserSystem)
admin.site.register(UserStudent)
admin.site.register(LoginLog)
admin.site.register(Software)
admin.site.register(SoftwareLog)
admin.site.register(Storage)
admin.site.register(SysLog)
admin.site.register(Equipment)
admin.site.register(Cpu)
admin.site.register(Disk)