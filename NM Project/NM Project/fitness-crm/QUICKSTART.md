# Quick Start Guide for FitHub CRM

## Windows Users

### Using PowerShell or Command Prompt:

```bash
# 1. Navigate to project directory
cd "e:\NM Project\fitness-crm"

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# 3. Activate virtual environment
# For PowerShell:
.\venv\Scripts\Activate.ps1
# For Command Prompt:
.\venv\Scripts\activate.bat

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python run.py
```

### The application will output:
```
🏋️  FitHub CRM - Fitness Center Management System
🚀 Server starting at http://localhost:5000
==================================================
```

### Access the Dashboard:
Open your browser and go to: **http://localhost:5000**

---

## Features at a Glance

- 📊 **Real-time Dashboard** with KPI metrics
- 👥 **Member Management** with subscription tracking
- 🏃 **Class Scheduling** with trainer assignment
- 💰 **Payment Processing** with revenue tracking
- 📈 **Advanced Analytics** with charts and reports
- ⚡ **Real-time Updates** with synthetic data simulation

---

## What You'll See

### Dashboard Metrics:
- Total Revenue
- Active Members
- Active Training Sessions
- Average Gym Occupancy
- Member Retention Rate
- Available Trainers

### Interactive Sections:
- Members List (50+ members)
- Trainers Directory (12 trainers)
- Class Schedule (20+ classes)
- Payment History (80+ transactions)
- Attendance Records (150+ check-ins)
- Analytics Reports with Charts

---

## Navigation

Click on the menu items in the left sidebar to navigate:
- 📊 **Dashboard** - Overview and KPIs
- 👥 **Members** - Member management
- 🏃 **Trainers** - Trainer profiles
- 📅 **Classes** - Schedule and enrollment
- 💳 **Payments** - Transaction history
- ✅ **Attendance** - Check-in records
- 📈 **Analytics** - Reports and insights

---

## Synthetic Data

The system automatically generates realistic data including:
- 50 fitness center members
- 12 certified trainers
- 20 scheduled fitness classes
- Various payment records
- Attendance history
- Real-time activity updates every 5 seconds

---

## Troubleshooting

### Port 5000 already in use?
Edit `run.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module not found?
```bash
pip install -r requirements.txt
```

### Want fresh data?
```bash
# Delete the database file and restart
del fitness_crm.db
python run.py
```

---

## API Endpoints (for developers)

- GET `/api/analytics` - System metrics
- GET `/api/members` - All members
- GET `/api/trainers` - All trainers
- GET `/api/classes` - All classes
- GET `/api/payments` - Payment history
- GET `/api/attendance` - Check-in records
- GET `/api/realtime-data` - Real-time updates

---

**Enjoy exploring FitHub CRM!** 🚀💪
