from rest_framework import serializers
from .models import Student, Parent
from classes.models import Class

class ParentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Parent
        fields = ('id','full_name', 'phone_number', 'email')

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    parent_1 = ParentSerializer()
    parent_2 = ParentSerializer(allow_null=True, required=False)
    grade = serializers.ChoiceField(
        choices=[(i, i) for i in range(0, 12)],
        write_only=True
    )
    letter = serializers.ChoiceField(
        choices=[(chr(letter), chr(letter)) for letter in range(ord('а'), ord('я') + 1)],
        write_only=True
    )
    class_name = serializers.SerializerMethodField()

    def validate(self, data):
        grade = data.get('grade', self.instance.grade)
        letter = data.get('letter', self.instance.letter)

        current_class = self.instance.class_assigned

        if grade != current_class.grade or letter != current_class.letter:
            try:
                new_class = Class.objects.get(grade=grade, letter=letter)
            except Class.DoesNotExist:
                raise serializers.ValidationError(f"Класс с grade {grade} и letter {letter} не существует.")

            if new_class.grade < current_class.grade:
                raise serializers.ValidationError("Нельзя перевести ученика в класс ниже.")


            data['class_name'] = f"{new_class.grade}{new_class.letter}"

        return data

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'date_of_birth', 'birth_certificate_number', 'grade', 'letter',
                  'parent_1', 'parent_2','class_name']

    def get_class_name(self, obj):
        return f"{obj.grade}{obj.letter}"


    def create(self, validated_data):
        parent_1_data = validated_data.pop('parent_1')
        parent_2_data = validated_data.pop('parent_2', None)

        parent_1 = Parent.objects.create(**parent_1_data)
        parent_2 = Parent.objects.create(**parent_2_data) if parent_2_data else None

        student_class = validated_data.pop('class_assigned')

        student = Student.objects.create(
            parent_1=parent_1,
            parent_2=parent_2,
            class_assigned=student_class,
            **validated_data
        )

        return student

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.birth_certificate_number = validated_data.get('birth_certificate_number',
                                                               instance.birth_certificate_number)

        grade = validated_data.pop('grade', None)
        letter = validated_data.pop('letter', None)
        if grade is not None and letter is not None:
            student_class = Class.objects.filter(grade=grade, letter=letter).first()
            if not student_class:
                raise serializers.ValidationError(f"Класс с grade {grade} и letter {letter} не существует.")

            if student_class.grade < instance.class_assigned.grade:
                raise serializers.ValidationError(
                    f"Невозможно понизить класс с grade {instance.class_assigned.grade} на {student_class.grade}."
                )

            instance.class_assigned = student_class
            instance.grade = student_class.grade
            instance.letter = student_class.letter

        parent_1_data = validated_data.pop('parent_1', None)
        if parent_1_data:
            for attr, value in parent_1_data.items():
                if hasattr(instance.parent_1, attr):
                    setattr(instance.parent_1, attr, value)
            instance.parent_1.save()

        parent_2_data = validated_data.pop('parent_2', None)
        if parent_2_data:
            if isinstance(parent_2_data, int):
                instance.parent_2 = Parent.objects.get(id=parent_2_data)
            elif isinstance(parent_2_data, dict):
                if instance.parent_2:
                    for attr, value in parent_2_data.items():
                        if hasattr(instance.parent_2, attr):
                            setattr(instance.parent_2, attr, value)
                    instance.parent_2.save()
                else:
                    instance.parent_2 = Parent.objects.create(**parent_2_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance