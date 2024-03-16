from django.db import models
from django.core import validators
    
class TelegramUser(models.Model):
    full_name = models.CharField(max_length=40, null=True, blank=True)
    telegram_id =  models.CharField(max_length=10, verbose_name='Telegram_ID')
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.telegram_id

class Employee(models.Model):
    positions = (
        ('admin',"Admin"),
        ('manager', "Manager"),
        ('worker', "Ishchi"),
        ('student', "Shogird"),   
    )
    status = models.BooleanField(default=False)
    position = models.CharField(max_length=55, default='worker', choices=positions, verbose_name='Enter the position', help_text="Choose positions")
    full_name = models.CharField(max_length=155, verbose_name='Enter the name')
    phone_number = models.CharField(max_length=20, verbose_name='Enter the phone number')
    telegram_id = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='employees')
    image = models.ImageField(upload_to='images/', blank=True, validators=[
        validators.FileExtensionValidator(allowed_extensions=['ico','png','jpeg','jpg'], 
            message="Enter an image in the format below('ico','png','jpeg','jpg')")
        ])
    add_date = models.DateTimeField(auto_now_add=True)
       
    def get_employee_attendance_display(self):
        return "Kelgan" if self.status else "Kelmagan"
    
    def __str__(self):
        return f"{self.telegram_id} - {self.full_name}"

class Task(models.Model):
    STATUS_CHOICES = (
        ('active',"Aktiv"),
        ('progress', "Jarayonda"),
        ('done', "Bajarildi"), 
    )
    task_status = models.CharField(max_length=15, default='active', choices=STATUS_CHOICES, verbose_name='Enter the status', help_text="Choose status")
    name = models.TextField(verbose_name="Enter the task !")
    employees = models.ManyToManyField('Employee', blank=True, related_name='tasks_assigned', limit_choices_to={'position__in': ['manager', 'worker', 'student']})
    accepted = models.ManyToManyField(Employee, blank=True, related_name='tasks_accepted', symmetrical=False)
    image = models.ImageField(upload_to='images/', blank=True, validators=[
        validators.FileExtensionValidator(allowed_extensions=['ico','png','jpeg','jpg'], 
            message="Enter an image in the format below('ico','png','jpeg','jpg')")
        ])
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
class Advance(models.Model):
    desc = models.TextField(verbose_name="Enter the task !", blank=True)
    amount = models.BigIntegerField(verbose_name="Amount")
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.desc

class CompanyInfo(models.Model):
    text = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="files/", blank=True)
    image = models.ImageField(upload_to='images/', blank=True, validators=[
        validators.FileExtensionValidator(allowed_extensions=['ico','png','jpeg','jpg'], 
            message="Enter an image in the format below('ico','png','jpeg','jpg')")
        ])
    add_date = models.DateTimeField(auto_now_add=True)

class CompanyStructure(models.Model):
    text = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="files/", blank=True)
    image = models.ImageField(upload_to='images/', blank=True, validators=[
        validators.FileExtensionValidator(allowed_extensions=['ico','png','jpeg','jpg'], 
            message="Enter an image in the format below('ico','png','jpeg','jpg')")
        ])
    add_date = models.DateTimeField(auto_now_add=True)

class Offer(models.Model):
    desc = models.TextField(verbose_name="Enter the task !", blank=True)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.desc
    
class Complaint(models.Model):
    desc = models.TextField(verbose_name="Enter the task !", blank=True)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.desc
    

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.employee.full_name