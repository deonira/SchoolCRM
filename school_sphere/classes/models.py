from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Class(models.Model):
    class_teacher = models.ForeignKey('teachers.Teacher', related_name='managed_classes', on_delete=models.SET_NULL, null=True)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(11)])
    letter = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.grade}{self.letter}"

    def get_student_count(self):
        return self.students.count()