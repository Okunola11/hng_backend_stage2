from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


    def validate(self, data):
        errors = []

        # Validating firstName
        firstName = data.get('firstName')
        if not isinstance(firstName, str):
            errors.append({
                'field': 'firstName',
                'message': 'FirstName must be a string.'
            })

         # Validating lastName
        lastName = data.get('lastName')
        if not isinstance(lastName, str):
            errors.append({
                'field': 'lastName',
                'message': 'lastName must be a string.'
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