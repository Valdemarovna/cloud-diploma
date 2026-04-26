from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
import psycopg2
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize database (create DB, users)"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Initializing database...")

        self.create_database()
        self.run_migrations()
        self.create_users()

        self.stdout.write(self.style.SUCCESS("✅ Done"))

    def create_database(self):
        db_name = os.getenv("DB_NAME", "cloud_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "postgres")

        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host="db",  # для docker
                port="5432"
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            exists = cur.fetchone()

            if not exists:
                self.stdout.write(f"📦 Creating database {db_name}")
                cur.execute(f"CREATE DATABASE {db_name}")
            else:
                self.stdout.write("📦 Database already exists")

            cur.close()
            conn.close()

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"DB create skipped: {e}"))

    def run_migrations(self):
        from django.core.management import call_command

        self.stdout.write("⚙️ Running migrations...")
        call_command("migrate")

    def create_users(self):
        self.stdout.write("👤 Creating users...")

        # 👑 суперпользователь
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@mail.com",
                password="Admin123!",
                isAdmin = True
            )
            self.stdout.write("👑 Superuser created: admin / Admin123!")
        else:
            self.stdout.write("👑 Superuser already exists")

        # 👤 обычный пользователь
        if not User.objects.filter(username="user").exists():
            User.objects.create_user(
                username="user",
                email="user@mail.com",
                password="User123!"
            )
            self.stdout.write("👤 User created: user / User123!")
        else:
            self.stdout.write("👤 User already exists")