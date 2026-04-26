from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Device, Payload


class PayloadEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.payload = {
            'fCnt': 100,
            'devEUI': 'abcdabcdabcdabcd',
            'data': 'AQ==',
            'rxInfo': [
                {
                    'gatewayID': '1234123412341234',
                    'name': 'G1',
                    'time': '2022-07-19T11:00:00',
                    'rssi': -57,
                    'loRaSNR': 10,
                }
            ],
            'txInfo': {
                'frequency': 86810000,
                'dr': 5,
            },
        }

    def test_payload_submission_creates_device_and_payload(self):
        response = self.client.post('/api/payload/', self.payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'passing')
        self.assertTrue(Device.objects.filter(dev_eui='abcdabcdabcdabcd').exists())
        self.assertEqual(Payload.objects.count(), 1)

        payload = Payload.objects.first()
        self.assertEqual(payload.f_cnt, 100)
        self.assertEqual(payload.data_hex, '01')
        self.assertTrue(payload.status)

        device = payload.device
        self.assertTrue(device.latest_status)

    def test_duplicate_fcnt_returns_bad_request(self):
        self.client.post('/api/payload/', self.payload, format='json')
        response = self.client.post('/api/payload/', self.payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Duplicate fCnt', response.data.get('error', ''))
