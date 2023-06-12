"""
Settings - Department User Counts
This is a helper function to get the total count of users for each department.
"""

# Imports
from src.models import (
    User,
    Departments,
)


# Function - Get Department User Count
def get_department_user_count():
    """
    Get total count of users for each department
    """
    department_user_count = {}
    departments = Departments.query.all()

    for department in departments:
        department_user_count[department.name] = User.query.filter_by(
            department_id=department.id
        ).count()

    return department_user_count
