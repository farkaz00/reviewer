from django.contrib.auth.models import User

from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Company, Review
from .serializers import CompanySerializer, UserSerializer


class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListCreate(APIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, format=None):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
