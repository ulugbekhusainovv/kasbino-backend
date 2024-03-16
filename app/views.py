from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import timedelta, datetime
import requests, os
from .forms import EmployeeForm, TaskForm, CompanyInfoForm, CompanyStructureForm
from .models import Task, Employee, TelegramUser, Advance, CompanyInfo, CompanyStructure, Offer, Complaint 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

bot_token = "6967615919:AAGxLCWgolQagotzm0ubQLQXPso_W7HNBVE"
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_admin')  # Agar foydalanuvchi superuser emas bo'lsa, oddiy foydalanuvchi sahifasiga yo'naltirish
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        employees = Employee.objects.count()
        tasks = Task.objects.count()
        advances = Advance.objects.count()
        today_advances = Advance.objects.filter(add_date__date=today)
        today_tasks = Task.objects.filter(add_date__date=today)
        today_employee = Employee.objects.filter(add_date__date=today)
        all_tasks = today_tasks.count()
        all_employee = today_employee.count()
        all_advances = today_advances.count()
        
        context['tasks'] = tasks
        context['advances'] = advances
        context['all_tasks'] = all_tasks
        context['all_advances'] = all_advances
        context['employees'] = employees
        context['today_tasks'] = today_tasks
        context['all_employee'] = all_employee
        return context

class SimpleView(LoginRequiredMixin, TemplateView):
    template_name = 'simple_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        today_tasks = Task.objects.filter(add_date__date=today)
        tasks = Task.objects.count()
        all_tasks = today_tasks.count()
        context['tasks'] = tasks
        context['all_tasks'] = all_tasks
        context['today_tasks'] = today_tasks
        return context

    
    
class AddTaskView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_add_task')  # Agar foydalanuvchi superuser emas bo'lsa, oddiy foydalanuvchi sahifasiga yo'naltirish
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        xodimlar = Employee.objects.exclude(position='admin')
        return render(request, 'add_task.html', {"xodimlar": xodimlar})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            selected_employees_ids = request.POST.getlist('employees')
            task.employees.set(selected_employees_ids)
            # Send messages to selected employees
            chat_id = '2083239343'
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            def get_status_display(status):
                status_map = {
                    'active': 'Aktiv',
                    'progress': 'Jarayonda',
                    'done': 'Bajarildi'
                }
                return status_map.get(status, status)
            
            for employee_id in selected_employees_ids:
                employee = Employee.objects.get(id=employee_id)
                text = f"<b>Assalamu alaykum sizga yangi Topshiriq bor kuningiz hayrli o'tsin\n\nId: #{task.id}\nText: {task.name}\nHolati: {get_status_display(task.task_status)}</b>"
                keyboard = [[InlineKeyboardButton("Qabul qilish", callback_data=f'done_work:{task.id}')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                params = {
                    'chat_id': employee.telegram_id or chat_id,
                    'text': text,
                    'reply_markup': reply_markup.to_json(),
                    'parse_mode': 'HTML', 
                }
                response = requests.post(url, params=params)

                if response.status_code != 200:
                    messages.warning(request, f"Error sending message to {employee.full_name}")

            return redirect('main:task')
        
        return render(request, 'task.html', {'form': form})

class SimpleAddTaskView(LoginRequiredMixin, View):
    def get(self, request):
        xodimlar = Employee.objects.exclude(position='admin')
        return render(request, 'simple_add_task.html', {"xodimlar": xodimlar})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            selected_employees_ids = request.POST.getlist('employees')
            task.employees.set(selected_employees_ids)
            # Send messages to selected employees
            chat_id = '2083239343'
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            def get_status_display(status):
                status_map = {
                    'active': 'Aktiv',
                    'progress': 'Jarayonda',
                    'done': 'Bajarildi'
                }
                return status_map.get(status, status)
            
            for employee_id in selected_employees_ids:
                employee = Employee.objects.get(id=employee_id)
                text = f"<b>Assalamu alaykum sizga yangi Topshiriq bor kuningiz hayrli o'tsin\n\nId: #{task.id}\nText: {task.name}\nHolati: {get_status_display(task.task_status)}</b>"
                keyboard = [[InlineKeyboardButton("Qabul qilish", callback_data=f'done_work:{task.id}')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                params = {
                    'chat_id': employee.telegram_id or chat_id,
                    'text': text,
                    'reply_markup': reply_markup.to_json(),
                    'parse_mode': 'HTML', 
                }
                response = requests.post(url, params=params)

                if response.status_code != 200:
                    messages.warning(request, f"Error sending message to {employee.full_name}")

            return redirect('main:simple_task')
        
        return render(request, 'simple_add_task.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_update_task')  # Agar foydalanuvchi superuser emas bo'lsa, oddiy foydalanuvchi sahifasiga yo'naltirish
        return super().dispatch(request, *args, **kwargs)
    
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    success_url = reverse_lazy('main:task')

    def form_valid(self, form):
        return super(TaskUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TaskUpdateView, self).form_invalid(form)
    
class CompanyInfoView(LoginRequiredMixin, View):
    model = CompanyInfo
    form_class = CompanyInfoForm
    template_name = 'company_info.html'
    success_url = reverse_lazy('main:company_info')
    
    def get(self, request):
        form = CompanyInfoForm()
        try:
            latest_company_info = CompanyInfo.objects.latest('add_date')
        except CompanyInfo.DoesNotExist:
            latest_company_info = None
        return render(request, 'company_info.html', {'form': form, 'latest_company_info': latest_company_info})


    def is_video(self, file_path):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        _, extension = os.path.splitext(file_path)
        return extension.lower() in video_extensions        

    def post(self, request):
        form = CompanyInfoForm(request.POST, request.FILES)

        if form.is_valid():
            video_file = request.FILES.get('video')
            if video_file and not self.is_video(video_file.name):
                form.add_error('video', 'Fayl formati noto\'g\'ri. Faqat video fayllarni yuklash mumkin.')
                return render(request, 'company_info.html', {'form': form})

            form.save()
            messages.success(request, 'Malumot muvaffaqiyatli saqlandi.')
            return redirect('main:company_info')
        else:
            messages.error(request, 'Xatolik yuz berdi, iltimos, ma\'lumotlarni tekshiring.')
            return render(request, 'company_info.html', {'form': form})
        

class CompanyInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyInfo
    form_class = CompanyInfoForm
    template_name = 'update_company_info.html'
    success_url = reverse_lazy('main:company_info')
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class CompanyStructureView(LoginRequiredMixin, View):
    model = CompanyStructure
    form_class = CompanyStructureForm
    template_name = 'company_structure.html'
    success_url = reverse_lazy('main:company_structure')
    
    def get(self, request):
        form = CompanyStructureForm()
        try:
            latest_company_info = CompanyStructure.objects.latest('add_date')
        except CompanyStructure.DoesNotExist:
            latest_company_info = None
        return render(request, 'company_structure.html', {'form': form, 'latest_company_info': latest_company_info})

    def is_video(self, file_path):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        _, extension = os.path.splitext(file_path)
        return extension.lower() in video_extensions    
        
    def post(self, request):
        form = CompanyStructureForm(request.POST, request.FILES)

        if form.is_valid():
            video_file = request.FILES.get('video')
            if video_file and not self.is_video(video_file.name):
                form.add_error('video', 'Fayl formati noto\'g\'ri. Faqat video fayllarni yuklash mumkin.')
                return render(request, 'company_structure.html', {'form': form})

            form.save()
            messages.success(request, 'Malumot muvaffaqiyatli saqlandi.')
            return redirect('main:company_structure')
        else:
            messages.error(request, 'Xatolik yuz berdi, iltimos, ma\'lumotlarni tekshiring.')
            return render(request, 'company_structure.html', {'form': form})
    
class CompanyStructureUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyStructure
    form_class = CompanyStructureForm
    template_name = 'update_company_structure.html'
    success_url = reverse_lazy('main:company_structure')
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class TaskDetailView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_task')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'task_detail.html', {'task': task})
    

class SimpleTaskDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):  # Use 'pk' instead of 'task_id'
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'simple_task_detail.html', {'task': task})
    

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_task')  # Agar foydalanuvchi superuser emas bo'lsa, oddiy foydalanuvchi sahifasiga yo'naltirish
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        one_week_ago = datetime.now() - timedelta(days=7)
        tasks = Task.objects.filter(add_date__gte=one_week_ago).order_by('-add_date')
        context['tasks'] = tasks

        return context

 

class SimpleTaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'simple_task.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        one_week_ago = datetime.now() - timedelta(days=7)
        tasks = Task.objects.filter(add_date__gte=one_week_ago).order_by('-add_date')
        context['tasks'] = tasks
        return context
    
    

class SimpleTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'simple_update_task.html'
    success_url = reverse_lazy('main:simple_task')

    def form_valid(self, form):
        return super(SimpleTaskUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SimpleTaskUpdateView, self).form_invalid(form)
    

class DeleteTaskView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('main:simple_task')  # Agar foydalanuvchi superuser emas bo'lsa, oddiy foydalanuvchi sahifasiga yo'naltirish
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('/task')
    
    
class SimpleDeleteTaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('/simple_task')
    
class AddEmployeeView(LoginRequiredMixin, View):
    template_name = 'add_employee.html'
    form_class = EmployeeForm

    def get(self, request):
        form = self.form_class()
        users = TelegramUser.objects.all() 
        print(users.last().telegram_id)
        return render(request, self.template_name, {'form': form, 'users': users})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            telegram_id = request.POST.get('telegram_id')
            telegram_user = TelegramUser.objects.get(id=telegram_id)
            employee.telegram_id = telegram_user
            employee.save()
            return redirect('main:employee')
        else:
            errors = form.errors
            users = TelegramUser.objects.all() 
        return render(request, self.template_name, {'form': form, "errors": errors, 'users': users})

class EmployeeView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = Employee.objects.all()            
        context['employees'] = employees
        return context
    
class UpdateEmployeeView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'update_employee.html'
    success_url = reverse_lazy('main:employee')

    def form_valid(self, form):
        return super(UpdateEmployeeView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateEmployeeView, self).form_invalid(form)

class DeleteEmployeeView(View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect('/employee')
    
class AdvanceView(LoginRequiredMixin, ListView):
    model = Advance
    template_name = 'advance.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advance = Advance.objects.all()            
        context['advance'] = advance
        return context 
    def post(self, request):
        answer = request.POST.get('answer')
        advance_id = request.POST.get('advance_id')
        advance = Advance.objects.get(id=advance_id)
        employee = advance.employees
        chat_id = '2083239343'
        
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        if len(advance.desc) <= 400:
            new_text = f"Assalamu alaykum Avans:\n{advance.desc}\n<i>So'rovingiz uchun javob</i>:⤵️\n\n{answer}"
        else:
            new_text = f"Assalamu alaykum Avans:\n{advance.desc[:400]}...\n<i>So'rovingiz uchun javob</i>:⤵️\n\n{answer}"

        if employee.telegram_id:
            params = {
                'chat_id': employee.telegram_id,
                'text': new_text,
                'parse_mode': 'HTML', 
            }
        else:
            params = {
                'chat_id': chat_id,
                'text': answer,
                'parse_mode': 'HTML', 
            }
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            messages.success(request, "Xabar botga muvaffaqiyatli yuborildi!")
        else:
            messages.error(request, "Xatolik yuz berdi!")

        return redirect('main:advance')
    
class DeleteAdvanceView(LoginRequiredMixin, View):
    def get(self, request, pk):
        advance = get_object_or_404(Advance, pk=pk)
        advance.delete()
        return redirect('/advance')
    
    
class OfferView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'offer.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = Offer.objects.all()            
        context['offers'] = offers
        return context
    
    def post(self, request):
        answer = request.POST.get('answer')
        offer_id = request.POST.get('offer_id')
        offer = Offer.objects.get(id=offer_id)
        employee = offer.employees
        chat_id = '2083239343'
        
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        if len(offer.desc) <= 400:
            new_text = f"Assalamu alaykum Taklifingiz:\n{offer.desc}\n<i>Uchun javob</i>:⤵️\n\n{answer}"
        else:
            new_text = f"Assalamu alaykum Taklifingiz:\n{offer.desc[:400]}...\n<i>Uchun javob</i>:⤵️\n\n{answer}"

        if employee.telegram_id:
            params = {
                'chat_id': employee.telegram_id,
                'text': new_text,
                'parse_mode': 'HTML', 
            }
        else:
            params = {
                'chat_id': chat_id,
                'text': answer,
                'parse_mode': 'HTML', 
            }
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            messages.warning(request, "Xabar botga muvaffaqiyatli yuborildi!")
        else:
            messages.warning(request, "Xatolik yuz berdi!")

        return redirect('main:offer')
    

class DeleteOfferView(LoginRequiredMixin, View):
    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        offer.delete()
        return redirect('/offer')

class ComplaintView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaint.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint = Complaint.objects.all()            
        context['complaint'] = complaint
        return context

    def post(self, request):
        answer = request.POST.get('answer')
        complaint_id = request.POST.get('complaint_id')
        complaint = Complaint.objects.get(id=complaint_id)
        employee = complaint.employees
        chat_id = '2083239343'
        
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        if len(complaint.desc) <= 400:
            new_text = f"Assalamu alaykum Shikoyatingiz:\n{complaint.desc}\n<i>Uchun javob</i>:⤵️\n\n{answer}"
        else:
            new_text = f"Assalamu alaykum Shikoyatingiz:\n{complaint.desc[:400]}...\n<i>Uchun javob</i>:⤵️\n\n{answer}"

        if employee.telegram_id:
            params = {
                'chat_id': employee.telegram_id,
                'text': new_text,
                'parse_mode': 'HTML', 
            }
        else:
            params = {
                'chat_id': chat_id,
                'text': answer,
                'parse_mode': 'HTML', 
            }
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            messages.warning(request, "Xabar botga muvaffaqiyatli yuborildi!")
        else:
            messages.warning(request, "Xatolik yuz berdi!")

        return redirect('main:complaint')
    
    
class DeleteComplaintView(LoginRequiredMixin, View):
    def get(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.delete()
        return redirect('/complaint')
    
class AdminsView(LoginRequiredMixin, View):
    template_name = 'admins.html'

    def get(self, request):
        user = User.objects.all()[1:]
        return render(request, self.template_name, {'user': user})

class DeleteAdminsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('/admins')
    
def login_view(request):
    form = AuthenticationForm()
    context = {"form": form}

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:home")

    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('main:login')

class RegisterView(LoginRequiredMixin,View):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            login(request, user)

            messages.success(request, "Foydalanuvchi ro'yxatdan o'tdi!")
            return redirect("main:login")
        else:
            messages.error(request, "Foydalanuvchi ro'yxatdan o'tmadi!")

        context = {"form": form}
        return render(request, self.template_name, context)

class SearchView(LoginRequiredMixin, View):
    template_name = 'search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = []

        employees = Employee.objects.filter(full_name__icontains=query)
        employees_telegram_id = Employee.objects.filter(telegram_id__telegram_id__icontains=query)

        results.extend(employees)
        results.extend(employees_telegram_id)

        context = {
            'results': results,
            'query': query
        }
        return render(request, self.template_name, context)