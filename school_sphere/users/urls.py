from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AssistantLoginView, AssistantDashboardView, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('assistant-login/', AssistantLoginView.as_view(), name='assistant_login'),
    path('assistant-dashboard/', AssistantDashboardView.as_view(), name='assistant_dashboard'),
]