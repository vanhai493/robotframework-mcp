"""
Data-driven testing templates for Robot Framework
"""

from string import Template
from .base import BaseTemplate


class DataDrivenTestTemplate(BaseTemplate):
    """Template for generating data-driven tests"""
    
    def generate(
        self,
        test_data_file: str = "test_data.csv",
        test_type: str = "login",
        include_setup: bool = True,
    ) -> str:
        """
        Generate data-driven test template
        
        Args:
            test_data_file: Path to test data file (CSV)
            test_type: Type of test (login, form, search, etc.)
            include_setup: Include setup instructions
        """
        result = self._get_header("Data-Driven Test")
        result += self._get_settings(test_data_file)
        result += self._get_variables()
        
        if test_type == "login":
            result += self._get_login_test()
        elif test_type == "form":
            result += self._get_form_test()
        elif test_type == "search":
            result += self._get_search_test()
        else:
            result += self._get_generic_test()
        
        result += self._get_keywords()
        
        if include_setup:
            result += self._get_data_file_instructions(test_data_file, test_type)
        
        return result
    
    def _get_settings(self, test_data_file: str) -> str:
        return f"""*** Settings ***
Library    SeleniumLibrary
Library    DataDriver    {test_data_file}    encoding=utf-8
Library    Collections
Library    String

Test Template    Execute Data Driven Test
Suite Setup    Initialize Test Suite
Suite Teardown    Close All Browsers
Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot

"""
    
    def _get_variables(self) -> str:
        return """*** Variables ***
${BROWSER}        Chrome
${BASE_URL}       ${EMPTY}
${TIMEOUT}        10s

"""
    
    def _get_login_test(self) -> str:
        return """*** Test Cases ***
Login Test With ${username} And ${password}
    [Documentation]    Data-driven login test
    [Tags]    data-driven    login

*** Keywords ***
Execute Data Driven Test
    [Arguments]    ${username}    ${password}    ${expected_result}
    [Documentation]    Template for data-driven login tests
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    id=username    ${TIMEOUT}
    Input Text    id=username    ${username}
    Input Text    id=password    ${password}
    Click Button    css=button[type='submit']
    Verify Test Result    ${expected_result}
    [Teardown]    Close Browser

Verify Test Result
    [Arguments]    ${expected_result}
    [Documentation]    Verify test result based on expected outcome
    IF    '${expected_result}' == 'success'
        Wait Until Page Contains Element    css=.dashboard    ${TIMEOUT}
        Page Should Contain    Welcome
    ELSE IF    '${expected_result}' == 'error'
        Wait Until Element Is Visible    css=.error-message    ${TIMEOUT}
        Element Should Be Visible    css=.error-message
    ELSE IF    '${expected_result}' == 'locked'
        Wait Until Element Is Visible    css=.account-locked    ${TIMEOUT}
    ELSE
        Fail    Unknown expected result: ${expected_result}
    END

"""
    
    def _get_form_test(self) -> str:
        return """*** Test Cases ***
Form Submission Test With ${test_name}
    [Documentation]    Data-driven form submission test
    [Tags]    data-driven    form

*** Keywords ***
Execute Data Driven Test
    [Arguments]    ${test_name}    ${field1}    ${field2}    ${field3}    ${expected_result}
    [Documentation]    Template for data-driven form tests
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    css=form    ${TIMEOUT}
    Fill Form Fields    ${field1}    ${field2}    ${field3}
    Submit Form    css=form
    Verify Form Result    ${expected_result}
    [Teardown]    Close Browser

Fill Form Fields
    [Arguments]    ${field1}    ${field2}    ${field3}
    [Documentation]    Fill form with provided data
    Input Text    id=field1    ${field1}
    Input Text    id=field2    ${field2}
    Input Text    id=field3    ${field3}

Verify Form Result
    [Arguments]    ${expected_result}
    [Documentation]    Verify form submission result
    IF    '${expected_result}' == 'success'
        Wait Until Page Contains    Form submitted successfully    ${TIMEOUT}
    ELSE
        Wait Until Element Is Visible    css=.validation-error    ${TIMEOUT}
    END

"""
    
    def _get_search_test(self) -> str:
        return """*** Test Cases ***
Search Test With ${search_term}
    [Documentation]    Data-driven search test
    [Tags]    data-driven    search

*** Keywords ***
Execute Data Driven Test
    [Arguments]    ${search_term}    ${expected_count}    ${expected_first_result}
    [Documentation]    Template for data-driven search tests
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    css=input[type='search']    ${TIMEOUT}
    Input Text    css=input[type='search']    ${search_term}
    Click Button    css=button[type='submit']
    Verify Search Results    ${expected_count}    ${expected_first_result}
    [Teardown]    Close Browser

Verify Search Results
    [Arguments]    ${expected_count}    ${expected_first_result}
    [Documentation]    Verify search results
    Wait Until Element Is Visible    css=.search-results    ${TIMEOUT}
    ${actual_count}=    Get Element Count    css=.search-result-item
    Should Be True    ${actual_count} >= ${expected_count}
    IF    '${expected_first_result}' != 'any'
        ${first_result}=    Get Text    css=.search-result-item:first-child
        Should Contain    ${first_result}    ${expected_first_result}
    END

"""
    
    def _get_generic_test(self) -> str:
        return """*** Test Cases ***
Generic Data Driven Test ${test_id}
    [Documentation]    Generic data-driven test
    [Tags]    data-driven

*** Keywords ***
Execute Data Driven Test
    [Arguments]    ${test_id}    ${input_data}    ${expected_output}
    [Documentation]    Generic template for data-driven tests
    Log    Executing test: ${test_id}
    Log    Input: ${input_data}
    Log    Expected: ${expected_output}
    # Add your test logic here
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    # Perform actions based on input_data
    # Verify expected_output
    [Teardown]    Close Browser

"""
    
    def _get_keywords(self) -> str:
        return """
Initialize Test Suite
    [Documentation]    Initialize the test suite
    Log    Starting data-driven test suite
    Set Selenium Speed    0.1s

Log Test Data
    [Arguments]    @{data}
    [Documentation]    Log test data for debugging
    FOR    ${item}    IN    @{data}
        Log    Data: ${item}
    END

Convert CSV Row To Dictionary
    [Arguments]    ${row}    ${headers}
    [Documentation]    Convert CSV row to dictionary
    ${dict}=    Create Dictionary
    ${length}=    Get Length    ${headers}
    FOR    ${i}    IN RANGE    ${length}
        Set To Dictionary    ${dict}    ${headers}[${i}]    ${row}[${i}]
    END
    RETURN    ${dict}

Skip Test If Condition
    [Arguments]    ${condition}    ${message}=Test skipped
    [Documentation]    Skip test based on condition
    IF    ${condition}
        Skip    ${message}
    END

Retry On Failure
    [Arguments]    ${keyword}    @{args}    ${retries}=3    ${delay}=1s
    [Documentation]    Retry keyword on failure
    FOR    ${i}    IN RANGE    ${retries}
        ${status}=    Run Keyword And Return Status    ${keyword}    @{args}
        IF    ${status}
            RETURN
        END
        Sleep    ${delay}
    END
    Fail    ${keyword} failed after ${retries} retries

"""
    
    def _get_data_file_instructions(self, test_data_file: str, test_type: str) -> str:
        if test_type == "login":
            return f"""
*** Comments ***
# ============================================
# TEST DATA FILE SETUP
# ============================================
# Create {test_data_file} with the following format:
#
# username,password,expected_result
# valid_user,valid_pass,success
# invalid_user,valid_pass,error
# valid_user,invalid_pass,error
# locked_user,valid_pass,locked
# ,valid_pass,error
# valid_user,,error
# sql_injection,'; DROP TABLE users;--,error
#
# ============================================
"""
        elif test_type == "form":
            return f"""
*** Comments ***
# ============================================
# TEST DATA FILE SETUP
# ============================================
# Create {test_data_file} with the following format:
#
# test_name,field1,field2,field3,expected_result
# valid_data,John,Doe,john@example.com,success
# missing_email,John,Doe,,error
# invalid_email,John,Doe,invalid-email,error
# special_chars,John<script>,Doe,john@test.com,error
#
# ============================================
"""
        elif test_type == "search":
            return f"""
*** Comments ***
# ============================================
# TEST DATA FILE SETUP
# ============================================
# Create {test_data_file} with the following format:
#
# search_term,expected_count,expected_first_result
# robot framework,5,Robot Framework Documentation
# selenium,10,any
# nonexistent12345,0,any
# ,0,any
#
# ============================================
"""
        else:
            return f"""
*** Comments ***
# ============================================
# TEST DATA FILE SETUP
# ============================================
# Create {test_data_file} with your test data.
# The first row should contain column headers.
# Each subsequent row represents a test case.
#
# Example:
# test_id,input_data,expected_output
# TC001,input1,output1
# TC002,input2,output2
#
# ============================================
"""
