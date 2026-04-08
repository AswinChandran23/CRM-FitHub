# FitHub CRM - API Testing Guide

This guide contains example curl commands to test the FitHub CRM API endpoints.

## Base URL
```
http://localhost:5000/api
```

## Prerequisites
- Application must be running (`python run.py`)
- curl installed (or use Postman/Insomnia)

---

## Analytics Endpoints

### Get Overall Analytics
```bash
curl http://localhost:5000/api/analytics
```

### Get Real-time Data
```bash
curl http://localhost:5000/api/realtime-data
```

---

## Members Endpoints

### List All Members
```bash
curl http://localhost:5000/api/members
```

### Get Specific Member
```bash
curl http://localhost:5000/api/members/1
```

### Get Members Statistics
```bash
curl http://localhost:5000/api/members/stats
```

---

## Trainers Endpoints

### List All Trainers
```bash
curl http://localhost:5000/api/trainers
```

### Get Specific Trainer
```bash
curl http://localhost:5000/api/trainers/1
```

### Get Trainers Statistics
```bash
curl http://localhost:5000/api/trainers/stats
```

### Get Top Rated Trainers
```bash
curl http://localhost:5000/api/trainers/top-rated
```

---

## Classes Endpoints

### List All Classes
```bash
curl http://localhost:5000/api/classes
```

### Get Specific Class
```bash
curl http://localhost:5000/api/classes/1
```

### Get Classes Statistics
```bash
curl http://localhost:5000/api/classes/stats
```

---

## Payments Endpoints

### List All Payments
```bash
curl http://localhost:5000/api/payments
```

### Get Payments Statistics
```bash
curl http://localhost:5000/api/payments/stats
```

### Get Revenue by Plan
```bash
curl http://localhost:5000/api/revenue/by-plan
```

---

## Attendance Endpoints

### List Recent Attendance
```bash
curl http://localhost:5000/api/attendance
```

### Get Attendance Statistics
```bash
curl http://localhost:5000/api/attendance/stats
```

---

## Example Response Formats

### Members Response
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john@email.com",
  "phone": "+1234567890",
  "membership_plan": "Gold",
  "join_date": "2024-01-15",
  "renewal_date": "2025-01-15",
  "status": "Active",
  "total_classes": 42
}
```

### Trainers Response
```json
{
  "id": 1,
  "name": "Sarah Johnson",
  "email": "sarah@fithouse.com",
  "specialization": "Strength Coach",
  "availability": "Mon-Fri 9AM-6PM",
  "experience_years": 8,
  "rating": 4.8,
  "status": "Available"
}
```

### Classes Response
```json
{
  "id": 1,
  "name": "Morning Yoga",
  "type": "Yoga",
  "trainer_id": 1,
  "trainer_name": "Sarah Johnson",
  "schedule_time": "2024-04-05 07:00",
  "duration_minutes": 60,
  "max_capacity": 30,
  "current_enrollment": 28,
  "status": "Scheduled",
  "utilization": 93.3
}
```

### Payments Response
```json
{
  "id": 1,
  "member_id": 1,
  "member_name": "John Smith",
  "amount": 79.99,
  "payment_date": "2024-04-05 14:30",
  "status": "Completed",
  "payment_type": "Credit Card"
}
```

### Analytics Response
```json
{
  "total_revenue": 5234.50,
  "total_members": 50,
  "active_classes": 8,
  "avg_occupancy": 78.5,
  "member_retention_rate": 85.0,
  "timestamp": "2024-04-05 14:35:20"
}
```

---

## Testing with Python requests

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Get all members
response = requests.get(f"{BASE_URL}/members")
members = response.json()
print(json.dumps(members[:1], indent=2))

# Get analytics
response = requests.get(f"{BASE_URL}/analytics")
analytics = response.json()
print(json.dumps(analytics, indent=2))

# Get trainers stats
response = requests.get(f"{BASE_URL}/trainers/stats")
stats = response.json()
print(json.dumps(stats, indent=2))
```

---

## Testing with PowerShell

```powershell
# Get members
Invoke-WebRequest -Uri http://localhost:5000/api/members | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Get analytics
Invoke-WebRequest -Uri http://localhost:5000/api/analytics | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Pretty print
$response = Invoke-WebRequest -Uri http://localhost:5000/api/trainers/stats
$json = $response.Content | ConvertFrom-Json
$json | ConvertTo-Json
```

---

## Notes

- All responses are in JSON format
- Endpoints support CORS for cross-origin requests
- Real-time data updates every 5 seconds in the `/api/realtime-data` endpoint
- Synthetic data is generated on first application run
- To reset data, delete `fitness_crm.db` and restart the application

---

## Status Codes

- `200 OK` - Request successful
- `404 NOT FOUND` - Resource not found
- `500 INTERNAL SERVER ERROR` - Server error

---

For more information, see the README.md file.
