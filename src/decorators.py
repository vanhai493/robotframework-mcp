"""
Error handling decorators for Robot Framework MCP Server
"""

from functools import wraps
from typing import Callable, Any
import time

from .validators import ValidationError
from .logger import get_logger


logger = get_logger()


def mcp_tool_handler(tool_name: str):
    """
    Decorator for MCP tool error handling and logging
    
    Handles:
    - Tool execution timing
    - Validation errors
    - Unexpected errors
    - Logging
    
    Args:
        tool_name: Name of the tool being decorated
        
    Returns:
        Decorated function with error handling and logging
        
    Example:
        @mcp.tool()
        @mcp_tool_handler("create_login_test_case")
        def create_login_test_case(url: str, username: str, password: str, ...) -> str:
            # Validation
            validated_url = InputValidator.validate_url(url)
            # ... rest of implementation
            return result
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            start_time = time.time()
            logger.log_tool_call(tool_name, **kwargs)
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.log_tool_result(tool_name, True, duration_ms)
                return result
                
            except ValidationError as e:
                logger.log_validation_error(e.field or "unknown", e.message)
                duration_ms = (time.time() - start_time) * 1000
                logger.log_tool_result(tool_name, False, duration_ms)
                return format_validation_error(e)
                
            except Exception as e:
                logger.exception(f"Unexpected error in {tool_name}: {e}")
                duration_ms = (time.time() - start_time) * 1000
                logger.log_tool_result(tool_name, False, duration_ms)
                return format_unexpected_error(e)
        
        return wrapper
    return decorator


def format_validation_error(error: ValidationError) -> str:
    """
    Format validation error with helpful context
    
    Args:
        error: ValidationError instance
        
    Returns:
        Formatted error message
    """
    output = "# VALIDATION ERROR\n\n"
    
    if error.field:
        output += f"## Field: {error.field}\n"
    
    output += f"## Issue: {error.message}\n\n"
    output += "## Suggestion:\n"
    output += "Please correct the input and try again.\n"
    
    return output


def format_unexpected_error(error: Exception) -> str:
    """
    Format unexpected error with helpful context
    
    Args:
        error: Exception instance
        
    Returns:
        Formatted error message
    """
    output = "# UNEXPECTED ERROR\n\n"
    output += f"## Error Type: {type(error).__name__}\n"
    output += f"## Message: {str(error)}\n\n"
    output += "## Suggestion:\n"
    output += "This is an unexpected error. Please contact support or check the logs for more details.\n"
    
    return output
