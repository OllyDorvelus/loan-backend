import uuid

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from phonenumber_field.modelfields import PhoneNumberField
from app.api.whats_app_client import WhatsAppClient


class AbstractModel(models.Model):
    """Abstract model that handles common fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone_number:
            raise ValueError("User must have an email address")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Customer.objects.create_customer(user)
        return user

    def create_superuser(self, phone_number, password):
        """Creates and saves a new super user"""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomerManager(models.Manager):
    def create_customer(self, user, **extra_fields):
        """Create and save a new customer"""
        if not user:
            raise ValueError("Customer must have a user")

        customer = self.model(user=user, **extra_fields)
        customer.save(using=self._db)
        return customer


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    secondary_phone_number = PhoneNumberField(unique=True, null=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def whatsapp_number(self):
        return f"whatsapp:{self.phone_number}"

    @property
    def number(self):
        return str(self.phone_number)


class Customer(AbstractModel):
    user = models.OneToOneField(
        "User", on_delete=models.PROTECT, related_name="customer"
    )
    payslip = models.FileField(upload_to="uploads/payslips", blank=True)
    id_file = models.FileField(upload_to="uploads/ids", blank=True)
    is_blacklisted = models.BooleanField(default=False)
    objects = CustomerManager()

    def __str__(self):
        return f"{self.user}"


# signals
def send_welcome_message(sender, instance, **kwargs):
    if kwargs["created"]:
        WhatsAppClient.send_account_created_message(
            instance.whatsapp_number, instance.full_name
        )


post_save.connect(send_welcome_message, sender=User)
