"""
Tests if the add department page is working properly.
"""

# Imports
import pytest
import faker
from pages.navbar import Navbar
from pages.page_login import LoginPage
from pages.page_settings import SettingsPage
from pages.page_add_department import SettingsAddEditDepartmentPage


# Faker
fake = faker.Faker()

# Test Case - Add Department


def test_add_department(browserChrome):
    """
    Tests if the add department page is working properly.
    """

    # Admin Credentials
    email = "admin@healthtrio.com"
    password = "admin@healthtrio.com"

    # Create the LoginPage
    login_page = LoginPage(browserChrome)

    # Load the page
    login_page.load()

    # Log in
    login_page.login(email, password)

    # Click the settings link
    navbar = Navbar(browserChrome)
    navbar.click_settings_link()

    # Click the add department button
    settings_page = SettingsPage(browserChrome)
    settings_page.click_add_department_button()

    # Add a department
    settings_add_edit_department_page = SettingsAddEditDepartmentPage(
        browserChrome)
    settings_add_edit_department_page.add_department(fake.job())

    # Verify that the department was added
    assert settings_add_edit_department_page.successful_banner_present()
