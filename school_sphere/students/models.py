from django.db import models
from classes.models import Class
from django.core.exceptions import ValidationError

class Parent(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    birth_certificate_number = models.CharField(max_length=50)
    grade = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(0, 12)], null=True, blank=True)
    letter = models.CharField(max_length=1, null=True, blank=True)
    parent_1 = models.ForeignKey(Parent, related_name='parent_1', on_delete=models.CASCADE)
    parent_2 = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent_2', blank=True, null=True)
    class_assigned = models.ForeignKey(Class, related_name='students', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)