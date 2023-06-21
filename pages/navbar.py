"""
This model contains the Navigation Menu for the website.
"""

# Imports
from selenium.webdriver.common.by import By


class Navbar:
    """
    Object for the navbar.
    """

    # Locators
    NAVBAR_LOGO = (By.CLASS_NAME, "navbar-brand")
    NAVBAR_HOME = (By.LINK_TEXT, "Home")
    NAVBAR_KUDOS = (By.LINK_TEXT, "Kudos")
    NAVBAR_LOGIN = (By.LINK_TEXT, "Login")
    NAVBAR_LOGOUT = (By.LINK_TEXT, "Logout")
    NAVBAR_PROFILE = (By.LINK_TEXT, "Profile")

    # Intializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
