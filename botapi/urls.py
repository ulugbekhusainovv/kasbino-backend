from django.urls import path,include
from .views import (BotUserViewset,GetUser, EmployeeViewset, GetEmployee, TaskViewset, GetTask, AdvanceViewset, GetAdvance, OfferViewset, GetOffer, ComplaintViewset, GetComplaint, UpdateTaskStatus , UpdateTaskAccepted , CompanyStructureAPIView, CompanyInfoAPIView, AttendanceAPIView, CategoryInfoViewSet, CategoryStructuraViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('botuser',BotUserViewset)
router.register('employees',EmployeeViewset)
router.register('tasks', TaskViewset)
router.register('advances', AdvanceViewset)
router.register('offers', OfferViewset)
router.register('complaints', ComplaintViewset)
router.register('category_info', CategoryInfoViewSet)
router.register('category_structure', CategoryStructuraViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('get_user/', GetUser.as_view()),
    path('get_employee/', GetEmployee.as_view()),
    path('get_task/', GetTask.as_view()),
    path('get_advance/', GetAdvance.as_view()),
    path('get_offer/', GetOffer.as_view()),
    path('get_complaint/', GetComplaint.as_view()),
    path('update_task_status/<int:id>/', UpdateTaskStatus.as_view()),
    path('update_task_accepted/<int:id>/', UpdateTaskAccepted.as_view()),
    path('company-info/', CompanyInfoAPIView.as_view()),
    path('company-structure/', CompanyStructureAPIView.as_view()),
    path('attendances/', AttendanceAPIView.as_view()),
]