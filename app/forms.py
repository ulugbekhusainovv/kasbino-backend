from django import forms
from .models import Employee, Task, CompanyInfo, CompanyStructure, Category, CategoryStructure

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class CategoryStructureForm(forms.ModelForm):
    class Meta:
        model = CategoryStructure
        fields = ['name']
        
class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['category', 'text', 'video', 'image', 'pdf']

class CompanyStructureForm(forms.ModelForm):
    class Meta:
        model = CompanyStructure
        fields = ['category', 'text', 'video', 'image', 'pdf']
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'phone_number', 'telegram_id']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update({'class': 'form-control'})
        self.fields['telegram_id'].widget.attrs.update({'class': 'form-control'})
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "employees"]
        
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['employees'].widget.attrs.update({'class': 'form-control'})
        