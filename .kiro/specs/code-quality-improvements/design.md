# Code Quality Improvements - Design Document

## 1. Architecture Overview

This design document outlines the technical approach for improving code quality, security, testing, and maintainability of the Robot Framework MCP Server v2.0.

## 2. Design Principles

### 2.1 SOLID Principles
- **Single Responsibility**: Each class/function has one clear purpose
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Many specific interfaces over one general interface
- **Dependency Inversion**: Depend on abstractions, not concretions

### 2.2 DRY (Don't Repeat Yourself)
- Extract common patterns into reusable components
- Use decorators for cross-cutting concerns
- Create base classes for shared functionality

### 2.3 Security First
- Validate all inputs
- Sanitize all outputs
- Never trust user data
- Use parameterized queries
- Implement least privilege

## 3. Component Design

### 3.1 Error Handling Decorator

**Purpose**: Eliminate code duplication in error handling across all MCP tools

**Design**:
```python
from functools import wraps
from typing import Callable, Any
import time

def mcp_tool_handler(tool_name: str):
    """
    Decorator for MCP tool error handling and logging
    
    Handles:
    - Tool execution timing
    - Validation errors
    - Unexpected errors
    - Logging
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
```

**Usage**:
```python
@mcp.tool()
@mcp_tool_handler("create_login_test_case")
def create_login_test_case(url: str, username: str, password: str, ...) -> str:
    # Validation
    validated_url = InputValidator.validate_url(url)
    # ... rest of implementation
    return result
```

### 3.2 Enhanced Error Messages

**Purpose**: Provide actionable error messages with context and suggestions

**Design**:
```python
@dataclass
class ErrorContext:
    """Context information for errors"""
    error_code: str
    field: str
    message: str
    suggestion: str
    example: Optional[str] = None
    documentation_url: Optional[str] = None

class ErrorFormatter:
    """Format errors with helpful context"""
    
    ERROR_CODES = {
        "VAL001": "Invalid URL format",
        "VAL002": "Invalid credentials",
        "VAL003": "Invalid selector",
        "SEC001": "Potential SQL injection",
        "SEC002": "Potential command injection",
    }
    
    @classmethod
    def format_validation_error(cls, error: ValidationError) -> str:
        """Format validation error with context"""
        context = cls._get_error_context(error)
        
        output = f"# VALIDATION ERROR [{context.error_code}]\n\n"
        output += f"## Field: {context.field}\n"
        output += f"## Issue: {context.message}\n\n"
        output += f"## Suggestion:\n{context.suggestion}\n\n"
        
        if context.example:
            output += f"## Example:\n{context.example}\n\n"
        
        if context.documentation_url:
            output += f"## Documentation:\n{context.documentation_url}\n"
        
        return output
```

### 3.3 Template Base Class Refactoring

**Purpose**: Reduce code duplication in template classes

**Design**:
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTemplate(ABC):
    """Enhanced base template with common functionality"""
    
    # Common constants
    SECTION_SETTINGS = "*** Settings ***"
    SECTION_VARIABLES = "*** Variables ***"
    SECTION_TEST_CASES = "*** Test Cases ***"
    SECTION_KEYWORDS = "*** Keywords ***"
    
    def __init__(self):
        self._validate_template_config()
    
    @abstractmethod
    def generate(self, **kwargs) -> str:
        """Generate template content"""
        pass
    
    @abstractmethod
    def validate_inputs(self, **kwargs) -> None:
        """Validate template inputs"""
        pass
    
    def _get_header(self, title: str) -> str:
        """Generate standard header"""
        return f"""# {title}
# Generated by Robot Framework MCP Server v2.0
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    def _format_section(self, section_name: str, content: str) -> str:
        """Format a Robot Framework section"""
        return f"{section_name}\n{content}\n"
    
    def _sanitize_input(self, value: str, max_length: int = 1000) -> str:
        """Sanitize input value"""
        return InputValidator.sanitize_string(value, max_length)
```

### 3.4 Configuration Validation

**Purpose**: Ensure configuration files are valid before use

**Design**:
```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ConfigValidationResult:
    """Result of configuration validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ConfigValidator:
    """Validate configuration files"""
    
    @classmethod
    def validate_config(cls, config: ServerConfig) -> ConfigValidationResult:
        """Validate server configuration"""
        errors = []
        warnings = []
        
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config.log_level not in valid_levels:
            errors.append(f"Invalid log_level: {config.log_level}")
        
        # Validate timeouts
        if not cls._is_valid_timeout(config.timeouts.implicit_wait):
            errors.append(f"Invalid implicit_wait: {config.timeouts.implicit_wait}")
        
        # Validate performance thresholds
        if config.performance.page_load_ms < 0:
            errors.append("page_load_ms must be positive")
        
        # Validate retry config
        if config.retry.max_retries < 0:
            errors.append("max_retries must be non-negative")
        
        # Warnings for suboptimal settings
        if config.performance.page_load_ms > 10000:
            warnings.append("page_load_ms is very high (>10s)")
        
        return ConfigValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    @staticmethod
    def _is_valid_timeout(timeout: str) -> bool:
        """Check if timeout format is valid"""
        import re
        return bool(re.match(r'^\d+(ms|s|m|h)?$', timeout))
```

### 3.5 Caching Layer

**Purpose**: Improve performance by caching frequently accessed data

**Design**:
```python
from functools import lru_cache
import re

class CachedValidator:
    """Validator with caching for performance"""
    
    # Cache compiled regex patterns
    _pattern_cache: Dict[str, re.Pattern] = {}
    
    @classmethod
    @lru_cache(maxsize=128)
    def get_selector_config(cls, template_type: str) -> Dict[str, str]:
        """Get selector config with caching"""
        return SELECTOR_CONFIGS.get(template_type, SELECTOR_CONFIGS["generic"])
    
    @classmethod
    def get_compiled_pattern(cls, pattern: str) -> re.Pattern:
        """Get compiled regex pattern with caching"""
        if pattern not in cls._pattern_cache:
            cls._pattern_cache[pattern] = re.compile(pattern)
        return cls._pattern_cache[pattern]
```

### 3.6 Test Infrastructure

**Purpose**: Comprehensive test coverage with reusable fixtures

**Design**:
```python
# tests/conftest.py
import pytest
from src.validators import InputValidator
from src.config import ServerConfig

@pytest.fixture
def valid_url():
    """Fixture for valid URL"""
    return "https://example.com"

@pytest.fixture
def valid_credentials():
    """Fixture for valid credentials"""
    return ("testuser", "testpass123")

@pytest.fixture
def sample_robot_code():
    """Fixture for sample Robot Framework code"""
    return """*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Test Example
    Log    Hello World
"""

@pytest.fixture
def server_config():
    """Fixture for server configuration"""
    return ServerConfig()

@pytest.fixture
def mock_logger(mocker):
    """Fixture for mocked logger"""
    return mocker.patch('src.logger.get_logger')
```

### 3.7 Integration Test Framework

**Purpose**: Test end-to-end workflows

**Design**:
```python
# tests/integration/test_workflows.py
import pytest
from src.server import mcp

class TestLoginWorkflow:
    """Integration tests for login workflow"""
    
    def test_complete_login_test_generation(self):
        """Test complete login test generation workflow"""
        # Generate test case
        result = mcp.call_tool(
            "create_login_test_case",
            url="https://example.com/login",
            username="testuser",
            password="testpass",
            template_type="generic"
        )
        
        # Verify structure
        assert "*** Settings ***" in result
        assert "*** Test Cases ***" in result
        assert "*** Keywords ***" in result
        
        # Validate generated code
        validation = mcp.call_tool(
            "validate_robot_framework_syntax",
            robot_code=result
        )
        
        assert "VALIDATION PASSED" in validation
```

### 3.8 CI/CD Pipeline

**Purpose**: Automate quality checks and testing

**Design**:
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          black --check src tests
          mypy src
      
      - name: Run security scan
        run: bandit -r src
      
      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

## 4. Data Models

### 4.1 Error Code Registry
```python
class ErrorCode(Enum):
    """Registry of error codes"""
    # Validation errors (VAL)
    VAL_EMPTY_INPUT = "VAL001"
    VAL_INVALID_URL = "VAL002"
    VAL_INVALID_CREDENTIALS = "VAL003"
    VAL_INVALID_SELECTOR = "VAL004"
    VAL_INVALID_TEMPLATE = "VAL005"
    
    # Security errors (SEC)
    SEC_SQL_INJECTION = "SEC001"
    SEC_COMMAND_INJECTION = "SEC002"
    SEC_PATH_TRAVERSAL = "SEC003"
    SEC_XSS = "SEC004"
    
    # Configuration errors (CFG)
    CFG_INVALID_FORMAT = "CFG001"
    CFG_MISSING_REQUIRED = "CFG002"
    CFG_INVALID_VALUE = "CFG003"
```

### 4.2 Validation Result Enhancement
```python
@dataclass
class EnhancedValidationResult:
    """Enhanced validation result with more context"""
    is_valid: bool
    value: Any
    errors: List[ErrorContext]
    warnings: List[ErrorContext]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "is_valid": self.is_valid,
            "value": self.value,
            "errors": [asdict(e) for e in self.errors],
            "warnings": [asdict(w) for w in self.warnings],
            "metadata": self.metadata
        }
```

## 5. Security Considerations

### 5.1 Input Validation Strategy
- **Whitelist approach**: Only allow known-good inputs
- **Length limits**: Enforce maximum lengths for all inputs
- **Type checking**: Validate data types before processing
- **Regex validation**: Use strict patterns for format validation
- **Sanitization**: Remove or escape dangerous characters

### 5.2 SQL Injection Prevention
- **Parameterized queries**: Always use parameterized queries
- **ORM usage**: Prefer ORM over raw SQL
- **Input validation**: Validate all SQL inputs
- **Least privilege**: Use minimal database permissions

### 5.3 Command Injection Prevention
- **Whitelist commands**: Only allow predefined commands
- **No shell execution**: Avoid shell=True in subprocess
- **Input validation**: Validate all command inputs
- **Escaping**: Properly escape command arguments

## 6. Performance Optimization

### 6.1 String Operations
- Use list comprehension + join instead of concatenation
- Pre-allocate string buffers for large outputs
- Use f-strings for formatting

### 6.2 Caching Strategy
- Cache compiled regex patterns
- Cache selector configurations
- Cache validation results for identical inputs
- Use LRU cache for frequently accessed data

### 6.3 Lazy Loading
- Load templates on demand
- Defer expensive operations until needed
- Use generators for large datasets

## 7. Testing Strategy

### 7.1 Unit Tests
- Test each function in isolation
- Mock external dependencies
- Cover all code paths
- Test edge cases and boundary conditions

### 7.2 Integration Tests
- Test component interactions
- Test end-to-end workflows
- Test error propagation
- Test configuration loading

### 7.3 Property-Based Tests
- Test validation logic with random inputs
- Test invariants across all inputs
- Test error handling with invalid inputs

### 7.4 Performance Tests
- Benchmark template generation
- Benchmark validation operations
- Test memory usage
- Test concurrent operations

## 8. Migration Strategy

### 8.1 Phase 1: Critical Fixes (Completed ✅)
- Fix syntax errors
- Add input validation
- Document security issues

### 8.2 Phase 2: Code Quality (Week 1-2)
- Implement error handling decorator
- Refactor template base class
- Add enhanced error messages
- Reduce code duplication

### 8.3 Phase 3: Testing (Week 2-3)
- Add comprehensive unit tests
- Add integration tests
- Add property-based tests
- Achieve 80% coverage

### 8.4 Phase 4: Infrastructure (Week 3-4)
- Set up CI/CD pipeline
- Add pre-commit hooks
- Add code quality checks
- Add security scanning

### 8.5 Phase 5: Documentation (Week 4-6)
- Update API documentation
- Add usage examples
- Create architecture docs
- Update contributing guide

## 9. Correctness Properties

### 9.1 Validation Properties
**Property 1.1**: All valid inputs must pass validation
**Property 1.2**: All invalid inputs must fail validation
**Property 1.3**: Validation must be idempotent
**Property 1.4**: Validation errors must include field name

### 9.2 Template Generation Properties
**Property 2.1**: Generated code must be valid Robot Framework syntax
**Property 2.2**: Generated code must include all required sections
**Property 2.3**: Generated code must be deterministic for same inputs
**Property 2.4**: Generated code must not contain user input without sanitization

### 9.3 Error Handling Properties
**Property 3.1**: All errors must be caught and handled
**Property 3.2**: Error messages must include context
**Property 3.3**: Errors must not expose sensitive information
**Property 3.4**: Errors must be logged appropriately

## 10. Monitoring and Observability

### 10.1 Metrics to Track
- Tool execution time
- Validation success/failure rate
- Error frequency by type
- Template generation time
- Memory usage

### 10.2 Logging Strategy
- Log all tool invocations
- Log all validation failures
- Log all errors with stack traces
- Log performance metrics
- Use structured logging

## 11. Backward Compatibility

### 11.1 API Compatibility
- Maintain existing function signatures
- Add new parameters as optional
- Deprecate old features gracefully
- Provide migration guides

### 11.2 Configuration Compatibility
- Support old configuration format
- Provide automatic migration
- Warn about deprecated options
- Document breaking changes

## 12. Future Enhancements

### 12.1 Planned Features
- Plugin system for custom templates
- Template marketplace
- Visual template editor
- AI-powered test generation

### 12.2 Technical Debt
- Refactor legacy code
- Improve type hints
- Add more comprehensive docs
- Optimize performance further
