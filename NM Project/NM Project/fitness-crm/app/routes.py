from flask import Blueprint, render_template, jsonify, request, session
from app import db
from app.models import User, Member, Trainer, FitnessClass, Payment, Attendance, Analytics
from datetime import datetime, timedelta
import random

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ==================== Main Routes ====================

@main_bp.route('/')
def index():
    return render_template('landing.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('index.html')

# ==================== Authentication Routes ====================

@api_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()
        role = data.get('role', 'Manager')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash password (simple hash for demo, use bcrypt in production)
        hashed_password = hash_password(password)
        
        # Create user
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not verify_password(password, user.password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


# ==================== API Routes ====================

# Dashboard Analytics
@api_bp.route('/analytics', methods=['GET'])
def get_analytics():
    analytics = Analytics.query.order_by(Analytics.timestamp.desc()).first()
    if not analytics:
        # Calculate on the fly if not in DB
        members = Member.query.all()
        classes = FitnessClass.query.all()
        payments = Payment.query.filter_by(status='Completed').all()
        
        active_classes = len([c for c in classes if c.status == 'In Progress'])
        total_revenue = sum([p.amount for p in payments])
        avg_occupancy = sum([c.current_enrollment / c.max_capacity * 100 for c in classes]) / len(classes) if classes else 0
        retention = (len([m for m in members if m.status == 'Active']) / len(members) * 100) if members else 0
        
        return jsonify({
            'total_revenue': round(total_revenue, 2),
            'total_members': len(members),
            'active_classes': active_classes,
            'avg_occupancy': round(avg_occupancy, 1),
            'member_retention_rate': round(retention, 1),
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(analytics.to_dict())


# Members
@api_bp.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([member.to_dict() for member in members])


@api_bp.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return jsonify(member.to_dict())


@api_bp.route('/members/stats', methods=['GET'])
def get_members_stats():
    members = Member.query.all()
    stats = {
        'total_members': len(members),
        'active_members': len([m for m in members if m.status == 'Active']),
        'pending_renewals': len([m for m in members if m.renewal_date and m.renewal_date < datetime.utcnow() + timedelta(days=7)]),
        'new_this_month': len([m for m in members if m.join_date > datetime.utcnow() - timedelta(days=30)])
    }
    return jsonify(stats)


# Trainers
@api_bp.route('/trainers', methods=['GET'])
def get_trainers():
    trainers = Trainer.query.all()
    return jsonify([trainer.to_dict() for trainer in trainers])


@api_bp.route('/trainers/<int:id>', methods=['GET'])
def get_trainer(id):
    trainer = Trainer.query.get_or_404(id)
    return jsonify(trainer.to_dict())


@api_bp.route('/trainers/stats', methods=['GET'])
def get_trainers_stats():
    trainers = Trainer.query.all()
    stats = {
        'total_trainers': len(trainers),
        'available': len([t for t in trainers if t.status == 'Available']),
        'in_session': len([t for t in trainers if t.status == 'In Session']),
        'avg_rating': round(sum([t.rating for t in trainers]) / len(trainers), 2) if trainers else 0
    }
    return jsonify(stats)


# Fitness Classes
@api_bp.route('/classes', methods=['GET'])
def get_classes():
    classes = FitnessClass.query.all()
    return jsonify([cls.to_dict() for cls in classes])


@api_bp.route('/classes/<int:id>', methods=['GET'])
def get_class(id):
    fitness_class = FitnessClass.query.get_or_404(id)
    return jsonify(fitness_class.to_dict())


@api_bp.route('/classes/stats', methods=['GET'])
def get_classes_stats():
    classes = FitnessClass.query.all()
    stats = {
        'total_classes': len(classes),
        'scheduled': len([c for c in classes if c.status == 'Scheduled']),
        'in_progress': len([c for c in classes if c.status == 'In Progress']),
        'avg_occupancy': round(sum([c.current_enrollment / c.max_capacity * 100 for c in classes]) / len(classes), 1) if classes else 0
    }
    return jsonify(stats)


# Payments
@api_bp.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    return jsonify([payment.to_dict() for payment in payments])


@api_bp.route('/payments/stats', methods=['GET'])
def get_payments_stats():
    payments = Payment.query.all()
    completed_payments = [p for p in payments if p.status == 'Completed']
    
    stats = {
        'total_transactions': len(payments),
        'completed': len(completed_payments),
        'pending': len([p for p in payments if p.status == 'Pending']),
        'total_revenue': round(sum([p.amount for p in completed_payments]), 2),
        'avg_transaction': round(sum([p.amount for p in completed_payments]) / len(completed_payments), 2) if completed_payments else 0
    }
    return jsonify(stats)


# Attendance
@api_bp.route('/attendance', methods=['GET'])
def get_attendance():
    attendance = Attendance.query.order_by(Attendance.check_in_time.desc()).limit(50).all()
    return jsonify([att.to_dict() for att in attendance])


@api_bp.route('/attendance/stats', methods=['GET'])
def get_attendance_stats():
    attendance = Attendance.query.all()
    today = datetime.utcnow().date()
    
    today_checkins = len([a for a in attendance if a.check_in_time.date() == today])
    this_week_checkins = len([a for a in attendance if a.check_in_time > datetime.utcnow() - timedelta(days=7)])
    
    stats = {
        'today_checkins': today_checkins,
        'this_week_checkins': this_week_checkins,
        'total_records': len(attendance),
        'avg_daily_attendance': round(this_week_checkins / 7, 1) if this_week_checkins > 0 else 0
    }
    return jsonify(stats)


# Real-time data update endpoint
@api_bp.route('/realtime-data', methods=['GET'])
def get_realtime_data():
    """Simulated real-time data with random updates"""
    
    # Randomly update some data
    if random.random() > 0.5:
        classes = FitnessClass.query.all()
        for cls in random.sample(classes, min(2, len(classes))):
            cls.current_enrollment = min(cls.max_capacity, cls.current_enrollment + random.randint(-2, 3))
    
    if random.random() > 0.7:
        trainers = Trainer.query.all()
        for trainer in random.sample(trainers, min(1, len(trainers))):
            trainer.status = random.choice(['Available', 'In Session', 'Break'])
    
    # Process random new payments
    if random.random() > 0.6:
        from app.models import Payment
        members = Member.query.all()
        if members:
            new_payment = Payment(
                member_id=random.choice([m.id for m in members]),
                amount=round(random.choice([29.99, 49.99, 79.99, 99.99]), 2),
                payment_date=datetime.utcnow(),
                status=random.choice(['Completed', 'Pending']),
                payment_type=random.choice(['Credit Card', 'Bank Transfer'])
            )
            db.session.add(new_payment)
    
    # Process random check-ins
    if random.random() > 0.5:
        from app.models import Attendance
        members = Member.query.all()
        classes = FitnessClass.query.all()
        if members and classes:
            new_check_in = Attendance(
                member_id=random.choice([m.id for m in members]),
                class_id=random.choice([c.id for c in classes]),
                check_in_time=datetime.utcnow()
            )
            db.session.add(new_check_in)
    
    db.session.commit()
    
    return jsonify({
        'members': len(Member.query.all()),
        'active_sessions': len([c for c in FitnessClass.query.all() if c.status == 'In Progress']),
        'recent_payments': len(Payment.query.filter(Payment.payment_date > datetime.utcnow() - timedelta(hours=1)).all()),
        'trainer_status': {
            'available': len([t for t in Trainer.query.all() if t.status == 'Available']),
            'in_session': len([t for t in Trainer.query.all() if t.status == 'In Session']),
            'on_break': len([t for t in Trainer.query.all() if t.status == 'Break'])
        },
        'timestamp': datetime.utcnow().isoformat()
    })


# Revenue by plan
@api_bp.route('/revenue/by-plan', methods=['GET'])
def get_revenue_by_plan():
    members = Member.query.all()
    payments = Payment.query.filter_by(status='Completed').all()
    
    revenue_by_plan = {}
    for plan in ['Silver', 'Gold', 'Platinum']:
        plan_members = [m.id for m in members if m.membership_plan == plan]
        revenue_by_plan[plan] = round(sum([p.amount for p in payments if p.member_id in plan_members]), 2)
    
    return jsonify(revenue_by_plan)


# Top trainers
@api_bp.route('/trainers/top-rated', methods=['GET'])
def get_top_trainers():
    trainers = Trainer.query.order_by(Trainer.rating.desc()).limit(5).all()
    return jsonify([trainer.to_dict() for trainer in trainers])


# ==================== Helper Functions ====================

def hash_password(password):
    """Simple password hashing (use bcrypt in production)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed
