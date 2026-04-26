import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# БД
DB_NAME = "cloud_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "db"
DB_PORT = "5432"

# Хранилище
FILES_ROOT = os.path.join(BASE_DIR, "storage")

# Логирование
LOG_LEVEL = "DEBUG"