from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


    def validate(self, data):
        errors = []

        # Validating first_name
        first_name = data.get('first_name')
        if not isinstance(first_name, str):
            errors.append({
                'field': 'first_name',
                'message': 'First_name must be a string.'
            })

         # Validating last_name
        last_name = data.get('last_name')
        if not isinstance(last_name, str):
            errors.append({
                'field': 'last_name',
                'message': 'last_name must be a string.'
            })

        # Validating email
        email = data.get('email')
        if not isinstance(email, str):
            errors.append({
                'field': 'email',
                'message': 'Email must be a string.'
            })

         # Validating Phone
        phone = data.get('phone')
        if not isinstance(phone, str):
            errors.append({
                'field': 'phone',
                'message': 'phone must be a string.'
            })

        # Raise validation error if there are any errors
        if errors:
            raise serializers.ValidationError({'errors': errors})

        return data