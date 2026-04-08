import os
from app import create_app, db
from app.data_generator import generate_synthetic_data
from app.models import Member

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Generate synthetic data on first run
        member_count = Member.query.count()
        if member_count == 0:
            print("📊 Generating synthetic data...")
            generate_synthetic_data()
            print("✅ Data generation complete!")
        else:
            print(f"📦 Found {member_count} existing members in database")
        
        print("\n" + "=" * 50)
        print("🏋️  FitHub CRM - Fitness Center Management System")
        print("🚀 Server starting at http://localhost:5000")
        print("=" * 50 + "\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
