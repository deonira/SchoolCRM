from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    subjects = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    education_university = models.CharField(max_length=255, blank=True, null=True)
    education_specialty = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.full_name
