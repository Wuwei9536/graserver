from rest_framework import serializers
from .models import UserSystem, UserStudent, LoginLog, Software, SoftwareLog, Storage, SysLog, Equipment, Cpu, Disk


class UserSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSystem
        fields = ('id', 'email','name', 'status',
                  'homedirectory', 'groupname')


class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:  
        model = UserStudent
        fields = ('id', 'stu_name', 'stu_password', 'stu_num',
                  'academy', 'class_grade', 'status')


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'equip_name', 'ip', 'node_type', 'cpu_model',
                  'core_num', 'storage', 'disk', 'isagent', 'remarks')


class CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpu
        fields = ('id', 'equip_id', 'usage_rate', 'check_date','create_time')


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = ('id', 'equip_id', 'usage_rate', 'check_date','create_time')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'equip_id', 'usage_rate', 'check_date','create_time')


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = ('id', 'equip_id', 'soft_name', 'soft_log_name', 'describe')


class SoftwareLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareLog
        fields = ('id', 'equip_id', 'soft_name', 'soft_log')


class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = ('id', 'login_name', 'login_time',
                  'logout_time', 'login_ip', 'terminal_type')


class SysLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysLog
        fields = ('id', 'level', 'content', 'remarks')
