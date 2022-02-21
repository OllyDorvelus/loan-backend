import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class AbstractModel(models.Model):
    """Abstract model that handles common fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomerManager(models.Manager):
    def create_customer(self, user, phone_number, **extra_fields):
        """Create and save a new customer"""
        if not user:
            raise ValueError("Customer must have a user")
        if not phone_number:
            raise ValueError("Customer must have phone number")

        customer = self.model(user=user, phone_number=phone_number, **extra_fields)
        customer.save(using=self._db)
        return customer


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, blank=True)
    phone_number = PhoneNumberField(unique=True)
    secondary_phone_number = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Customer(AbstractModel):
    user = models.OneToOneField('User', on_delete=models.PROTECT, related_name='customer')
    payslip = models.FileField(upload_to='uploads/payslips', blank=True)
    id_file = models.FileField(upload_to='uploads/ids', blank=True)
    is_blacklisted = models.BooleanField(default=False)
    objects = CustomerManager()

    def __str__(self):
        return self.user.email

    @property
    def number(self):
        return str(self.phone_number)

    @property
    def whatsapp_number(self):
        return f'whatsapp:{self.phone_number}'
