# IoT Payload Parser

A Django REST Framework application for parsing IoT device payloads with token authentication.

## Features

- **Device Management**: Tracks IoT devices with their latest status (passing/failing)
- **Payload Processing**: Parses incoming payloads, decodes Base64 data, and validates frame counters
- **Token Authentication**: Uses JWT tokens for API access
- **Duplicate Prevention**: Ensures no duplicate messages based on frame counter (fCnt)
- **Status Tracking**: Automatically updates device status based on payload data

## Models

### Device
- `dev_eui`: Unique 16-character device identifier
- `name`: Optional device name
- `latest_status`: Boolean indicating current status (True = passing, False = failing)
- `created_at`/`updated_at`: Timestamps

### Payload
- `device`: Foreign key to Device
- `f_cnt`: Frame counter (unique per device)
- `data_hex`: Decoded hexadecimal data
- `status`: Boolean status (True if data value is 1)
- `rx_info`/`tx_info`: JSON fields for gateway and transmission info
- `received_at`: Timestamp

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT token pair
- `POST /api/token/refresh/`: Refresh JWT token

### Payload Submission
- `POST /api/payload/`: Submit IoT payload (requires authentication)

## Setup Instructions

### Prerequisites
- Python 3.9+
- uv package manager

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd iot-payload-parser
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run migrations:
   ```bash
   uv run python manage.py migrate
   ```

4. Create a superuser (optional, for admin access):
   ```bash
   uv run python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   uv run python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Usage

### Obtain Authentication Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Submit Payload

```bash
curl -X POST http://127.0.0.1:8000/api/payload/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fCnt": 100,
    "devEUI": "abcdabcdabcdabcd",
    "data": "AQ==",
    "rxInfo": [
      {
        "gatewayID": "1234123412341234",
        "name": "G1",
        "time": "2022-07-19T11:00:00",
        "rssi": -57,
        "loRaSNR": 10
      }
    ],
    "txInfo": {
      "frequency": 86810000,
      "dr": 5
    }
  }'
```

### Payload Processing Logic

1. **Authentication**: Request must include valid JWT token
2. **Duplicate Check**: Validates fCnt is unique for the device
3. **Data Decoding**: Base64 data is decoded to bytes, then converted to hex
4. **Status Determination**: If decoded value equals 1 (0x01), status is "passing"; otherwise "failing"
5. **Device Creation/Update**: Creates device if it doesn't exist, updates latest status
6. **Payload Storage**: Saves payload with all metadata

## Testing

The application includes a default superuser:
- Username: `admin`
- Password: `admin123`

Use this to obtain tokens for testing the payload endpoint.

## Technologies Used

- **Django**: Web framework
- **Django REST Framework**: API framework
- **Simple JWT**: Token authentication
- **uv**: Package management
- **SQLite**: Database (development)

## Deployment

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting `DEBUG = False`
- Configuring proper `SECRET_KEY`
- Using environment variables for sensitive data
- Setting up proper CORS and security headers