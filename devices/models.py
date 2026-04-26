class Device(models.Model):
    dev_eui = models.CharField(max_length=32, unique=True)
    latest_status = models.CharField(max_length=10, default="UNKNOWN")

    def __str__(self):
        return self.dev_eui
    

class Payload(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="payloads")
    f_cnt = models.IntegerField()
    data = models.CharField(max_length=255)
    hex_data = models.CharField(max_length=255)
    status = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('device', 'f_cnt')  # prevents duplicates