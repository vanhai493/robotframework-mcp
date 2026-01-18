"""
Unit tests for decorators module
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.decorators import mcp_tool_handler, format_validation_error, format_unexpected_error
from src.validators import ValidationError


class TestMCPToolHandler:
    """Tests for mcp_tool_handler decorator"""
    
    @patch('src.decorators.logger')
    def test_successful_execution(self, mock_logger):
        """Test decorator with successful function execution"""
        @mcp_tool_handler("test_tool")
        def test_function(value: str) -> str:
            return f"Success: {value}"
        
        result = test_function("test")
        
        assert result == "Success: test"
        mock_logger.log_tool_call.assert_called_once()
        mock_logger.log_tool_result.assert_called_once()
        # Verify success was logged
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][0] == "test_tool"
        assert call_args[0][1] is True  # success=True
    
    @patch('src.decorators.logger')
    def test_validation_error_handling(self, mock_logger):
        """Test decorator handles ValidationError correctly"""
        @mcp_tool_handler("test_tool")
        def test_function(value: str) -> str:
            raise ValidationError("Invalid input", field="value")
        
        result = test_function("test")
        
        assert "VALIDATION ERROR" in result
        assert "Invalid input" in result
        mock_logger.log_validation_error.assert_called_once_with("value", "Invalid input")
        mock_logger.log_tool_result.assert_called_once()
        # Verify failure was logged
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # success=False
    
    @patch('src.decorators.logger')
    def test_unexpected_error_handling(self, mock_logger):
        """Test decorator handles unexpected errors correctly"""
        @mcp_tool_handler("test_tool")
        def test_function(value: str) -> str:
            raise ValueError("Unexpected error")
        
        result = test_function("test")
        
        assert "UNEXPECTED ERROR" in result
        assert "ValueError" in result
        assert "Unexpected error" in result
        mock_logger.exception.assert_called_once()
        mock_logger.log_tool_result.assert_called_once()
        # Verify failure was logged
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # success=False
    
    @patch('src.decorators.logger')
    def test_timing_measurement(self, mock_logger):
        """Test decorator measures execution time"""
        @mcp_tool_handler("test_tool")
        def test_function() -> str:
            return "Success"
        
        test_function()
        
        # Verify duration_ms was passed to log_tool_result
        call_args = mock_logger.log_tool_result.call_args
        assert len(call_args[0]) >= 2
        duration_ms = call_args[0][2] if len(call_args[0]) > 2 else call_args[1].get('duration_ms')
        assert duration_ms is not None
        assert duration_ms >= 0
    
    @patch('src.decorators.logger')
    def test_kwargs_logged(self, mock_logger):
        """Test decorator logs function kwargs"""
        @mcp_tool_handler("test_tool")
        def test_function(arg1: str, arg2: int) -> str:
            return "Success"
        
        test_function(arg1="value1", arg2=42)
        
        # Verify kwargs were logged
        mock_logger.log_tool_call.assert_called_once_with(
            "test_tool", arg1="value1", arg2=42
        )
    
    @patch('src.decorators.logger')
    def test_validation_error_without_field(self, mock_logger):
        """Test decorator handles ValidationError without field"""
        @mcp_tool_handler("test_tool")
        def test_function() -> str:
            raise ValidationError("Error without field")
        
        result = test_function()
        
        assert "VALIDATION ERROR" in result
        mock_logger.log_validation_error.assert_called_once_with("unknown", "Error without field")
    
    def test_preserves_function_metadata(self):
        """Test decorator preserves function metadata"""
        @mcp_tool_handler("test_tool")
        def test_function() -> str:
            """Test docstring"""
            return "Success"
        
        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Test docstring"


class TestFormatValidationError:
    """Tests for format_validation_error function"""
    
    def test_format_with_field(self):
        """Test formatting validation error with field"""
        error = ValidationError("Invalid URL format", field="url")
        result = format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "Field: url" in result
        assert "Invalid URL format" in result
        assert "Suggestion:" in result
    
    def test_format_without_field(self):
        """Test formatting validation error without field"""
        error = ValidationError("Invalid input")
        result = format_validation_error(error)
        
        assert "VALIDATION ERROR" in result
        assert "Invalid input" in result
        assert "Field:" not in result
    
    def test_format_includes_suggestion(self):
        """Test formatted error includes suggestion"""
        error = ValidationError("Test error", field="test")
        result = format_validation_error(error)
        
        assert "Suggestion:" in result
        assert "correct the input" in result.lower()


class TestFormatUnexpectedError:
    """Tests for format_unexpected_error function"""
    
    def test_format_value_error(self):
        """Test formatting ValueError"""
        error = ValueError("Test error message")
        result = format_unexpected_error(error)
        
        assert "UNEXPECTED ERROR" in result
        assert "Error Type: ValueError" in result
        assert "Test error message" in result
        assert "Suggestion:" in result
    
    def test_format_type_error(self):
        """Test formatting TypeError"""
        error = TypeError("Type mismatch")
        result = format_unexpected_error(error)
        
        assert "UNEXPECTED ERROR" in result
        assert "Error Type: TypeError" in result
        assert "Type mismatch" in result
    
    def test_format_includes_support_message(self):
        """Test formatted error includes support message"""
        error = Exception("Generic error")
        result = format_unexpected_error(error)
        
        assert "contact support" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
