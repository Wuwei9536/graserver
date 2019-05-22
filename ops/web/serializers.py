from rest_framework import serializers
from .models import UserSystem, UserStudent, LoginLog, Storage, SysLog, Equipment, Cpu, Disk, StudentClass, Network, SysLoginLog, Linux


class UserSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSystem
        fields = ('id', 'email', 'name', 'status',
                  'homedirectory', 'groupname')


class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStudent
        fields = ('id', 'name', 'number',
                  'spell', 'classID')


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ('id', 'classname', 'academy',
                  'classspell')


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'equip_name', 'ip', 'node_type', 'cpu_model',
                  'core_num', 'storage', 'disk', 'isagent', 'remarks')


class CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpu
        fields = ('id', 'hostID', 'usage', 'date', 'create_time')


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = ('id', 'hostID', 'usage', 'date', 'create_time')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'hostID', 'usage', 'date', 'create_time')


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id', 'hostID', 'receive_speed',
                  'transmit_speed', 'date', 'create_time')


# class SoftwareSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Software
#         fields = ('id', 'equip_id', 'soft_name', 'soft_log_name', 'describe')


# class SoftwareLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SoftwareLog
#         fields = ('id', 'equip_id', 'soft_name', 'soft_log')


class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = ('id', 'loginname', 'port', 'createtime',
                  'ipaddress', 'state')


class SysLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysLog
        fields = ('id', 'level', 'content', 'remarks')


class SysLoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysLoginLog
        fields = ('id', 'loginEmail', 'ip', 'create_time',
                  'password', 'state', 'update_time')


class LinuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linux
        fields = ('id', 'logname', 'userspace','used', 'createtime',
                  'groupa', 'directory', 'state', 'updatetime')
