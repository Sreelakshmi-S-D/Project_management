from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager



# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username=models.CharField(null=True,blank=True)
    email = models.EmailField(unique=True)
    Fullname = models.CharField(max_length=100,null=True,blank=False)
    photo = models.FileField(upload_to="media/", null=True, default="None")
    phone = models.BigIntegerField(null=False, default=0)
    dob = models.DateField(null=True,blank=True)
    job_type = models.CharField(max_length=100,default='None')
    objects = CustomUserManager()
    status=models.CharField(default='not approved')

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['Fullname']



class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField()