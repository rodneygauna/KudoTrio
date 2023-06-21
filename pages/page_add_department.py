"""
This model contains the Settings - Add/Edit Department page.
"""

# Imports
from selenium.webdriver.common.by import By


class SettingsAddEditDepartmentPage:
    """
    Object for the Settings - Add/Edit Department page.
    """

    # Locators
    NAME_INPUT = (By.ID, "name")
    SAVE_BUTTON = (By.ID, "submit")
    SUCCESSFUL_BANNER = (By.CLASS_NAME, "alert-success")

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def add_department(self, name):
        """
        Adds a department with the given name.
        """

        # Enter the name
        name_input = self.browser.find_element(*self.NAME_INPUT)
        name_input.send_keys(name)

        # Click the save button
        save_button = self.browser.find_element(*self.SAVE_BUTTON)
        save_button.click()

    def successful_banner_present(self):
        """
        Returns whether the successful banner is present.
        """

        return self.browser.find_element(
            *self.SUCCESSFUL_BANNER
        ).is_displayed()
