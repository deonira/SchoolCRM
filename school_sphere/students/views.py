from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Parent, Class
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ConfirmDeleteFromClassView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            return Response({
                'message': f"Вы уверены, что хотите удалить ученика {student.full_name} из класса {student.class_assigned.grade}{student.class_assigned.letter}? Это действие невозможно будет отменить.",
                'actions': [
                    {'action': 'yes', 'url': f'/api/students/{student_id}/delete-from-class/?confirmed=true'},
                    {'action': 'no', 'url': f'/api/students/{student_id}/delete-from-class/?confirmed=false'}
                ]
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Студент не найден.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteFromClassView(APIView):
    def get(self, request, student_id, *args, **kwargs):
        confirmed = request.GET.get('confirmed', 'false') == 'true'

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        if confirmed:
            student.class_assigned = None
            student.save()
            return Response({"message": f"Учебный класс ученика {student.full_name} удален."},
                            status=status.HTTP_200_OK)

        return Response({
            "message": f"Вы уверены, что хотите удалить ученика {student.full_name} из класса? Это действие невозможно будет отменить."
        }, status=status.HTTP_200_OK)