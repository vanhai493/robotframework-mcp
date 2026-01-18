"""
Comprehensive tests for timing and logging functionality in decorators
Task 2.1.2: Add timing and logging functionality
"""

import pytest
import time
from unittest.mock import Mock, patch, call
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.decorators import mcp_tool_handler
from src.validators import ValidationError


class TestTimingFunctionality:
    """Tests for timing measurement in decorator"""
    
    @patch('src.decorators.logger')
    def test_timing_for_fast_function(self, mock_logger):
        """Test timing measurement for fast-executing function"""
        @mcp_tool_handler("fast_tool")
        def fast_function() -> str:
            return "Quick result"
        
        result = fast_function()
        
        assert result == "Quick result"
        
        # Verify timing was measured and logged
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][0] == "fast_tool"
        assert call_args[0][1] is True  # success
        duration_ms = call_args[0][2]
        assert duration_ms is not None
        assert duration_ms >= 0
        assert duration_ms < 1000  # Should be very fast
    
    @patch('src.decorators.logger')
    def test_timing_for_slow_function(self, mock_logger):
        """Test timing measurement for slow-executing function"""
        @mcp_tool_handler("slow_tool")
        def slow_function() -> str:
            time.sleep(0.1)  # Sleep for 100ms
            return "Slow result"
        
        result = slow_function()
        
        assert result == "Slow result"
        
        # Verify timing captured the delay
        call_args = mock_logger.log_tool_result.call_args
        duration_ms = call_args[0][2]
        assert duration_ms >= 100  # Should be at least 100ms
        assert duration_ms < 200  # But not too much more
    
    @patch('src.decorators.logger')
    def test_timing_on_validation_error(self, mock_logger):
        """Test timing is measured even when validation fails"""
        @mcp_tool_handler("validation_tool")
        def failing_function() -> str:
            time.sleep(0.05)  # Sleep for 50ms
            raise ValidationError("Invalid input", field="test")
        
        result = failing_function()
        
        assert "VALIDATION ERROR" in result
        
        # Verify timing was still measured
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # failure
        duration_ms = call_args[0][2]
        assert duration_ms >= 50  # Should include the sleep time
    
    @patch('src.decorators.logger')
    def test_timing_on_unexpected_error(self, mock_logger):
        """Test timing is measured even on unexpected errors"""
        @mcp_tool_handler("error_tool")
        def error_function() -> str:
            time.sleep(0.05)  # Sleep for 50ms
            raise RuntimeError("Unexpected error")
        
        result = error_function()
        
        assert "UNEXPECTED ERROR" in result
        
        # Verify timing was still measured
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # failure
        duration_ms = call_args[0][2]
        assert duration_ms >= 50  # Should include the sleep time
    
    @patch('src.decorators.logger')
    @patch('src.decorators.time')
    def test_timing_calculation_accuracy(self, mock_time, mock_logger):
        """Test timing calculation is accurate"""
        # Mock time.time() to return specific values
        mock_time.time.side_effect = [1000.0, 1000.5]  # 500ms difference
        
        @mcp_tool_handler("test_tool")
        def test_function() -> str:
            return "Success"
        
        test_function()
        
        # Verify duration calculation
        call_args = mock_logger.log_tool_result.call_args
        duration_ms = call_args[0][2]
        assert duration_ms == 500.0  # Exactly 500ms


class TestLoggingFunctionality:
    """Tests for logging functionality in decorator"""
    
    @patch('src.decorators.logger')
    def test_logs_tool_call_with_no_params(self, mock_logger):
        """Test logging tool call with no parameters"""
        @mcp_tool_handler("simple_tool")
        def simple_function() -> str:
            return "Success"
        
        simple_function()
        
        # Verify tool call was logged
        mock_logger.log_tool_call.assert_called_once_with("simple_tool")
    
    @patch('src.decorators.logger')
    def test_logs_tool_call_with_positional_args(self, mock_logger):
        """Test logging tool call with positional arguments"""
        @mcp_tool_handler("args_tool")
        def args_function(arg1: str, arg2: int) -> str:
            return f"{arg1}-{arg2}"
        
        args_function("test", 42)
        
        # Verify tool call was logged with args
        mock_logger.log_tool_call.assert_called_once_with("args_tool")
    
    @patch('src.decorators.logger')
    def test_logs_tool_call_with_kwargs(self, mock_logger):
        """Test logging tool call with keyword arguments"""
        @mcp_tool_handler("kwargs_tool")
        def kwargs_function(url: str, timeout: int = 30) -> str:
            return f"{url}-{timeout}"
        
        kwargs_function(url="https://example.com", timeout=60)
        
        # Verify tool call was logged with kwargs
        mock_logger.log_tool_call.assert_called_once_with(
            "kwargs_tool",
            url="https://example.com",
            timeout=60
        )
    
    @patch('src.decorators.logger')
    def test_logs_tool_call_with_mixed_args(self, mock_logger):
        """Test logging tool call with mixed positional and keyword arguments"""
        @mcp_tool_handler("mixed_tool")
        def mixed_function(arg1: str, arg2: int, kwarg1: str = "default") -> str:
            return f"{arg1}-{arg2}-{kwarg1}"
        
        mixed_function("test", 42, kwarg1="custom")
        
        # Verify tool call was logged
        mock_logger.log_tool_call.assert_called_once()
        call_args = mock_logger.log_tool_call.call_args
        assert call_args[0][0] == "mixed_tool"
    
    @patch('src.decorators.logger')
    def test_logs_successful_result(self, mock_logger):
        """Test logging successful tool result"""
        @mcp_tool_handler("success_tool")
        def success_function() -> str:
            return "Success"
        
        success_function()
        
        # Verify result was logged as success
        mock_logger.log_tool_result.assert_called_once()
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][0] == "success_tool"
        assert call_args[0][1] is True  # success=True
        assert call_args[0][2] >= 0  # duration_ms >= 0
    
    @patch('src.decorators.logger')
    def test_logs_validation_error_details(self, mock_logger):
        """Test logging validation error details"""
        @mcp_tool_handler("validation_tool")
        def validation_function() -> str:
            raise ValidationError("Invalid URL format", field="url")
        
        validation_function()
        
        # Verify validation error was logged
        mock_logger.log_validation_error.assert_called_once_with(
            "url",
            "Invalid URL format"
        )
        
        # Verify result was logged as failure
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # success=False
    
    @patch('src.decorators.logger')
    def test_logs_unexpected_error_with_exception(self, mock_logger):
        """Test logging unexpected error with exception details"""
        @mcp_tool_handler("error_tool")
        def error_function() -> str:
            raise ValueError("Something went wrong")
        
        error_function()
        
        # Verify exception was logged
        mock_logger.exception.assert_called_once()
        call_args = mock_logger.exception.call_args
        assert "error_tool" in call_args[0][0]
        assert "Something went wrong" in call_args[0][0]
        
        # Verify result was logged as failure
        result_call_args = mock_logger.log_tool_result.call_args
        assert result_call_args[0][1] is False  # success=False
    
    @patch('src.decorators.logger')
    def test_logs_all_phases_of_execution(self, mock_logger):
        """Test that all phases of execution are logged"""
        @mcp_tool_handler("complete_tool")
        def complete_function(param: str) -> str:
            return f"Result: {param}"
        
        complete_function(param="test")
        
        # Verify all logging calls were made in order
        assert mock_logger.log_tool_call.call_count == 1
        assert mock_logger.log_tool_result.call_count == 1
        
        # Verify order: call -> result
        call_names = [call[0] for call in mock_logger.method_calls]
        assert 'log_tool_call' in call_names
        assert 'log_tool_result' in call_names
        
        # log_tool_call should come before log_tool_result
        call_index = call_names.index('log_tool_call')
        result_index = call_names.index('log_tool_result')
        assert call_index < result_index


class TestTimingAndLoggingIntegration:
    """Integration tests for timing and logging working together"""
    
    @patch('src.decorators.logger')
    def test_timing_and_logging_for_complete_workflow(self, mock_logger):
        """Test timing and logging work together for complete workflow"""
        @mcp_tool_handler("workflow_tool")
        def workflow_function(step: str) -> str:
            time.sleep(0.05)  # Simulate work
            return f"Completed: {step}"
        
        result = workflow_function(step="validation")
        
        assert result == "Completed: validation"
        
        # Verify logging
        mock_logger.log_tool_call.assert_called_once_with(
            "workflow_tool",
            step="validation"
        )
        
        # Verify timing
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][0] == "workflow_tool"
        assert call_args[0][1] is True
        duration_ms = call_args[0][2]
        assert duration_ms >= 50  # At least 50ms due to sleep
    
    @patch('src.decorators.logger')
    def test_timing_and_logging_preserved_on_error(self, mock_logger):
        """Test timing and logging are preserved even on errors"""
        @mcp_tool_handler("error_workflow_tool")
        def error_workflow_function(step: str) -> str:
            time.sleep(0.05)  # Simulate work before error
            raise ValidationError("Step failed", field=step)
        
        result = error_workflow_function(step="authentication")
        
        assert "VALIDATION ERROR" in result
        
        # Verify logging
        mock_logger.log_tool_call.assert_called_once()
        mock_logger.log_validation_error.assert_called_once_with(
            "authentication",
            "Step failed"
        )
        
        # Verify timing
        call_args = mock_logger.log_tool_result.call_args
        assert call_args[0][1] is False  # failure
        duration_ms = call_args[0][2]
        assert duration_ms >= 50  # At least 50ms due to sleep


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
