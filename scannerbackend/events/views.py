from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, QRCode
from .serializers import EventModelSerializer, QRCodeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all().order_by('-created_at')
    serializer_class = QRCodeSerializer

@api_view(['POST'])
def generate_qr(request):
    qr_type = request.data.get('type')
    data = request.data.get('data')
    fill_color = request.data.get('fill_color', 'black')
    back_color = request.data.get('back_color', 'white')
    box_size = int(request.data.get('box_size', 10))
    border = int(request.data.get('border', 4))

    if qr_type == 'url':
        qr_data = data
    elif qr_type == 'text':
        qr_data = data
    elif qr_type == 'email':
        email = request.data.get('email')
        subject = request.data.get('subject', '')
        body = request.data.get('body', '')
        qr_data = f"mailto:{email}?subject={subject}&body={body}"
    elif qr_type == 'wifi':
        ssid = request.data.get('ssid')
        password = request.data.get('password')
        qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    elif qr_type == 'vcard':
        name = request.data.get('name')
        phone = request.data.get('phone')
        email = request.data.get('vcardEmail')
        qr_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
    else:
        qr_data = data  # default to text

    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(qr_data)
    qr.make(fit=True)

    image = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Save to model
    qr_code_instance = QRCode.objects.create(
        qr_type=qr_type,
        data=qr_data
    )
    fname = f'generated_qr_{qr_code_instance.id}.png'
    qr_code_instance.qr_image.save(fname, ContentFile(buffer.getvalue()), save=True)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
