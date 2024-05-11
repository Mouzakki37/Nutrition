from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.CharField(max_length=20)
    
    def __str__(self):
        return f"User: {self.pk}, {self.gender}, {self.age} "






class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    activity = models.CharField(max_length=20)
    calories_maintenance = models.DecimalField(max_digits=8, decimal_places=0, default=0.0)  
    calories_weight_loss = models.DecimalField(max_digits=8, decimal_places=0, default=0.0)  
    calories_weight_gain = models.DecimalField(max_digits=8, decimal_places=0, default=0.0) 

    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
            