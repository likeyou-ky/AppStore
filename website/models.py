from django.db import models

# Create your models here.

class Users(models.Model):
    display_photo = models.CharField(max_length=200)
    display_name = models.CharField(max_length=64)
    your_email = models.CharField(primary_key=True, max_length=64)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=64)
    vaccination_status = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    rating = models.FloatField(blank=True, null=True)
    count_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Buddies(models.Model):
    your_email = models.CharField(primary_key=True, max_length=128)
    education = models.CharField(max_length=256)
    height = models.IntegerField(blank=True, null=True)
    rate_per_hour = models.IntegerField(blank=True, null=True)
    interest_1 = models.CharField(max_length=256)
    interest_2 = models.CharField(max_length=256)
    interest_3 = models.CharField(max_length=256)
    interest_4 = models.CharField(max_length=256)
    interest_5 = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'buddies'

class Interests(models.Model):
    interest = models.CharField(primary_key=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'interests'
