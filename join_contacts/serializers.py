
from rest_framework import serializers
from join_contacts.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model. Handles the serialization and deserialization
    of contact data, including name, email, phone, initials, and color.

    Fields:
        - id: The contact's ID (auto-generated).
        - name: The name of the contact.
        - email: The email of the contact.
        - phone: The phone number of the contact.
        - initials: The initials of the contact's name.
        - color: A color associated with the contact.
        - created_at: The timestamp when the contact was created.
    """
    class Meta:
        model = Contact
        fields = ('id','name', 'email', 'phone', 'initials', 'color', 'created_at')
    
    def to_representation(self, instance):
        """
        Modify the default representation to include a custom response message.
        """
        data = super().to_representation(instance)
        data['response'] = 'Contact details retrieved successfully.'
        return data
    