from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class Role(models.Model):
    
    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('estudiante', 'Estudiante'),
        ('admin', 'Admin')
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
    


# Metodo para la creacion de usuario admin o superusuario
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        from apps.users.models import Role

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.objects.get(name="admin"))

        return self.create_user(email, password, **extra_fields)
    
    
    
# modelo user heredando del user propio de django    
class User(AbstractUser):
    
    username = None
    
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    