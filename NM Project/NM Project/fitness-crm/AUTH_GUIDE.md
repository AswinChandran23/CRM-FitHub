# 🔐 FitHub CRM - Authentication & User Management Guide

## Overview

FitHub CRM now includes a complete authentication system with landing page, login, and signup functionality. Users must authenticate before accessing the dashboard.

---

## 🚀 Quick Start

### Using Demo Credentials

When you first run the application, three demo users are automatically created:

**Option 1: Admin Account** (Recommended for testing)
- Email: `admin@fithouse.com`
- Password: `password123`
- Role: Manager

**Option 2: Manager Account**
- Email: `john@fithouse.com`
- Password: `password123`
- Role: Manager

**Option 3: Trainer Account**
- Email: `sarah@fithouse.com`
- Password: `password123`
- Role: Trainer

---

## 📋 User Flow

### 1. **Landing Page** (http://localhost:5000/)
- Shows project information and features
- "Get Started" button → Signup Modal
- "Login" button → Login Modal

### 2. **Sign Up**
- Enter full name
- Enter email
- Select role (Gym Manager, Trainer, or Staff)
- Enter password (minimum 6 characters)
- Confirm password
- Account is created and user is automatically logged in
- Redirected to dashboard

### 3. **Login**
- Enter email
- Enter password
- Account verified
- Redirected to dashboard with user info displayed

### 4. **Dashboard**
- User's name displayed in header (top-right)
- Click on user profile to see dropdown menu
- Options: View Profile, Logout

### 5. **Logout**
- Click on user profile dropdown
- Select "Logout"
- Confirm logout
- Redirected to landing page

---

## 🔧 Technical Implementation

### Database Model: User

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='Manager')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### API Endpoints

#### Sign Up
```bash
POST /api/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@email.com",
  "password": "password123",
  "confirm_password": "password123",
  "role": "Manager"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@email.com",
    "role": "Manager",
    "created_at": "2026-04-05"
  }
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@fithouse.com",
  "password": "password123"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "Admin User",
    "email": "admin@fithouse.com",
    "role": "Manager",
    "created_at": "2026-04-05"
  }
}
```

#### Logout
```bash
POST /api/auth/logout
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Error Responses

**Duplicate Email (409):**
```json
{
  "error": "Email already registered"
}
```

**Invalid Login (401):**
```json
{
  "error": "Invalid email or password"
}
```

**Validation Error (400):**
```json
{
  "error": "Passwords do not match"
}
```

---

## 🎯 Frontend Implementation

### Authentication Flow (JavaScript)

#### 1. Store User Info
```javascript
const user = {
  id: 1,
  name: "John Doe",
  email: "john@email.com",
  role: "Manager"
};

// Store in session storage
sessionStorage.setItem('user', JSON.stringify(user));
```

#### 2. Retrieve User Info
```javascript
const user = AuthManager.getUser();
console.log(user.name); // "John Doe"
```

#### 3. Check Authentication
```javascript
if (!AuthManager.isAuthenticated()) {
  window.location.href = '/'; // Redirect to landing
}
```

#### 4. Logout
```javascript
AuthManager.logout(); // Remove from storage
window.location.href = '/'; // Redirect to landing
```

### AuthManager Class (auth.js)

```javascript
class AuthManager {
    static getUser() {
        const userStr = sessionStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    static setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    static logout() {
        sessionStorage.removeItem('user');
    }

    static isAuthenticated() {
        return this.getUser() !== null;
    }

    static requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/';
        }
    }
}
```

---

## 📁 File Structure

### New Files Created

```
fitness-crm/
├── templates/
│   ├── landing.html        ← Landing page with login/signup modals
│   └── index.html          ← Dashboard (unchanged, now requires auth)
├── static/
│   ├── js/
│   │   ├── auth.js         ← Authentication utilities
│   │   └── main.js         ← Updated with user display
│   └── css/
│       └── style.css       ← Added user dropdown styles
└── app/
    ├── models.py           ← Added User model
    ├── routes.py           ← Added auth endpoints
    └── data_generator.py   ← Creates demo users
```

---

## 🔐 Security Considerations

### Current Implementation (Demo)
- Uses SHA256 hashing for passwords
- Session storage (not persistent, cleared when browser closes)
- Basic validation

### For Production, Implement:
1. **Use bcrypt** instead of SHA256
   ```bash
   pip install bcrypt
   ```

2. **JWT Tokens** for API authentication
   ```bash
   pip install PyJWT
   ```

3. **Email Verification**
   - Verify email addresses
   - Send confirmation email

4. **Password Strength**
   - Minimum complexity requirements
   - Password reset functionality

5. **Rate Limiting**
   - Limit login attempts
   - Prevent brute force attacks

6. **HTTPS**
   - Use SSL/TLS in production
   - Secure cookies

7. **CORS Configuration**
   - Restrict to trusted domains only

---

## 🧪 Testing Auth System

### Test 1: Create New Account
1. Go to http://localhost:5000
2. Click "Get Started"
3. Fill in form with:
   - Name: Test User
   - Email: test@example.com
   - Role: Gym Manager
   - Password: testpass123
4. Submit
5. Should see dashboard with "Test User" in header

### Test 2: Login with Demo Account
1. Go to http://localhost:5000
2. Click "Login"
3. Enter: admin@fithouse.com / password123
4. Should see dashboard with "Admin User" in header

### Test 3: Logout
1. When logged in, click on user profile in top-right
2. Select "Logout"
3. Confirm logout
4. Should be redirected to landing page

### Test 4: Auth Protected
1. Open browser developer console
2. Run: `window.location.href = '/dashboard'`
3. Should redirect back to landing page if not authenticated

### Test 5: Session Persistence
1. Login and go to dashboard
2. Refresh the page (F5)
3. Should remain on dashboard (session storage persists)
4. Close browser and reopen
5. Session is cleared (fresh login required)

---

## 📝 Customization

### Change Demo Credentials
Edit `app/data_generator.py`:

```python
demo_users = [
    User(name='Your Name', email='your@email.com', password=hash_password('your_password'), role='Manager'),
]
```

### Customize Login Page
Edit `templates/landing.html`:
- Change logo, colors, text
- Modify form fields
- Adjust modal styling

### Change Password Requirements
Edit `app/routes.py` in `/api/auth/signup`:

```python
if len(password) < 8:  # Change minimum length
    return jsonify({'error': 'Password must be at least 8 characters'}), 400
```

### Add New Roles
Edit `app/models.py` User model and update signup form in `landing.html`:

```python
# In signup form
<option value="Role1">Role 1</option>
<option value="Role2">Role 2</option>
```

---

## 🚨 Troubleshooting

### Issue: "Invalid email or password" on login
**Solution**: Check that you're using correct credentials
- Try: admin@fithouse.com / password123

### Issue: Redirects to landing after every refresh
**Solution**: Session storage was cleared
- Make sure browser hasn't cleared local/session storage
- Check browser dev tools > Application > Session Storage

### Issue: User dropdown doesn't appear
**Solution**: Click on user profile in header
- Make sure JavaScript is enabled
- Check browser console for errors

### Issue: Can't create account - "Email already registered"
**Solution**: Email exists in database
- Use different email
- Or reset database: Delete `fitness_crm.db` and restart

### Issue: Dashboard doesn't load
**Solution**: Authentication check failing
- Make sure you're logged in (have user in session storage)
- Try logging in again

---

## 📊 Database Queries

### View All Users
```python
from app.models import User
users = User.query.all()
for user in users:
    print(f"{user.name} ({user.email})")
```

### Find User by Email
```python
user = User.query.filter_by(email='admin@fithouse.com').first()
```

### Update User Role
```python
user = User.query.get(1)
user.role = 'Trainer'
db.session.commit()
```

### Delete User
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

---

## 🔄 Workflow Examples

### Example 1: Complete User Journey
```
1. New user visits http://localhost:5000 (Landing Page)
2. Clicks "Get Started" → Signup Modal
3. Fills form and creates account
4. Auto-logged in and redirected to dashboard
5. Name shows in header: "John Doe"
6. Clicks profile → Admin User
7. User sees their name and can logout
```

### Example 2: Returning User
```
1. User visits http://localhost:5000 (Landing Page)
2. Clicks "Login" → Login Modal
3. Enters credentials and clicks Login
4. Redirected to dashboard
5. User info loaded from session
6. Can access all features
```

### Example 3: Multi-User Scenario
```
1. Manager logs in → sees Manager dashboard
2. Logs out
3. Trainer logs in → sees Trainer dashboard (same for now)
4. Each session is independent
```

---

## 📈 Future Enhancements

### Planned Features
- [ ] Email verification on signup
- [ ] Password reset functionality
- [ ] Remember me checkbox
- [ ] Two-factor authentication (2FA)
- [ ] Role-based access control (RBAC)
- [ ] User profile page with edit capability
- [ ] Password change functionality
- [ ] Account deactivation
- [ ] Login history tracking
- [ ] Session management

### API Improvements
- [ ] Implement JWT tokens
- [ ] Add refresh token rotation
- [ ] Implement CORS properly for production
- [ ] Add rate limiting to auth endpoints
- [ ] Implement OAuth2 (Google, GitHub login)

---

## ✅ Checklist

- ✅ Landing page created
- ✅ Login functionality implemented
- ✅ Signup functionality implemented
- ✅ User display in dashboard header
- ✅ Logout functionality
- ✅ Session storage for user data
- ✅ Auth protection on dashboard
- ✅ Demo user setup
- ✅ Database migration for User model
- ✅ Error handling and validation

---

## 📞 Support

For issues with authentication:
1. Check browser console (F12) for errors
2. Verify database exists (fitness_crm.db)
3. Check that Flask server is running
4. Try clearing browser cache
5. Reset database if needed (delete fitness_crm.db)

---

## 🎉 Summary

Your FitHub CRM now has a professional authentication system!

**To use:**
1. Start the app: `python run.py`
2. Visit: http://localhost:5000
3. Login with demo account: admin@fithouse.com / password123
4. Or create a new account
5. Enjoy! 

---

**Version**: 1.1 (with Authentication)  
**Last Updated**: April 5, 2026  

Happy managing! 🏋️‍♂️💪
