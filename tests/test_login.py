"""
Tests if the login page is working properly.
"""

# Imports
import pytest
from pages.navbar import Navbar
from pages.login import LoginPage


def test_login(browserChrome):
    """
    Tests if the login page is working properly.
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

    # Verify that the login was successful
    assert login_page.login_successful_banner_present()
