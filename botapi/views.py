from .serializer import (EmployeeSerializer,TaskSerializer, TelegramUserSerializer, AdvanceSerializer, OfferSerializer, ComplaintSerializer, CompanyInfoSerializer, CompanyStructureSerializer, AttendanceSerializer, CategoryCompanyInfoSeralizer, CategoryStructureSeralizer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from app.models import (Employee, Task,TelegramUser, Advance, CompanyInfo, CompanyStructure, Offer, Complaint, Attendance, CategoryStructure, Category)
from datetime import  datetime
import pytz
from rest_framework.exceptions import ValidationError


class BotUserViewset(ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

class GetUser(APIView):
    def get(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = TelegramUser.objects.get(telegram_id=data['telegram_id'])
                serializer = TelegramUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except TelegramUser.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeViewset(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class GetEmployee(APIView):
    def get(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        if telegram_id:
            try:
                employee = Employee.objects.get(telegram_id__telegram_id=telegram_id)
                serializer = EmployeeSerializer(employee, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            raise ValidationError("telegram_id parametri talab qilinadi.")



class TaskViewset(ModelViewSet):
    queryset = Task.objects.all()
    tasks = Task.objects.filter().order_by('-add_date')
    serializer_class = TaskSerializer


class GetTask(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        data = data.dict()
        if data.get('id',None):
            try:
                task = Task.objects.get(id=data['id'])
                serializer = TaskSerializer(task, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except Task.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)

class UpdateTaskStatus(APIView):
    def put(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        new_status = request.data.get('new_status')

        if task_id and new_status:
            try:
                task = Task.objects.get(id=task_id)
                task.task_status = new_status
                task.save()

                serializer = TaskSerializer(task, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskAccepted(APIView):
    def put(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        employee_id = request.data.get('employee_id')

        if task_id and employee_id:
            try:
                task = Task.objects.get(id=task_id)
                employee = Employee.objects.get(id=employee_id)
                task.accepted.add(employee)
                task.save()

                serializer = TaskSerializer(task, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            except Employee.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class AdvanceViewset(ModelViewSet):
    queryset = Advance.objects.all()
    serializer_class = AdvanceSerializer

class GetAdvance(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        data = data.dict()
        if data.get('id',None):
            try:
                advance = Advance.objects.get(id=data['id'])
                serializer = AdvanceSerializer(advance, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except Advance.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        serializer = AdvanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferViewset(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class GetOffer(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        data = data.dict()
        if data.get('id',None):
            try:
                offer = Offer.objects.get(id=data['id'])
                serializer = OfferSerializer(offer, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except Offer.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintViewset(ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer


class GetComplaint(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        data = data.dict()
        if data.get('id',None):
            try:
                complaint = Complaint.objects.get(id=data['id'])
                serializer = ComplaintSerializer(complaint, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except Complaint.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        company_info = CompanyInfo.objects.all()
        serializer = CompanyInfoSerializer(company_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CompanyStructureAPIView(APIView):
    def get(self, request, *args, **kwargs):
        company_structure = CompanyStructure.objects.all()
        serializer = CompanyStructureSerializer(company_structure, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryInfoViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCompanyInfoSeralizer

class CategoryStructuraViewSet(ModelViewSet):
    queryset = CategoryStructure.objects.all()
    serializer_class = CategoryStructureSeralizer

class AttendanceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
        today = datetime.now(uzbekistan_timezone).date()
        attendances = Attendance.objects.filter(add_date__date=today)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)