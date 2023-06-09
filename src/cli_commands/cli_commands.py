"""
CLI Commands for the app.
"""

# Imports
from faker import Faker
from flask import Blueprint
from src import db


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
