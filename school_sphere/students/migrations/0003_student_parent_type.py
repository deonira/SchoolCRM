# Generated by Django 5.1.2 on 2024-11-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_class_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_type',
            field=models.CharField(choices=[('2_parents', '2 родителя'), ('1_parent', '1 родитель'), ('guardian', 'Опекун'), ('orphan', 'Сирота')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
