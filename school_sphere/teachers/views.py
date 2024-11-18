from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        teacher_class = serializer.validated_data.get('class_assigned')
        if teacher_class and teacher_class.class_teacher:
            raise serializers.ValidationError(f"Teacher already assigned to class {teacher_class.class_name}")

        serializer.save()