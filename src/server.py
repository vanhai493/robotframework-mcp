"""
Robot Framework MCP Server - Main Server Module
Enhanced version with improved architecture, logging, and new tools
"""

import sys
import time
from typing import Optional
from mcp.server.fastmcp import FastMCP

from .validators import InputValidator, ValidationError, ValidationResult
from .config import (
    ServerConfig, 
    get_selector_config, 
    SELECTOR_CONFIGS,
    load_config_from_file,
)
from .logger import get_logger, configure_logging
from .templates.login import LoginTestTemplate, LoginPageObjectTemplate
from .templates.selenium_keywords import AdvancedSeleniumKeywords
from .templates.extended_keywords import ExtendedSeleniumKeywords
from .templates.performance import PerformanceTestTemplate
from .templates.api import APITestTemplate
from .templates.data_driven import DataDrivenTestTemplate
from .templates.mobile import MobileTestTemplate
from .templates.visual import VisualRegressionTemplate
from .templates.database import DatabaseTestTemplate
from .templates.cicd import CICDTemplate


# Initialize logger
logger = get_logger()

# Create MCP server instance
mcp = FastMCP("Robot Framework MCP Server v2.0")


def _log_tool_execution(tool_name: str, **params):
    """Log tool execution with timing"""
    logger.log_tool_call(tool_name, **params)
    return time.time()


def _log_tool_result(tool_name: str, start_time: float, success: bool = True):
    """Log tool result with duration"""
    duration_ms = (time.time() - start_time) * 1000
    logger.log_tool_result(tool_name, success, duration_ms)


# ============================================
# Login Test Tools
# ============================================

@mcp.tool()
def create_login_test_case(
    url: str,
    username: str,
    password: str,
    template_type: str = "generic",
    browser: str = "Chrome",
    timeout: str = "10s",
    include_negative_tests: bool = False,
    headless: bool = False,
) -> str:
    """
    Generate Robot Framework test case code for login functionality.
    Returns complete .robot file content - does not execute the test.
    
    Args:
        url: Target URL for login page
        username: Test username
        password: Test password  
        template_type: Selector template (generic, appLocator, bootstrap, materialui, antdesign)
        browser: Browser to use (Chrome, Firefox, Edge)
        timeout: Wait timeout (e.g., '10s', '30s')
        include_negative_tests: Include negative test cases
        headless: Run browser in headless mode
    """
    start_time = _log_tool_execution(
        "create_login_test_case", 
        url=url, template_type=template_type, browser=browser
    )
    
    try:
        # Validate inputs
        validated_url = InputValidator.validate_url(url)
        validated_username, validated_password = InputValidator.validate_credentials(
            username, password
        )
        validated_template = InputValidator.validate_template_type(
            template_type, list(SELECTOR_CONFIGS.keys())
        )
        
        # Generate template
        template = LoginTestTemplate()
        result = template.generate(
            url=validated_url,
            username=validated_username,
            password=validated_password,
            template_type=validated_template,
            browser=browser,
            timeout=timeout,
            include_negative_tests=include_negative_tests,
            headless=headless,
        )
        
        _log_tool_result("create_login_test_case", start_time, True)
        return result
        
    except ValidationError as e:
        logger.log_validation_error(e.field or "unknown", e.message)
        _log_tool_result("create_login_test_case", start_time, False)
        return f"# VALIDATION ERROR: {e.message}\n# Please correct the input and try again."
    except Exception as e:
        logger.exception(f"Unexpected error in create_login_test_case: {e}")
        _log_tool_result("create_login_test_case", start_time, False)
        return f"# UNEXPECTED ERROR: {str(e)}\n# Please contact support."


@mcp.tool()
def create_page_object_login(
    template_type: str = "generic",
    include_wait_keywords: bool = True,
    include_validation_keywords: bool = True,
) -> str:
    """
    Generate Robot Framework page object model code for login page.
    Returns .robot file content - does not execute.
    
    Args:
        template_type: Selector template (generic, appLocator, bootstrap, materialui, antdesign)
        include_wait_keywords: Include wait-related keywords
        include_validation_keywords: Include validation keywords
    """
    start_time = _log_tool_execution("create_page_object_login", template_type=template_type)
    
    try:
        validated_template = InputValidator.validate_template_type(
            template_type, list(SELECTOR_CONFIGS.keys())
        )
        
        template = LoginPageObjectTemplate()
        result = template.generate(
            template_type=validated_template,
            include_wait_keywords=include_wait_keywords,
            include_validation_keywords=include_validation_keywords,
        )
        
        _log_tool_result("create_page_object_login", start_time, True)
        return result
        
    except ValidationError as e:
        logger.log_validation_error(e.field or "unknown", e.message)
        _log_tool_result("create_page_object_login", start_time, False)
        return f"# VALIDATION ERROR: {e.message}\n# Please correct the input and try again."
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_page_object_login", start_time, False)
        return f"# ERROR: {str(e)}\n# Please contact support."


# ============================================
# Selenium Keywords Tools
# ============================================

@mcp.tool()
def create_advanced_selenium_keywords() -> str:
    """
    Generate Robot Framework keywords for advanced Selenium operations.
    Includes: dropdowns, checkboxes, file uploads, alerts, mouse operations,
    scrolling, window management, JavaScript execution, waits, tables, forms.
    Returns .robot file content - does not execute.
    """
    start_time = _log_tool_execution("create_advanced_selenium_keywords")
    
    try:
        template = AdvancedSeleniumKeywords()
        result = template.generate()
        _log_tool_result("create_advanced_selenium_keywords", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_advanced_selenium_keywords", start_time, False)
        return f"# ERROR: {str(e)}"


@mcp.tool()
def create_extended_selenium_keywords() -> str:
    """
    Generate extended Robot Framework keywords for screenshots, 
    performance monitoring, and window management.
    Returns .robot file content - does not execute.
    """
    start_time = _log_tool_execution("create_extended_selenium_keywords")
    
    try:
        template = ExtendedSeleniumKeywords()
        result = template.generate()
        _log_tool_result("create_extended_selenium_keywords", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_extended_selenium_keywords", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Performance Testing Tools
# ============================================

@mcp.tool()
def create_performance_monitoring_test(
    test_url: str = "${TEST_URL}",
    load_threshold_ms: int = 3000,
    dom_ready_threshold_ms: int = 2000,
    first_paint_threshold_ms: int = 1000,
) -> str:
    """
    Generate Robot Framework performance monitoring test code.
    Tests page load time, DOM ready, first paint, memory usage, and scroll performance.
    Returns complete .robot file content - does not execute.
    
    Args:
        test_url: URL to test (can use variable like ${TEST_URL})
        load_threshold_ms: Maximum acceptable page load time in milliseconds
        dom_ready_threshold_ms: Maximum acceptable DOM ready time
        first_paint_threshold_ms: Maximum acceptable first paint time
    """
    start_time = _log_tool_execution(
        "create_performance_monitoring_test",
        test_url=test_url,
        load_threshold_ms=load_threshold_ms
    )
    
    try:
        template = PerformanceTestTemplate()
        result = template.generate(
            test_url=test_url,
            load_threshold_ms=load_threshold_ms,
            dom_ready_threshold_ms=dom_ready_threshold_ms,
            first_paint_threshold_ms=first_paint_threshold_ms,
        )
        _log_tool_result("create_performance_monitoring_test", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_performance_monitoring_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Data-Driven Testing Tools
# ============================================

@mcp.tool()
def create_data_driven_test(
    test_data_file: str = "test_data.csv",
    test_type: str = "login",
    include_setup: bool = True,
) -> str:
    """
    Generate Robot Framework data-driven test template code.
    Uses DataDriver library for CSV-based test data.
    Returns .robot file content - does not execute.
    
    Args:
        test_data_file: Path to CSV test data file
        test_type: Type of test (login, form, search, generic)
        include_setup: Include data file setup instructions
    """
    start_time = _log_tool_execution(
        "create_data_driven_test",
        test_data_file=test_data_file,
        test_type=test_type
    )
    
    try:
        template = DataDrivenTestTemplate()
        result = template.generate(
            test_data_file=test_data_file,
            test_type=test_type,
            include_setup=include_setup,
        )
        _log_tool_result("create_data_driven_test", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_data_driven_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# API Testing Tools
# ============================================

@mcp.tool()
def create_api_integration_test(
    base_url: str,
    endpoint: str = "/api",
    method: str = "GET",
    include_auth: bool = True,
    include_crud: bool = True,
    include_error_handling: bool = True,
) -> str:
    """
    Generate Robot Framework API integration test code.
    Uses RequestsLibrary for HTTP requests.
    Returns .robot file content - does not execute.
    
    Args:
        base_url: Base URL for API (e.g., https://api.example.com)
        endpoint: API endpoint to test (e.g., /users, /products)
        method: Primary HTTP method (GET, POST, PUT, DELETE)
        include_auth: Include authentication tests
        include_crud: Include CRUD operation tests
        include_error_handling: Include error handling tests
    """
    start_time = _log_tool_execution(
        "create_api_integration_test",
        base_url=base_url,
        endpoint=endpoint,
        method=method
    )
    
    try:
        validated_url = InputValidator.validate_url(base_url)
        validated_method = InputValidator.validate_http_method(method)
        
        template = APITestTemplate()
        result = template.generate(
            base_url=validated_url,
            endpoint=endpoint,
            method=validated_method,
            include_auth=include_auth,
            include_crud=include_crud,
            include_error_handling=include_error_handling,
        )
        _log_tool_result("create_api_integration_test", start_time, True)
        return result
        
    except ValidationError as e:
        logger.log_validation_error(e.field or "unknown", e.message)
        _log_tool_result("create_api_integration_test", start_time, False)
        return f"# VALIDATION ERROR: {e.message}\n# Please correct the input and try again."
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_api_integration_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Mobile Testing Tools
# ============================================

@mcp.tool()
def create_mobile_test(
    platform: str = "android",
    app_package: str = "",
    app_activity: str = "",
    device_name: str = "emulator-5554",
    include_gestures: bool = True,
) -> str:
    """
    Generate Robot Framework mobile app test code using Appium.
    Returns .robot file content - does not execute.
    
    Args:
        platform: Mobile platform (android or ios)
        app_package: Android app package name (e.g., com.example.app)
        app_activity: Android app activity (e.g., .MainActivity)
        device_name: Device name or emulator ID
        include_gestures: Include gesture keywords (swipe, pinch, etc.)
    """
    start_time = _log_tool_execution(
        "create_mobile_test",
        platform=platform,
        app_package=app_package
    )
    
    try:
        template = MobileTestTemplate()
        result = template.generate(
            platform=platform,
            app_package=app_package,
            app_activity=app_activity,
            device_name=device_name,
            include_gestures=include_gestures,
        )
        _log_tool_result("create_mobile_test", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_mobile_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Visual Regression Testing Tools
# ============================================

@mcp.tool()
def create_visual_regression_test(
    base_url: str = "${BASE_URL}",
    baseline_dir: str = "baselines",
    diff_dir: str = "diffs",
    threshold: float = 0.95,
) -> str:
    """
    Generate Robot Framework visual regression test code.
    Compares screenshots against baseline images.
    Returns .robot file content - does not execute.
    
    Args:
        base_url: Base URL for testing
        baseline_dir: Directory for baseline images
        diff_dir: Directory for diff images
        threshold: Similarity threshold (0.0 to 1.0, default 0.95)
    """
    start_time = _log_tool_execution(
        "create_visual_regression_test",
        base_url=base_url,
        threshold=threshold
    )
    
    try:
        template = VisualRegressionTemplate()
        result = template.generate(
            base_url=base_url,
            baseline_dir=baseline_dir,
            diff_dir=diff_dir,
            threshold=threshold,
        )
        _log_tool_result("create_visual_regression_test", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_visual_regression_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Database Testing Tools
# ============================================

@mcp.tool()
def create_database_test(
    db_type: str = "postgresql",
    host: str = "localhost",
    port: str = "5432",
    database: str = "testdb",
    include_crud: bool = True,
    include_validation: bool = True,
) -> str:
    """
    Generate Robot Framework database test code.
    Uses DatabaseLibrary for database operations.
    Returns .robot file content - does not execute.
    
    Args:
        db_type: Database type (postgresql, mysql, sqlite, oracle)
        host: Database host
        port: Database port
        database: Database name
        include_crud: Include CRUD operation tests
        include_validation: Include data validation tests
    """
    start_time = _log_tool_execution(
        "create_database_test",
        db_type=db_type,
        database=database
    )
    
    try:
        template = DatabaseTestTemplate()
        result = template.generate(
            db_type=db_type,
            host=host,
            port=port,
            database=database,
            include_crud=include_crud,
            include_validation=include_validation,
        )
        _log_tool_result("create_database_test", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_database_test", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# CI/CD Integration Tools
# ============================================

@mcp.tool()
def create_cicd_config(
    platform: str = "github",
    test_command: str = "robot",
    python_version: str = "3.11",
    include_parallel: bool = True,
) -> str:
    """
    Generate CI/CD configuration file for Robot Framework tests.
    Returns configuration file content for the specified platform.
    
    Args:
        platform: CI/CD platform (github, gitlab, jenkins, azure)
        test_command: Command to run tests (default: robot)
        python_version: Python version to use
        include_parallel: Include parallel test execution configuration
    """
    start_time = _log_tool_execution(
        "create_cicd_config",
        platform=platform,
        python_version=python_version
    )
    
    try:
        template = CICDTemplate()
        result = template.generate(
            platform=platform,
            test_command=test_command,
            python_version=python_version,
            include_parallel=include_parallel,
        )
        _log_tool_result("create_cicd_config", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("create_cicd_config", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Validation Tools
# ============================================

@mcp.tool()
def validate_robot_framework_syntax(robot_code: str) -> str:
    """
    Validate Robot Framework syntax and provide improvement suggestions.
    Returns validation report - does not execute code.
    
    Args:
        robot_code: Robot Framework code to validate
    """
    start_time = _log_tool_execution("validate_robot_framework_syntax")
    
    try:
        result = InputValidator.validate_robot_code(robot_code)
        
        report = "# ROBOT FRAMEWORK SYNTAX VALIDATION\n\n"
        
        if result.errors:
            report += "## ❌ ERRORS (Must Fix):\n"
            report += '\n'.join(f"- {error}" for error in result.errors) + "\n\n"
        
        if result.warnings:
            report += "## ⚠️ WARNINGS (Recommended Fixes):\n"
            report += '\n'.join(f"- {warning}" for warning in result.warnings) + "\n\n"
        
        if result.is_valid and not result.warnings:
            report += "## ✅ VALIDATION PASSED\n"
            report += "No syntax errors or warnings found.\n"
        elif result.is_valid:
            report += "## ⚠️ VALIDATION PASSED WITH WARNINGS\n"
            report += "No critical errors, but consider fixing the warnings above.\n"
        else:
            report += "## ❌ VALIDATION FAILED\n"
            report += "Critical errors found that must be fixed before running tests.\n"
        
        _log_tool_result("validate_robot_framework_syntax", start_time, result.is_valid)
        return report
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("validate_robot_framework_syntax", start_time, False)
        return f"# VALIDATION ERROR: {str(e)}"


# ============================================
# Utility Tools
# ============================================

@mcp.tool()
def list_available_templates() -> str:
    """
    List all available selector templates and their configurations.
    Returns formatted list of templates with their selectors.
    """
    start_time = _log_tool_execution("list_available_templates")
    
    try:
        result = "# AVAILABLE SELECTOR TEMPLATES\n\n"
        
        for template_name, selectors in SELECTOR_CONFIGS.items():
            result += f"## {template_name}\n"
            for selector_name, selector_value in selectors.items():
                result += f"  - {selector_name}: {selector_value}\n"
            result += "\n"
        
        result += "## Usage\n"
        result += "Pass the template name to any tool that accepts `template_type` parameter.\n"
        result += "Example: create_login_test_case(url='...', template_type='bootstrap')\n"
        
        _log_tool_result("list_available_templates", start_time, True)
        return result
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("list_available_templates", start_time, False)
        return f"# ERROR: {str(e)}"


@mcp.tool()
def get_server_info() -> str:
    """
    Get information about the MCP server and available tools.
    Returns server version, available tools, and configuration.
    """
    start_time = _log_tool_execution("get_server_info")
    
    try:
        info = """# ROBOT FRAMEWORK MCP SERVER v2.0

## Available Tools

### Test Generation
- create_login_test_case: Generate login test cases
- create_page_object_login: Generate login page object model
- create_data_driven_test: Generate data-driven tests
- create_api_integration_test: Generate API tests
- create_mobile_test: Generate mobile app tests (Appium)
- create_visual_regression_test: Generate visual regression tests
- create_database_test: Generate database tests
- create_performance_monitoring_test: Generate performance tests

### Keywords Generation
- create_advanced_selenium_keywords: Advanced Selenium operations
- create_extended_selenium_keywords: Screenshots, performance, window management

### CI/CD Integration
- create_cicd_config: Generate CI/CD configuration (GitHub, GitLab, Jenkins, Azure)

### Utilities
- validate_robot_framework_syntax: Validate Robot Framework code
- list_available_templates: List selector templates
- get_server_info: This information

## Supported Selector Templates
- generic: Standard web applications
- appLocator: SauceDemo-style applications
- bootstrap: Bootstrap-based applications
- materialui: Material UI applications
- antdesign: Ant Design applications

## Features
- Input validation with detailed error messages
- Structured logging for debugging
- Configurable timeouts and thresholds
- Support for multiple browsers (Chrome, Firefox, Edge, Safari)
- Headless mode support
- Parallel test execution templates
- Retry mechanisms for flaky tests

## Version: 2.0.0
## Author: Meenu Rani <meenu.rani@sourcefuse.com>
"""
        _log_tool_result("get_server_info", start_time, True)
        return info
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("get_server_info", start_time, False)
        return f"# ERROR: {str(e)}"


# ============================================
# Main Entry Point
# ============================================

def main():
    """Entry point for the Robot Framework MCP server"""
    # Configure logging
    configure_logging(level="INFO")
    
    # Check if running in stdio mode
    is_stdio = len(sys.argv) > 1 and '--stdio' in sys.argv
    
    if not is_stdio:
        logger.info("Starting Robot Framework MCP server v2.0...")
        logger.info("Available templates: " + ", ".join(SELECTOR_CONFIGS.keys()))
        logger.info("Features: Input validation, logging, multiple test types")
    
    try:
        mcp.run()
    except Exception as e:
        if not is_stdio:
            logger.exception(f"Error starting server: {e}")
        raise


if __name__ == "__main__":
    main()
