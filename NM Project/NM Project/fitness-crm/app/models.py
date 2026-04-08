from app import db
from datetime import datetime, timedelta
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='Manager')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    membership_plan = db.Column(db.String(50), default='Gold')
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    renewal_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Active')
    total_classes = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'membership_plan': self.membership_plan,
            'join_date': self.join_date.strftime('%Y-%m-%d'),
            'renewal_date': self.renewal_date.strftime('%Y-%m-%d') if self.renewal_date else None,
            'status': self.status,
            'total_classes': self.total_classes
        }


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    specialization = db.Column(db.String(100))
    availability = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Available')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'specialization': self.specialization,
            'availability': self.availability,
            'experience_years': self.experience_years,
            'rating': self.rating,
            'status': self.status
        }


class FitnessClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    schedule_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    max_capacity = db.Column(db.Integer, default=30)
    current_enrollment = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Scheduled')
    
    trainer = db.relationship('Trainer', backref='classes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'trainer_id': self.trainer_id,
            'trainer_name': self.trainer.name if self.trainer else 'Unassigned',
            'schedule_time': self.schedule_time.strftime('%Y-%m-%d %H:%M') if self.schedule_time else None,
            'duration_minutes': self.duration_minutes,
            'max_capacity': self.max_capacity,
            'current_enrollment': self.current_enrollment,
            'status': self.status,
            'utilization': round((self.current_enrollment / self.max_capacity) * 100, 1) if self.max_capacity > 0 else 0
        }


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Completed')
    payment_type = db.Column(db.String(50))
    
    member = db.relationship('Member', backref='payments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'member_name': self.member.name if self.member else 'Unknown',
            'amount': self.amount,
            'payment_date': self.payment_date.strftime('%Y-%m-%d %H:%M'),
            'status': self.status,
            'payment_type': self.payment_type
        }


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'))
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    member = db.relationship('Member', backref='attendances')
    fitness_class = db.relationship('FitnessClass', backref='attendances')
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'member_name': self.member.name if self.member else 'Unknown',
            'class_id': self.class_id,
            'class_name': self.fitness_class.name if self.fitness_class else 'Unknown',
            'check_in_time': self.check_in_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_revenue = db.Column(db.Float, default=0)
    total_members = db.Column(db.Integer, default=0)
    active_classes = db.Column(db.Integer, default=0)
    avg_occupancy = db.Column(db.Float, default=0)
    member_retention_rate = db.Column(db.Float, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'total_revenue': round(self.total_revenue, 2),
            'total_members': self.total_members,
            'active_classes': self.active_classes,
            'avg_occupancy': round(self.avg_occupancy, 1),
            'member_retention_rate': round(self.member_retention_rate, 1),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
