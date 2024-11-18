import os
import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models.signals import post_save
from .models import Contract
from io import BytesIO
from django.dispatch import receiver
from .serializers import ContractSerializer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from students.models import Student, Parent
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    if not os.path.exists(font_path):
        raise Exception("Font not found")
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))

    @receiver(post_save, sender=Student)
    def generate_or_update_contract_pdf(sender, instance, created, **kwargs):
        try:
            student = instance

            if isinstance(student.date_of_birth, str):
                student.date_of_birth = datetime.datetime.strptime(student.date_of_birth, '%Y-%m-%d').date()

            contract, contract_created = Contract.objects.get_or_create(
                student=instance,
                defaults={'start_date': datetime.date(2024, 9, 1), 'end_date': datetime.date(2025, 5, 25)}
            )

            pdf_buffer = BytesIO()
            p = canvas.Canvas(pdf_buffer, pagesize=letter)
            p.setFont('DejaVu', 12)

            p.drawString(100, 750, "Договор о предоставлении образовательных услуг")
            p.drawString(100, 730, f"Дата: {datetime.date.today().strftime('%Y-%m-%d')}")

            p.drawString(100, 680, "Ученик:")
            p.drawString(120, 660, f"ФИО: {student.full_name}")
            p.drawString(120, 640, f"Дата рождения: {student.date_of_birth.strftime('%Y-%m-%d')}")
            p.drawString(120, 620, f"Номер свидетельства о рождении: {student.birth_certificate_number}")

            p.drawString(100, 580, "Родитель(и):")
            y_position = 560
            parents = []
            if student.parent_1:
                parents.append(student.parent_1)
            if student.parent_2:
                parents.append(student.parent_2)

            for parent in parents:
                if parent.full_name and parent.phone_number:
                    p.drawString(120, y_position, f"ФИО: {parent.full_name}, Телефон: {parent.phone_number}")
                elif parent.full_name:
                    p.drawString(120, y_position, f"ФИО: {parent.full_name}")
                elif parent.phone_number:
                    p.drawString(120, y_position, f"Телефон: {parent.phone_number}")
                y_position -= 20

            p.drawString(100, y_position - 20, "Подписи:")
            p.drawString(100, y_position - 40, "___________________")
            p.drawString(100, y_position - 60, "Родитель(и)")
            p.drawString(400, y_position - 40, "___________________")
            p.drawString(400, y_position - 60, "Представитель школы")

            p.showPage()
            p.save()

            pdf_content = pdf_buffer.getvalue()
            pdf_file = ContentFile(pdf_content)
            student_name = student.full_name.replace(" ", "_")
            contract.pdf.save(f"contract_{student_name}.pdf", pdf_file)

            pdf_buffer.close()

        except Exception as e:
            print(f"Ошибка при создании или обновлении контракта для студента {instance.full_name}: {str(e)}")