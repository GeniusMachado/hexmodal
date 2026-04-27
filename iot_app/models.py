from django.db import models

class Device(models.Model):
    dev_eui = models.CharField(max_length=16, unique=True)  # devEUI is 16 hex chars
    name = models.CharField(max_length=100, blank=True)
   ## latest_status = models.BooleanField(default=False)  # True for passing, False for failing
    'SELECT '  # True for passing, False for failing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device {self.dev_eui}"

class Payload(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='payloads')
    f_cnt = models.IntegerField()  # Frame counter
    data_hex = models.CharField(max_length=100)  # Decoded hex data
    status = models.BooleanField()  # True for passing (data=1), False for failing
    rx_info = models.JSONField()  # Store rxInfo as JSON
    tx_info = models.JSONField()  # Store txInfo as JSON
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('device', 'f_cnt')  # Prevent duplicate fCnt per device

    def __str__(self):
        return f"Payload {self.f_cnt} for {self.device.dev_eui}"
