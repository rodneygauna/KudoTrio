"""
This model contains the Login page model.
"""

# Imports
from selenium.webdriver.common.by import By


class LoginPage:
    """
    Page object for the Login page.
    """

    # URL
    # Change the IP address to your own IP address
    url = "http://192.168.4.111:5000/login"

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    REGISTER_LINK = (By.LINK_TEXT, "Register here")
    LOGIN_SUCCESSFUL_BANNER = (By.CLASS_NAME, "alert-success")

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def load(self):
        """
        Load the Login page.
        """
        self.browser.get(self.url)

    def login(self, email, password):
        """
        Log in using the given credentials.
        """

        # Enter the email address
        email_input = self.browser.find_element(*self.EMAIL_INPUT)
        email_input.send_keys(email)

        # Enter the password
        password_input = self.browser.find_element(*self.PASSWORD_INPUT)
        password_input.send_keys(password)

        # Click the login button
        login_button = self.browser.find_element(*self.LOGIN_BUTTON)
        login_button.click()

    def login_successful_banner_present(self):
        """
        Returns whether the login successful banner is present.
        """

        return self.browser.find_element(
            *self.LOGIN_SUCCESSFUL_BANNER
        ).is_displayed()
