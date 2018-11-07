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
                'email',
                'is_staff'
                )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
                'id',
                'title',
                'summary',
                'rating',
                )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')
