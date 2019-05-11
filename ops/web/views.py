from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from web.models import UserSystem, Equipment, Cpu, UserStudent, Storage, Disk, LoginLog, StudentClass,Network
from web.serializers import UserSystemSerializer, EquipmentSerializer, CpuSerializer, UserStudentSerializer, DiskSerializer, StorageSerializer, LoginLogSerializer, StudentClassSerializer,NetworkSerializer
from io import BytesIO
from datetime import datetime
from django.db import transaction
from django.core.mail import send_mail
import time
import json
import xlwt
import xlrd


# 登陆login

@csrf_exempt
def login(request):
    params = request.GET  # 获取Get参数
    systemUser = UserSystem.manager.filter(
        email=params['email'], password=params['password']).exclude(status=-1)  # QuerySet对象
    systemUserSerializer = UserSystemSerializer(
        systemUser, many=True)  # 序列化后的QuerySet对象    数据在 QuerySet.data 里
    if len(systemUser) > 0:  # 计算数组长度需要用QuerySet对象

        systemUser.update(status=1)  # 在线

        userId = systemUserSerializer.data[0]['id']
        response = JsonResponse({'status': 'ok', 'data': systemUserSerializer.data,
                                 'currentAuthority': 'admin', 'type': params['type']}, safe=False)
        response.set_cookie('user_id', userId)  # 设置cookie
        return response
    else:
        return JsonResponse({'status': 'error', 'data': '您还未注册', 'currentAuthority': 'guest', 'type': params['type']})

# 登出
@csrf_exempt
def logout(request):
    userId = request.COOKIES['user_id']
    systemUser = UserSystem.manager.filter(id=userId)  # QuerySet对象
    systemUser.update(status=0)
    return HttpResponse('ok')

# 获取登陆用户信息
@csrf_exempt
def getCurrentUser(request):
    if 'user_id' in request.COOKIES:
        userId = request.COOKIES['user_id']
    else:
        res = []
        return JsonResponse(res, safe=False)
    systemUser = UserSystem.manager.filter(
        id=userId).exclude(status=-1)  # QuerySet对象
    systemUserSerializer = UserSystemSerializer(
        systemUser, many=True)  # 序列化后的QuerySet对象    数据在 QuerySet.data 里
    return JsonResponse(systemUserSerializer.data, safe=False)


# 注册 增加系统用户

@csrf_exempt
def createSystemUser(request):
    params = json.loads(request.body)
    UserSystem.manager.create(**params)
    systemUser = UserSystem.manager.filter(name=params['name'])
    systemUserSerializer = UserSystemSerializer(systemUser, many=True)
    return JsonResponse(systemUserSerializer.data, safe=False)

# 拉取系统用户


@csrf_exempt
def getSystemUser(request):
    params = request.GET.dict()  # 获取Get参数
    if(params):
        if('name' in params and 'groupname' in params):
            systemUser = UserSystem.manager.filter(
                name=params['name'], groupname=params['groupname'])
        elif('name' in params):
            systemUser = UserSystem.manager.filter(name=params['name'])
        else:
            systemUser = UserSystem.manager.filter(
                groupname=params['groupname'])
    else:
        systemUser = UserSystem.manager.all()
    systemUserSerializer = UserSystemSerializer(systemUser, many=True)
    res = []
    for item in systemUserSerializer.data:
        res.append({
            'key': item['id'],
            'name': item['name'],
            'status': item['status'],
            'catalogue': item['homedirectory'],
            'group': item['groupname'],
        })
    return JsonResponse(res, safe=False)


# 删除系统用户

@csrf_exempt
def deleteSystemUser(request):
    params = request.GET
    res = UserSystem.manager.filter(id=params['id'])
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = UserSystemSerializer(res, many=True)
    systemUser = res.delete()
    return JsonResponse(resData.data, safe=False)


# 更新系统用户

@csrf_exempt
def updateSystemUser(request):
    # request.body 是二进制数据， json.loads转换未json格式
    params = json.loads(request.body)
    if 'id' in params:
        paramsId = params['id']
    else:
        paramsId = request.COOKIES['user_id']
    res = UserSystem.manager.filter(id=paramsId)
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = UserSystemSerializer(res, many=True)
    systemUser = res.update(**params)  # **就是js里的...
    return JsonResponse(resData.data, safe=False)


# 系统用户导出excel

@csrf_exempt
def downloadExcel(request):
    params = request.GET
    print(params['needData'])
  # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=systemUser.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('systemUser-sheet')

    # 写入文件标题
    sheet.write(0, 0, '姓名')
    sheet.write(0, 1, '邮箱')
    sheet.write(0, 2, '主目录')
    sheet.write(0, 3, '用户组')

    if(params['needData'] != 'false'):
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in UserSystem.manager.all():  # 这边查询结果是object对象，用.来访问属性
            # 格式化datetime
            # pri_time = i.pri_date.strftime('%Y-%m-%d')
            # oper_time = i.operating_time.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.name)
            sheet.write(data_row, 1, i.email)
            sheet.write(data_row, 2, i.homedirectory)
            sheet.write(data_row, 3, i.groupname)
            data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 系统用户导入excel

@csrf_exempt
def uploadExcel(request):
    if request.method == 'POST':
        for i in request.FILES:  # i是key值  request.FILES是类dict对象 ,上传多分文件以键值对的形式存放
            f = request.FILES[i]
            excel_type = f.name.split('.')[1]
            if excel_type in ['xlsx', 'xls']:
                    # 开始解析上传的excel表格
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                table = wb.sheets()[0]
                rows = table.nrows  # 总行数
                try:
                    with transaction.atomic():  # 控制数据库事务交易
                        for i in range(1, rows):
                            rowVlaues = table.row_values(i)
                            UserSystem.manager.create(
                                name=rowVlaues[0], email=rowVlaues[1], homedirectory=rowVlaues[2], groupname=rowVlaues[3])
                except:
                    print('解析excel文件或者数据插入错误')
                    return JsonResponse({'message': '导入失败', 'detail': '解析excel文件或者数据插入错误'}, safe=False)
            else:
                print('上传文件类型错误！')
                return JsonResponse({'message': '导入失败', 'detail': '上传文件类型错误！'}, safe=False)

        return JsonResponse({'message': '导入成功'}, safe=False)


# 拉取学生用户

@csrf_exempt
def getStudentUser(request):
    params = request.GET.dict()  # 获取Get参数 stu_name class_grade
    if(params):
        if('stu_name' in params and 'class_grade' in params):
            studentClass = StudentClass.manager.filter(
                classname=params['class_grade'])
            if len(studentClass) > 0:
                studentClassSerializer = StudentClassSerializer(
                    studentClass, many=True)
                classId = studentClassSerializer.data[0]['id']
            else:
                classId = -1
            studentUser = UserStudent.manager.filter(
                name=params['stu_name'], classID=classId)
        elif('stu_name' in params):
            studentUser = UserStudent.manager.filter(
                name=params['stu_name'])
        else:
            studentClass = StudentClass.manager.filter(
                classname=params['class_grade'])
            if len(studentClass) > 0:
                studentClassSerializer = StudentClassSerializer(
                    studentClass, many=True)
                classId = studentClassSerializer.data[0]['id']
            else:
                classId = -1
            studentUser = UserStudent.manager.filter(classID=classId)
    else:
        studentUser = UserStudent.manager.all()
    studentUserSerializer = UserStudentSerializer(studentUser, many=True)
    res = []
    for item in studentUserSerializer.data:
        classinfo = StudentClass.manager.filter(
            id=item['classID'])
        classinfoSerializer = StudentClassSerializer(classinfo, many=True)
        res.append({
            'key': item['id'],
            'name': item['name'],
            'class': classinfoSerializer.data[0]['classname'],
            'academy': classinfoSerializer.data[0]['academy'],
            'number': item['number'],
        })
    return JsonResponse(res, safe=False)


# 删除学生用户

@csrf_exempt
def deleteStudentUser(request):
    params = request.GET
    res = UserStudent.manager.filter(id=params['id'])
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = UserStudentSerializer(res, many=True)
    studentUser = res.delete()
    return JsonResponse(resData.data, safe=False)


# 更新学生用户

@csrf_exempt
def updateStudentUser(request):
    # request.body 是二进制数据， json.loads转换未json格式
    params = json.loads(request.body)
    stu_name = params['stu_name']
    academy = params['academy']
    class_grade = params['class_grade']
    stu_num = params['stu_num']
    spell = params['spell']
    classSpell=params['classSpell']

    res = UserStudent.manager.filter(id=params['id'])
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = UserStudentSerializer(res, many=True)

    studentClass = StudentClass.manager.filter( #检索有无此班级学院
        id=resData.data[0]['classID'])
    if len(studentClass) > 0:  # 有就取用id
        studentClassSerializer = StudentClassSerializer(
            studentClass, many=True)
        classId = studentClassSerializer.data[0]['id']
    else: # 没有就新建后取用id
        StudentClass.manager.create(classname=class_grade, academy=academy,classspell=classSpell)
        createClass = StudentClass.manager.filter(classname=class_grade)
        createClassSerializer = StudentClassSerializer(createClass, many=True)
        classId = createClassSerializer.data[0]['id']


    # **就是js里的...
    res.update(name=stu_name, number=stu_num, classID=classId,spell=spell)
    return JsonResponse(resData.data, safe=False)


# 增加学生用户

@csrf_exempt
def createStudentUser(request):
    params = json.loads(request.body)
    stu_name = params['stu_name']
    academy = params['academy']
    class_grade = params['class_grade']
    stu_num = params['stu_num']
    spell = params['spell']
    classSpell=params['classSpell']

    classinfo = StudentClass.manager.filter(classname=class_grade) #有无此班级
    classinfoSerializer = StudentClassSerializer(classinfo, many=True)
    if len(classinfo) > 0: #有就取用id
        classId = classinfoSerializer.data[0]['id']
    else: #没有新建后取用id
        StudentClass.manager.create(classname=class_grade, academy=academy,classspell=classSpell)
        createClass = StudentClass.manager.filter(classname=class_grade)
        createClassSerializer = StudentClassSerializer(createClass, many=True)
        classId = createClassSerializer.data[0]['id']
    #新建用户    
    UserStudent.manager.create(name=stu_name, number=stu_num, classID=classId,spell=spell)
    studentUser = UserStudent.manager.filter(name=params['stu_name'])
    studentUserSerializer = UserStudentSerializer(studentUser, many=True)
    return JsonResponse(studentUserSerializer.data, safe=False)


# 学生用户导出excel

@csrf_exempt
def downloadExcelStu(request):
    params = request.GET
  # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=studentUser.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('studentUser-sheet')

    # 写入文件标题
    sheet.write(0, 0, '姓名')
    sheet.write(0, 1, '学号')
    sheet.write(0, 2, '学院')
    sheet.write(0, 3, '班级')
    sheet.write(0, 4, '姓名拼音')
    sheet.write(0, 5, '班级拼音')
    

    if(params['needData'] != 'false'):
        # 写入数据
        data_row = 1
        # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in UserStudent.manager.all():  # 这边查询结果是object对象，用.来访问属性
            # 格式化datetime
            # pri_time = i.pri_date.strftime('%Y-%m-%d')
            # oper_time = i.operating_time.strftime('%Y-%m-%d')
            classinfo = StudentClass.manager.filter(id=i.classID)
            sheet.write(data_row, 0, i.name)
            sheet.write(data_row, 1, i.number)
            sheet.write(data_row, 2, classinfo[0].academy)
            sheet.write(data_row, 3, classinfo[0].classname)
            sheet.write(data_row, 4, i.spell)
            sheet.write(data_row, 5, classinfo[0].classspell)
            data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 导入excel

@csrf_exempt
def uploadExcelStu(request):
    if request.method == 'POST':
        for i in request.FILES:  # i是key值  request.FILES是类dict对象 ,上传多分文件以键值对的形式存放
            f = request.FILES[i]
            excel_type = f.name.split('.')[1]
            if excel_type in ['xlsx', 'xls']:
                    # 开始解析上传的excel表格
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                table = wb.sheets()[0]
                rows = table.nrows  # 总行数
                try:
                    with transaction.atomic():  # 控制数据库事务交易
                        for i in range(1, rows):
                            rowVlaues = table.row_values(i)
                            classinfo = StudentClass.manager.filter(classname=rowVlaues[3])
                            if len(classinfo) > 0:
                                classId = classinfo[0].id
                            else:
                                StudentClass.manager.create(classname=rowVlaues[3],academy=rowVlaues[2],classspell=rowVlaues[5])
                                newClassinfo = StudentClass.manager.filter(classname=rowVlaues[3])
                                classId = newClassinfo[0].id
                            UserStudent.manager.create(
                                name=rowVlaues[0], number=rowVlaues[1], spell=rowVlaues[4], classID=classId)
                except:
                    print('解析excel文件或者数据插入错误')
                    return JsonResponse({'message': '导入失败', 'detail': '解析excel文件或者数据插入错误'}, safe=False)
            else:
                print('上传文件类型错误！')
                return JsonResponse({'message': '导入失败', 'detail': '上传文件类型错误！'}, safe=False)

        return JsonResponse({'message': '导入成功'}, safe=False)


# 获取设备
@csrf_exempt
def getEquipmentData(request):  # param equip_name:设备名称 status：使用状态 0 1 2
    params = json.loads(request.body)
    if 'today' in params:
        today = params['today']
    else:
        today = None

    if 'name' in params and 'ip' in params:
        equipments = Equipment.manager.filter(
            equip_name=params['name'], ip=params['ip'])
    elif 'name'in params:
        equipments = Equipment.manager.filter(
            equip_name=params['name'])  # 遍历到底是遍历queryset呢还是序列化后的data呢
    elif 'ip' in params:
        equipments = Equipment.manager.filter(ip=params['ip'])
    else:
        equipments = Equipment.manager.all()

    equipmentsSerializer = EquipmentSerializer(equipments, many=True)

    res = []
    for item in equipmentsSerializer.data:

        cpu = Cpu.manager.filter(hostID=item['id'], date=today)
        cpulength = len(cpu)
        if(cpulength > 0):
            cpuSerializer = CpuSerializer(cpu, many=True)
            cpuUseRate = cpuSerializer.data[cpulength - 1]['usage']
        else:
            cpuUseRate = 0

        storage = Storage.manager.filter(hostID=item['id'], date=today)
        storagelength = len(storage)
        if(storagelength > 0):
            storageSerializer = StorageSerializer(storage, many=True)
            storageUseRate = storageSerializer.data[storagelength-1]['usage']
        else:
            storageUseRate = 0

        disk = Disk.manager.filter(hostID=item['id'], date=today)
        disklength = len(disk)
        if(disklength > 0):
            diskSerializer = DiskSerializer(disk, many=True)
            diskUseRate = diskSerializer.data[disklength - 1]['usage']
        else:
            diskUseRate = 0

        res.append({
            'key': item['id'],
            'name': item['equip_name'],
            'ip': item['ip'],
            'type': item['node_type'],
            'model': item['cpu_model'],
            'cpu': '{rate}%'.format(rate=cpuUseRate),
            'number': item['core_num'],
            'storage': '{rate}%'.format(rate=storageUseRate),
            'disk': '{rate}%'.format(rate=diskUseRate),
            'software': 1,
            'agent': "是" if item['isagent'] == 1 else "否",
        })
    return JsonResponse(res, safe=False)

# 新建设备
@csrf_exempt
def createEquipment(request):
    params = json.loads(request.body)
    print(params)
    Equipment.manager.create(**params)
    equipment = Equipment.manager.filter(equip_name=params['equip_name'])
    equipmentSerializer = EquipmentSerializer(equipment, many=True)
    return JsonResponse(equipmentSerializer.data, safe=False)

# 删除设备
@csrf_exempt
def deleteEquipment(request):
    params = request.GET
    res = Equipment.manager.filter(id=params['id'])
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = EquipmentSerializer(res, many=True)
    res.delete()
    return JsonResponse(resData.data, safe=False)

# 更新设备


@csrf_exempt
def updateEquipment(request):
    # request.body 是二进制数据， json.loads转换未json格式
    params = json.loads(request.body)
    print(params)
    res = Equipment.manager.filter(id=params['id'])
    # 序列化必须在res.delete之前，否则res就不存在了。
    resData = EquipmentSerializer(res, many=True)
    res.update(**params)  # **就是js里的...
    return JsonResponse(resData.data, safe=False)


# 获取cpu检测数据
def getCpu(request):
    params = request.GET
    hostID = params['id']
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前日期
    cpu = Cpu.manager.filter(hostID=hostID, date=date)
    cpuSerializer = CpuSerializer(cpu, many=True)
    return JsonResponse(cpuSerializer.data, safe=False)

# 获取storage检测数据


def getStorage(request):
    params = request.GET
    hostID = params['id']
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前日期
    storage = Storage.manager.filter(hostID=hostID, date=date)
    storageSerializer = StorageSerializer(storage, many=True)
    return JsonResponse(storageSerializer.data, safe=False)

# 获disk检测数据


def getDisk(request):
    params = request.GET
    hostID = params['id']
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前日期
    disk = Disk.manager.filter(hostID=hostID, date=date)
    diskSerializer = DiskSerializer(disk, many=True)
    return JsonResponse(diskSerializer.data, safe=False)

# 获取网络检测数据

def getNetwork(request):
    params = request.GET
    hostID = params['id']
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前日期
    network = Network.manager.filter(hostID=hostID, date=date)
    networkSerializer = NetworkSerializer(network, many=True)
    return JsonResponse(networkSerializer.data, safe=False)# # 获软件数据

# def getSoftware(request):
#     params = request.GET
#     equip_id = params['id']
#     software = Software.manager.filter(equip_id=equip_id)
#     softwareSerializer = SoftwareSerializer(software, many=True)
#     res = []
#     for item in softwareSerializer.data:
#         res.append({
#             'key': item['id'],
#             'softName': item['soft_name'],
#             'logName': item['soft_log_name'],
#             'describe': item['describe'],
#         })
#     return JsonResponse(res, safe=False)

# 发送邮件
@csrf_exempt
def registerEmail(request):
    # request.body 是二进制数据， json.loads转换未json格式
    params = json.loads(request.body)
    mail = params['mail']
    password = params['password']
    name = params['name']

    UserSystem.manager.create(name=name, email=mail,
                              password=password, status=-1)
    systemUser = UserSystem.manager.filter(email=mail)
    systemUserSerializer = UserSystemSerializer(systemUser, many=True)
    registerId = systemUserSerializer.data[0]['id']
    msg = "<a href='http://njit.wwwien.top:8000/activeaccount?id={registerId}' target='_blank'>点击激活</a>".format(
        registerId=registerId)
    send_mail(
        '大数据平台管理系统注册',
        '请点击下方按钮激活',
        '2268348563@qq.com',
        [mail],
        fail_silently=False,
        html_message=msg
    )
    return JsonResponse({'status': 'ok'}, safe=False)

# 激活
@csrf_exempt
def activeAccount(request):
    params = request.GET
    UserSystem.manager.filter(id=params['id']).update(status=0)  # 根据id激活
    return JsonResponse({'status': 'ok'}, safe=False)




# 测试
@csrf_exempt
def test(request):
    print('path:', request.path)
    print('request.user:', request.user)
    print()
    print()
    print()
    print()
    print('request.META', request.META)
    print("ip:", request.META.get('REMOTE_ADDR'))
    return HttpResponse('ok')
    # for item in equipmentsSerializer.data:
    #     cpu = Cpu.manager.filter(equip_id=item['id'])
    #     cpuSerializer = CpuSerializer(cpu, many=True)
    #     timeArray = time.strptime(
    #         cpuSerializer.data[0]['check_time'], '%Y-%m-%dT%H:%M:%S')  # 东八区时间转换成时间元组
    #     timestamp = time.mktime(timeArray)*1000  # 时间元组转换成时间戳（以秒为单位）所以要乘以1000
