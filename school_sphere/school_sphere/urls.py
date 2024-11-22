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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from students.views import StudentViewSet, ConfirmDeleteFromClassView, DeleteFromClassView
from classes.views import ClassViewSet
from teachers.views import TeacherViewSet
from contracts.views import ContractViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SchoolSphere API",
        default_version='v1',
        description="Документация для API SchoolSphere",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="deonirra@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'students', StudentViewSet, basename='student')
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path('api/auth/', include('users.urls')),
    path('students/<int:student_id>/confirm-delete-from-class/', ConfirmDeleteFromClassView.as_view(), name='confirm_delete_from_class'),
    path('students/<int:student_id>/delete-from-class/', DeleteFromClassView.as_view(), name='delete_from_class'),
]
