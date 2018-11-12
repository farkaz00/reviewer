from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED,
        HTTP_404_NOT_FOUND,
        HTTP_200_OK,
        HTTP_201_CREATED)

from .models import Company, Review
from .serializers import CompanySerializer, UserSerializer, ReviewSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
    status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


class CompanyListCreate(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class UserListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        User.objects.create_user(
            username=serializer['username'].value,
            password=serializer['password'].value,
            email=serializer['email'].value,
            first_name=serializer['first_name'].value,
            last_name=serializer['last_name'].value)
        return Response(serializer.data, status=HTTP_201_CREATED) 


class ReviewListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        print(serializer.validated_data['reviewer'])
        print(request.user)
        if serializer.validated_data['reviewer'] != request.user:
            return Response(serializer.errors, status=HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED) 

    
    def get_queryset(self):
        request = self.request
        if request.user.is_staff:
            return Review.objects.all()
        else:
            return Review.objects.all().filter(reviewer_id=request.user.id)
