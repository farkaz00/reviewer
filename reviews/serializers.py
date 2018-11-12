from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Review, Company


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
                'first_name',
                'last_name',
                'username',
                'password',
                'email',
                'is_staff'
                )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                'company',
                'reviewer',
                'title',
                'summary',
                'rating',
                'ip_address',
                )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')
