from django.contrib import admin
from .models import Task, Employee, CompanyInfo, CompanyStructure, TelegramUser, Advance, Complaint, Offer,Attendance
from django.utils.html import format_html

# Register your models here.


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_employees', 'add_date', 'task_status']

    def display_employees(self, obj):
        employees = obj.employees.all()
        return ", ".join([employee.full_name for employee in employees])
    
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'telegram_id', 'add_date']


    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'add_date']

@admin.register(Advance)
class AdvanceModelAdmin(admin.ModelAdmin):
    list_display = ['desc', 'employees', 'add_date', 'amount']

@admin.register(Offer)
class AdvanceModelAdmin(admin.ModelAdmin):
    list_display = ['desc', 'employees', 'add_date']

@admin.register(Complaint)
class AdvanceModelAdmin(admin.ModelAdmin):
    list_display = ['desc', 'employees', 'add_date']
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', "phone_number", "telegram_id", "show_image"]
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50px" />'.format(obj.image.url))  
        return "No Image"

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['text', "show_image"]
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50px" />'.format(obj.image.url))  
        return "No Image"

@admin.register(CompanyStructure)
class CompanyStructureAdmin(admin.ModelAdmin):
    list_display = ['text', "show_image"]
    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50px" />'.format(obj.image.url))  
        return "No Image"
