#!/usr/bin/env python
"""
Utility script for FitHub CRM database management
"""

import os
import sys
from app import create_app, db
from app.data_generator import generate_synthetic_data
from app.models import Member, Trainer, FitnessClass, Payment, Attendance, Analytics

def init_db():
    """Initialize database with tables"""
    print("📦 Initializing database...")
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")

def reset_db():
    """Reset database and regenerate synthetic data"""
    print("🗑️  Resetting database...")
    
    # Delete database file if exists
    if os.path.exists('fitness_crm.db'):
        os.remove('fitness_crm.db')
        print("✅ Database file removed")
    
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database recreated")
        generate_synthetic_data()
        print("✅ Synthetic data loaded")

def show_stats():
    """Show database statistics"""
    app = create_app()
    with app.app_context():
        members = Member.query.count()
        trainers = Trainer.query.count()
        classes = FitnessClass.query.count()
        payments = Payment.query.count()
        attendance = Attendance.query.count()
        
        print("\n📊 Database Statistics:")
        print(f"  Members:     {members:>4}")
        print(f"  Trainers:    {trainers:>4}")
        print(f"  Classes:     {classes:>4}")
        print(f"  Payments:    {payments:>4}")
        print(f"  Attendance:  {attendance:>4}")
        print(f"  " + "=" * 20)
        print(f"  Total:       {members + trainers + classes + payments + attendance:>4}")

def clear_logs():
    """Clear log files"""
    print("🧹 Clearing logs...")
    # Add log clearing logic here if needed
    print("✅ Logs cleared")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("FitHub CRM - Database Management Tool")
        print("\nUsage: python manage.py [command]")
        print("\nCommands:")
        print("  init      - Initialize database")
        print("  reset     - Reset database with new synthetic data")
        print("  stats     - Show database statistics")
        print("  clean     - Clear logs")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'reset':
        confirm = input("⚠️  This will delete all data. Continue? (y/n): ")
        if confirm.lower() == 'y':
            reset_db()
        else:
            print("❌ Cancelled")
    elif command == 'stats':
        show_stats()
    elif command == 'clean':
        clear_logs()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
