from django.urls import path
from web import views

urlpatterns = [
    # 登陆接口
    path('login', views.login),
    # 创建系统用户
    path('createsystemuser', views.createSystemUser),
    # 获取系统用户
    path('getsystemuser', views.getSystemUser),
    # 删除系统用户
    path('deletesystemuser', views.deleteSystemUser),
    # 更新系统用户
    path('updatesystemuser', views.updateSystemUser),
    # 导出excel 系统
    path('downloadexcel', views.downloadExcel),
    # 导入excel 系统
    path('uploadexcel', views.uploadExcel),
    # 获取系统用户
    path('getstudentuser', views.getStudentUser),
    # 删除学生用户
    path('deletestudentuser', views.deleteStudentUser),
    # 更新学生用户
    path('updatestudentuser', views.updateStudentUser),
    # 增加学生用户
    path('createstudentuser', views.createStudentUser),
    # 导出excel 学生
    path('downloadexcelstu', views.downloadExcelStu),
    # 导入excel 学生
    path('uploadexcelstu', views.uploadExcelStu),
    # 获取登陆用户信息
    path('getcurrentuser', views.getCurrentUser),
    # 获取设备列表
    path('getequipment', views.getEquipmentData),
    # 新建设备
    path('createequipment', views.createEquipment),
    # 删除设备
    path('deleteequipment', views.deleteEquipment),
    # 更新设备
    path('updateequipment', views.updateEquipment),
    # 获取cpu数据
    path('getcpu', views.getCpu),
    # 获取storage数据
    path('getstorage', views.getStorage),
    # 获取disk数据
    path('getdisk', views.getDisk),
    # 获取软件数据
    path('getsoftware', views.getSoftware),
    # 发送注册邮件 
    path('registeremail', views.registerEmail),
    # 激活
    path('activeaccount', views.activeAccount),
    # 测试
    path('test',views.test)
]
