from django.db.models.signals import post_save
from django.dispatch import receiver
from custom_auth.models import User
from join.models import Contact
import logging
import random

logger = logging.getLogger(__name__)

def generate_random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@receiver(post_save, sender=User)
def create_contact_for_user(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for user: {instance.email}, Name: {instance.real_name}, Phone: {instance.phone}")
        contact = Contact.objects.create(
            name=instance.first_name or "Default Name",
            email=instance.email,
            phone=instance.phone,
        )
        instance.contact_id = contact
        instance.save()
        print(f"Contact created with ID: {contact.id} and name: {contact.name}")