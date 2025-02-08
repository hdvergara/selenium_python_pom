# Python - Selenium - POM

<div align="center">

![Badge 1](https://img.shields.io/badge/Python-3.12-blue)
![Badge 2](https://img.shields.io/badge/Allure-Reports-green)
![Badge 3](https://img.shields.io/badge/Selenium-Webdriver-yellow)
![Badge 4](https://img.shields.io/badge/Loguru-logs-red)
![Badge 5](https://img.shields.io/badge/Pydantic-ciam)
</div>

**Project Description**

This project aims to automate tasks in web browsers using Python and Selenium WebDriver. The Page Object Model (POM)
design pattern has been implemented to enhance code maintainability and organization.

**Key Dependencies**

1. **Allure:** Used for generating reports. Ensure you have the Allure binary installed and its environment variable
   configured to view the reports
2. **Pytest:** Used for running tests.
3. **Loguru:** Used for generating console logs without requiring specific log configurations.
4. **Pydantic:** Used for data validation and configuration management.

**Project Structure**

```plaintext
selenium_python_pom/
├── core/
│   ├── actions/
│   │   └── actions.py  # Contains common Selenium actions (e.g., clicking, sending text).
│   ├── browser/
│       ├── browser_settings.py  # Configures browser settings and selects the browser to use.
│       └── browser_type.py  # Defines browser types (e.g., Chrome, Firefox, Edge).
├── config/
│   ├── __init__.py  # Initializes the config package.
│   └── browser_config.py  # Contains browser-specific configurations.
├── pages/
│   └── login_page.py  # Maps and interacts with elements on the login page.
├── tests/
│   ├── __init__.py  # Initializes the tests package.
│   ├── contrast.py  # Contains contrast-related tests.
│   └── test_login_2.py  # Contains login-related test cases.
├── env/  # Environment-specific files (e.g., environment variables).
├── .gitignore  # Specifies files and directories to be ignored by Git.
├── Pipfile  # Defines project dependencies using Pipenv.
├── Pipfile.lock  # Locks dependency versions for reproducibility.
└── README.md  # Provides an overview of the project and instructions.
```

**Prerequisites**

* **Python:** Ensure you have Python 3.10 or higher installed.
* **Pipenv:** Ensure you have Pipenv installed. It is used to manage project dependencies.

```bash
   pip install pipenv
```

**Note:** It is recommended to work with the PyCharm IDE as it is natively designed for Python development. However,
using Visual Studio Code is also fine as long as it is properly configured for Python.

**Installation**

1. Clone the repository.
2. Create and activate the virtual environment.

```bash
  pipenv install
```

3. Activate the virtual environment

```bash
  pipenv shell
```

**Running Tests**

Tests can be executed in the following ways:

1. Clone the repository.
2. Create and activate the virtual environment:
```bash
  pipenv install
```
3. Activate the virtual environment
  ```bash
  pipenv shell
```
## Deployment

1. Running Tests in PyCharm:
  - Open the Test class you want to run
  - Click on the Run option provided by PyCharm for the class or individual test. This option runs the tests but does not generate any report; you will only see a console log of the execution.
2. Running Tests via Terminal:
  - Open the terminal within the project and run the following command:
  ```bash
  pytest -s
```
This command runs all tests located in the test folder at the project root. This execution also does not generate any report.

3. Running Tests with Allure Report Generation
  - Open the terminal within the project and run the following command:
  ```bash
  pytest --alluredir=reports/allure-results
```
This command runs all tests located in the test folder at the project root. It creates a folder named reports at the project root, containing the necessary information for report generation and visualization.

4. Viewing the Allure Report.
  - To view the report, run the following command:
  ```bash
  allure serve reports/allure-results
```
This command opens an HTML report containing the test execution details.