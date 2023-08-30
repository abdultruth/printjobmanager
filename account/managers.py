from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an Email Address !')
        email = self.normalize_email(email) 
        user = self.model(
            email=email,**extra_fields
        )
        
        user.set_password(password)
        user.is_active = False
        user.is_admin = False
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)