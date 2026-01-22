from rest_framework import serializers
from .models import Event, QRCode

class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'qr_code', 'date')

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ('id', 'qr_type', 'data', 'qr_image', 'created_at')