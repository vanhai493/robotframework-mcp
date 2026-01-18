# Contributing to Robot Framework MCP Server

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 **Report Bugs** - Help us identify and fix issues
- ✨ **Suggest Features** - Share ideas for new functionality
- 📝 **Improve Documentation** - Help others understand the project
- 🧪 **Write Tests** - Increase code coverage and reliability
- 💻 **Submit Code** - Fix bugs or implement features
- 🎨 **Add Templates** - Create new selector templates or test types
- 🌍 **Translate** - Help make the project accessible to more users

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/robotframework-MCP.git
cd robotframework-MCP
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 💻 Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validators.py -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Manual Testing

```bash
# Test template generation
python -c "
from src.templates.login import LoginTestTemplate
template = LoginTestTemplate()
result = template.generate(
    url='https://example.com',
    username='test',
    password='pass'
)
print(result)
"

# Test validators
python -c "
from src.validators import InputValidator
print(InputValidator.validate_url('https://example.com'))
"

# Test server (requires mcp package)
python mcp_server.py
```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line Length**: 100 characters
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized with `isort`

### Code Structure

```python
"""
Module docstring explaining purpose
"""

import standard_library
import third_party
from local_module import something

# Constants
CONSTANT_NAME = "value"

# Classes
class MyClass:
    """Class docstring"""
    
    def __init__(self):
        """Constructor docstring"""
        pass
    
    def method(self, param: str) -> str:
        """
        Method docstring
        
        Args:
            param: Parameter description
            
        Returns:
            Return value description
        """
        return param

# Functions
def my_function(param: str) -> str:
    """
    Function docstring
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    return param
```

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional

def process_data(
    data: List[str],
    config: Dict[str, any],
    optional_param: Optional[str] = None
) -> Dict[str, List[str]]:
    """Process data with configuration"""
    pass
```

### Documentation

- **Modules**: Docstring at the top
- **Classes**: Docstring after class definition
- **Methods/Functions**: Docstring with Args, Returns, Raises
- **Complex Logic**: Inline comments

## 🧪 Writing Tests

### Test Structure

```python
"""
Unit tests for module_name
"""

import pytest
from src.module_name import MyClass

class TestMyClass:
    """Tests for MyClass"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        obj = MyClass()
        result = obj.method("input")
        assert result == "expected"
    
    def test_error_handling(self):
        """Test error handling"""
        obj = MyClass()
        with pytest.raises(ValueError):
            obj.method("invalid")
```

### Test Coverage

- Aim for **80%+ coverage**
- Test happy paths and edge cases
- Test error handling
- Test validation logic

### Running Specific Tests

```bash
# Run tests matching pattern
pytest tests/ -k "test_url"

# Run tests with markers
pytest tests/ -m "slow"

# Run failed tests only
pytest tests/ --lf
```

## 📦 Adding New Features

### 1. New Template

Create a new template in `src/templates/`:

```python
"""
Description of template
"""

from .base import BaseTemplate

class MyNewTemplate(BaseTemplate):
    """Template for generating X"""
    
    def generate(self, **kwargs) -> str:
        """
        Generate template
        
        Args:
            **kwargs: Template parameters
            
        Returns:
            Generated Robot Framework code
        """
        result = self._get_header("My New Template")
        result += self._get_settings(libraries=["Library"])
        # Add your logic
        return result
```

Add to `src/templates/__init__.py`:

```python
from .my_new_template import MyNewTemplate

__all__ = [
    # ... existing
    'MyNewTemplate',
]
```

### 2. New Tool

Add tool to `src/server.py`:

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """
    Tool description
    
    Args:
        param: Parameter description
    """
    start_time = _log_tool_execution("my_new_tool", param=param)
    
    try:
        # Validate input
        validated_param = InputValidator.validate_something(param)
        
        # Generate output
        template = MyNewTemplate()
        result = template.generate(param=validated_param)
        
        _log_tool_result("my_new_tool", start_time, True)
        return result
        
    except ValidationError as e:
        logger.log_validation_error(e.field or "unknown", e.message)
        _log_tool_result("my_new_tool", start_time, False)
        return f"# VALIDATION ERROR: {e.message}"
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _log_tool_result("my_new_tool", start_time, False)
        return f"# ERROR: {str(e)}"
```

### 3. New Validator

Add to `src/validators.py`:

```python
@classmethod
def validate_something(cls, value: str) -> str:
    """
    Validate something
    
    Args:
        value: Value to validate
        
    Returns:
        Validated value
        
    Raises:
        ValidationError: If validation fails
    """
    if not value or not value.strip():
        raise ValidationError("Value cannot be empty", field="value")
    
    # Add validation logic
    
    return value.strip()
```

### 4. Tests

Add tests in `tests/`:

```python
def test_my_new_template():
    """Test new template generation"""
    template = MyNewTemplate()
    result = template.generate(param="value")
    
    assert "*** Settings ***" in result
    assert "value" in result
```

## 🔄 Pull Request Process

### 1. Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (black, isort)
- [ ] No linting errors (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### 2. Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add mobile testing support
fix: correct selector template lookup
docs: update installation instructions
test: add tests for validators
refactor: reorganize template structure
style: format code with black
chore: update dependencies
```

### 3. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### 4. Review Process

1. Automated checks run (tests, linting)
2. Maintainer reviews code
3. Address feedback
4. Approval and merge

## 🎨 Adding Selector Templates

To add a new UI framework template:

1. **Add to config** (`src/config.py`):

```python
SELECTOR_CONFIGS["vuetify"] = {
    "username_field": "css=.v-text-field input[type='text']",
    "password_field": "css=.v-text-field input[type='password']",
    "login_button": "css=.v-btn--primary",
    "success_indicator": "css=.v-app-bar",
    "error_message": "css=.v-alert--error",
    "logout_button": "css=.v-btn--text",
    "menu_button": "css=.v-app-bar__nav-icon",
}
```

2. **Update documentation** (README.md):

```markdown
- `vuetify` - Vuetify applications
```

3. **Add tests** (`tests/test_templates.py`):

```python
def test_generate_with_vuetify_template():
    """Test generating with Vuetify template"""
    template = LoginTestTemplate()
    result = template.generate(
        url="https://example.com",
        username="test",
        password="pass",
        template_type="vuetify"
    )
    assert "v-text-field" in result
```

## 📚 Documentation

### README Updates

When adding features, update:
- Features list
- Available Tools table
- Usage Examples
- Configuration section

### Code Documentation

- Add docstrings to all public functions/classes
- Include type hints
- Provide usage examples in docstrings

### Wiki

For major features, consider adding Wiki pages:
- Tutorials
- How-to guides
- Architecture documentation

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try latest version
3. Verify it's not a configuration issue

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Call function X with Y
2. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11]
- Package version: [e.g., 2.0.0]

**Additional context**
Any other relevant information
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired functionality

**Describe alternatives you've considered**
Other approaches you've thought about

**Additional context**
Any other relevant information
```

## 📞 Getting Help

- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/robotframework-MCP/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/robotframework-MCP/issues)
- 📧 **Email**: your.email@example.com

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers.

## 🙏 Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
