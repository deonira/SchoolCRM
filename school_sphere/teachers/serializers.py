from rest_framework import serializers
from .models import Teacher
from classes.models import Class

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