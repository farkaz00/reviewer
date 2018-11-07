from django.contrib.auth.models import User

from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Company, Review
from .serializers import CompanySerializer, UserSerializer, ReviewUserSerializer, ReviewSerializer


class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UserListCreate(APIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        review_user_serializer = ReviewUserSerializer(data=request.data)
        if user_serializer.is_valid() and review_user_serializer.is_valid():
            user_serializer.save()
            review_user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        if request.user.is_staff:
            print('Is super user')
        else:
            print('SCRAM!!!')
        reviews = [review.title for review in Review.objects.all()]
        return Response(reviews)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
