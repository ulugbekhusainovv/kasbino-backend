
from app.models import Employee, Task,TelegramUser, Advance, CompanyInfo, CompanyStructure, Offer, Complaint, Attendance
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(source='telegram_id.telegram_id')

    class Meta:
        model = Employee
        fields = ['id', 'status', 'position', 'full_name', 'phone_number', 'add_date', 'telegram_id']

class TaskSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    accepted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "name", "task_status", "employees", "accepted"]

    def get_accepted(self, obj):
        accepted_employee_ids = obj.accepted.all()
        accepted_employees = Employee.objects.filter(id__in=accepted_employee_ids)
        serializer = EmployeeSerializer(accepted_employees, many=True)
        return serializer.data


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'

class CompanyStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStructure
        fields = '__all__'


class AdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance
        fields = ["id", "desc", "amount", "add_date", "employees"]

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'add_date','employee']