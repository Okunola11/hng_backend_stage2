import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Organisation
from .serializers import OrganisationSerializer, OrganisationCreationSerializer
from rest_framework.response import Response 
from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()



class OrganisationListCreateView(APIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = user.organisations.all()
        serializer = OrganisationSerializer(queryset, many=True)
        data = serializer.data

        response_data = {
            "status": "success",
            "message": "Successfully retrieved user organisations",
            "data": {
                "organisations": data
            }
        }

        return Response(response_data)


    def post(self, request, *args, **kwargs):
        serializer = OrganisationCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        # Generating orgId
        organisation = serializer.save(orgId=str(uuid.uuid4()))

        # Add the authenticated user as a member
        organisation.members.add(request.user)

        # Successful response data
        response_data = {
            "status": "success",
            "message": "Organisation created successfully",
            "data": {
                "orgId": organisation.orgId,
                "name": organisation.name,
                "description": organisation.description
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, orgId, *args, **kwargs):
        try:
            # Get the particular organisation instance
            organisation = Organisation.objects.get(orgId=orgId)

            # Get the user from request data
            user_id = request.data.get('userId')
            if not user_id:
                return Response({'message': 'Missing userId in request body'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(user_id=user_id)  

            # Add user as a member to the organisation
            organisation.members.add(user)

            return Response({
                "status": "success",
                'message': 'User added to organisation successfully'
                }, status=status.HTTP_200_OK)

        # Handling Errors
        except Organisation.DoesNotExist:
            # Organisation not found
            return Response({'message': 'Organisation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            # User not found
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other potential errors
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, orgId, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(orgId=orgId)

            # Check if user is a member of the organisation
            if request.user not in organisation.members.all():
                return Response({'message': 'You are not a member of this organisation'}, status=status.HTTP_403_FORBIDDEN)

            # Success response
            return Response({
                "status": "success",
                "message": "Organisation details retrieved successfully",
                "data": {
                    "orgId": organisation.orgId,
                    "name": organisation.name,
                    "description": organisation.description,
                }
            }, status=status.HTTP_200_OK)

        # Handling errors
        except Organisation.DoesNotExist:
            return Response({'message': 'Organisation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


