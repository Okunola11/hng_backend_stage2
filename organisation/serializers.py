from rest_framework import serializers
from .models import Organisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description', 'members']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['members'] = [member.email for member in instance.members.all()]  
        return data


# Creation serializer
class OrganisationCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('name', 'description')  

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name is required")
        return value
