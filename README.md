# Robot Framework MCP Server v2.0

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Robot Framework](https://img.shields.io/badge/Robot%20Framework-6.0+-00C4B3.svg)](https://robotframework.org/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-purple.svg)](https://modelcontextprotocol.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A Model Context Protocol (MCP) server for Robot Framework test automation with comprehensive code generation capabilities.

[Features](#-features) • [Installation](#-installation--usage) • [Usage](#-usage-examples) • [Documentation](#-resources) • [Contributing](#-contributing)

</div>

<a href="https://glama.ai/mcp/servers/@sourcefuse/robotframework-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@sourcefuse/robotframework-mcp/badge" alt="Robot Framework Server MCP server" />
</a>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/robotframework-MCP.git
cd robotframework-MCP

# Install dependencies
pip install -r requirements.txt

# Generate your first test
python -c "
from src.templates.login import LoginTestTemplate
template = LoginTestTemplate()
print(template.generate(
    url='https://www.saucedemo.com',
    username='standard_user',
    password='secret_sauce'
))
" > test_login.robot

# Run the test
robot test_login.robot
```

## 📑 Table of Contents

- [What's New in v2.0](#-whats-new-in-v20)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation & Usage](#-installation--usage)
- [Available Tools](#️-available-tools)
- [Usage Examples](#-usage-examples)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Advanced Usage](#-advanced-usage)
- [Best Practices](#-best-practices)
- [Performance Tips](#-performance-tips)
- [Contributing](#-contributing)
- [Changelog](#-changelog)
- [Roadmap](#️-roadmap)
- [Resources](#-resources)
- [FAQ](#-faq)
- [Contact & Support](#-contact--support)
- [License](#-license)

## ✨ What's New in v2.0

- 🏗️ **Modular Architecture** - Clean separation of concerns with dedicated modules
- 📝 **Comprehensive Logging** - Structured logging for debugging and monitoring
- ✅ **Input Validation** - Robust validation with detailed error messages
- 🧪 **Unit Tests** - Full test coverage for validators and templates
- 📱 **Mobile Testing** - Appium support for Android and iOS
- 🔌 **API Testing** - RequestsLibrary integration for REST APIs
- 🗄️ **Database Testing** - Support for PostgreSQL, MySQL, SQLite, Oracle
- 👁️ **Visual Regression** - Screenshot comparison testing
- 🚀 **CI/CD Templates** - GitHub Actions, GitLab CI, Jenkins, Azure Pipelines
- 🎨 **More UI Frameworks** - Material UI, Ant Design selector templates

## 🎯 Features

### Test Generation
- 🤖 Login test cases with multiple selector templates
- 📄 Page Object Model generation
- 📊 Data-driven testing with CSV support
- ⚡ Performance monitoring tests
- 🔄 Retry mechanisms for flaky tests

### Supported Platforms
- 🌐 Web (Selenium) - Chrome, Firefox, Edge, Safari
- 📱 Mobile (Appium) - Android, iOS
- 🔌 API (Requests) - REST, GraphQL
- 🗄️ Database - PostgreSQL, MySQL, SQLite, Oracle

### Selector Templates
- `generic` - Standard web applications
- `appLocator` - SauceDemo-style applications
- `bootstrap` - Bootstrap-based applications
- `materialui` - Material UI applications
- `antdesign` - Ant Design applications

## 📋 Prerequisites

- **Python 3.10 or higher**
- **Node.js 14.0 or higher** (for npx method)
- **UV** (optional but recommended)

## 🚀 Installation & Usage

### Method 1: Clone Repository (Recommended)

```bash
# Clone from your GitHub repository
git clone https://github.com/YOUR_USERNAME/robotframework-MCP.git
cd robotframework-MCP

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python mcp_server.py
```

**For MCP Clients (VS Code, Claude Desktop, etc.):**

```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "python",
      "args": ["/path/to/robotframework-MCP/mcp_server.py"],
      "type": "stdio"
    }
  }
}
```

### Method 2: Install Directly from GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/YOUR_USERNAME/robotframework-MCP.git

# Run the server
python -m src.server
```

**MCP Configuration:**
```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "type": "stdio"
    }
  }
}
```

### Method 3: Using npx (Node.js)

```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "git+https://github.com/YOUR_USERNAME/robotframework-MCP.git"
      ],
      "type": "stdio"
    }
  }
}
```

### Method 4: Using UV (Python Package Manager)

```bash
# Install UV
pip install uv
```

**MCP Configuration:**
```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/YOUR_USERNAME/robotframework-MCP.git",
        "python",
        "-c",
        "from src.server import main; main()"
      ],
      "type": "stdio"
    }
  }
}
```

### Method 5: Local Development Setup

### Method 5: Local Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/robotframework-MCP.git
cd robotframework-MCP

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development

python mcp_server.py
```

**For MCP Clients:**

```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/robotframework-MCP/mcp_server.py"],
      "type": "stdio"
    }
  }
}
```

Or using Node.js wrapper:

```json
{
  "mcpServers": {
    "robotframework-mcp": {
      "command": "node",
      "args": [
        "/absolute/path/to/robotframework-MCP/bin/robotframework-mcp.js"
      ],
      "type": "stdio"
    }
  }
}
```

---

## 📦 Publishing to PyPI (Optional)

If you want to publish your fork to PyPI so others can install via `pip install`:

### 1. Create PyPI Account

- Sign up at [https://pypi.org/account/register/](https://pypi.org/account/register/)
- Create API token at [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)

### 2. Update Package Name

Edit `pyproject.toml` to use a unique name:

```toml
[project]
name = "robotframework-mcp-yourname"  # Change this to avoid conflicts
version = "2.0.0"
```

### 3. Build and Upload

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### 4. Install from PyPI

After publishing, users can install with:

```bash
pip install robotframework-mcp-yourname
```

**Note**: Replace `YOUR_USERNAME` and `yourname` with your actual GitHub username throughout the README.

## 🛠️ Available Tools

### Test Generation Tools

| Tool | Description |
|------|-------------|
| `create_login_test_case` | Generate login test with configurable selectors |
| `create_page_object_login` | Generate login page object model |
| `create_data_driven_test` | Generate data-driven test templates |
| `create_api_integration_test` | Generate API tests with CRUD operations |
| `create_mobile_test` | Generate Appium mobile tests |
| `create_visual_regression_test` | Generate visual comparison tests |
| `create_database_test` | Generate database tests |
| `create_performance_monitoring_test` | Generate performance tests |

### Keywords Generation Tools

| Tool | Description |
|------|-------------|
| `create_advanced_selenium_keywords` | Dropdowns, checkboxes, alerts, mouse, scroll, tables |
| `create_extended_selenium_keywords` | Screenshots, performance, window management |

### CI/CD Tools

| Tool | Description |
|------|-------------|
| `create_cicd_config` | Generate CI/CD config (GitHub, GitLab, Jenkins, Azure) |

### Utility Tools

| Tool | Description |
|------|-------------|
| `validate_robot_framework_syntax` | Validate Robot Framework code |
| `list_available_templates` | List all selector templates |
| `get_server_info` | Get server information |

## 📖 Usage Examples

### 1. Generate Login Test

```python
create_login_test_case(
    url="https://www.saucedemo.com",
    username="standard_user",
    password="secret_sauce",
    template_type="appLocator",  # Options: generic, appLocator, bootstrap, materialui, antdesign
    browser="Chrome",             # Options: Chrome, Firefox, Edge, Safari
    timeout="10s",
    include_negative_tests=True,  # Include invalid login tests
    headless=False                # Run in headless mode
)
```

**Output**: Complete `.robot` file with:
- Valid login test case
- Negative test cases (invalid username, password, empty fields, SQL injection)
- Reusable keywords
- Proper teardown and error handling

### 2. Generate Page Object Model

```python
create_page_object_login(
    template_type="bootstrap",
    include_wait_keywords=True,      # Add wait-related keywords
    include_validation_keywords=True # Add validation keywords
)
```

**Output**: Page Object Model with:
- Input keywords (Input Username, Input Password)
- Composite keywords (Login With Credentials)
- Wait keywords (Wait For Login Page, Wait For Dashboard)
- Validation keywords (Verify Login Success, Verify Error Message)

### 3. Generate API Test

```python
create_api_integration_test(
    base_url="https://api.example.com",
    endpoint="/users",
    method="GET",              # Options: GET, POST, PUT, DELETE, PATCH
    include_auth=True,         # Include authentication tests
    include_crud=True,         # Include CRUD operation tests
    include_error_handling=True # Include error handling tests
)
```

**Output**: API test suite with:
- Health check and basic requests
- Authentication tests (valid/invalid tokens)
- CRUD operations (Create, Read, Update, Delete)
- Error handling (404, 400, 401, 429)
- Response validation

### 4. Generate Mobile Test

```python
create_mobile_test(
    platform="android",              # Options: android, ios
    app_package="com.example.app",
    app_activity=".MainActivity",
    device_name="emulator-5554",
    include_gestures=True            # Include swipe, pinch, drag gestures
)
```

**Output**: Appium test with:
- App launch and navigation tests
- Login flow and form input
- Scroll and gesture operations
- Orientation change handling
- Background/foreground lifecycle

### 5. Generate Performance Test

```python
create_performance_monitoring_test(
    test_url="https://example.com",
    load_threshold_ms=3000,      # Max page load time
    dom_ready_threshold_ms=2000, # Max DOM ready time
    first_paint_threshold_ms=1000 # Max first paint time
)
```

**Output**: Performance test suite with:
- Page load time measurement
- DOM ready time validation
- First paint and first contentful paint
- Memory usage monitoring
- Resource loading analysis
- Scroll performance testing

### 6. Generate Data-Driven Test

```python
create_data_driven_test(
    test_data_file="test_data.csv",
    test_type="login",  # Options: login, form, search, generic
    include_setup=True  # Include CSV file setup instructions
)
```

**Output**: Data-driven test with:
- DataDriver library integration
- CSV-based test data
- Template for multiple test scenarios
- Setup instructions for CSV file

### 7. Generate Visual Regression Test

```python
create_visual_regression_test(
    base_url="https://example.com",
    baseline_dir="baselines",
    diff_dir="diffs",
    threshold=0.95  # Similarity threshold (0.0-1.0)
)
```

**Output**: Visual regression suite with:
- Baseline image creation
- Screenshot comparison
- Responsive testing across viewports
- Element-specific comparison
- Diff image generation

### 8. Generate Database Test

```python
create_database_test(
    db_type="postgresql",  # Options: postgresql, mysql, sqlite, oracle
    host="localhost",
    port="5432",
    database="testdb",
    include_crud=True,
    include_validation=True
)
```

**Output**: Database test suite with:
- Connection and schema validation
- CRUD operations (Insert, Select, Update, Delete)
- Data integrity checks
- Constraint validation (NOT NULL, UNIQUE, FK)
- Bulk operations

### 9. Generate CI/CD Configuration

```python
create_cicd_config(
    platform="github",  # Options: github, gitlab, jenkins, azure
    test_command="robot",
    python_version="3.11",
    include_parallel=True  # Include parallel execution
)
```

**Output**: CI/CD config file with:
- Multi-browser testing
- Parallel execution
- Test result publishing
- Artifact management
- Failure notifications

### 10. Generate Advanced Selenium Keywords

```python
create_advanced_selenium_keywords()
```

**Output**: Comprehensive keyword library with:
- Dropdown operations (by label, value, index)
- Checkbox operations (select, unselect, toggle)
- File upload operations
- Alert handling (accept, dismiss, input)
- Mouse operations (hover, double-click, right-click, drag-drop)
- Scroll operations (to element, top, bottom, by pixels)
- Window management (switch, close, new tab)
- JavaScript execution
- Advanced wait operations
- Table operations
- Form validation

### 11. Validate Robot Framework Code

```python
validate_robot_framework_syntax(robot_code="""
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
My Test
    Log    Hello World
""")
```

**Output**: Validation report with:
- Syntax errors (must fix)
- Warnings (recommended fixes)
- Best practice suggestions
- Pass/fail status

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v
```

## 📁 Project Structure

```
robotframework-MCP/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── validators.py      # Input validation
│   ├── config.py          # Configuration management
│   ├── logger.py          # Logging utilities
│   └── templates/
│       ├── __init__.py
│       ├── base.py        # Base template class
│       ├── login.py       # Login templates
│       ├── selenium_keywords.py
│       ├── extended_keywords.py
│       ├── performance.py
│       ├── api.py
│       ├── data_driven.py
│       ├── mobile.py
│       ├── visual.py
│       ├── database.py
│       └── cicd.py
├── tests/
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_templates.py
├── bin/
│   └── robotframework-mcp.js
├── mcp_server.py          # Entry point (backward compatible)
├── run_mcp.py             # UV entry point
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── package.json
└── README.md
```

## 🔧 Configuration

### Custom Configuration File

Create a `config.json` file for custom settings:

```json
{
  "log_level": "INFO",
  "log_file": "logs/mcp_server.log",
  "default_browser": "chrome",
  "headless": false,
  "timeouts": {
    "implicit_wait": "10s",
    "explicit_wait": "30s",
    "page_load": "60s",
    "script_timeout": "30s"
  },
  "performance": {
    "page_load_ms": 3000,
    "dom_ready_ms": 2000,
    "first_paint_ms": 1000,
    "first_contentful_paint_ms": 1500,
    "time_to_interactive_ms": 3500
  },
  "retry": {
    "max_retries": 3,
    "retry_delay_seconds": 1.0,
    "retry_on_failure": true
  },
  "screenshots": {
    "on_failure": true,
    "directory": "screenshots",
    "format": "png",
    "full_page": false
  }
}
```

### Environment Variables

```bash
# Set log level
export MCP_LOG_LEVEL=DEBUG

# Set custom config file
export MCP_CONFIG_FILE=/path/to/config.json

# Set browser
export DEFAULT_BROWSER=firefox
```

### Selector Template Customization

You can add custom selector templates by extending `SELECTOR_CONFIGS` in `src/config.py`:

```python
SELECTOR_CONFIGS["custom"] = {
    "username_field": "id=custom-username",
    "password_field": "id=custom-password",
    "login_button": "css=.custom-login-btn",
    "success_indicator": "css=.custom-dashboard",
    "error_message": "css=.custom-error",
    "logout_button": "css=.custom-logout",
    "menu_button": "css=.custom-menu",
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Module Not Found

```bash
# Error: ModuleNotFoundError: No module named 'mcp'
pip install mcp robotframework robotframework-seleniumlibrary

# Or install all dependencies
pip install -r requirements.txt
```

#### 2. WebDriver Issues

```bash
# Install webdriver-manager
pip install webdriver-manager

# Or manually download drivers
# Chrome: https://chromedriver.chromium.org/
# Firefox: https://github.com/mozilla/geckodriver/releases
```

#### 3. Permission Errors on Windows

```powershell
# Run as Administrator or use:
python -m pip install --user robotframework-mcp
```

#### 4. Import Errors

```python
# If you get import errors, ensure src is in Python path
import sys
sys.path.insert(0, '.')
from src.server import main
```

#### 5. MCP Server Not Starting

```bash
# Check Python version (must be 3.10+)
python --version

# Check if all dependencies are installed
pip list | grep -E "mcp|robotframework|selenium"

# Run with debug logging
export MCP_LOG_LEVEL=DEBUG
python mcp_server.py
```

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
from src.logger import configure_logging

configure_logging(level="DEBUG", log_file="debug.log")
```

### Validation Errors

If you encounter validation errors, check:

1. **URL Format**: Must include protocol (http:// or https://)
2. **Credentials**: No special characters like `<`, `>`, `&`, `"`, `'`
3. **Selectors**: Must follow Robot Framework selector syntax
4. **Template Type**: Must be one of: generic, appLocator, bootstrap, materialui, antdesign

## 📚 Advanced Usage

### Custom Template Creation

Create your own templates by extending `BaseTemplate`:

```python
from src.templates.base import BaseTemplate

class MyCustomTemplate(BaseTemplate):
    def generate(self, **kwargs) -> str:
        result = self._get_header("My Custom Test")
        result += self._get_settings(libraries=["SeleniumLibrary"])
        result += self._get_variables({"URL": "https://example.com"})
        # Add your custom logic
        return result
```

### Batch Test Generation

Generate multiple tests at once:

```python
from src.templates.login import LoginTestTemplate

template = LoginTestTemplate()

test_cases = [
    {"url": "https://app1.com", "username": "user1", "password": "pass1"},
    {"url": "https://app2.com", "username": "user2", "password": "pass2"},
]

for i, test_data in enumerate(test_cases):
    result = template.generate(**test_data)
    with open(f"test_login_{i+1}.robot", "w") as f:
        f.write(result)
```

### Integration with Robot Framework

Run generated tests:

```bash
# Run single test
robot test_login.robot

# Run with specific browser
robot --variable BROWSER:firefox test_login.robot

# Run with custom output directory
robot --outputdir results test_login.robot

# Run in parallel
pabot --processes 4 tests/

# Run with tags
robot --include smoke tests/

# Generate report
robot --report custom_report.html tests/
```

### Using with CI/CD

#### GitHub Actions Example

```yaml
name: Robot Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: robot --outputdir results tests/
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: robot-results
          path: results/
```

## 🎓 Best Practices

### 1. Use Page Object Model

Separate test logic from page elements:

```robot
*** Settings ***
Resource    pages/login_page.robot

*** Test Cases ***
Login Test
    Open Login Page
    Login With Credentials    ${USERNAME}    ${PASSWORD}
    Verify Login Success
```

### 2. Use Data-Driven Testing

Keep test data separate from test logic:

```csv
username,password,expected_result
valid_user,valid_pass,success
invalid_user,valid_pass,error
```

### 3. Implement Retry Logic

Handle flaky tests:

```robot
*** Keywords ***
Retry On Failure
    [Arguments]    ${keyword}    @{args}
    Wait Until Keyword Succeeds    3x    1s    ${keyword}    @{args}
```

### 4. Use Proper Waits

Avoid `Sleep`, use explicit waits:

```robot
Wait Until Element Is Visible    ${LOCATOR}    timeout=10s
Wait Until Page Contains    Expected Text    timeout=10s
```

### 5. Organize Tests

Structure your test suite:

```
tests/
├── smoke/          # Critical tests
├── regression/     # Full test suite
├── api/           # API tests
├── mobile/        # Mobile tests
└── performance/   # Performance tests
```

## 📊 Performance Tips

1. **Use Headless Mode** for faster execution:
   ```python
   create_login_test_case(..., headless=True)
   ```

2. **Run Tests in Parallel**:
   ```bash
   pabot --processes 4 tests/
   ```

3. **Optimize Waits**:
   - Use explicit waits instead of implicit waits
   - Set appropriate timeout values
   - Avoid unnecessary `Sleep` commands

4. **Reuse Browser Sessions**:
   ```robot
   Suite Setup    Open Browser    ${URL}    ${BROWSER}
   Suite Teardown    Close Browser
   ```

5. **Use Screenshot Only on Failure**:
   ```robot
   Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot
   ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/robotframework-MCP.git
   cd robotframework-MCP
   ```

2. **Set Up Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Make Changes**
   ```bash
   git checkout -b feature/amazing-feature
   # Make your changes
   ```

4. **Test Your Changes**
   ```bash
   pytest tests/ -v
   black src/ tests/
   flake8 src/ tests/
   ```

5. **Submit Pull Request**
   ```bash
   git commit -m "feat: add amazing feature"
   git push origin feature/amazing-feature
   ```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Publishing Your Fork

Want to publish your fork to PyPI? See [PUBLISHING.md](PUBLISHING.md) for step-by-step instructions.

## 🔄 Changelog

### v2.0.0 (2025-01-18)

**Major Changes:**
- 🏗️ Complete architecture refactor with modular design
- 📝 Added comprehensive logging system
- ✅ Implemented robust input validation
- 🧪 Added unit tests for all modules

**New Features:**
- 📱 Mobile testing support (Appium)
- 🔌 API testing templates
- 🗄️ Database testing support
- 👁️ Visual regression testing
- 🚀 CI/CD configuration generators
- 🎨 Material UI and Ant Design templates

**Improvements:**
- Better error messages
- Type hints throughout codebase
- Improved documentation
- Performance optimizations

**Bug Fixes:**
- Fixed selector template lookup
- Fixed import errors
- Improved Windows compatibility

### v1.0.0 (2024-12-01)

- Initial release
- Basic login test generation
- Selenium keywords
- Page Object Model support

## 🗺️ Roadmap

### v2.1.0 (Planned)

- [ ] GraphQL API testing support
- [ ] Playwright integration
- [ ] Docker support
- [ ] Test data generation tools
- [ ] More CI/CD platforms (CircleCI, Travis CI)

### v2.2.0 (Planned)

- [ ] AI-powered test generation
- [ ] Visual test recorder
- [ ] Test maintenance tools
- [ ] Performance optimization suggestions
- [ ] Multi-language support

### v3.0.0 (Future)

- [ ] Web UI for test generation
- [ ] Cloud test execution
- [ ] Test analytics dashboard
- [ ] Integration with test management tools

## 📖 Resources

### Documentation

- [Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- [SeleniumLibrary Documentation](https://robotframework.org/SeleniumLibrary/)
- [Appium Documentation](http://appium.io/docs/en/latest/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

### Tutorials

- [Getting Started with Robot Framework](https://robotframework.org/#getting-started)
- [Selenium Best Practices](https://www.selenium.dev/documentation/test_practices/)
- [Mobile Testing with Appium](http://appium.io/docs/en/latest/quickstart/)

### Community

- [Robot Framework Forum](https://forum.robotframework.org/)
- [Robot Framework Slack](https://robotframework-slack-invite.herokuapp.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/robotframework)

## ❓ FAQ

### Q: Can I use this with existing Robot Framework tests?

**A:** Yes! The generated code is standard Robot Framework syntax and can be integrated with existing test suites.

### Q: Do I need to install Robot Framework separately?

**A:** No, Robot Framework is included in the dependencies and will be installed automatically.

### Q: Can I customize the generated code?

**A:** Yes, all generated code is fully editable. You can modify it to fit your specific needs.

### Q: Does this support BDD (Behavior-Driven Development)?

**A:** The generated tests use Robot Framework's keyword-driven approach, which is similar to BDD. You can easily adapt them to BDD style.

### Q: Can I use this for non-web testing?

**A:** Yes! The server supports mobile (Appium), API (Requests), and database testing in addition to web testing.

### Q: Is there a limit to how many tests I can generate?

**A:** No, you can generate as many tests as you need.

### Q: Can I contribute new templates?

**A:** Absolutely! We welcome contributions. See the Contributing section for details.

### Q: Does this work on Windows/Mac/Linux?

**A:** Yes, the server is cross-platform and works on all major operating systems.

### Q: How do I report bugs or request features?

**A:** Please open an issue on [GitHub Issues](https://github.com/sourcefuse/robotframework-MCP/issues).

### Q: Is there commercial support available?

**A:** For commercial support, please contact meenu.rani@sourcefuse.com.

## 📬 Contact & Support

### Get Help

- 📧 **Email**: meenu.rani@sourcefuse.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/sourcefuse/robotframework-MCP/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/sourcefuse/robotframework-MCP/discussions)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/sourcefuse/robotframework-MCP/wiki)

### Maintainers

- **Meenu Rani** - [@meenurani1](https://github.com/meenurani1)
- **Sourcefuse Team** - [@sourcefuse](https://github.com/sourcefuse)

### Acknowledgments

Special thanks to:
- Robot Framework community
- MCP Protocol contributors
- All open source contributors

## ⭐ Show Your Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📝 Improving documentation
- 🔀 Contributing code

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Sourcefuse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Made with ❤️ by [Sourcefuse](https://www.sourcefuse.com/)**

[Website](https://www.sourcefuse.com/) • [GitHub](https://github.com/sourcefuse) • [LinkedIn](https://www.linkedin.com/company/sourcefuse)

</div>
