import os
import datetime
from rest_framework import viewsets
from django.db.models.signals import post_save
from .models import Contract
from io import BytesIO
from django.dispatch import receiver
from .serializers import ContractSerializer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from students.models import Student, Parent
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


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

            styles = getSampleStyleSheet()
            normal_style = styles['Normal']
            normal_style.fontSize = 12
            normal_style.fontName = 'DejaVu'

            p = canvas.Canvas(pdf_buffer, pagesize=letter)

            title = "Договор о предоставлении образовательных услуг"
            title_paragraph = Paragraph(title, normal_style)
            title_paragraph.wrapOn(p, 400, 100)
            title_paragraph.drawOn(p, 80, 750)

            date_text = f"Дата: {datetime.date.today().strftime('%Y-%m-%d')}"
            date_paragraph = Paragraph(date_text, normal_style)
            date_paragraph.wrapOn(p, 400, 100)
            date_paragraph.drawOn(p, 80, 710)

            student_info = f"""
            <b>Ученик:</b><br/>
            ФИО: {student.full_name}<br/>
            Дата рождения: {student.date_of_birth.strftime('%Y-%m-%d')}<br/>
            Номер свидетельства о рождении: {student.birth_certificate_number}
            """
            student_paragraph = Paragraph(student_info, normal_style)
            student_paragraph.wrapOn(p, 400, 100)
            student_paragraph.drawOn(p, 80, 660)

            parents_content = "<b>Родитель(и):</b><br/>"
            parents = []
            if student.parent_1:
                parents.append(student.parent_1)
            if student.parent_2:
                parents.append(student.parent_2)

            for parent in parents:
                if parent.full_name and parent.phone_number:
                    parents_content += f"ФИО: {parent.full_name}, Телефон: {parent.phone_number}<br/>"
                elif parent.full_name:
                    parents_content += f"ФИО: {parent.full_name}<br/>"
                elif parent.phone_number:
                    parents_content += f"Телефон: {parent.phone_number}<br/>"

            parents_paragraph = Paragraph(parents_content, normal_style)
            parents_paragraph.wrapOn(p, 400, 100)
            parents_paragraph.drawOn(p, 80, 610)

            conditions = """
            <b> Условия договора:</b><br/>
            1. Образовательный процесс будет проходить в соответствии с учебным планом школы.<br/>
            2. Студент обязуется соблюдать правила внутреннего распорядка учебного заведения.<br/>
            3. Родители обязуются своевременно оплачивать обучение и содействовать в образовательном процессе.<br/>
            4. Школа обязуется предоставлять образовательные услуги в соответствии с законодательством Кыргызской Республики.
            """
            conditions_paragraph = Paragraph(conditions, normal_style)
            conditions_paragraph.wrapOn(p, 400, 100)
            conditions_paragraph.drawOn(p, 80, 500)

            signatures = """
            <b>Подписи:</b><br/>
            
            ___________________ <br/>
            Родитель(и)<br/><br/>
            
            ___________________ <br/>
            Представитель школы
            """
            signatures_paragraph = Paragraph(signatures, normal_style)
            signatures_paragraph.wrapOn(p, 400, 100)
            signatures_paragraph.drawOn(p, 80, 300)

            p.showPage()
            p.save()

            pdf_content = pdf_buffer.getvalue()
            pdf_file = ContentFile(pdf_content)
            student_name = student.full_name.replace(" ", "_")
            contract.pdf.save(f"contract_{student_name}.pdf", pdf_file)

            pdf_buffer.close()

        except Exception as e:
            print(f"Ошибка при создании или обновлении контракта для студента {instance.full_name}: {str(e)}")
