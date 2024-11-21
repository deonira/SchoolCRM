"""
URL configuration for school_sphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, ConfirmDeleteFromClassView, DeleteFromClassView
from classes.views import ClassViewSet
from teachers.views import TeacherViewSet
from contracts.views import ContractViewSet

router = DefaultRouter()

router.register(r'students', StudentViewSet, basename='student')
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('users.urls')),
    path('api/students/<int:student_id>/confirm-delete-from-class/', ConfirmDeleteFromClassView.as_view(), name='confirm_delete_from_class'),
    path('api/students/<int:student_id>/delete-from-class/', DeleteFromClassView.as_view(), name='delete_from_class'),
]
