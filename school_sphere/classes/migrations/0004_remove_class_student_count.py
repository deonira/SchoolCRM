# Generated by Django 5.1.2 on 2024-11-17 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_remove_class_class_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='student_count',
        ),
    ]
