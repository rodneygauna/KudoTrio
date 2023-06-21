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
    NAVBAR_SETTINGS = (By.LINK_TEXT, "Settings")
    NAVBAR_LOGIN = (By.LINK_TEXT, "Login")
    NAVBAR_LOGOUT = (By.LINK_TEXT, "Logout")
    NAVBAR_PROFILE = (By.LINK_TEXT, "Profile")

    # Intializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def click_logo(self):
        """Clicks the logo."""

        self.browser.find_element(*self.NAVBAR_LOGO).click()

    def click_home_link(self):
        """Clicks the home link."""

        self.browser.find_element(*self.NAVBAR_HOME).click()

    def click_kudos_link(self):
        """Clicks the kudos link."""

        self.browser.find_element(*self.NAVBAR_KUDOS).click()

    def click_settings_link(self):
        """Clicks the settings link."""

        self.browser.find_element(*self.NAVBAR_SETTINGS).click()

    def click_login_link(self):
        """Clicks the login link."""

        self.browser.find_element(*self.NAVBAR_LOGIN).click()

    def click_logout_link(self):
        """Clicks the logout link."""

        self.browser.find_element(*self.NAVBAR_LOGOUT).click()

    def click_profile_link(self):
        """Clicks the profile link."""

        self.browser.find_element(*self.NAVBAR_PROFILE).click()
