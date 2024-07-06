import uuid
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from organisation.models import Organisation
from .serializers import UserSerializer
from organisation.serializers import OrganisationSerializer
from django.contrib.auth import authenticate
import jwt
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        try: 
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            org_name = f"{user.first_name}'s Organisation"
            organisation = Organisation.objects.create(
                org_id=uuid.uuid4().hex,
                name=org_name,
            )
            organisation.users.add(user)
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
            # errors = [{'field': field, 'message': message} for field, message in serializer.errors.items()]
            # return Response({'errors': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except serializers.ValidationError as e:
            errors = [{'field': field, 'message': message[0]} for field, message in e.detail.items()]
            return Response({'errors': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
           
        except Exception as e:
            return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
                'details': str(e)
            }, statusCode=status.HTTP_400_BAD_REQUEST)

        return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
            }, statusCode=status.HTTP_400_BAD_REQUEST)

        
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

# class UserDetailView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         self.queryset.filter(user_id=self.request.user.user_id)

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        data = serializer.data

        message = f"Retrieved details for {user.email}"  

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "userId": data["user_id"],
                "firstName": data["first_name"],
                "lastName": data["last_name"],
                "email": data["email"],
                "phone": data.get("phone", ""),
            }
        })
        

    