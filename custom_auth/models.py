from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.utils import timezone
from join.models import Contact

class User(AbstractUser):
    """
    Benutzerdefiniertes User-Modell, das das Standard-AbstractUser-Modell erweitert,
    um E-Mail für die Authentifizierung zu verwenden und zusätzliche Felder hinzuzufügen.
    """
    username = models.CharField(max_length=150, blank=True, null=True)  # Optional
    email = models.EmailField(unique=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    initials = models.CharField(max_length=2, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    real_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(default=timezone.now)
    contact_id = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        
        if not self.initials and self.real_name:
            self.initials = ''.join([word[0] for word in self.real_name.split()[:2]]).upper()
        super().save(*args, **kwargs)
