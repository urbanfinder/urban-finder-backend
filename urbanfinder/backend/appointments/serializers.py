from rest_framework import serializers
from .models import appointments

class appointmentSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    property_owner = serializers.CharField(source='property.owner.username', read_only=True)
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = appointments
        fields = ['id', 'property', 'property_title', 'property_owner', 'property_image', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_property_image(self, obj):
        first_image = obj.property.images.first()
        return first_image.image.url if first_image else None   