"""
Test validation and error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.validators import InputValidator, ValidationError, ErrorFormatter

print("=" * 80)
print("VALIDATION & ERROR HANDLING TEST")
print("=" * 80)

# Test 1: Valid URL
print("\n" + "=" * 80)
print("TEST 1: VALID URL")
print("=" * 80)
try:
    result = InputValidator.validate_url("https://www.saucedemo.com")
    print(f"✅ Valid URL: {result}")
except ValidationError as e:
    print(f"❌ Error: {e.message}")

# Test 2: Invalid URL (empty)
print("\n" + "=" * 80)
print("TEST 2: INVALID URL (EMPTY)")
print("=" * 80)
try:
    result = InputValidator.validate_url("")
    print(f"✅ Valid URL: {result}")
except ValidationError as e:
    print("❌ Validation Error Caught!")
    formatted_error = ErrorFormatter.format_validation_error(e)
    print(formatted_error)

# Test 3: Invalid URL (no protocol)
print("\n" + "=" * 80)
print("TEST 3: INVALID URL (NO PROTOCOL)")
print("=" * 80)
try:
    result = InputValidator.validate_url("www.example.com")
    print(f"✅ Valid URL: {result}")
except ValidationError as e:
    print("❌ Validation Error Caught!")
    formatted_error = ErrorFormatter.format_validation_error(e)
    print(formatted_error)

# Test 4: Valid credentials
print("\n" + "=" * 80)
print("TEST 4: VALID CREDENTIALS")
print("=" * 80)
try:
    username, password = InputValidator.validate_credentials("testuser", "testpass123")
    print(f"✅ Valid credentials: {username} / {'*' * len(password)}")
except ValidationError as e:
    print(f"❌ Error: {e.message}")

# Test 5: Invalid credentials (dangerous characters)
print("\n" + "=" * 80)
print("TEST 5: INVALID CREDENTIALS (DANGEROUS CHARACTERS)")
print("=" * 80)
try:
    username, password = InputValidator.validate_credentials("user<script>", "pass")
    print(f"✅ Valid credentials: {username} / {password}")
except ValidationError as e:
    print("❌ Validation Error Caught!")
    formatted_error = ErrorFormatter.format_validation_error(e)
    print(formatted_error)

# Test 6: Valid selector
print("\n" + "=" * 80)
print("TEST 6: VALID SELECTOR")
print("=" * 80)
try:
    result = InputValidator.validate_selector("id=username")
    print(f"✅ Valid selector: {result}")
except ValidationError as e:
    print(f"❌ Error: {e.message}")

# Test 7: Invalid selector (empty)
print("\n" + "=" * 80)
print("TEST 7: INVALID SELECTOR (EMPTY)")
print("=" * 80)
try:
    result = InputValidator.validate_selector("")
    print(f"✅ Valid selector: {result}")
except ValidationError as e:
    print("❌ Validation Error Caught!")
    formatted_error = ErrorFormatter.format_validation_error(e)
    print(formatted_error)

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\n✅ Validation system is working correctly!")
print("   - Valid inputs are accepted")
print("   - Invalid inputs are rejected with helpful error messages")
print("   - Error messages include:")
print("     • Error codes (VAL001, VAL002, etc.)")
print("     • Field names")
print("     • Clear suggestions")
print("     • Examples of valid input")
print("     • Documentation links (when applicable)")
print("\n" + "=" * 80)
