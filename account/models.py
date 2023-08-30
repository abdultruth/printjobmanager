from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group, Permission



from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=20, null=True, blank=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = CustomUserManager()
    
    class Meta:
        ordering = ['date_joined']
        
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, add_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        # The user is identified by their email address
        return self.email
        
        
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

    
    
class PrintManager():
    pass
    
    