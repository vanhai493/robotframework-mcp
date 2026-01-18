"""
Unit tests for validators module
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validators import InputValidator, ValidationError, ValidationResult, ErrorContext, ErrorFormatter


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


class TestErrorContext:
    """Tests for ErrorContext dataclass"""
    
    def test_error_context_creation_with_all_fields(self):
        """Test ErrorContext creation with all fields"""
        context = ErrorContext(
            error_code="VAL001",
            field="url",
            message="Invalid URL format",
            suggestion="Ensure URL starts with http:// or https://",
            example="https://example.com",
            documentation_url="https://docs.example.com/validation"
        )
        assert context.error_code == "VAL001"
        assert context.field == "url"
        assert context.message == "Invalid URL format"
        assert context.suggestion == "Ensure URL starts with http:// or https://"
        assert context.example == "https://example.com"
        assert context.documentation_url == "https://docs.example.com/validation"
    
    def test_error_context_creation_with_required_fields_only(self):
        """Test ErrorContext creation with only required fields"""
        context = ErrorContext(
            error_code="VAL002",
            field="username",
            message="Username cannot be empty",
            suggestion="Provide a valid username"
        )
        assert context.error_code == "VAL002"
        assert context.field == "username"
        assert context.message == "Username cannot be empty"
        assert context.suggestion == "Provide a valid username"
        assert context.example is None
        assert context.documentation_url is None
    
    def test_error_context_with_example_only(self):
        """Test ErrorContext with example but no documentation URL"""
        context = ErrorContext(
            error_code="VAL003",
            field="selector",
            message="Invalid selector format",
            suggestion="Use a valid selector format",
            example="id=username or css=.login-button"
        )
        assert context.error_code == "VAL003"
        assert context.example == "id=username or css=.login-button"
        assert context.documentation_url is None
    
    def test_error_context_with_documentation_url_only(self):
        """Test ErrorContext with documentation URL but no example"""
        context = ErrorContext(
            error_code="SEC001",
            field="query",
            message="Potential SQL injection detected",
            suggestion="Use parameterized queries",
            documentation_url="https://docs.example.com/security/sql-injection"
        )
        assert context.error_code == "SEC001"
        assert context.documentation_url == "https://docs.example.com/security/sql-injection"
        assert context.example is None
    
    def test_error_context_is_dataclass(self):
        """Test that ErrorContext is a proper dataclass"""
        from dataclasses import is_dataclass
        assert is_dataclass(ErrorContext)
    
    def test_error_context_equality(self):
        """Test ErrorContext equality comparison"""
        context1 = ErrorContext(
            error_code="VAL001",
            field="url",
            message="Invalid URL",
            suggestion="Fix URL"
        )
        context2 = ErrorContext(
            error_code="VAL001",
            field="url",
            message="Invalid URL",
            suggestion="Fix URL"
        )
        assert context1 == context2
    
    def test_error_context_inequality(self):
        """Test ErrorContext inequality comparison"""
        context1 = ErrorContext(
            error_code="VAL001",
            field="url",
            message="Invalid URL",
            suggestion="Fix URL"
        )
        context2 = ErrorContext(
            error_code="VAL002",
            field="username",
            message="Invalid username",
            suggestion="Fix username"
        )
        assert context1 != context2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestErrorFormatter:
    """Tests for ErrorFormatter class"""
    
    def test_error_codes_registry_exists(self):
        """Test that error codes registry is defined"""
        assert hasattr(ErrorFormatter, 'ERROR_CODES')
        assert isinstance(ErrorFormatter.ERROR_CODES, dict)
        assert len(ErrorFormatter.ERROR_CODES) > 0
    
    def test_error_codes_have_descriptions(self):
        """Test that all error codes have descriptions"""
        for code, description in ErrorFormatter.ERROR_CODES.items():
            assert isinstance(code, str)
            assert isinstance(description, str)
            assert len(description) > 0
    
    def test_format_validation_error_url_empty(self):
        """Test formatting empty URL validation error"""
        error = ValidationError("URL cannot be empty", field="url")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL009" in result
        assert "Field: url" in result
        assert "Suggestion:" in result
        assert "Example:" in result
        assert "https://example.com" in result
    
    def test_format_validation_error_url_protocol(self):
        """Test formatting URL protocol validation error"""
        error = ValidationError("URL must use http or https protocol", field="url")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL001" in result
        assert "Field: url" in result
        assert "protocol" in result.lower()
        assert "Example:" in result
    
    def test_format_validation_error_username_empty(self):
        """Test formatting empty username validation error"""
        error = ValidationError("Username cannot be empty", field="username")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL009" in result
        assert "Field: username" in result
        assert "testuser" in result.lower()
    
    def test_format_validation_error_password_invalid_char(self):
        """Test formatting password with invalid character error"""
        error = ValidationError("Password contains invalid character: '&'", field="password")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL002" in result
        assert "Field: password" in result
        assert "special characters" in result.lower()
    
    def test_format_validation_error_selector_empty(self):
        """Test formatting empty selector validation error"""
        error = ValidationError("Selector cannot be empty", field="selector")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL009" in result
        assert "Field: selector" in result
        assert "id=" in result or "css=" in result
    
    def test_format_validation_error_selector_invalid(self):
        """Test formatting invalid selector validation error"""
        error = ValidationError("Invalid selector format: invalid", field="selector")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL003" in result
        assert "Field: selector" in result
        assert "Example:" in result
        assert "xpath=" in result or "css=" in result
    
    def test_format_validation_error_template_type(self):
        """Test formatting invalid template type error"""
        error = ValidationError("Invalid template type: invalid", field="template_type")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL004" in result
        assert "Field: template_type" in result
    
    def test_format_validation_error_path_traversal(self):
        """Test formatting path traversal error"""
        error = ValidationError("Invalid file path: path traversal not allowed", field="path")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "SEC003" in result
        assert "Field: path" in result
        assert "relative path" in result.lower()
    
    def test_format_validation_error_http_method(self):
        """Test formatting invalid HTTP method error"""
        error = ValidationError("Invalid HTTP method: INVALID", field="method")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL007" in result
        assert "Field: method" in result
        assert "GET" in result or "POST" in result
    
    def test_format_validation_error_timeout(self):
        """Test formatting invalid timeout error"""
        error = ValidationError("Invalid timeout format: invalid", field="timeout")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL008" in result
        assert "Field: timeout" in result
        assert "10s" in result or "500ms" in result
    
    def test_format_validation_error_unknown_field(self):
        """Test formatting error with unknown field"""
        error = ValidationError("Some error", field="unknown_field")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL001" in result
        assert "Field: unknown_field" in result
        assert "Suggestion:" in result
    
    def test_format_validation_error_no_field(self):
        """Test formatting error without field"""
        error = ValidationError("Some error")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "Field: unknown" in result
    
    def test_format_unexpected_error(self):
        """Test formatting unexpected error"""
        error = ValueError("Something went wrong")
        result = ErrorFormatter.format_unexpected_error(error)
        
        assert "UNEXPECTED ERROR" in result
        assert "Error Type: ValueError" in result
        assert "Message: Something went wrong" in result
        assert "Suggestion:" in result
    
    def test_format_unexpected_error_different_types(self):
        """Test formatting different types of unexpected errors"""
        errors = [
            TypeError("Type error"),
            KeyError("Key error"),
            AttributeError("Attribute error"),
        ]
        
        for error in errors:
            result = ErrorFormatter.format_unexpected_error(error)
            assert "UNEXPECTED ERROR" in result
            assert type(error).__name__ in result
            assert str(error) in result
    
    def test_get_error_context_url_too_long(self):
        """Test getting error context for URL too long"""
        error = ValidationError("URL too long (max 2048 characters)", field="url")
        context = ErrorFormatter._get_error_context(error)
        
        assert context.error_code == "VAL010"
        assert context.field == "url"
        assert "2048" in context.suggestion
    
    def test_get_error_context_credentials_too_long(self):
        """Test getting error context for credentials too long"""
        error = ValidationError("Username too long (max 100 characters)", field="username")
        context = ErrorFormatter._get_error_context(error)
        
        assert context.error_code == "VAL010"
        assert context.field == "username"
        assert "100" in context.suggestion
    
    def test_format_validation_error_includes_all_sections(self):
        """Test that formatted error includes all expected sections"""
        error = ValidationError("URL cannot be empty", field="url")
        result = ErrorFormatter.format_validation_error(error)
        
        # Check for all expected sections
        assert "# VALIDATION ERROR" in result
        assert "## Field:" in result
        assert "## Issue:" in result
        assert "## Suggestion:" in result
        assert "## Example:" in result
    
    def test_format_validation_error_with_documentation_url(self):
        """Test formatting error that includes documentation URL"""
        error = ValidationError("URL cannot be empty", field="url")
        result = ErrorFormatter.format_validation_error(error)
        
        # URL empty errors should include documentation
        if "Documentation:" in result:
            assert "http" in result
    
    def test_error_formatter_is_class_method(self):
        """Test that ErrorFormatter methods are class methods"""
        import inspect
        
        # Check that format_validation_error is a classmethod
        assert isinstance(inspect.getattr_static(ErrorFormatter, 'format_validation_error'), classmethod)
        assert isinstance(inspect.getattr_static(ErrorFormatter, 'format_unexpected_error'), classmethod)
        assert isinstance(inspect.getattr_static(ErrorFormatter, '_get_error_context'), classmethod)
    
    def test_error_codes_follow_naming_convention(self):
        """Test that error codes follow the naming convention"""
        for code in ErrorFormatter.ERROR_CODES.keys():
            # Error codes should be 3 letters + 3 digits
            assert len(code) == 6
            assert code[:3].isalpha()
            assert code[3:].isdigit()
            # First 3 letters should be uppercase
            assert code[:3].isupper()
    
    def test_error_codes_categories(self):
        """Test that error codes are properly categorized"""
        val_codes = [code for code in ErrorFormatter.ERROR_CODES.keys() if code.startswith("VAL")]
        sec_codes = [code for code in ErrorFormatter.ERROR_CODES.keys() if code.startswith("SEC")]
        cfg_codes = [code for code in ErrorFormatter.ERROR_CODES.keys() if code.startswith("CFG")]
        
        # Should have codes in each category
        assert len(val_codes) > 0, "Should have validation error codes"
        assert len(sec_codes) > 0, "Should have security error codes"
        assert len(cfg_codes) > 0, "Should have configuration error codes"
    
    def test_format_validation_error_path_extension(self):
        """Test formatting path extension error"""
        error = ValidationError("Invalid file extension. Allowed: .robot, .py", field="path")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL006" in result
        assert "Field: path" in result
        assert "extension" in result.lower()
    
    def test_format_validation_error_selector_too_long(self):
        """Test formatting selector too long error"""
        error = ValidationError("Selector too long (max 500 characters)", field="selector")
        result = ErrorFormatter.format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "VAL010" in result
        assert "Field: selector" in result
        assert "500" in result
