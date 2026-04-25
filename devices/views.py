import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Payload

class PayloadView(APIView):

    def post(self, request):
        f_cnt = request.data.get("fCnt")
        dev_eui = request.data.get("devEUI")
        data = request.data.get("data")

        # Get or create device
        device, _ = Device.objects.get_or_create(dev_eui=dev_eui)

        # Check duplicate fCnt
        if Payload.objects.filter(device=device, f_cnt=f_cnt).exists():
            return Response({"error": "Duplicate payload"}, status=400)

        # Decode Base64 → bytes → hex
        decoded_bytes = base64.b64decode(data)
        hex_value = decoded_bytes.hex()

        # Convert to int
        value = int.from_bytes(decoded_bytes, byteorder='big')

        status_value = "PASS" if value == 1 else "FAIL"

        # Save payload
        payload = Payload.objects.create(
            device=device,
            f_cnt=f_cnt,
            data=data,
            hex_data=hex_value,
            status=status_value
        )

        # Update device latest status
        device.latest_status = status_value
        device.save()

        return Response({
            "message": "Payload processed",
            "status": status_value,
            "hex": hex_value
        }, status=201)