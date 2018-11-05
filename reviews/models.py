from django.db import models

# Create your models here.
class Reviewer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    hash = models.CharField(max_length=255)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

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
    rating = models.CharField(choices=RATING_CHOICES)
    ip_address = models.IPAddressField()
    submission_date = models.DateField(auto_now=True)
    reviewer = models.ForeignKey('Reviewer', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
