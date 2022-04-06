from django.db import models

# Create your models here.

class Users(models.Model):
    display_photo = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    your_email = models.CharField(primary_key=True, max_length=128)
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

#class Buddy(models.Model):