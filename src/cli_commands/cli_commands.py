"""
CLI Commands for the app.
"""

# Imports
import random
from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash
from src import db
from src.models import (
    User,
    Departments,
    Kudo,
)
from src.dictionaries.dictionaries import (
    USER_DEPARTMENT_CHOICES,
    USER_ROLE_CHOICES,
    STATUS_CHOICES,
)



# Faker Generator
faker = Faker()

# Blueprint Configuration
commands_bp = Blueprint('commands', __name__)


# Create DB
@commands_bp.cli.command('create_db')
def create_db():
    """
    Creates the database.
    """

    db.create_all()
    print('Database created!')


# Drop DB
@commands_bp.cli.command('drop_db')
def drop_db():
    """
    Drops the database.
    """

    db.drop_all()
    print('Database dropped!')


# Seed DB
@commands_bp.cli.command('seed_db')
def seed_db():
    """
    Seeds the database with fake data.
    """

    # Data to seed the database with
    entry = []

    # Create Admin User
    admin_user = User(
            email="admin@healthtrio.com",
            password_hash=generate_password_hash(
                "admin@healthtrio.com"),
            firstname="Admin",
            lastname="AdminUser",
            role="admin",
            status="active",
        )

    # Create 10 users
    for i in range(10+1):
        entry.append(
            User(
                email=f"test{i}@healthtrio.com",
                password_hash=generate_password_hash(
                    f"test{i}@healthtrio.com"),
                firstname=faker.first_name(),
                lastname=faker.last_name(),
                role=random.choices(
                    USER_ROLE_CHOICES)[0],
                status=random.choices(
                    STATUS_CHOICES)[0],
            )
        )

    # Create 10 departments
    for i in range(10+1):
        entry.append(
            Departments(
                department=faker.word(),
            )
        )

    # Create 10 kudos
    for i in range(10+1):
        entry.append(
            Kudo(
                submitting_user_id=random.randint(1, 10),
                receiving_user_id=random.randint(1, 10),
                kudo_message=faker.text(),
            )
        )

    # Add the data to the database
    db.session.add(admin_user)

    for data in entry:
        db.session.add(data)
    db.session.commit()
    print('Database seeded!')
