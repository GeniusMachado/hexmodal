from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from .serializers import PayloadSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_payload(request):
    serializer = PayloadSerializer(data=request.data)
    if serializer.is_valid():
        try:
            payload = serializer.save()
            return Response({
                'message': 'Payload processed successfully',
                'payload_id': payload.id,
                'status': 'passing' if payload.status else 'failing'
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({
                'error': 'Duplicate fCnt for this device'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
