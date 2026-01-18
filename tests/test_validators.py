"""
Unit tests for validators module
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validators import InputValidator, ValidationError, ValidationResult


class TestURLValidation:
    """Tests for URL validation"""
    
    def test_valid_https_url(self):
        """Test valid HTTPS URL"""
        url = "https://example.com"
        result = InputValidator.validate_url(url)
        assert result == url
    
    def test_valid_http_url(self):
        """Test valid HTTP URL"""
        url = "http://example.com"
        result = InputValidator.validate_url(url)
        assert result == url
    
    def test_url_with_path(self):
        """Test URL with path"""
        url = "https://example.com/login"
        result = InputValidator.validate_url(url)
        assert result == url
    
    def test_url_with_port(self):
        """Test URL with port"""
        url = "https://example.com:8080/api"
        result = InputValidator.validate_url(url)
        assert result == url
    
    def test_empty_url_raises_error(self):
        """Test empty URL raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_url("")
        assert "cannot be empty" in str(exc_info.value)
    
    def test_whitespace_url_raises_error(self):
        """Test whitespace-only URL raises ValidationError"""
        with pytest.raises(ValidationError):
            InputValidator.validate_url("   ")
    
    def test_invalid_protocol_raises_error(self):
        """Test invalid protocol raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_url("ftp://example.com")
        assert "http or https" in str(exc_info.value)
    
    def test_missing_protocol_raises_error(self):
        """Test missing protocol raises ValidationError"""
        with pytest.raises(ValidationError):
            InputValidator.validate_url("example.com")
    
    def test_url_strips_whitespace(self):
        """Test URL whitespace is stripped"""
        url = "  https://example.com  "
        result = InputValidator.validate_url(url)
        assert result == "https://example.com"
    
    def test_localhost_allowed_by_default(self):
        """Test localhost is allowed by default"""
        url = "http://localhost:3000"
        result = InputValidator.validate_url(url)
        assert result == url
    
    def test_localhost_blocked_when_disabled(self):
        """Test localhost blocked when allow_localhost=False"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_url("http://localhost:3000", allow_localhost=False)
        assert "Localhost" in str(exc_info.value)


class TestCredentialsValidation:
    """Tests for credentials validation"""
    
    def test_valid_credentials(self):
        """Test valid credentials"""
        username, password = InputValidator.validate_credentials("user", "pass123")
        assert username == "user"
        assert password == "pass123"
    
    def test_empty_username_raises_error(self):
        """Test empty username raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials("", "password")
        assert "Username" in str(exc_info.value)
    
    def test_empty_password_raises_error(self):
        """Test empty password raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials("user", "")
        assert "Password" in str(exc_info.value)
    
    def test_username_too_long_raises_error(self):
        """Test username too long raises ValidationError"""
        long_username = "a" * 101
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials(long_username, "pass")
        assert "too long" in str(exc_info.value)
    
    def test_password_too_long_raises_error(self):
        """Test password too long raises ValidationError"""
        long_password = "a" * 101
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials("user", long_password)
        assert "too long" in str(exc_info.value)
    
    def test_dangerous_chars_in_username_raises_error(self):
        """Test dangerous characters in username raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials("user<script>", "pass")
        assert "invalid character" in str(exc_info.value)
    
    def test_dangerous_chars_in_password_raises_error(self):
        """Test dangerous characters in password raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_credentials("user", "pass&word")
        assert "invalid character" in str(exc_info.value)
    
    def test_credentials_strip_whitespace(self):
        """Test credentials whitespace is stripped"""
        username, password = InputValidator.validate_credentials("  user  ", "  pass  ")
        assert username == "user"
        assert password == "pass"
    
    def test_special_chars_allowed_when_enabled(self):
        """Test special characters allowed when allow_special_chars=True"""
        username, password = InputValidator.validate_credentials(
            "user<test>", "pass&word", allow_special_chars=True
        )
        assert username == "user<test>"
        assert password == "pass&word"


class TestSelectorValidation:
    """Tests for selector validation"""
    
    def test_valid_id_selector(self):
        """Test valid ID selector"""
        result = InputValidator.validate_selector("id=username")
        assert result == "id=username"
    
    def test_valid_css_selector(self):
        """Test valid CSS selector"""
        result = InputValidator.validate_selector("css=.login-button")
        assert result == "css=.login-button"
    
    def test_valid_xpath_selector(self):
        """Test valid XPath selector"""
        result = InputValidator.validate_selector("xpath=//div[@id='test']")
        assert result == "xpath=//div[@id='test']"
    
    def test_valid_name_selector(self):
        """Test valid name selector"""
        result = InputValidator.validate_selector("name=email")
        assert result == "name=email"
    
    def test_empty_selector_raises_error(self):
        """Test empty selector raises ValidationError"""
        with pytest.raises(ValidationError):
            InputValidator.validate_selector("")
    
    def test_selector_too_long_raises_error(self):
        """Test selector too long raises ValidationError"""
        long_selector = "id=" + "a" * 500
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_selector(long_selector)
        assert "too long" in str(exc_info.value)


class TestTemplateTypeValidation:
    """Tests for template type validation"""
    
    def test_valid_template_type(self):
        """Test valid template type"""
        valid_types = ["generic", "bootstrap", "materialui"]
        result = InputValidator.validate_template_type("generic", valid_types)
        assert result == "generic"
    
    def test_template_type_case_insensitive(self):
        """Test template type is case insensitive"""
        valid_types = ["generic", "bootstrap"]
        result = InputValidator.validate_template_type("GENERIC", valid_types)
        assert result == "generic"
    
    def test_invalid_template_type_raises_error(self):
        """Test invalid template type raises ValidationError"""
        valid_types = ["generic", "bootstrap"]
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_template_type("invalid", valid_types)
        assert "Invalid template type" in str(exc_info.value)


class TestRobotCodeValidation:
    """Tests for Robot Framework code validation"""
    
    def test_valid_robot_code(self):
        """Test valid Robot Framework code"""
        code = """*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Test Example
    Log    Hello World
"""
        result = InputValidator.validate_robot_code(code)
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_empty_code_fails(self):
        """Test empty code fails validation"""
        result = InputValidator.validate_robot_code("")
        assert not result.is_valid
    
    def test_unclosed_section_header(self):
        """Test unclosed section header is detected"""
        code = """*** Settings
Library    SeleniumLibrary
"""
        result = InputValidator.validate_robot_code(code)
        assert len(result.errors) > 0
        assert any("***" in error for error in result.errors)
    
    def test_double_brace_warning(self):
        """Test double brace syntax generates warning"""
        code = """*** Variables ***
${{URL}}    https://example.com
"""
        result = InputValidator.validate_robot_code(code)
        assert len(result.warnings) > 0


class TestHTTPMethodValidation:
    """Tests for HTTP method validation"""
    
    def test_valid_get_method(self):
        """Test valid GET method"""
        result = InputValidator.validate_http_method("GET")
        assert result == "GET"
    
    def test_valid_post_method(self):
        """Test valid POST method"""
        result = InputValidator.validate_http_method("post")
        assert result == "POST"
    
    def test_invalid_method_raises_error(self):
        """Test invalid method raises ValidationError"""
        with pytest.raises(ValidationError):
            InputValidator.validate_http_method("INVALID")


class TestTimeoutValidation:
    """Tests for timeout validation"""
    
    def test_valid_seconds_timeout(self):
        """Test valid seconds timeout"""
        result = InputValidator.validate_timeout("10s")
        assert result == "10s"
    
    def test_valid_milliseconds_timeout(self):
        """Test valid milliseconds timeout"""
        result = InputValidator.validate_timeout("500ms")
        assert result == "500ms"
    
    def test_valid_minutes_timeout(self):
        """Test valid minutes timeout"""
        result = InputValidator.validate_timeout("2m")
        assert result == "2m"
    
    def test_invalid_timeout_raises_error(self):
        """Test invalid timeout raises ValidationError"""
        with pytest.raises(ValidationError):
            InputValidator.validate_timeout("invalid")


class TestValidationResult:
    """Tests for ValidationResult class"""
    
    def test_success_result(self):
        """Test success result creation"""
        result = ValidationResult.success("value", ["warning1"])
        assert result.is_valid
        assert result.value == "value"
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
    
    def test_failure_result(self):
        """Test failure result creation"""
        result = ValidationResult.failure(["error1"], ["warning1"])
        assert not result.is_valid
        assert result.value is None
        assert len(result.errors) == 1
        assert len(result.warnings) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
