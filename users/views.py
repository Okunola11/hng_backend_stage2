import uuid
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from organisation.models import Organisation, Membership
from .serializers import UserSerializer
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        try: 
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            org_name = f"{user.firstName}'s Organisation"
            organisation = Organisation.objects.create(
                orgId=uuid.uuid4().hex,
                name=org_name,
            )
            # Add user to the organisation
            membership = Membership.objects.create(user=user, organisation=organisation)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': access_token,
                    'user': serializer.data
                }
            }, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            errors = [{'field': field, 'message': message[0]} for field, message in e.detail.items()]
            return Response({'errors': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
           
        except Exception as e:
            return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
            }, status=status.HTTP_400_BAD_REQUEST)

        
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token) 
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': access_token,
                    'user': serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(user_id=user_id)

            # Check if user the requesting user_id is same as the requested id
            if request.user.user_id != user_id:
                return Response({'message': 'You have no permission'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.serializer_class(user)
            data = serializer.data
            message = f"Retrieved details for {user.email}"

            # Success response
            return Response({
                "status": "success",
                "message": message,
                "data": {
                "userId": data["user_id"],
                "firstName": data["firstName"],
                "lastName": data["lastName"],
                "email": data["email"],
                "phone": data.get("phone", ""),
                }
            })

        # Handling errors
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    