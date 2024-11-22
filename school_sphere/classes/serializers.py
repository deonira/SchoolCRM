from rest_framework import serializers
from .models import Class
# from school_sphere.students.models import Student
from teachers.serializers import TeacherSerializer
from teachers.models import Teacher
from students.serializers import StudentSerializer


class ClassSerializer(serializers.ModelSerializer):
    class_teacher = TeacherSerializer(read_only=True)
    students = serializers.SerializerMethodField()
    grade = serializers.ChoiceField(
        choices=[(i, i) for i in range(1, 12)],
        write_only=True,
    )
    letter = serializers.ChoiceField(
        choices=[(chr(letter), chr(letter)) for letter in range(ord('а'), ord('я') + 1)],
        write_only=True,
    )
    class_name = serializers.SerializerMethodField()
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), write_only=True, required=False)

    class Meta:
        model = Class
        fields = ['id', 'grade', 'letter', 'class_name', 'teacher', 'class_teacher', 'students']

    def get_students(self, obj):
        students = obj.students.all()
        return [{"id": student.id, "full_name": student.full_name, "date_of_birth": student.date_of_birth} for student
                in students]

    def get_student_count(self, obj):
        return obj.students.count()

    def create(self, validated_data):
        teacher_data = validated_data.pop('teacher', None)
        grade = validated_data.get('grade')
        letter = validated_data.get('letter')

        validated_data.pop('grade', None)
        validated_data.pop('letter', None)


        if teacher_data and Class.objects.filter(class_teacher=teacher_data).exists():
            raise serializers.ValidationError(
                f"Учитель {teacher_data.full_name} уже является классным руководителем другого класса."
            )


        student_class, created = Class.objects.get_or_create(grade=grade, letter=letter, **validated_data)

        if created:
            if teacher_data:
                student_class.class_teacher = teacher_data
                student_class.save()

            return student_class
        else:
            raise serializers.ValidationError(f"Класс с grade {grade} и letter {letter} уже существует.")

    def update(self, instance, validated_data):
        teacher_data = validated_data.pop('teacher', None)

        instance.grade = validated_data.get('grade', instance.grade)
        instance.letter = validated_data.get('letter', instance.letter)

        if teacher_data:
            if Class.objects.filter(class_teacher=teacher_data).exclude(id=instance.id).exists():
                raise serializers.ValidationError(
                    f"Учитель {teacher_data.full_name} уже является классным руководителем в другом классе.")
            instance.class_teacher = teacher_data

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        class_teacher = instance.class_teacher
        if class_teacher:
            representation['class_teacher'] = {
                'id': class_teacher.id,
                'full_name': class_teacher.full_name,
            }
        else:
            representation['class_teacher'] = None

        return representation

    def get_class_name(self, obj):
        return f"{obj.grade}{obj.letter}"
