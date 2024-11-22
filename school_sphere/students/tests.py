from rest_framework.test import APITestCase
from rest_framework import status
from students.models import Student, Parent
from classes.models import Class
from django.contrib.auth.models import User
from teachers.models import Teacher
from django.contrib.auth import get_user_model

User = get_user_model()
class TestDeleteStudentFromClass(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post('/api/auth/token/', {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.teacher = Teacher.objects.create(
            full_name="Teacher Test",
            subjects="Math",
            date_of_birth="1980-01-01",
            phone_number="1234567890",
            email="teacher@test.com"
        )
        self.student_class = Class.objects.create(
            grade=3,
            letter="A",
            class_teacher=self.teacher
        )
        self.parent = Parent.objects.create(
            full_name="Parent Test",
            phone_number="+996999654321",
            email="parent@test.com"
        )
        self.student = Student.objects.create(
            full_name="Student Test",
            date_of_birth="2010-01-01",
            birth_certificate_number="ABC123456",
            parent_1=self.parent,
            class_assigned=self.student_class
        )

    def test_confirm_delete_student_from_class(self):
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())
        url = f'/students/{self.student.id}/confirm-delete-from-class/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_student_from_class_confirmed(self):
        url = f'/students/{self.student.id}/delete-from-class/?confirmed=true'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Учебный класс ученика", response.data["message"])


        self.student.refresh_from_db()
        self.assertIsNone(self.student.class_assigned)

    def test_delete_student_from_class_not_confirmed(self):
        url = f'/students/{self.student.id}/delete-from-class/?confirmed=false'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Вы уверены, что хотите удалить ученика", response.data["message"])

        self.student.refresh_from_db()
        self.assertIsNotNone(self.student.class_assigned)

    def test_delete_non_existent_student(self):
        url = '/students/999/delete-from-class/?confirmed=true'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Student not found", response.data["detail"])