"""
URL configuration for Bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('f04b9654-72d1-46fe-8d65-e595ef2dda85/',include('botapi.urls')),
    path('bca38f02-e349-49ea-8849-bf79e415a1f6/', admin.site.urls),
    path('', include('app.urls')),
]+ static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL ,document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)s
