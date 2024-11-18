from django.db import models
from students.models import Student
import datetime

def get_start_date():
    today = datetime.date.today()
    return datetime.date(today.year, 9, 1)

def get_end_date():
    today = datetime.date.today()
    return datetime.date(today.year + 1, 5, 25)

class Contract(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='contracts')
    contract_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(default=get_start_date)
    end_date = models.DateField(default=get_end_date)
    pdf = models.FileField(upload_to='contracts/media/', null=True, blank=True)

    def __str__(self):
        return f"Contract for {self.student.full_name}"
