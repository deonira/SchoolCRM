import datetime
import io
from pdfminer.high_level import extract_text
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Contract
from students.models import Student, Parent
from classes.models import Class
from teachers.models import Teacher
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
class ContractViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        response = self.client.post('/api/auth/token/', {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.teacher = Teacher.objects.create(
            full_name="Mr. Smith",
            subjects="Math",
            date_of_birth='1997-05-03',
            phone_number='0999486078',
            email='1231313@mail.ru'
        )


        self.student_class = Class.objects.create(
            grade=3,
            letter='в',
            class_teacher=self.teacher,


        )

        self.parent1 = Parent.objects.create(full_name="Parent One", phone_number="1234567890", email='123q@mail.ru')
        #self.parent2 = Parent.objects.create(full_name="Parent Two", phone_number="0987654321", email='123q@mail.ru')

        self.student = Student.objects.create(
            full_name="John Doe",
            date_of_birth="2010-01-01",
            birth_certificate_number="123456789",
            parent_1=self.parent1,
            parent_2=None,
            grade=3,
            letter='в',
            class_assigned=self.student_class,


        )


        self.contracts = Contract.objects.filter(student=self.student)

        self.assertEqual(self.contracts.count(), 1)

        self.contract = self.contracts.first()

    def test_generate_pdf(self):
        self.assertIsNotNone(self.contract.pdf)

        pdf_file = io.BytesIO(self.contract.pdf.read())
        pdf_text = extract_text(pdf_file)

        self.assertIn("Договор о предоставлении образовательных услуг", pdf_text)
        self.assertIn("Ученик:", pdf_text)
        self.assertIn("John Doe", pdf_text)

        if self.student.parent_2:
            self.assertIn("Parent One", pdf_text)
            self.assertIn("Parent Two", pdf_text)
        else:
            self.assertIn("Parent One", pdf_text)
            self.assertNotIn("Parent Two", pdf_text)



    def test_update_student_and_add_parent(self):

        self.assertEqual(self.student.full_name, "John Doe")
        self.assertEqual(self.student.parent_1.full_name, "Parent One")


        parent2_data = {
            "full_name": "Updated Parent Two",
            "phone_number": "+996999486078",
            "email": "updated2@mail.ru"
        }
        parent2 = Parent.objects.create(**parent2_data)


        new_data = {
            "full_name": "John Doe Updated",
            "grade":3,
            "letter":"в",
            "parent_2": parent2.id,

            "parent_2": {
                "full_name": parent2.full_name,
                "phone_number": parent2.phone_number,
                "email": parent2.email,
            "parent_1": {
                "full_name": '123',

            }

            }
        }

        url = f'/students/{self.student.id}/'
        response = self.client.patch(url, new_data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        updated_student = Student.objects.get(id=self.student.id)
        self.assertEqual(updated_student.full_name, "John Doe Updated")
        self.assertEqual(self.student.parent_2.full_name, "Updated Parent Two")

        self.contracts = Contract.objects.filter(student=self.student)
        self.assertEqual(self.contracts.count(), 1)
        self.contract = self.contracts.first()

        self.contract = Contract.objects.get(student=self.student)
        self.assertIsNotNone(self.contract.pdf)

        pdf_file = io.BytesIO(self.contract.pdf.read())
        pdf_text = extract_text(pdf_file)

        self.assertIn("John Doe Updated", pdf_text)
        self.assertIn("Parent Two", pdf_text)
