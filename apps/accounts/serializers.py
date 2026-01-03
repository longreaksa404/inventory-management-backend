from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'username', 'phone_number', 'role', 'is_staff', 'password', 'password2'
        ]

    # check validate if pw dose not much
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUser.objects.create_user(**validated_data)
