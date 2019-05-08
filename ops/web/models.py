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
    stu_name = models.CharField(max_length=30)
    # 密码
    stu_password = models.CharField(max_length=30)
    # 学号
    stu_num = models.IntegerField()
    # 学院
    academy = models.CharField(max_length=30)
    # 班级
    class_grade = models.CharField(max_length=30)
    # 登陆状态 默认0：离线  1:登陆
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'user_stu'  # 自定义表名称
        verbose_name = '学生用户列表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 登陆日志


class LoginLog(models.Model):
    # 登录名
    login_name = models.CharField(max_length=30)
    # 登入时间
    login_time = models.DateTimeField(auto_now_add=True)
    # 登出时间
    logout_time = models.DateTimeField()
    # 登陆ip
    login_ip = models.CharField(max_length=30)
    # 终端类型
    terminal_type = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'login_log'  # 自定义表名称
        verbose_name = '登陆日志'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


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
    core_num = models.IntegerField()
    # 内存
    storage = models.IntegerField()
    # 磁盘空间
    disk = models.IntegerField()
    # 是否安装agent
    isagent = models.IntegerField(default=0)
    # 备注
    remarks = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'equipment'  # 自定义表名称
        verbose_name = '服务器列表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# cpu动态表


class Cpu(models.Model):
    equip_id = models.IntegerField()
    usage_rate = models.FloatField()
    check_date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'cpu'  # 自定义表名称
        verbose_name = 'cpu动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 内存动态表


class Storage(models.Model):
    equip_id = models.IntegerField()
    usage_rate = models.FloatField()
    check_date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'storage'  # 自定义表名称
        verbose_name = 'storage动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 磁盘动态表


class Disk(models.Model):
    equip_id = models.IntegerField()
    usage_rate = models.FloatField()
    check_date = models.DateField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'disk'  # 自定义表名称
        verbose_name = 'disk动态表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


# 系统日志表

class SysLog(models.Model):
    # 级别 0:正常 1:警告 2:危险
    level = models.IntegerField(default=0)
    # 内容
    content = models.CharField(max_length=30)
    # 备注
    remarks = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'sys_log'  # 自定义表名称
        verbose_name = '系统日志'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


class Software(models.Model):
    # 服务器id
    equip_id = models.IntegerField()
    # 软件名称
    soft_name = models.CharField(max_length=100)
    # 日志文件名
    soft_log_name = models.CharField(max_length=100)
    # 描述
    describe = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'software'  # 自定义表名称
        verbose_name = '软件列表'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)


class SoftwareLog(models.Model):
    # 服务器id
    equip_id = models.IntegerField()
    # 软件名称
    soft_name = models.CharField(max_length=100)
    # 日志信息
    soft_log = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    manager = models.Manager()

    class Meta:
        db_table = 'software_log'  # 自定义表名称
        verbose_name = '软件日志'  # 指定在admin管理界面中显示的名称
        ordering = ('create_time',)
