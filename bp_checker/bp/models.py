from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    sex = (
        ('Male', 'Male'), 
        ('Female', 'Female')
        )
    phone_no = models.CharField(max_length=11)
    gender = models.CharField(max_length=6, choices=sex)

numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=100)
    age = models.IntegerField() 
    bmi = models.FloatField(max_length=10)
    current_smoker = models.CharField(max_length=5)
    heart_rate = models.IntegerField()
    result = models.IntegerField()
    
    # def __str__(self):
    #     return self.result
    
    
    