import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from organisation.models import Organisation

class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have a first name')
        if not lastName:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, email, firstName, lastName, password=None):
        user = self.create_user(
            email,
            password=password,
            firstName=firstName,
            lastName=lastName,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=32, unique=True, blank=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    organisations = models.ManyToManyField('organisation.Organisation', through='organisation.Membership', related_name='user_organisations')
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.userId:
            self.userId = uuid.uuid4().hex[:32]  
        super().save(*args, **kwargs)

