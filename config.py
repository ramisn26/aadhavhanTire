import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost/aadhavhan_tire'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # File storage configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    S3_REGION = os.environ.get('S3_REGION')
    
    # WhatsApp/SMS configuration
    WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY')
    SMS_API_KEY = os.environ.get('SMS_API_KEY')
    
    # Business configuration
    BUSINESS_NAME = os.environ.get('BUSINESS_NAME', 'Aadhavhan Tire')
    BUSINESS_ADDRESS = os.environ.get('BUSINESS_ADDRESS')
    BUSINESS_PHONE = os.environ.get('BUSINESS_PHONE')
    BUSINESS_EMAIL = os.environ.get('BUSINESS_EMAIL')
    BUSINESS_GST = os.environ.get('BUSINESS_GST')
    INVOICE_PREFIX = os.environ.get('INVOICE_PREFIX', 'AAD/23-24/')