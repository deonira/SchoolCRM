from rest_framework import viewsets
from .models import Student, Parent
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


