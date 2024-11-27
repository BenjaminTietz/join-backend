from django.db import models
from phone_field import PhoneField
from datetime import date
import random

# Create your models here.
class Contact(models.Model):
    COLOR_CHOICES = [
        "#6E52FF",  # blue
        "#462F8A",  # dark blue
        "#FC71FF",  # pink
        "#9327FF",  # purple
        "#FF7A00",  # orange
        "#1FD7C1",  # light green
        "#FF4646",  # red
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    initials = models.CharField(max_length=2, blank=True)
    color = models.CharField(max_length=7, blank=True, default='')
    created_at = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if not self.initials:
            self.initials = ''.join([n[0] for n in self.name.split()[:2]]).upper()
        if not self.color:
            self.color = random.choice(self.COLOR_CHOICES)
        super(Contact, self).save(*args, **kwargs)