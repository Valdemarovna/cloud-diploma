import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'secretKey'

DEBUG = True

ALLOWED_HOSTS = []

# PostgreSQL
DB_NAME = 'cloud_storage'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

# File storage
FILE_STORAGE_ROOT = os.path.join(BASE_DIR, 'storage')

# Logging
LOG_LEVEL = 'DEBUG'