# Generated by Django 5.1.2 on 2024-11-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_rename_subjects_teacher_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='subject',
            new_name='subjects',
        ),
    ]
