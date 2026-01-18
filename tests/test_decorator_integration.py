"""
Integration tests for decorator usage
"""

import pytest
import sys
import os
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.decorators import mcp_tool_handler
from src.validators import InputValidator, ValidationError


class TestDecoratorIntegration:
    """Integration tests for decorator with validators"""
    
    @patch('src.decorators.logger')
    def test_decorator_with_url_validation(self, mock_logger):
        """Test decorator with URL validation"""
        @mcp_tool_handler("test_url_tool")
        def validate_url_tool(url: str) -> str:
            validated_url = InputValidator.validate_url(url)
            return f"Valid URL: {validated_url}"
        
        # Test with valid URL
        result = validate_url_tool("https://example.com")
        assert "Valid URL: https://example.com" in result
        
        # Test with invalid URL
        result = validate_url_tool("")
        assert "VALIDATION ERROR" in result
        assert "cannot be empty" in result
    
    @patch('src.decorators.logger')
    def test_decorator_with_credentials_validation(self, mock_logger):
        """Test decorator with credentials validation"""
        @mcp_tool_handler("test_credentials_tool")
        def validate_credentials_tool(username: str, password: str) -> str:
            validated_username, validated_password = InputValidator.validate_credentials(
                username, password
            )
            return f"Valid credentials: {validated_username}"
        
        # Test with valid credentials
        result = validate_credentials_tool("user", "pass123")
        assert "Valid credentials: user" in result
        
        # Test with invalid credentials
        result = validate_credentials_tool("", "pass")
        assert "VALIDATION ERROR" in result
        assert "Username" in result
    
    @patch('src.decorators.logger')
    def test_decorator_with_multiple_validations(self, mock_logger):
        """Test decorator with multiple validation steps"""
        @mcp_tool_handler("test_multi_validation_tool")
        def multi_validation_tool(url: str, username: str, password: str) -> str:
            validated_url = InputValidator.validate_url(url)
            validated_username, validated_password = InputValidator.validate_credentials(
                username, password
            )
            return f"All valid: {validated_url}, {validated_username}"
        
        # Test with all valid inputs
        result = multi_validation_tool("https://example.com", "user", "pass")
        assert "All valid" in result
        
        # Test with invalid URL (should fail on first validation)
        result = multi_validation_tool("", "user", "pass")
        assert "VALIDATION ERROR" in result
        assert "url" in result.lower()
    
    @patch('src.decorators.logger')
    def test_decorator_preserves_validation_error_field(self, mock_logger):
        """Test decorator preserves field information from ValidationError"""
        @mcp_tool_handler("test_field_tool")
        def field_validation_tool(selector: str) -> str:
            validated_selector = InputValidator.validate_selector(selector)
            return f"Valid selector: {validated_selector}"
        
        # Test with empty selector
        result = field_validation_tool("")
        assert "VALIDATION ERROR" in result
        assert "Field: selector" in result
    
    @patch('src.decorators.logger')
    def test_decorator_with_runtime_error(self, mock_logger):
        """Test decorator handles runtime errors during validation"""
        @mcp_tool_handler("test_runtime_error_tool")
        def runtime_error_tool(value: str) -> str:
            # Simulate a runtime error
            if value == "trigger_error":
                raise RuntimeError("Simulated runtime error")
            return f"Success: {value}"
        
        # Test normal execution
        result = runtime_error_tool("normal")
        assert "Success: normal" in result
        
        # Test with runtime error
        result = runtime_error_tool("trigger_error")
        assert "UNEXPECTED ERROR" in result
        assert "RuntimeError" in result
        assert "Simulated runtime error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
