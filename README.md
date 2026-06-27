# Tichi Application – QA Intern Technical Assignment

**Application Under Test:** https://tichi-app-webapp-stage.web.app

---

## Deliverables

### 1. Test Case Document (`Tichi_QA_Assignment.xlsx` → Sheet: Test Cases)
Contains 30 test cases covering the Login and Signup functionality of the Tichi application.

| Module | No. of Test Cases |
|--------|------------------|
| Login  | 15               |
| Signup | 15               |
| **Total** | **30**        |

Each test case includes: Test Case ID, Module, Title, Preconditions, Test Steps, Test Data, Expected Result, Priority.

---

### 2. Defect Report (`Tichi_QA_Assignment.xlsx` → Sheet: Defect Report)
A formal defect report for the identified issue:

> **BUG_001** – The application allows users to attempt login with an invalid email format without showing any client-side validation error.

The report covers: Defect ID, Title, Severity, Priority, Steps to Reproduce, Expected vs Actual Result, Impact, Root Cause, and Fix Recommendation.

---

### 3. Automation – Login Test Suite (`test_tichi_login.py`)

**Tool:** Selenium WebDriver  
**Language:** Python 3  
**Framework:** pytest

Automates 11 Login test scenarios including valid login, invalid inputs, empty fields, password masking, SQL injection, and UI element verification.

#### Setup & Execution

**Install dependencies:**
```bash
pip install selenium pytest pytest-html webdriver-manager
```

**Run tests and generate report:**
```bash
pytest test_tichi_login.py -v --html=execution_report.html --self-contained-html
```

> Note: Update `VALID_EMAIL` and `VALID_PASSWORD` at the top of `test_tichi_login.py` with valid Tichi account credentials before running.

#### Automated Test Cases

| Test ID | Scenario |
|---------|----------|
| TC_LOG_01 | Successful login with valid credentials |
| TC_LOG_02 | Login with incorrect password |
| TC_LOG_03 | Login with invalid email format |
| TC_LOG_04 | Login with unregistered email |
| TC_LOG_05 | Login with empty email field |
| TC_LOG_06 | Login with empty password field |
| TC_LOG_07 | Login with both fields empty |
| TC_LOG_08 | Password field character masking |
| TC_LOG_09 | Case-insensitive email login |
| TC_LOG_13 | Login page UI elements verification |
| TC_LOG_14 | SQL injection in email field |
