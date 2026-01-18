"""
Login test templates for Robot Framework
"""

from string import Template
from typing import Dict
from .base import BaseTemplate
from ..config import get_selector_config, SELECTOR_CONFIGS


class LoginTestTemplate(BaseTemplate):
    """Template for generating login test cases"""
    
    def generate(
        self,
        url: str,
        username: str,
        password: str,
        template_type: str = "generic",
        browser: str = "Chrome",
        timeout: str = "10s",
        success_text: str = "Dashboard",
        include_negative_tests: bool = False,
        headless: bool = False,
    ) -> str:
        """
        Generate a complete login test case
        
        Args:
            url: Target URL for login
            username: Test username
            password: Test password
            template_type: Selector template type
            browser: Browser to use
            timeout: Wait timeout
            success_text: Text to verify on successful login
            include_negative_tests: Include negative test cases
            headless: Run in headless mode
        """
        selectors = get_selector_config(template_type)
        
        browser_options = ""
        if headless:
            browser_options = "options=add_argument('--headless=new')"
        
        template = Template("""*** Settings ***
Library    SeleniumLibrary
Library    Collections

Suite Setup    Log    Starting Login Test Suite
Suite Teardown    Close All Browsers
Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot

*** Variables ***
$${URL}                  $url
$${USERNAME}             $username
$${PASSWORD}             $password
$${BROWSER}              $browser
$${TIMEOUT}              $timeout

# Selector Variables
$${USERNAME_FIELD}       $username_field
$${PASSWORD_FIELD}       $password_field
$${LOGIN_BUTTON}         $login_button
$${SUCCESS_INDICATOR}    $success_indicator
$${ERROR_MESSAGE}        $error_message

*** Test Cases ***
Valid Login Test
    [Documentation]    Test successful login with valid credentials
    [Tags]    smoke    login    positive    $template_type
    Open Browser    $${URL}    $${BROWSER}    $browser_options
    Maximize Browser Window
    Wait Until Element Is Visible    $${USERNAME_FIELD}    $${TIMEOUT}
    Input Text    $${USERNAME_FIELD}    $${USERNAME}
    Input Text    $${PASSWORD_FIELD}    $${PASSWORD}
    Click Button    $${LOGIN_BUTTON}
    Wait Until Page Contains Element    $${SUCCESS_INDICATOR}    $${TIMEOUT}
    Page Should Contain    $success_text
    [Teardown]    Close Browser
""")
        
        result = template.substitute(
            url=url,
            username=username,
            password=password,
            browser=browser,
            timeout=timeout,
            template_type=template_type,
            browser_options=browser_options,
            success_text=success_text,
            username_field=selectors["username_field"],
            password_field=selectors["password_field"],
            login_button=selectors["login_button"],
            success_indicator=selectors["success_indicator"],
            error_message=selectors["error_message"],
        )
        
        if include_negative_tests:
            result += self._generate_negative_tests(selectors, timeout)
        
        result += self._generate_keywords()
        
        return result
    
    def _generate_negative_tests(self, selectors: Dict, timeout: str) -> str:
        """Generate negative test cases"""
        return """
Invalid Username Test
    [Documentation]    Test login with invalid username
    [Tags]    login    negative
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Input Text    ${USERNAME_FIELD}    invalid_user
    Input Text    ${PASSWORD_FIELD}    ${PASSWORD}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    ${TIMEOUT}
    Element Should Be Visible    ${ERROR_MESSAGE}
    [Teardown]    Close Browser

Invalid Password Test
    [Documentation]    Test login with invalid password
    [Tags]    login    negative
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Input Text    ${USERNAME_FIELD}    ${USERNAME}
    Input Text    ${PASSWORD_FIELD}    wrong_password
    Click Button    ${LOGIN_BUTTON}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    ${TIMEOUT}
    Element Should Be Visible    ${ERROR_MESSAGE}
    [Teardown]    Close Browser

Empty Credentials Test
    [Documentation]    Test login with empty credentials
    [Tags]    login    negative    boundary
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Clear Element Text    ${USERNAME_FIELD}
    Clear Element Text    ${PASSWORD_FIELD}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    ${TIMEOUT}
    Element Should Be Visible    ${ERROR_MESSAGE}
    [Teardown]    Close Browser

SQL Injection Test
    [Documentation]    Test login is protected against SQL injection
    [Tags]    login    security
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Input Text    ${USERNAME_FIELD}    ' OR '1'='1
    Input Text    ${PASSWORD_FIELD}    ' OR '1'='1
    Click Button    ${LOGIN_BUTTON}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    ${TIMEOUT}
    Element Should Be Visible    ${ERROR_MESSAGE}
    [Teardown]    Close Browser
"""
    
    def _generate_keywords(self) -> str:
        """Generate reusable keywords"""
        return """
*** Keywords ***
Login With Credentials
    [Arguments]    ${user}    ${pass}
    [Documentation]    Reusable keyword for login
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Clear Element Text    ${USERNAME_FIELD}
    Clear Element Text    ${PASSWORD_FIELD}
    Input Text    ${USERNAME_FIELD}    ${user}
    Input Text    ${PASSWORD_FIELD}    ${pass}
    Click Button    ${LOGIN_BUTTON}

Verify Login Success
    [Documentation]    Verify successful login
    Wait Until Page Contains Element    ${SUCCESS_INDICATOR}    ${TIMEOUT}
    Element Should Be Visible    ${SUCCESS_INDICATOR}

Verify Login Failure
    [Documentation]    Verify login failure
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    ${TIMEOUT}
    Element Should Be Visible    ${ERROR_MESSAGE}

Safe Close Browser
    [Documentation]    Safely close browser if open
    ${browser_open}=    Run Keyword And Return Status    Get Window Handles
    Run Keyword If    ${browser_open}    Close Browser
"""


class LoginPageObjectTemplate(BaseTemplate):
    """Template for generating login page object model"""
    
    def generate(
        self,
        template_type: str = "generic",
        include_wait_keywords: bool = True,
        include_validation_keywords: bool = True,
    ) -> str:
        """
        Generate a login page object model
        
        Args:
            template_type: Selector template type
            include_wait_keywords: Include wait-related keywords
            include_validation_keywords: Include validation keywords
        """
        selectors = get_selector_config(template_type)
        
        template = Template("""*** Settings ***
Library    SeleniumLibrary
Library    String

*** Variables ***
# $template_type Application Selectors
$${LOGIN_USERNAME_FIELD}    $username_field
$${LOGIN_PASSWORD_FIELD}    $password_field
$${LOGIN_BUTTON}            $login_button
$${LOGIN_ERROR_MESSAGE}     $error_message
$${LOGIN_SUCCESS}           $success_indicator
$${LOGOUT_BUTTON}           $logout_button

# Timeouts
$${DEFAULT_TIMEOUT}         10s
$${SHORT_TIMEOUT}           5s

*** Keywords ***
# ============================================
# Input Keywords
# ============================================

Input Username
    [Arguments]    $${username}
    [Documentation]    Enter username in the username field
    Wait Until Element Is Visible    $${LOGIN_USERNAME_FIELD}    $${DEFAULT_TIMEOUT}
    Clear Element Text    $${LOGIN_USERNAME_FIELD}
    Input Text    $${LOGIN_USERNAME_FIELD}    $${username}

Input Password
    [Arguments]    $${password}
    [Documentation]    Enter password in the password field
    Wait Until Element Is Visible    $${LOGIN_PASSWORD_FIELD}    $${DEFAULT_TIMEOUT}
    Clear Element Text    $${LOGIN_PASSWORD_FIELD}
    Input Text    $${LOGIN_PASSWORD_FIELD}    $${password}

Click Login Button
    [Documentation]    Click the login button
    Wait Until Element Is Enabled    $${LOGIN_BUTTON}    $${DEFAULT_TIMEOUT}
    Click Button    $${LOGIN_BUTTON}

# ============================================
# Composite Keywords
# ============================================

Login With Credentials
    [Arguments]    $${username}    $${password}
    [Documentation]    Complete login process with given credentials
    Input Username    $${username}
    Input Password    $${password}
    Click Login Button

Login And Verify Success
    [Arguments]    $${username}    $${password}
    [Documentation]    Login and verify successful authentication
    Login With Credentials    $${username}    $${password}
    Verify Login Success

Logout
    [Documentation]    Perform logout action
    Wait Until Element Is Visible    $${LOGOUT_BUTTON}    $${DEFAULT_TIMEOUT}
    Click Element    $${LOGOUT_BUTTON}
    Wait Until Element Is Visible    $${LOGIN_USERNAME_FIELD}    $${DEFAULT_TIMEOUT}
""")
        
        result = template.substitute(
            template_type=template_type.upper(),
            username_field=selectors["username_field"],
            password_field=selectors["password_field"],
            login_button=selectors["login_button"],
            error_message=selectors["error_message"],
            success_indicator=selectors["success_indicator"],
            logout_button=selectors["logout_button"],
        )
        
        if include_wait_keywords:
            result += self._generate_wait_keywords()
        
        if include_validation_keywords:
            result += self._generate_validation_keywords()
        
        return result
    
    def _generate_wait_keywords(self) -> str:
        """Generate wait-related keywords"""
        return """
# ============================================
# Wait Keywords
# ============================================

Wait For Login Page
    [Documentation]    Wait for login page to be fully loaded
    Wait Until Element Is Visible    ${LOGIN_USERNAME_FIELD}    ${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    ${LOGIN_PASSWORD_FIELD}    ${DEFAULT_TIMEOUT}
    Wait Until Element Is Enabled    ${LOGIN_BUTTON}    ${DEFAULT_TIMEOUT}

Wait For Dashboard
    [Documentation]    Wait for dashboard/home page after login
    Wait Until Element Is Visible    ${LOGIN_SUCCESS}    ${DEFAULT_TIMEOUT}

Wait For Error Message
    [Documentation]    Wait for error message to appear
    Wait Until Element Is Visible    ${LOGIN_ERROR_MESSAGE}    ${DEFAULT_TIMEOUT}
"""
    
    def _generate_validation_keywords(self) -> str:
        """Generate validation keywords"""
        return """
# ============================================
# Validation Keywords
# ============================================

Verify Login Success
    [Documentation]    Verify successful login
    Wait Until Element Is Visible    ${LOGIN_SUCCESS}    ${DEFAULT_TIMEOUT}
    Element Should Be Visible    ${LOGIN_SUCCESS}

Verify Login Failure
    [Documentation]    Verify login failure with error message
    Wait Until Element Is Visible    ${LOGIN_ERROR_MESSAGE}    ${DEFAULT_TIMEOUT}
    Element Should Be Visible    ${LOGIN_ERROR_MESSAGE}

Verify Error Message
    [Arguments]    ${expected_message}
    [Documentation]    Verify specific error message is displayed
    Wait Until Element Is Visible    ${LOGIN_ERROR_MESSAGE}    ${DEFAULT_TIMEOUT}
    ${actual_message}=    Get Text    ${LOGIN_ERROR_MESSAGE}
    Should Contain    ${actual_message}    ${expected_message}

Verify Login Page Is Displayed
    [Documentation]    Verify login page elements are visible
    Element Should Be Visible    ${LOGIN_USERNAME_FIELD}
    Element Should Be Visible    ${LOGIN_PASSWORD_FIELD}
    Element Should Be Visible    ${LOGIN_BUTTON}

Get Error Message Text
    [Documentation]    Get the text of the error message
    Wait Until Element Is Visible    ${LOGIN_ERROR_MESSAGE}    ${DEFAULT_TIMEOUT}
    ${text}=    Get Text    ${LOGIN_ERROR_MESSAGE}
    RETURN    ${text}
"""
