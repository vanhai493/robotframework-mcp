"""
Demonstration of ErrorFormatter class usage

This script demonstrates how the ErrorFormatter class provides
helpful, actionable error messages with context, suggestions,
examples, and documentation links.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validators import InputValidator, ValidationError, ErrorFormatter


def demo_url_validation_errors():
    """Demonstrate URL validation error formatting"""
    print("=" * 80)
    print("URL VALIDATION ERROR EXAMPLES")
    print("=" * 80)
    
    # Example 1: Empty URL
    print("\n1. Empty URL Error:")
    print("-" * 80)
    try:
        InputValidator.validate_url("")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)
    
    # Example 2: Invalid protocol
    print("\n2. Invalid Protocol Error:")
    print("-" * 80)
    try:
        InputValidator.validate_url("ftp://example.com")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)


def demo_credentials_validation_errors():
    """Demonstrate credentials validation error formatting"""
    print("\n" + "=" * 80)
    print("CREDENTIALS VALIDATION ERROR EXAMPLES")
    print("=" * 80)
    
    # Example 1: Empty username
    print("\n1. Empty Username Error:")
    print("-" * 80)
    try:
        InputValidator.validate_credentials("", "password123")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)
    
    # Example 2: Invalid character in password
    print("\n2. Invalid Character in Password Error:")
    print("-" * 80)
    try:
        InputValidator.validate_credentials("user", "pass&word")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)


def demo_selector_validation_errors():
    """Demonstrate selector validation error formatting"""
    print("\n" + "=" * 80)
    print("SELECTOR VALIDATION ERROR EXAMPLES")
    print("=" * 80)
    
    # Example 1: Empty selector
    print("\n1. Empty Selector Error:")
    print("-" * 80)
    try:
        InputValidator.validate_selector("")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)
    
    # Example 2: Invalid selector format
    print("\n2. Invalid Selector Format Error:")
    print("-" * 80)
    try:
        InputValidator.validate_selector("!!!invalid!!!")
    except ValidationError as e:
        formatted_error = ErrorFormatter.format_validation_error(e)
        print(formatted_error)


def demo_unexpected_error():
    """Demonstrate unexpected error formatting"""
    print("\n" + "=" * 80)
    print("UNEXPECTED ERROR EXAMPLE")
    print("=" * 80)
    print("\n1. Unexpected ValueError:")
    print("-" * 80)
    
    error = ValueError("Something unexpected happened")
    formatted_error = ErrorFormatter.format_unexpected_error(error)
    print(formatted_error)


def demo_error_codes():
    """Demonstrate error code registry"""
    print("\n" + "=" * 80)
    print("ERROR CODE REGISTRY")
    print("=" * 80)
    print("\nAvailable Error Codes:")
    print("-" * 80)
    
    for code, description in sorted(ErrorFormatter.ERROR_CODES.items()):
        print(f"{code}: {description}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "ErrorFormatter Demonstration" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")
    
    demo_url_validation_errors()
    demo_credentials_validation_errors()
    demo_selector_validation_errors()
    demo_unexpected_error()
    demo_error_codes()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nThe ErrorFormatter class provides:")
    print("  ✓ Clear error codes for programmatic handling")
    print("  ✓ Field-specific error messages")
    print("  ✓ Actionable suggestions for fixing errors")
    print("  ✓ Examples of valid input")
    print("  ✓ Documentation links (where applicable)")
    print("\n")
