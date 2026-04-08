# FitHub CRM - Fitness Center Management System

A comprehensive Salesforce-inspired fitness center management system built with Flask backend and modern HTML/CSS/JavaScript frontend. The system features real-time data visualization with synthetic data, member management, class scheduling, trainer assignment, payment tracking, and advanced analytics.

## 🚀 Features

### Core Functionality
- **Member Management**: Register, track, and manage fitness center members with subscription plans
- **Class Scheduling**: Create and manage fitness classes with trainer assignment
- **Trainer Management**: Track trainer availability, specialization, and performance ratings
- **Payment Processing**: Manage transactions, subscriptions, and revenue tracking
- **Attendance Tracking**: Real-time check-in system for members
- **Analytics & Reporting**: Comprehensive dashboards with charts and insights

### Smart Features
- **Smart Trainer Allocation**: Automatically assign trainers based on availability and specialization
- **Predictive Renewal Alerts**: Identify members at risk of churn
- **Real-time Dashboard**: Live data updates with animated metrics
- **Revenue Analytics**: Track revenue by membership plan and payment trends
- **Member Analytics**: Retention rates, growth trends, and engagement metrics

### UI/UX
- Modern dark-themed dashboard with gradient effects
- Responsive design (desktop, tablet, mobile)
- Interactive charts and visualizations using Chart.js
- Real-time status indicators and activity feeds
- Intuitive navigation with collapsible sidebar

## 📋 Technology Stack

- **Backend**: Python Flask 2.3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Charts**: Chart.js 3.9.1
- **Icons**: FontAwesome 6.4.0
- **Cross-Origin**: Flask-CORS for API endpoints

## 📁 Project Structure

```
fitness-crm/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── routes.py             # API endpoints
│   └── data_generator.py     # Synthetic data generation
├── static/
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── main.js           # Frontend JavaScript
├── templates/
│   └── index.html            # Main HTML template
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd fitness-crm
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python run.py
```

The application will:
1. Create a SQLite database (`fitness_crm.db`)
2. Generate synthetic data automatically
3. Start the Flask server at `http://localhost:5000`

### Step 3: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 💾 Database Models

### Member
- Personal information (name, email, phone)
- Membership plan (Silver, Gold, Platinum)
- Subscription tracking (join date, renewal date)
- Status (Active, Inactive, Pending)
- Total classes attended

### Trainer
- Professional information and specialization
- Availability schedule
- Years of experience
- Performance rating
- Current status (Available, In Session, Break)

### FitnessClass
- Class details (name, type, duration)
- Trainer assignment
- Schedule information
- Capacity management (max capacity, current enrollment)
- Status tracking

### Payment
- Member and transaction details
- Amount and payment type
- Payment date and status
- Transaction history

### Attendance
- Member check-in records
- Class association
- Check-in timestamps

### Analytics
- Revenue metrics
- Member statistics
- Occupancy data
- Retention rates
- Timestamp for tracking trends

## 📊 API Endpoints

### Dashboard Analytics
- `GET /api/analytics` - Overall system metrics
- `GET /api/realtime-data` - Real-time data updates

### Members
- `GET /api/members` - List all members
- `GET /api/members/<id>` - Get member details
- `GET /api/members/stats` - Member statistics

### Trainers
- `GET /api/trainers` - List all trainers
- `GET /api/trainers/<id>` - Get trainer details
- `GET /api/trainers/stats` - Trainer statistics
- `GET /api/trainers/top-rated` - Top 5 rated trainers

### Classes
- `GET /api/classes` - List all classes
- `GET /api/classes/<id>` - Get class details
- `GET /api/classes/stats` - Class statistics

### Payments
- `GET /api/payments` - List all payments
- `GET /api/payments/stats` - Payment statistics
- `GET /api/revenue/by-plan` - Revenue breakdown by membership plan

### Attendance
- `GET /api/attendance` - List recent attendance
- `GET /api/attendance/stats` - Attendance statistics

## 🎨 Dashboard Sections

### 1. Dashboard (Home)
- KPI cards: Revenue, Members, Active Sessions, Occupancy, Retention, Trainers
- Revenue distribution by membership plan
- Trainer status overview
- Recent activity feed (real-time)

### 2. Members
- Member statistics and renewals tracking
- Searchable member table with filters
- Membership plan breakdown
- Member profile actions

### 3. Trainers
- Trainer inventory and status
- Performance ratings and specialization
- Availability tracking
- Top trainers highlights

### 4. Classes
- Class schedule and enrollment
- Trainer assignments
- Occupancy rates and utilization
- Class type distribution

### 5. Payments
- Transaction history and status
- Revenue tracking
- Payment method breakdown
- Monthly revenue trends

### 6. Attendance
- Daily check-in records
- Member attendance patterns
- Weekly attendance trends
- Peak hours analysis

### 7. Analytics
- Member growth trends
- Class type distribution
- Payment trends
- Top performers

## 🔄 Real-time Updates

The system simulates real-time data updates by:
- Polling the `/api/realtime-data` endpoint every 5 seconds
- Randomly generating realistic updates (member check-ins, payments, trainer status changes)
- Updating UI elements without full page reload
- Maintaining synthetic data consistency

## 📊 Synthetic Data

The system includes a comprehensive data generator that creates:
- **50 Members** with various membership plans and status
- **12 Trainers** with different specializations and ratings
- **20 Fitness Classes** across different types and schedules
- **80 Payment Records** with various statuses
- **150 Attendance Records** for class participation

All data is randomly generated and realistic for demonstration purposes.

## 🎯 Usage Scenarios

### Scenario 1: Check Daily Revenue
1. Go to Dashboard
2. View "Total Revenue" KPI card
3. Click on Revenue chart for details

### Scenario 2: Manage Member Renewals
1. Navigate to Members section
2. Check "Pending Renewals" stat
3. See renewal dates in the members table
4. Send renewal reminders to at-risk members

### Scenario 3: Optimize Class Scheduling
1. Go to Classes section
2. Review "Avg. Occupancy" metric
3. Identify underutilized classes
4. Adjust schedules or marketing

### Scenario 4: Track Trainer Performance
1. Visit Trainers section
2. Sort by rating to find top performers
3. View trainer status and availability
4. Optimize trainer assignments

## 🛠️ Customization

### Modify Synthetic Data
Edit `app/data_generator.py` to change:
- Number of members, trainers, classes
- Data ranges and distributions
- Default membership plans
- Trainer specializations

### Customize Styling
Edit `static/css/style.css` to modify:
- Color scheme (CSS variables)
- Layout and responsive breakpoints
- Component styling

### Add New Features
1. Create new database model in `app/models.py`
2. Add API routes in `app/routes.py`
3. Create UI section in `templates/index.html`
4. Add styling in `static/css/style.css`
5. Add JavaScript logic in `static/js/main.js`

## 📱 Responsive Design

The dashboard is fully responsive:
- **Desktop** (1200px+): Full layout with sidebar
- **Tablet** (768px - 1199px): Collapsible sidebar
- **Mobile** (< 768px): Hamburger menu, optimized tables

## 🔐 Security Considerations

For production use, implement:
- User authentication with JWT tokens
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection prevention (already using ORM)
- HTTPS/SSL encryption
- Rate limiting on API endpoints
- CORS configuration for frontend domain

## 📈 Performance Optimization

The system includes:
- Chart.js for efficient chart rendering
- Debounced API calls
- Client-side data caching
- Lazy loading of sections
- Optimized CSS with minimal repaints

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete old database and regenerate
rm fitness_crm.db
python run.py
```

### Port Already in Use
```bash
# Change port in run.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### CORS Errors
- Ensure Flask-CORS is installed
- Check CORS configuration in `app/__init__.py`

### Missing Data
- Verify synthetic data was generated (check console output)
- Check database connection in `app/__init__.py`

## 📚 Future Enhancements

- Mobile app for members and trainers
- Integration with payment gateways (Stripe, PayPal)
- Wearable device integration (Fitbit, Apple Watch)
- AI-based workout recommendations
- Gamification features (badges, leaderboards)
- Email/SMS notification system
- Calendar integration for class scheduling
- Video streaming for virtual classes

## 📄 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Development Notes

### Adding a New Page Section
1. Add nav link in `templates/index.html` sidebar
2. Create section div with unique ID
3. Add event listener in `static/js/main.js`
4. Implement load function and API calls
5. Style using `static/css/style.css`

### Database Migrations
- Modify model in `models.py`
- Delete `fitness_crm.db` to regenerate with new schema
- Or use Flask-Migrate for versioned migrations

### Testing
- Test API endpoints with Postman or curl
- Check browser console for JavaScript errors
- Verify responsive design at different screen sizes

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs (F12 in browser)
3. Verify all dependencies are installed
4. Check requirements.txt versions

---

**FitHub CRM v1.0** - Smart Fitness Center Management System
Built with ❤️ for fitness centers worldwide
