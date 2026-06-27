"""
Tichi Application - Login Automation Test Suite
URL: https://tichi-app-webapp-stage.web.app
Tool: Selenium WebDriver + pytest
Language: Python 3

Setup:
    pip install selenium pytest pytest-html webdriver-manager

Run tests:
    pytest test_tichi_login.py -v --html=execution_report.html --self-contained-html

Requirements:
    - Chrome browser installed
    - Internet connection
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
APP_URL      = "https://tichi-app-webapp-stage.web.app"
VALID_EMAIL    = "jjeevikha@gmail.com"   #UPDATE
VALID_PASSWORD = "BlahBlah@123"          #UPDATE       
WAIT_TIMEOUT   = 10


# ─── FIXTURES ─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """Launch Chrome browser before each test and quit after."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Uncomment next line to run headless (no visible browser window)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Navigate to the login page before each test."""
    driver.get(APP_URL)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # Click Login link/button if on landing page
    try:
        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH,
                "//*[contains(text(),'Login') or contains(text(),'Sign In') or contains(@href,'login')]"))
        )
        login_btn.click()
    except Exception:
        pass  # Already on login page

    # Wait for email field to appear
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email' or @placeholder[contains(translate(.,'EMAIL','email'),'email')]]")
    ))
    return driver


def get_email_field(driver):
    return driver.find_element(By.XPATH,
        "//input[@type='email' or @name='email' or @id='email' or @placeholder[contains(translate(.,'EMAIL','email'),'email')]]")

def get_password_field(driver):
    return driver.find_element(By.XPATH,
        "//input[@type='password' or @name='password' or @id='password']")

def get_login_button(driver):
    return driver.find_element(By.XPATH,
        "//button[contains(translate(text(),'LOGIN','login'),'login') or contains(translate(text(),'SIGNIN','signin'),'sign in')]")

def page_has_error(driver, keywords=None):
    """Return True if error message/text is visible on page."""
    if keywords is None:
        keywords = ["invalid", "error", "incorrect", "required", "valid email", "not found"]
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    return any(k in page_text for k in keywords)


# ══════════════════════════════════════════════════════════════════════════════
# TEST CASES
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginPage:

    def test_TC_LOG_01_valid_login(self, login_page):
        """TC_LOG_01: Successful login with valid credentials"""
        driver = login_page
        get_email_field(driver).send_keys(VALID_EMAIL)
        get_password_field(driver).send_keys(VALID_PASSWORD)
        get_login_button(driver).click()
        time.sleep(2)

        current_url = driver.current_url
        assert current_url != APP_URL + "/login", \
            "Login failed – URL did not change after valid login"
        assert "login" not in current_url.lower() or "dashboard" in current_url.lower() or \
               "home" in current_url.lower(), \
            f"Expected to land on dashboard/home, got: {current_url}"

    def test_TC_LOG_02_wrong_password(self, login_page):
        """TC_LOG_02: Login with incorrect password shows error"""
        driver = login_page
        get_email_field(driver).send_keys(VALID_EMAIL)
        get_password_field(driver).send_keys("WrongPassword!999")
        get_login_button(driver).click()
        time.sleep(2)

        assert page_has_error(driver, ["invalid", "incorrect", "error", "wrong"]), \
            "Expected error message for wrong password, but none found"

    def test_TC_LOG_03_invalid_email_format(self, login_page):
        """TC_LOG_03: Login with invalid email format – validation must block it"""
        driver = login_page
        invalid_emails = ["invalidemail", "user@", "@domain.com", "user.com"]

        for bad_email in invalid_emails:
            email_field = get_email_field(driver)
            email_field.clear()
            email_field.send_keys(bad_email)

            pwd_field = get_password_field(driver)
            pwd_field.clear()
            pwd_field.send_keys("AnyPassword123")

            get_login_button(driver).click()
            time.sleep(1)

            # Check: should stay on login page OR show validation error
            current_url = driver.current_url
            has_error = page_has_error(driver, ["valid email", "invalid", "error", "required"])

            assert has_error or "login" in current_url.lower(), \
                f"BUG: App allowed login with invalid email '{bad_email}' without showing error!"

            email_field = get_email_field(driver)
            email_field.clear()

    def test_TC_LOG_04_unregistered_email(self, login_page):
        """TC_LOG_04: Login with unregistered email shows error"""
        driver = login_page
        get_email_field(driver).send_keys("notregistered_xyz999@test.com")
        get_password_field(driver).send_keys("AnyPassword@123")
        get_login_button(driver).click()
        time.sleep(2)

        assert page_has_error(driver, ["invalid", "not found", "error", "no account"]), \
            "Expected error for unregistered email, but none shown"

    def test_TC_LOG_05_empty_email_field(self, login_page):
        """TC_LOG_05: Login with empty email field shows validation error"""
        driver = login_page
        get_password_field(driver).send_keys("ValidPass@123")
        get_login_button(driver).click()
        time.sleep(1)

        has_error = page_has_error(driver, ["required", "email", "error", "empty"])
        # Also check if HTML5 validation prevented submission
        email_field = get_email_field(driver)
        is_required = email_field.get_attribute("required") is not None

        assert has_error or is_required, \
            "Expected validation error for empty email field"

    def test_TC_LOG_06_empty_password_field(self, login_page):
        """TC_LOG_06: Login with empty password field shows validation error"""
        driver = login_page
        get_email_field(driver).send_keys(VALID_EMAIL)
        get_login_button(driver).click()
        time.sleep(1)

        has_error = page_has_error(driver, ["required", "password", "error"])
        pwd_field = get_password_field(driver)
        is_required = pwd_field.get_attribute("required") is not None

        assert has_error or is_required, \
            "Expected validation error for empty password field"

    def test_TC_LOG_07_both_fields_empty(self, login_page):
        """TC_LOG_07: Login with both fields empty shows validation errors"""
        driver = login_page
        get_login_button(driver).click()
        time.sleep(1)

        has_error = page_has_error(driver, ["required", "error", "email", "password"])
        fields_required = (
            get_email_field(driver).get_attribute("required") is not None or
            get_password_field(driver).get_attribute("required") is not None
        )

        assert has_error or fields_required, \
            "Expected validation errors when both fields are empty"

    def test_TC_LOG_08_password_field_masked(self, login_page):
        """TC_LOG_08: Password field should mask characters"""
        driver = login_page
        pwd_field = get_password_field(driver)
        field_type = pwd_field.get_attribute("type")

        assert field_type == "password", \
            f"Password field type is '{field_type}', expected 'password' (masking)"

    def test_TC_LOG_09_case_insensitive_email(self, login_page):
        """TC_LOG_09: Email field is case-insensitive"""
        driver = login_page
        get_email_field(driver).send_keys(VALID_EMAIL.upper())
        get_password_field(driver).send_keys(VALID_PASSWORD)
        get_login_button(driver).click()
        time.sleep(2)

        current_url = driver.current_url
        assert "login" not in current_url.lower() or "dashboard" in current_url.lower(), \
            "Login failed with uppercase email – email field may be case-sensitive"

    def test_TC_LOG_13_ui_elements_present(self, login_page):
        """TC_LOG_13: All login page UI elements are present"""
        driver = login_page

        email_field    = get_email_field(driver)
        password_field = get_password_field(driver)
        login_btn      = get_login_button(driver)

        assert email_field.is_displayed(),    "Email field not visible"
        assert password_field.is_displayed(), "Password field not visible"
        assert login_btn.is_displayed(),      "Login button not visible"

    def test_TC_LOG_14_sql_injection_email(self, login_page):
        """TC_LOG_14: SQL injection in email field must not succeed"""
        driver = login_page
        get_email_field(driver).send_keys("' OR 1=1 --")
        get_password_field(driver).send_keys("anything")
        get_login_button(driver).click()
        time.sleep(2)

        current_url = driver.current_url
        page_text   = driver.find_element(By.TAG_NAME, "body").text.lower()

        assert "dashboard" not in current_url.lower() and "home" not in current_url.lower(), \
            "SECURITY BUG: SQL injection allowed login!"
        assert "sql" not in page_text and "syntax" not in page_text, \
            "SECURITY BUG: SQL error exposed in response!"
