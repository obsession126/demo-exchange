from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    user_mone = models.PositiveIntegerField()


    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    phone = models.CharField(max_length=20,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Profile of {self.user.email}"