"""
Input validation utilities for Robot Framework MCP Server
"""

import re
from typing import Tuple, Optional, List
from urllib.parse import urlparse
from dataclasses import dataclass


class ValidationError(Exception):
    """Custom exception for validation errors"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


@dataclass
class ValidationResult:
    """Result of a validation operation"""
    is_valid: bool
    value: any
    errors: List[str]
    warnings: List[str]
    
    @classmethod
    def success(cls, value: any, warnings: List[str] = None) -> 'ValidationResult':
        return cls(is_valid=True, value=value, errors=[], warnings=warnings or [])
    
    @classmethod
    def failure(cls, errors: List[str], warnings: List[str] = None) -> 'ValidationResult':
        return cls(is_valid=False, value=None, errors=errors, warnings=warnings or [])


class InputValidator:
    """Centralized input validation for MCP tools"""
    
    # Constants
    MAX_URL_LENGTH = 2048
    MAX_USERNAME_LENGTH = 100
    MAX_PASSWORD_LENGTH = 100
    MAX_SELECTOR_LENGTH = 500
    MAX_CODE_LENGTH = 100000
    
    # Dangerous characters for credentials
    DANGEROUS_CHARS = ['<', '>', '"', "'", '&', '\n', '\r', '\t', '\0']
    
    # Valid selector patterns
    SELECTOR_PATTERNS = [
        r'^id=.+',           # id=element-id
        r'^name=.+',         # name=element-name
        r'^class=.+',        # class=element-class
        r'^css=.+',          # css=.class-name
        r'^xpath=.+',        # xpath=//div[@id='test']
        r'^tag=.+',          # tag=input
        r'^link=.+',         # link=Click Here
        r'^partial link=.+', # partial link=Click
        r'^\w+',             # plain CSS selector
    ]
    
    @classmethod
    def validate_url(cls, url: str, allow_localhost: bool = True) -> str:
        """
        Validate and return sanitized URL
        
        Args:
            url: URL to validate
            allow_localhost: Whether to allow localhost URLs
            
        Returns:
            Sanitized URL string
            
        Raises:
            ValidationError: If URL is invalid
        """
        if not url or not url.strip():
            raise ValidationError("URL cannot be empty", field="url")
        
        url = url.strip()
        
        if len(url) > cls.MAX_URL_LENGTH:
            raise ValidationError(
                f"URL too long (max {cls.MAX_URL_LENGTH} characters)", 
                field="url"
            )
        
        try:
            result = urlparse(url)
            
            if not all([result.scheme, result.netloc]):
                raise ValidationError(f"Invalid URL format: {url}", field="url")
            
            if result.scheme not in ['http', 'https']:
                raise ValidationError(
                    f"URL must use http or https protocol: {url}", 
                    field="url"
                )
            
            # Check for localhost if not allowed
            if not allow_localhost:
                netloc_lower = result.netloc.lower()
                if 'localhost' in netloc_lower or '127.0.0.1' in netloc_lower:
                    raise ValidationError(
                        "Localhost URLs are not allowed", 
                        field="url"
                    )
            
            return url
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"URL validation failed: {str(e)}", field="url")

    @classmethod
    def validate_credentials(
        cls, 
        username: str, 
        password: str,
        allow_special_chars: bool = False
    ) -> Tuple[str, str]:
        """
        Validate and return sanitized credentials
        
        Args:
            username: Username to validate
            password: Password to validate
            allow_special_chars: Whether to allow special characters
            
        Returns:
            Tuple of (sanitized_username, sanitized_password)
            
        Raises:
            ValidationError: If credentials are invalid
        """
        # Validate username
        if not username or not username.strip():
            raise ValidationError("Username cannot be empty", field="username")
        
        username = username.strip()
        
        if len(username) > cls.MAX_USERNAME_LENGTH:
            raise ValidationError(
                f"Username too long (max {cls.MAX_USERNAME_LENGTH} characters)", 
                field="username"
            )
        
        # Validate password
        if not password or not password.strip():
            raise ValidationError("Password cannot be empty", field="password")
        
        password = password.strip()
        
        if len(password) > cls.MAX_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password too long (max {cls.MAX_PASSWORD_LENGTH} characters)", 
                field="password"
            )
        
        # Check for dangerous characters
        if not allow_special_chars:
            for char in cls.DANGEROUS_CHARS:
                if char in username:
                    raise ValidationError(
                        f"Username contains invalid character: {repr(char)}", 
                        field="username"
                    )
                if char in password:
                    raise ValidationError(
                        f"Password contains invalid character: {repr(char)}", 
                        field="password"
                    )
        
        return username, password
    
    @classmethod
    def validate_selector(cls, selector: str) -> str:
        """
        Validate and return sanitized selector
        
        Args:
            selector: CSS/XPath selector to validate
            
        Returns:
            Sanitized selector string
            
        Raises:
            ValidationError: If selector is invalid
        """
        if not selector or not selector.strip():
            raise ValidationError("Selector cannot be empty", field="selector")
        
        selector = selector.strip()
        
        if len(selector) > cls.MAX_SELECTOR_LENGTH:
            raise ValidationError(
                f"Selector too long (max {cls.MAX_SELECTOR_LENGTH} characters)", 
                field="selector"
            )
        
        # Check against valid patterns
        if not any(re.match(pattern, selector) for pattern in cls.SELECTOR_PATTERNS):
            raise ValidationError(
                f"Invalid selector format: {selector}", 
                field="selector"
            )
        
        return selector
    
    @classmethod
    def validate_template_type(cls, template_type: str, valid_types: List[str]) -> str:
        """
        Validate template type against allowed values
        
        Args:
            template_type: Template type to validate
            valid_types: List of valid template types
            
        Returns:
            Validated template type (lowercase)
            
        Raises:
            ValidationError: If template type is invalid
        """
        if not template_type or not template_type.strip():
            raise ValidationError("Template type cannot be empty", field="template_type")
        
        template_type = template_type.strip().lower()
        
        if template_type not in [t.lower() for t in valid_types]:
            raise ValidationError(
                f"Invalid template type: {template_type}. Valid types: {', '.join(valid_types)}", 
                field="template_type"
            )
        
        return template_type
    
    @classmethod
    def validate_robot_code(cls, code: str) -> ValidationResult:
        """
        Validate Robot Framework code syntax
        
        Args:
            code: Robot Framework code to validate
            
        Returns:
            ValidationResult with validation details
        """
        if not code or not code.strip():
            return ValidationResult.failure(["Code cannot be empty"])
        
        if len(code) > cls.MAX_CODE_LENGTH:
            return ValidationResult.failure([
                f"Code too long (max {cls.MAX_CODE_LENGTH} characters)"
            ])
        
        lines = code.split('\n')
        errors = []
        warnings = []
        
        in_section = None
        section_pattern = re.compile(r'^\*{3}\s*(.+?)\s*\*{3}$')
        valid_sections = ['Settings', 'Variables', 'Test Cases', 'Keywords', 'Comments', 'Tasks']
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Skip empty lines and comments
            if not line_stripped or line_stripped.startswith('#'):
                continue
            
            # Check section headers
            section_match = section_pattern.match(line_stripped)
            if section_match:
                section_name = section_match.group(1).strip()
                if section_name not in valid_sections:
                    warnings.append(
                        f"Line {i}: Unknown section '{section_name}'. "
                        f"Valid sections: {', '.join(valid_sections)}"
                    )
                in_section = section_name
                continue
            
            # Check for section header without closing ***
            if line_stripped.startswith('***') and not line_stripped.endswith('***'):
                errors.append(f"Line {i}: Section header must end with '***'")
            
            # Check for double-brace variable syntax (common mistake)
            if '${{' in line and '}}' in line:
                warnings.append(
                    f"Line {i}: Use ${{variable}} syntax instead of ${{{{variable}}}}"
                )
            
            # Check for unclosed variable syntax
            dollar_count = line.count('${')
            close_count = line.count('}')
            if dollar_count > close_count:
                errors.append(f"Line {i}: Unclosed variable syntax")
            
            # Check indentation in test cases and keywords
            if in_section in ['Test Cases', 'Keywords']:
                if not line.startswith(' ') and not line.startswith('\t'):
                    if not section_pattern.match(line_stripped):
                        # This might be a test case or keyword name
                        pass
                elif line.startswith(' ') and not line.startswith('    '):
                    warnings.append(
                        f"Line {i}: Use 4 spaces for indentation (Robot Framework convention)"
                    )
            
            # Check for proper spacing in Variables section
            if in_section == 'Variables':
                if line_stripped.startswith('${') and '    ' not in line and '=' not in line:
                    warnings.append(
                        f"Line {i}: Variables should use 4 spaces or '=' between name and value"
                    )
        
        if errors:
            return ValidationResult.failure(errors, warnings)
        
        return ValidationResult.success(code, warnings)
    
    @classmethod
    def validate_file_path(cls, path: str, allowed_extensions: List[str] = None) -> str:
        """
        Validate file path
        
        Args:
            path: File path to validate
            allowed_extensions: List of allowed file extensions (e.g., ['.robot', '.py'])
            
        Returns:
            Validated file path
            
        Raises:
            ValidationError: If path is invalid
        """
        if not path or not path.strip():
            raise ValidationError("File path cannot be empty", field="path")
        
        path = path.strip()
        
        # Check for path traversal attempts
        if '..' in path or path.startswith('/') or path.startswith('\\'):
            raise ValidationError(
                "Invalid file path: path traversal not allowed", 
                field="path"
            )
        
        # Check extension if specified
        if allowed_extensions:
            ext = '.' + path.split('.')[-1] if '.' in path else ''
            if ext.lower() not in [e.lower() for e in allowed_extensions]:
                raise ValidationError(
                    f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}", 
                    field="path"
                )
        
        return path
    
    @classmethod
    def validate_http_method(cls, method: str) -> str:
        """
        Validate HTTP method
        
        Args:
            method: HTTP method to validate
            
        Returns:
            Validated HTTP method (uppercase)
            
        Raises:
            ValidationError: If method is invalid
        """
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        
        if not method or not method.strip():
            raise ValidationError("HTTP method cannot be empty", field="method")
        
        method = method.strip().upper()
        
        if method not in valid_methods:
            raise ValidationError(
                f"Invalid HTTP method: {method}. Valid methods: {', '.join(valid_methods)}", 
                field="method"
            )
        
        return method
    
    @classmethod
    def validate_timeout(cls, timeout: str) -> str:
        """
        Validate timeout string format
        
        Args:
            timeout: Timeout string (e.g., '10s', '1m', '500ms')
            
        Returns:
            Validated timeout string
            
        Raises:
            ValidationError: If timeout format is invalid
        """
        if not timeout or not timeout.strip():
            raise ValidationError("Timeout cannot be empty", field="timeout")
        
        timeout = timeout.strip().lower()
        
        # Pattern for valid timeout formats
        pattern = r'^(\d+)(ms|s|m|h)?$'
        match = re.match(pattern, timeout)
        
        if not match:
            raise ValidationError(
                f"Invalid timeout format: {timeout}. Use format like '10s', '1m', '500ms'", 
                field="timeout"
            )
        
        return timeout
    
    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 1000) -> str:
        """
        Sanitize a string by removing dangerous characters
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not value:
            return ""
        
        # Remove dangerous characters
        for char in cls.DANGEROUS_CHARS:
            value = value.replace(char, '')
        
        # Truncate if too long
        if len(value) > max_length:
            value = value[:max_length]
        
        return value.strip()
