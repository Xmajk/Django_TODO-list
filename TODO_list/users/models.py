from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser,AbstractBaseUser, PermissionsMixin,BaseUserManager,Group,User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, password, **other_fields):

        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_staff", True)

        if other_fields.get("is_superuser") is not True and other_fields.get("is_staff") is not True:
            raise ValueError("bad setter of privilegie")
        return self.create_user(username, password, **other_fields)

    def create_user(self,username,password,**other_fields):
        user_now = self.model(username=username,**other_fields)
        user_now.set_password(password)
        user_now.save()
        return user_now

class User(AbstractBaseUser, PermissionsMixin):
    """
    Třída představující uživatele (authentikační třída)
    """

    username = models.CharField(_("username"),max_length=150,unique=True)
    first_name= models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name","last_name"]

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(f'{self.password}')
        super(User, self).save(*args, **kwargs)