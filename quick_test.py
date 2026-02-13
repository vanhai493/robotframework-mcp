"""
Quick test script to see what the MCP server generates
Run this to test as an end user
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.templates.login import LoginTestTemplate
from src.templates.api import APITestTemplate
from src.templates.mobile import MobileTestTemplate

print("=" * 80)
print("ROBOT FRAMEWORK MCP SERVER - QUICK TEST")
print("=" * 80)

# Test 1: Generate Login Test
print("\n" + "=" * 80)
print("TEST 1: GENERATE LOGIN TEST")
print("=" * 80)

login_template = LoginTestTemplate()
login_test = login_template.generate(
    url='https://www.saucedemo.com',
    username='standard_user',
    password='secret_sauce',
    template_type='appLocator',
    browser='Chrome',
    timeout='10s',
    include_negative_tests=True,
    headless=False
)

print("\n📝 Generated Login Test:")
print("-" * 80)
print(login_test[:1000])  # Print first 1000 characters
print("\n... (truncated)")
print(f"\n✅ Total length: {len(login_test)} characters")

# Save to file
with open('generated_login_test.robot', 'w', encoding='utf-8') as f:
    f.write(login_test)
print("💾 Saved to: generated_login_test.robot")

# Test 2: Generate API Test
print("\n" + "=" * 80)
print("TEST 2: GENERATE API TEST")
print("=" * 80)

api_template = APITestTemplate()
api_test = api_template.generate(
    base_url='https://jsonplaceholder.typicode.com',
    endpoint='/users',
    method='GET',
    include_auth=True,
    include_crud=True,
    include_error_handling=True
)

print("\n📝 Generated API Test:")
print("-" * 80)
print(api_test[:1000])  # Print first 1000 characters
print("\n... (truncated)")
print(f"\n✅ Total length: {len(api_test)} characters")

# Save to file
with open('generated_api_test.robot', 'w', encoding='utf-8') as f:
    f.write(api_test)
print("💾 Saved to: generated_api_test.robot")

# Test 3: Generate Mobile Test
print("\n" + "=" * 80)
print("TEST 3: GENERATE MOBILE TEST")
print("=" * 80)

mobile_template = MobileTestTemplate()
mobile_test = mobile_template.generate(
    platform='android',
    app_package='com.example.app',
    app_activity='.MainActivity',
    device_name='emulator-5554',
    include_gestures=True
)

print("\n📝 Generated Mobile Test:")
print("-" * 80)
print(mobile_test[:1000])  # Print first 1000 characters
print("\n... (truncated)")
print(f"\n✅ Total length: {len(mobile_test)} characters")

# Save to file
with open('generated_mobile_test.robot', 'w', encoding='utf-8') as f:
    f.write(mobile_test)
print("💾 Saved to: generated_mobile_test.robot")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\n✅ Successfully generated 3 test files:")
print("   1. generated_login_test.robot - Web login test with negative cases")
print("   2. generated_api_test.robot - API test with CRUD operations")
print("   3. generated_mobile_test.robot - Mobile test with gestures")
print("\n📂 Check the generated files to see the full content!")
print("\n🚀 To run the tests:")
print("   robot generated_login_test.robot")
print("   robot generated_api_test.robot")
print("   robot generated_mobile_test.robot")
print("\n" + "=" * 80)
