"""
Configuration file for the pytest framework.
"""

# Imports
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def browserChrome():
    # Set the Chrome options
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_service = ChromeService(ChromeDriverManager().install())

    # Initialize Chrome browser
    b = webdriver.Chrome(options=chrome_options,
                         service=chrome_service)

    # Implicitly wait for 10 seconds before throwing an exception
    b.implicitly_wait(10)

    # Return the driver object at the end of setup
    yield b

    # Quit the browser after the test is completed
    b.quit()
