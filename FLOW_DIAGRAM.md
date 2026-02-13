# Flow Diagram: create_login_test_case

## 📊 Call Flow

```
User/MCP Client
    |
    | calls create_login_test_case(url, username, password, ...)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ src/server.py                                               │
│ @mcp.tool()                                                 │
│ def create_login_test_case(...)                            │
│                                                             │
│ 1. Log tool execution start                                │
│ 2. Validate inputs:                                        │
│    ├─→ InputValidator.validate_url(url)                    │
│    ├─→ InputValidator.validate_credentials(user, pass)     │
│    └─→ InputValidator.validate_template_type(template)     │
│                                                             │
│ 3. Create template instance                                │
│    ↓                                                        │
└────┼────────────────────────────────────────────────────────┘
     |
     | template = LoginTestTemplate()
     ↓
┌─────────────────────────────────────────────────────────────┐
│ src/templates/login.py                                      │
│ class LoginTestTemplate(BaseTemplate)                      │
│                                                             │
│ def generate(url, username, password, ...)                 │
│                                                             │
│ 1. Get selector config:                                    │
│    ├─→ get_selector_config(template_type)                 │
│    └─→ Returns selectors from SELECTOR_CONFIGS            │
│                                                             │
│ 2. Build test content using Template:                      │
│    ├─→ Settings section (libraries, setup, teardown)      │
│    ├─→ Variables section (URL, credentials, selectors)    │
│    ├─→ Test Cases section:                                │
│    │   ├─→ Valid Login Test                               │
│    │   └─→ Negative Tests (if enabled):                   │
│    │       ├─→ Invalid Username Test                      │
│    │       ├─→ Invalid Password Test                      │
│    │       ├─→ Empty Credentials Test                     │
│    │       └─→ SQL Injection Test                         │
│    └─→ Keywords section (reusable keywords)               │
│                                                             │
│ 3. Return complete .robot file content                     │
│    ↓                                                        │
└────┼────────────────────────────────────────────────────────┘
     |
     | returns result (string)
     ↓
┌─────────────────────────────────────────────────────────────┐
│ src/server.py (continued)                                   │
│                                                             │
│ 4. Log tool result (success/failure)                       │
│ 5. Return result to MCP client                             │
│    ↓                                                        │
└────┼────────────────────────────────────────────────────────┘
     |
     | returns .robot file content
     ↓
User/MCP Client receives complete test code
```

## 🗂️ File Structure

```
src/
├── server.py                    ← Entry point (MCP tool definition)
│   └── create_login_test_case() ← Main function
│       ├── Uses: InputValidator (from validators.py)
│       └── Uses: LoginTestTemplate (from templates/login.py)
│
├── validators.py                ← Input validation
│   ├── InputValidator class
│   │   ├── validate_url()
│   │   ├── validate_credentials()
│   │   └── validate_template_type()
│   ├── ValidationError class
│   └── ErrorFormatter class
│
├── templates/
│   ├── base.py                  ← Base template class
│   │   └── BaseTemplate
│   │
│   └── login.py                 ← Login test generator
│       └── LoginTestTemplate(BaseTemplate)
│           └── generate()       ← Generates .robot file
│
└── config.py                    ← Configuration
    ├── SELECTOR_CONFIGS         ← Selector templates
    └── get_selector_config()    ← Get selectors by type
```

## 🔄 Detailed Method Calls

### 1. Entry Point
```python
# File: src/server.py
@mcp.tool()
def create_login_test_case(url, username, password, ...):
    # This is the MCP tool that clients call
```

### 2. Validation
```python
# File: src/validators.py
class InputValidator:
    @classmethod
    def validate_url(cls, url: str) -> str:
        # Validates URL format, protocol, length
        
    @classmethod
    def validate_credentials(cls, username: str, password: str) -> tuple:
        # Validates credentials, checks for dangerous characters
        
    @classmethod
    def validate_template_type(cls, template_type: str, valid_types: list) -> str:
        # Validates template type is in allowed list
```

### 3. Template Generation
```python
# File: src/templates/login.py
class LoginTestTemplate(BaseTemplate):
    def generate(self, url, username, password, ...) -> str:
        # 1. Get selectors from config
        selectors = get_selector_config(template_type)
        
        # 2. Build test using Python Template
        template = Template("""
        *** Settings ***
        Library    SeleniumLibrary
        ...
        """)
        
        # 3. Substitute variables
        result = template.substitute(
            url=url,
            username=username,
            password=password,
            username_field=selectors['username_field'],
            password_field=selectors['password_field'],
            ...
        )
        
        # 4. Return complete .robot file
        return result
```

### 4. Selector Configuration
```python
# File: src/config.py
SELECTOR_CONFIGS = {
    "generic": {
        "username_field": "id=username",
        "password_field": "id=password",
        "login_button": "css=button[type='submit']",
        ...
    },
    "appLocator": {
        "username_field": "id=user-name",
        "password_field": "id=password",
        "login_button": "id=login-button",
        ...
    },
    ...
}

def get_selector_config(template_type: str) -> dict:
    return SELECTOR_CONFIGS.get(template_type, SELECTOR_CONFIGS["generic"])
```

## 📝 Example Call Trace

```python
# User calls:
create_login_test_case(
    url="https://www.saucedemo.com",
    username="standard_user",
    password="secret_sauce",
    template_type="appLocator"
)

# Execution trace:
1. src/server.py:create_login_test_case()
   ├─→ InputValidator.validate_url("https://www.saucedemo.com")
   │   └─→ Returns: "https://www.saucedemo.com" ✅
   │
   ├─→ InputValidator.validate_credentials("standard_user", "secret_sauce")
   │   └─→ Returns: ("standard_user", "secret_sauce") ✅
   │
   ├─→ InputValidator.validate_template_type("appLocator", [...])
   │   └─→ Returns: "appLocator" ✅
   │
   ├─→ LoginTestTemplate().generate(...)
   │   │
   │   ├─→ get_selector_config("appLocator")
   │   │   └─→ Returns: {
   │   │         "username_field": "id=user-name",
   │   │         "password_field": "id=password",
   │   │         "login_button": "id=login-button",
   │   │         ...
   │   │       }
   │   │
   │   ├─→ Build test content using Template
   │   │   ├─→ Settings section
   │   │   ├─→ Variables section
   │   │   ├─→ Test Cases section
   │   │   └─→ Keywords section
   │   │
   │   └─→ Returns: Complete .robot file content (4,417 chars)
   │
   └─→ Returns result to MCP client
```

## 🎯 Key Points

1. **Entry Point**: `src/server.py:create_login_test_case()`
2. **Validation**: `src/validators.py:InputValidator`
3. **Generation**: `src/templates/login.py:LoginTestTemplate.generate()`
4. **Configuration**: `src/config.py:SELECTOR_CONFIGS`
5. **Output**: Complete Robot Framework `.robot` file as string

## 🔍 Where to Find Each Component

| Component | File | Line |
|-----------|------|------|
| MCP Tool Definition | `src/server.py` | Line 55 |
| LoginTestTemplate Class | `src/templates/login.py` | Line 11 |
| generate() Method | `src/templates/login.py` | Line 14 |
| InputValidator | `src/validators.py` | Line ~200 |
| SELECTOR_CONFIGS | `src/config.py` | Line ~50 |
| BaseTemplate | `src/templates/base.py` | Line 1 |

