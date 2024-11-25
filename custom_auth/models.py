from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.utils import timezone
from join_contacts.models import Contact

class User(AbstractUser):
    """
    Benutzerdefiniertes User-Modell, das das Standard-AbstractUser-Modell erweitert,
    um E-Mail für die Authentifizierung zu verwenden und zusätzliche Felder hinzuzufügen.
    """
    email = models.EmailField(unique=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    created_at = models.DateTimeField(default=timezone.now)
    contact_id = models.OneToOneField(
        'join_contacts.Contact',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user',
    )
    is_active = models.BooleanField(default=False)
    remember = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)