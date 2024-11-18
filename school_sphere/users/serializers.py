from rest_framework import serializers
from django.contrib.auth import authenticate


class AssistantLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Неверные учетные данные.")
            if not user.is_assistant:
                raise serializers.ValidationError("Доступ разрешен только административным ассистентам.")
        else:
            raise serializers.ValidationError("Необходимо указать имя пользователя и пароль.")

        data['user'] = user
        return data