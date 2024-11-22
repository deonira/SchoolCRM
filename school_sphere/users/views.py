from rest_framework.views import APIView
import logging
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import AssistantLoginSerializer
from .permissions import IsAssistant
from django.shortcuts import render

logger = logging.getLogger(__name__)

class AssistantLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AssistantLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            logger.error(f"Login failed for {request.data.get('username')}: {serializer.errors}")
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class AssistantDashboardView(APIView):
    permission_classes = [IsAssistant]

    def get(self, request):
        return Response({"message": "Добро пожаловать, ассистент!"})
