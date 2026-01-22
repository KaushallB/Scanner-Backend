from rest_framework import routers
from .views import EventsViewSet, QRCodeViewSet, generate_qr
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'events', EventsViewSet)
router.register(r'qrcodes', QRCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-qr/', generate_qr, name='generate_qr'),
]
