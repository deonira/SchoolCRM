import re
from rest_framework import serializers
from .models import Teacher
from classes.models import Class
from datetime import datetime

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'subjects', 'phone_number', 'email','date_of_birth','education_university',
                  'education_specialty', 'work_experience']

    def create(self, validated_data):
        teacher = Teacher.objects.create(**validated_data)
        return teacher

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.subjects = validated_data.get('subjects', instance.subjects)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.education_university = validated_data.get('education_university', instance.education_university)
        instance.education_specialty = validated_data.get('education_specialty', instance.education_specialty)
        instance.work_experience = validated_data.get('work_experience', instance.work_experience)
        instance.save()
        return instance

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError("Неверный формат электронной почты.")
        return email

    def validate_date_of_birth(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Дата рождения не может быть в будущем.")
        return value
    def validate_phone_number(self, phone_number):
        if phone_number and phone_number != "":
            phone_pattern = re.compile(r'^\+996\d{9}$')
            if not phone_pattern.match(phone_number):
                raise serializers.ValidationError("Неверный формат номера телефона. Должно быть в формате +996XXXXXXXXX.")
        return phone_number