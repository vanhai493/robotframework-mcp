# MCP Tool Handler Decorator Usage Guide

## Overview

The `mcp_tool_handler` decorator provides centralized error handling, logging, and timing for MCP tools. It eliminates code duplication and ensures consistent error handling across all tools.

## Features

- **Automatic Timing**: Measures and logs execution time for each tool call
- **Error Handling**: Catches and formats both validation errors and unexpected errors
- **Structured Logging**: Logs tool calls, results, and errors in a consistent format
- **User-Friendly Error Messages**: Provides helpful error messages with context and suggestions

## Basic Usage

```python
from src.decorators import mcp_tool_handler
from src.validators import InputValidator

@mcp.tool()
@mcp_tool_handler("create_login_test_case")
def create_login_test_case(url: str, username: str, password: str) -> str:
    """Generate Robot Framework test case for login functionality"""
    # Validation
    validated_url = InputValidator.validate_url(url)
    validated_username, validated_password = InputValidator.validate_credentials(
        username, password
    )
    
    # Implementation
    result = generate_test_code(validated_url, validated_username, validated_password)
    return result
```

## How It Works

### 1. Successful Execution

When a tool executes successfully:
- Logs the tool call with parameters
- Executes the function
- Measures execution time
- Logs success with duration
- Returns the result

```python
# Example output in logs:
# Tool called: create_login_test_case(url='https://example.com', username='user', password='***')
# Tool result: create_login_test_case - SUCCESS (45.23ms)
```

### 2. Validation Errors

When a `ValidationError` is raised:
- Catches the error
- Logs the validation error with field information
- Formats a user-friendly error message
- Returns formatted error instead of raising exception

```python
# Example error output:
# VALIDATION ERROR
#
# Field: url
# Issue: URL cannot be empty
#
# Suggestion:
# Please correct the input and try again.
```

### 3. Unexpected Errors

When any other exception occurs:
- Catches the exception
- Logs the full exception with traceback
- Formats a user-friendly error message
- Returns formatted error instead of raising exception

```python
# Example error output:
# UNEXPECTED ERROR
#
# Error Type: ValueError
# Message: Invalid template configuration
#
# Suggestion:
# This is an unexpected error. Please contact support or check the logs for more details.
```

## Benefits

### Before (Without Decorator)

```python
@mcp.tool()
def create_login_test_case(url: str, username: str, password: str) -> str:
    start_time = time.time()
    logger.log_tool_call("create_login_test_case", url=url, username=username)
    
    try:
        validated_url = InputValidator.validate_url(url)
        validated_username, validated_password = InputValidator.validate_credentials(
            username, password
        )
        
        result = generate_test_code(validated_url, validated_username, validated_password)
        
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_result("create_login_test_case", True, duration_ms)
        return result
        
    except ValidationError as e:
        logger.log_validation_error(e.field or "unknown", e.message)
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_result("create_login_test_case", False, duration_ms)
        return f"# VALIDATION ERROR: {e.message}\n# Please correct the input and try again."
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        duration_ms = (time.time() - start_time) * 1000
        logger.log_tool_result("create_login_test_case", False, duration_ms)
        return f"# ERROR: {str(e)}"
```

### After (With Decorator)

```python
@mcp.tool()
@mcp_tool_handler("create_login_test_case")
def create_login_test_case(url: str, username: str, password: str) -> str:
    validated_url = InputValidator.validate_url(url)
    validated_username, validated_password = InputValidator.validate_credentials(
        username, password
    )
    
    result = generate_test_code(validated_url, validated_username, validated_password)
    return result
```

**Result**: ~15 lines of boilerplate code eliminated per tool!

## Best Practices

### 1. Always Use with MCP Tools

Apply the decorator to all MCP tool functions:

```python
@mcp.tool()
@mcp_tool_handler("tool_name")
def tool_function(...) -> str:
    # Implementation
    pass
```

### 2. Use Descriptive Tool Names

The tool name should match the function name for clarity:

```python
@mcp_tool_handler("create_api_test")  # Good
def create_api_test(...) -> str:
    pass

@mcp_tool_handler("tool1")  # Bad - not descriptive
def create_api_test(...) -> str:
    pass
```

### 3. Validate Early

Perform all validation at the start of the function:

```python
@mcp_tool_handler("create_test")
def create_test(url: str, method: str) -> str:
    # Validate all inputs first
    validated_url = InputValidator.validate_url(url)
    validated_method = InputValidator.validate_http_method(method)
    
    # Then proceed with implementation
    result = generate_test(validated_url, validated_method)
    return result
```

### 4. Let Exceptions Bubble Up

Don't catch exceptions inside decorated functions - let the decorator handle them:

```python
# Good
@mcp_tool_handler("create_test")
def create_test(url: str) -> str:
    validated_url = InputValidator.validate_url(url)  # May raise ValidationError
    return generate_test(validated_url)

# Bad - unnecessary try/except
@mcp_tool_handler("create_test")
def create_test(url: str) -> str:
    try:
        validated_url = InputValidator.validate_url(url)
        return generate_test(validated_url)
    except ValidationError as e:
        # Decorator already handles this!
        return f"Error: {e}"
```

## Testing

The decorator is fully tested with comprehensive unit and integration tests:

- `tests/test_decorators.py` - Unit tests for decorator functionality
- `tests/test_decorator_integration.py` - Integration tests with validators

Run tests with:
```bash
python -m pytest tests/test_decorators.py -v
python -m pytest tests/test_decorator_integration.py -v
```

## Implementation Details

The decorator:
1. Uses `functools.wraps` to preserve function metadata
2. Measures execution time using `time.time()`
3. Logs using the centralized `MCPLogger` instance
4. Formats errors using helper functions
5. Always returns a string (never raises exceptions)

## Related Documentation

- [Validators Documentation](validators.md)
- [Logger Documentation](logger.md)
- [Error Handling Guide](error_handling.md)
