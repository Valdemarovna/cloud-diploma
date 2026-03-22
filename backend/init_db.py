import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SUPERUSER = os.getenv("POSTGRES_SUPERUSER")
SUPERPASSWORD = os.getenv("POSTGRES_SUPERPASSWORD")


def create_db_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=SUPERUSER,
            password=SUPERPASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # --- Проверка пользователя ---
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname=%s",
            (DB_USER,)
        )
        if not cursor.fetchone():
            cursor.execute(
                f"CREATE USER {DB_USER} WITH PASSWORD %s",
                (DB_PASSWORD,)
            )
            print("✅ Пользователь создан")
        else:
            print("ℹ️ Пользователь уже существует")

        # --- Проверка базы ---
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname=%s",
            (DB_NAME,)
        )
        if not cursor.fetchone():
            cursor.execute(
                f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}"
            )
            print("✅ База данных создана")
        else:
            print("ℹ️ База уже существует")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Ошибка при инициализации БД:", e)


if __name__ == "__main__":
    create_db_if_not_exists()