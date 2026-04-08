import random
from datetime import datetime, timedelta
from app import db
from app.models import User, Member, Trainer, FitnessClass, Payment, Attendance, Analytics
import hashlib

FIRST_NAMES = ['John', 'Sarah', 'Mike', 'Emma', 'David', 'Lisa', 'Tom', 'Jessica', 'Chris', 'Rachel', 
               'Alex', 'Amanda', 'Ryan', 'Nicole', 'Kevin', 'Ashley', 'James', 'Megan', 'Daniel', 'Lauren']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'White']

CLASS_TYPES = ['Yoga', 'Cardio', 'Strength', 'Pilates', 'CrossFit', 'Zumba', 'Spin', 'Boxing', 'HIIT', 'Dance Fitness']
SPECIALIZATIONS = ['Yoga Instructor', 'Strength Coach', 'Cardio Specialist', 'CrossFit Coach', 'Pilates Instructor',
                   'Nutrition Coach', 'Personal Trainer', 'Functional Fitness', 'Kickboxing Trainer', 'Dance Fitness Coach']

MEMBERSHIP_PLANS = ['Silver', 'Gold', 'Platinum']

def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_synthetic_data():
    """Generate synthetic data for the FitHub CRM system"""
    
    # Clear existing data
    db.session.query(Attendance).delete()
    db.session.query(Payment).delete()
    db.session.query(FitnessClass).delete()
    db.session.query(Member).delete()
    db.session.query(Trainer).delete()
    db.session.query(User).delete()
    db.session.query(Analytics).delete()
    db.session.commit()
    
    # Create demo users
    demo_users = [
        User(name='Admin User', email='admin@fithouse.com', password=hash_password('password123'), role='Manager'),
        User(name='John Manager', email='john@fithouse.com', password=hash_password('password123'), role='Manager'),
        User(name='Sarah Trainer', email='sarah@fithouse.com', password=hash_password('password123'), role='Trainer'),
    ]
    for user in demo_users:
        db.session.add(user)
    db.session.commit()
    
    # Generate Trainers
    trainers = []
    for i in range(12):
        trainer = Trainer(
            name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            email=f"trainer{i+1}@fithouse.com",
            specialization=random.choice(SPECIALIZATIONS),
            availability="Mon-Fri 9AM-6PM",
            experience_years=random.randint(2, 15),
            rating=round(random.uniform(4.0, 5.0), 1),
            status=random.choice(['Available', 'In Session', 'Break'])
        )
        trainers.append(trainer)
        db.session.add(trainer)
    
    db.session.commit()
    
    # Generate Members
    members = []
    for i in range(50):
        member = Member(
            name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            email=f"member{i+1}@email.com",
            phone=f"+1{random.randint(2000000000, 9999999999)}",
            membership_plan=random.choice(MEMBERSHIP_PLANS),
            join_date=datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            renewal_date=datetime.utcnow() + timedelta(days=random.randint(1, 365)),
            status=random.choice(['Active', 'Inactive', 'Pending']),
            total_classes=random.randint(5, 120)
        )
        members.append(member)
        db.session.add(member)
    
    db.session.commit()
    
    # Generate Fitness Classes
    current_time = datetime.utcnow()
    classes = []
    for i in range(20):
        class_obj = FitnessClass(
            name=f"{random.choice(CLASS_TYPES)} Class {i+1}",
            type=random.choice(CLASS_TYPES),
            trainer_id=random.choice([t.id for t in trainers]),
            schedule_time=current_time + timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 60)),
            duration_minutes=random.choice([30, 45, 60, 90]),
            max_capacity=random.randint(20, 40),
            current_enrollment=random.randint(5, 35),
            status=random.choice(['Scheduled', 'In Progress', 'Completed'])
        )
        classes.append(class_obj)
        db.session.add(class_obj)
    
    db.session.commit()
    
    # Generate Payments
    for i in range(80):
        payment = Payment(
            member_id=random.choice([m.id for m in members]),
            amount=round(random.choice([29.99, 49.99, 79.99, 99.99]), 2),
            payment_date=datetime.utcnow() - timedelta(days=random.randint(0, 90)),
            status=random.choice(['Completed', 'Pending', 'Failed']),
            payment_type=random.choice(['Credit Card', 'Bank Transfer', 'PayPal'])
        )
        db.session.add(payment)
    
    db.session.commit()
    
    # Generate Attendance Records
    for i in range(150):
        attendance = Attendance(
            member_id=random.choice([m.id for m in members]),
            class_id=random.choice([c.id for c in classes]),
            check_in_time=datetime.utcnow() - timedelta(hours=random.randint(0, 336))
        )
        db.session.add(attendance)
    
    db.session.commit()
    
    # Generate Analytics
    active_classes = len([c for c in classes if c.status == 'In Progress'])
    total_revenue = sum([p.amount for p in db.session.query(Payment).all() if p.status == 'Completed'])
    avg_occupancy = sum([c.current_enrollment / c.max_capacity * 100 for c in classes]) / len(classes) if classes else 0
    member_retention = (len([m for m in members if m.status == 'Active']) / len(members) * 100) if members else 0
    
    analytics = Analytics(
        total_revenue=total_revenue,
        total_members=len(members),
        active_classes=active_classes,
        avg_occupancy=avg_occupancy,
        member_retention_rate=member_retention,
        timestamp=datetime.utcnow()
    )
    db.session.add(analytics)
    db.session.commit()
    
    print("✓ Synthetic data generated successfully!")
    print(f"  - {len(demo_users)} Demo Users")
    print(f"  - {len(members)} Members")
    print(f"  - {len(trainers)} Trainers")
    print(f"  - {len(classes)} Classes")
    print(f"  - {len(db.session.query(Payment).all())} Payments")
    print(f"  - {len(db.session.query(Attendance).all())} Attendance Records")
    print("\n  Demo User Credentials:")
    for user in demo_users:
        print(f"    • {user.email} / password123")
