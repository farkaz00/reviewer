from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        app_label = "reviews"


class Review(models.Model):

    RATING_CHOICES=( 
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateField(auto_now=True)
    reviewer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta:
        app_label = "reviews"
