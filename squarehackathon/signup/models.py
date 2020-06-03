from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, address, password=None):
        if not email:
            raise ValueError("USERS MUST HAVE AN EMAIL ADDRESS")
        if not username:
            raise ValueError("USERS MUST HAVE A USERNAME")
        if not address:
            raise ValueError("USERS MUST HAVE AN ADDRESS")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            address = address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, address, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            address = address,
        )
        user.admin = True
        user.staff = True
        user.superuser = True

        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    address = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'address']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin
    
    def has_module_perms(self, app_label):
        return True
    

