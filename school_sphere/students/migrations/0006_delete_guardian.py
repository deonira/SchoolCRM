# Generated by Django 5.1.2 on 2024-11-11 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_remove_student_guardian_full_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Guardian',
        ),
    ]
