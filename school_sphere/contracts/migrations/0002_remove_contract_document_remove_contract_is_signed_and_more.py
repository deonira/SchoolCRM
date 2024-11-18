# Generated by Django 5.1.2 on 2024-11-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='document',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='is_signed',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='parent_name',
        ),
        migrations.AddField(
            model_name='contract',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='contracts/media/'),
        ),
    ]
