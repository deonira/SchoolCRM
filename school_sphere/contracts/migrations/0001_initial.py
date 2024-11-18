# Generated by Django 5.1.2 on 2024-10-09 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(max_length=255)),
                ('contract_date', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_signed', models.BooleanField(default=False)),
                ('document', models.FileField(upload_to='contracts/')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='students.student')),
            ],
        ),
    ]
