from django import forms
from .models import Employee, Task, CompanyInfo, CompanyStructure

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['text', 'video', 'image']

class CompanyStructureForm(forms.ModelForm):
    class Meta:
        model = CompanyStructure
        fields = ['text', 'video', 'image']
        
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
        