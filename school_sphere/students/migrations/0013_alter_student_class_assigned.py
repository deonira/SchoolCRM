# Generated by Django 5.1.2 on 2024-11-21 22:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_remove_class_student_count'),
        ('students', '0012_alter_student_parent_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='class_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='classes.class'),
        ),
    ]