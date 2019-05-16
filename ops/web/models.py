from django.db import models

# Create your models here.


# 系统用户


class UserSystem(models.Model):
    # 邮箱
    email = models.CharField(max_length=30)
    # 姓名
    name = models.CharField(max_length=30)
    # 密码
    password = models.CharField(default='123456', max_length=20)
    # 登陆状态 默认0：离线  1:登陆  -1:未激活
    status = models.IntegerField(default=0)
    homedirectory = models.CharField(max_length=30, blank=True)
    groupname = models.CharField(max_length=30, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'user_sys'  # 自定义表名称为user_sys
        verbose_name = '系统用户'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 学生用户


class UserStudent(models.Model):
    # 姓名
    name = models.CharField(max_length=20)
    # 学号
    number = models.CharField(max_length=20)
    # 拼音
    spell = models.CharField(max_length=20)
    # 班级id
    classID = models.IntegerField()
    # # 登陆状态 默认0：离线  1:登陆
    # status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'student'  # 自定义表名称
        verbose_name = '学生用户列表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)

# 班级

class StudentClass(models.Model):
    # 姓名
    classname = models.CharField(max_length=40)
    # 学号
    academy = models.CharField(max_length=40)
    # 拼音
    classspell = models.CharField(max_length=40)
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'class'  # 自定义表名称
        verbose_name = '学生班级列表'  # 指定在admin管理界面中显示的名称
        ordering = ('id',)


# 登陆日志


class LoginLog(models.Model):
    # 登录名
    loginname = models.CharField(max_length=20)
    # 登陆ip
    ipaddress = models.CharField(max_length=40)
    # 终端类型
    state = models.CharField(max_length=20)
    # 
    port = models.CharField(max_length=20)
    createtime = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'userlogin'  # 自定义表名称
        verbose_name = '登陆日志'  # 指定在admin管理界面中显示的名称
        ordering = ('createtime',)


# 服务器列表


class Equipment(models.Model):
    # 节点名称
    equip_name = models.CharField(max_length=30)
    # ip地址
    ip = models.CharField(max_length=30)
    # 节点类型
    node_type = models.CharField(max_length=30)
    # cpu型号
    cpu_model = models.CharField(max_length=30)
    # cpu 核数
    core_num = models.CharField(max_length=30)
    # 内存
    storage = models.CharField(max_length=30)
    # 磁盘空间
    disk = models.CharField(max_length=30)
    # 是否安装agent
    isagent = models.IntegerField(default=0)
    # 备注
    remarks = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'server_info'  # 自定义表名称
        verbose_name = '服务器列表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# cpu动态表


class Cpu(models.Model):
    hostID = models.IntegerField()
    usage = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'cpu_dynamic_info'  # 自定义表名称
        verbose_name = 'cpu动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 内存动态表


class Storage(models.Model):
    hostID = models.IntegerField()
    usage = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'mem_dynamic_info'  # 自定义表名称
        verbose_name = 'storage动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 磁盘动态表


class Disk(models.Model):
    hostID = models.IntegerField()
    usage = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'disk_dynamic_info'  # 自定义表名称
        verbose_name = 'disk动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 网络动态表


class Network(models.Model):
    hostID = models.IntegerField()
    receive_speed = models.CharField(max_length=50)
    transmit_speed = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'network_dynamic_info'  # 自定义表名称
        verbose_name = '网络动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 系统日志表

class SysLog(models.Model):
    # 服务器id
    hostID = models.IntegerField()
    # 级别 0:正常 1:警告 2:危险
    level = models.IntegerField(default=0)
    # 内容
    content = models.CharField(max_length=50)
    # 备注
    remarks = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'Log'  # 自定义表名称
        verbose_name = '系统日志'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# class Software(models.Model):
#     # 服务器id
#     equip_id = models.IntegerField()
#     # 软件名称
#     soft_name = models.CharField(max_length=100)
#     # 日志文件名
#     soft_log_name = models.CharField(max_length=100)
#     # 描述
#     describe = models.CharField(max_length=255)
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now=True)

#     manager = models.Manager()

#     class Meta:
#         db_table = 'software'  # 自定义表名称
#         verbose_name = '软件列表'  # 指定在admin管理界面中显示的名称
#         ordering = ('create_time',)


# class SoftwareLog(models.Model):
#     # 服务器id
#     equip_id = models.IntegerField()
#     # 软件名称
#     soft_name = models.CharField(max_length=100)
#     # 日志信息
#     soft_log = models.CharField(max_length=255)
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now=True)

#     manager = models.Manager()

#     class Meta:
#         db_table = 'software_log'  # 自定义表名称
#         verbose_name = '软件日志'  # 指定在admin管理界面中显示的名称
#         ordering = ('create_time',)
