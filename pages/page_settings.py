"""
This model contains the Settings page model.
"""

# Imports
from selenium.webdriver.common.by import By


class SettingsPage:
    """
    Object for the Settings page.
    """

    # Locators
    VIEW_DEPARTMENTS_BUTTON = (By.LINK_TEXT, "View Departments")
    ADD_DEPARTMENT_BUTTON = (By.LINK_TEXT, "Add Department")
    VIEW_USERS_BUTTON = (By.LINK_TEXT, "View Users")
    ADD_USER_BUTTON = (By.LINK_TEXT, "ADD Users")
    BULK_ADD_USER_BUTTON = (By.LINK_TEXT, "Bulk Add Users")

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def click_view_departments(self):
        """Clicks the View Departments button."""

        self.browser.find_element(*self.VIEW_DEPARTMENTS_BUTTON).click()

    def click_add_department(self):
        """Clicks the Add Department button."""

        self.browser.find_element(*self.ADD_DEPARTMENT_BUTTON).click()

    def click_view_users(self):
        """Clicks the View Users button."""

        self.browser.find_element(*self.VIEW_USERS_BUTTON).click()

    def click_add_user(self):
        """Clicks the Add User button."""

        self.browser.find_element(*self.ADD_USER_BUTTON).click()

    def click_bulk_add_user(self):
        """Clicks the Bulk Add User button."""

        self.browser.find_element(*self.BULK_ADD_USER_BUTTON).click()
