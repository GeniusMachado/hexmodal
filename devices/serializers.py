class PayloadSerializer(serializers.Serializer):
    fCnt = serializers.IntegerField()
    devEUI = serializers.CharField()
    data = serializers.CharField()