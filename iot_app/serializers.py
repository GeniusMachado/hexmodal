from rest_framework import serializers
from .models import Device, Payload

class PayloadSerializer(serializers.Serializer):
    fCnt = serializers.IntegerField()
    devEUI = serializers.CharField(max_length=16)
    data = serializers.CharField()
    rxInfo = serializers.ListField()
    txInfo = serializers.DictField()

    def create(self, validated_data):
        import base64

        dev_eui = validated_data['devEUI']
        f_cnt = validated_data['fCnt']
        data_b64 = validated_data['data']

        # Decode Base64 to bytes, then to hex
        data_bytes = base64.b64decode(data_b64)
        data_hex = data_bytes.hex()

        # Check if value is 1 (passing) or not
        status = data_bytes == b'\x01'  # 0x01 is 1

        # Get or create device
        device, created = Device.objects.get_or_create(
            dev_eui=dev_eui,
            defaults={'name': f'Device {dev_eui}'}
        )

        # Create payload
        payload = Payload.objects.create(
            device=device,
            f_cnt=f_cnt,
            data_hex=data_hex,
            status=status,
            rx_info=validated_data['rxInfo'],
            tx_info=validated_data['txInfo']
        )

        # Update device latest status
        device.latest_status = status
        device.save()

        return payload

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'