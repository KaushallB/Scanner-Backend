from django.shortcuts import render
from rest_framework import viewsets
from .models import Event
from .serializers import EventModelSerializer

# Create your views here.

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
