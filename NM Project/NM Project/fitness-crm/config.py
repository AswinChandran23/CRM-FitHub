# Configuration file for FitHub CRM

# Flask Configuration
class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CORS_ORIGINS = "*"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    DATABASE_PATH = 'fitness_crm.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Application settings
APP_SETTINGS = {
    'db_name': 'fitness_crm.db',
    'port': 5000,
    'host': '0.0.0.0',
    'debug': True,
    'workers': 4,
    'realtime_update_interval': 5  # seconds
}

# Synthetic Data Configuration
SYNTHETIC_DATA = {
    'num_members': 50,
    'num_trainers': 12,
    'num_classes': 20,
    'num_payments': 80,
    'num_attendance': 150,
    'membership_plans': ['Silver', 'Gold', 'Platinum'],
    'class_types': ['Yoga', 'Cardio', 'Strength', 'Pilates', 'CrossFit', 
                    'Zumba', 'Spin', 'Boxing', 'HIIT', 'Dance Fitness'],
}

# API Configuration
API_CONFIG = {
    'rate_limit': '100/hour',
    'timeout': 30,
    'max_results': 1000
}
