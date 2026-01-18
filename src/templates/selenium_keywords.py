"""
Advanced Selenium keywords templates for Robot Framework
"""

from .base import BaseTemplate


class AdvancedSeleniumKeywords(BaseTemplate):
    """Template for advanced Selenium operations"""
    
    def generate(self, include_all: bool = True) -> str:
        """Generate advanced Selenium keywords"""
        result = self._get_header("Advanced Selenium Keywords")
        result += self._get_settings()
        result += self._get_dropdown_keywords()
        result += self._get_checkbox_keywords()
        result += self._get_file_upload_keywords()
        result += self._get_alert_keywords()
        result += self._get_mouse_keywords()
        result += self._get_scroll_keywords()
        result += self._get_window_keywords()
        result += self._get_javascript_keywords()
        result += self._get_wait_keywords()
        result += self._get_table_keywords()
        result += self._get_form_keywords()
        return result
    
    def _get_settings(self) -> str:
        return """*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String

*** Variables ***
${DEFAULT_TIMEOUT}    10s

"""
    
    def _get_dropdown_keywords(self) -> str:
        return """*** Keywords ***
# ============================================
# Dropdown/Select Operations
# ============================================

Select Dropdown Option By Label
    [Arguments]    ${locator}    ${label}
    [Documentation]    Select option from dropdown by visible text
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Select From List By Label    ${locator}    ${label}

Select Dropdown Option By Value
    [Arguments]    ${locator}    ${value}
    [Documentation]    Select option from dropdown by value attribute
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Select From List By Value    ${locator}    ${value}

Select Dropdown Option By Index
    [Arguments]    ${locator}    ${index}
    [Documentation]    Select option from dropdown by index (0-based)
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Select From List By Index    ${locator}    ${index}

Get Selected Dropdown Value
    [Arguments]    ${locator}
    [Documentation]    Get currently selected value from dropdown
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${value}=    Get Selected List Value    ${locator}
    RETURN    ${value}

Get All Dropdown Options
    [Arguments]    ${locator}
    [Documentation]    Get all available options from dropdown
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${options}=    Get List Items    ${locator}
    RETURN    ${options}

"""
    
    def _get_checkbox_keywords(self) -> str:
        return """# ============================================
# Checkbox Operations
# ============================================

Select Checkbox If Not Selected
    [Arguments]    ${locator}
    [Documentation]    Select checkbox only if not already selected
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${is_selected}=    Run Keyword And Return Status    Checkbox Should Be Selected    ${locator}
    IF    not ${is_selected}
        Select Checkbox    ${locator}
    END

Unselect Checkbox If Selected
    [Arguments]    ${locator}
    [Documentation]    Unselect checkbox only if currently selected
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${is_selected}=    Run Keyword And Return Status    Checkbox Should Be Selected    ${locator}
    IF    ${is_selected}
        Unselect Checkbox    ${locator}
    END

Toggle Checkbox
    [Arguments]    ${locator}
    [Documentation]    Toggle checkbox state
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Click Element    ${locator}

Verify Checkbox State
    [Arguments]    ${locator}    ${expected_state}
    [Documentation]    Verify checkbox is in expected state (selected/unselected)
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    IF    '${expected_state}' == 'selected'
        Checkbox Should Be Selected    ${locator}
    ELSE
        Checkbox Should Not Be Selected    ${locator}
    END

"""
    
    def _get_file_upload_keywords(self) -> str:
        return """# ============================================
# File Upload Operations
# ============================================

Upload File To Element
    [Arguments]    ${locator}    ${file_path}
    [Documentation]    Upload file using file input element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Choose File    ${locator}    ${file_path}

Upload File With Drag And Drop
    [Arguments]    ${drop_zone_locator}    ${file_path}
    [Documentation]    Upload file using drag and drop (requires JavaScript)
    Wait Until Element Is Visible    ${drop_zone_locator}    ${DEFAULT_TIMEOUT}
    Execute JavaScript
    ...    var dropZone = document.evaluate("${drop_zone_locator}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    ...    var event = new DragEvent('drop', { dataTransfer: new DataTransfer() });
    ...    dropZone.dispatchEvent(event);

"""
    
    def _get_alert_keywords(self) -> str:
        return """# ============================================
# Alert/Pop-up Operations
# ============================================

Handle Alert And Accept
    [Documentation]    Handle JavaScript alert and accept it
    ${alert_present}=    Run Keyword And Return Status    Alert Should Be Present
    IF    ${alert_present}
        Handle Alert    ACCEPT
    END

Handle Alert And Dismiss
    [Documentation]    Handle JavaScript alert and dismiss it
    ${alert_present}=    Run Keyword And Return Status    Alert Should Be Present
    IF    ${alert_present}
        Handle Alert    DISMISS
    END

Get Alert Text And Accept
    [Documentation]    Get alert text and accept the alert
    ${alert_text}=    Handle Alert    ACCEPT
    RETURN    ${alert_text}

Get Alert Text And Dismiss
    [Documentation]    Get alert text and dismiss the alert
    ${alert_text}=    Handle Alert    DISMISS
    RETURN    ${alert_text}

Input Text To Alert And Accept
    [Arguments]    ${text}
    [Documentation]    Input text to prompt alert and accept
    Input Text Into Alert    ${text}    ACCEPT

Wait For Alert And Handle
    [Arguments]    ${action}=ACCEPT    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait for alert to appear and handle it
    Wait Until Keyword Succeeds    ${timeout}    1s    Alert Should Be Present
    ${text}=    Handle Alert    ${action}
    RETURN    ${text}

"""
    
    def _get_mouse_keywords(self) -> str:
        return """# ============================================
# Mouse Operations
# ============================================

Hover Over Element
    [Arguments]    ${locator}
    [Documentation]    Hover mouse over an element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Mouse Over    ${locator}

Double Click On Element
    [Arguments]    ${locator}
    [Documentation]    Double click on an element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Double Click Element    ${locator}

Right Click On Element
    [Arguments]    ${locator}
    [Documentation]    Right click (context menu) on an element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Open Context Menu    ${locator}

Click Element At Coordinates
    [Arguments]    ${locator}    ${x_offset}    ${y_offset}
    [Documentation]    Click element at specific coordinates offset
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Click Element At Coordinates    ${locator}    ${x_offset}    ${y_offset}

Drag And Drop Element
    [Arguments]    ${source_locator}    ${target_locator}
    [Documentation]    Drag element from source to target
    Wait Until Element Is Visible    ${source_locator}    ${DEFAULT_TIMEOUT}
    Wait Until Element Is Visible    ${target_locator}    ${DEFAULT_TIMEOUT}
    Drag And Drop    ${source_locator}    ${target_locator}

Drag And Drop By Offset
    [Arguments]    ${locator}    ${x_offset}    ${y_offset}
    [Documentation]    Drag element by pixel offset
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Drag And Drop By Offset    ${locator}    ${x_offset}    ${y_offset}

"""
    
    def _get_scroll_keywords(self) -> str:
        return """# ============================================
# Scroll Operations
# ============================================

Scroll To Element
    [Arguments]    ${locator}
    [Documentation]    Scroll element into view
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Scroll Element Into View    ${locator}

Scroll To Bottom Of Page
    [Documentation]    Scroll to the bottom of the page
    Execute JavaScript    window.scrollTo(0, document.body.scrollHeight)

Scroll To Top Of Page
    [Documentation]    Scroll to the top of the page
    Execute JavaScript    window.scrollTo(0, 0)

Scroll By Pixels
    [Arguments]    ${x}    ${y}
    [Documentation]    Scroll by specified pixels
    Execute JavaScript    window.scrollBy(${x}, ${y})

Scroll To Position
    [Arguments]    ${x}    ${y}
    [Documentation]    Scroll to absolute position
    Execute JavaScript    window.scrollTo(${x}, ${y})

Scroll Element Into Center
    [Arguments]    ${locator}
    [Documentation]    Scroll element to center of viewport
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Execute JavaScript
    ...    var element = arguments[0];
    ...    element.scrollIntoView({behavior: 'smooth', block: 'center'});
    ...    ARGUMENTS    ${locator}

"""
    
    def _get_window_keywords(self) -> str:
        return """# ============================================
# Window/Tab Operations
# ============================================

Switch To New Window
    [Documentation]    Switch to the newly opened window/tab
    ${handles}=    Get Window Handles
    ${count}=    Get Length    ${handles}
    Should Be True    ${count} > 1    No new window opened
    Switch Window    ${handles}[-1]

Switch To Window By Title
    [Arguments]    ${title}
    [Documentation]    Switch to window by its title
    @{handles}=    Get Window Handles
    FOR    ${handle}    IN    @{handles}
        Switch Window    ${handle}
        ${current_title}=    Get Title
        IF    '${current_title}' == '${title}'
            RETURN
        END
    END
    Fail    Window with title '${title}' not found

Switch To Window By URL
    [Arguments]    ${url_pattern}
    [Documentation]    Switch to window by URL pattern
    @{handles}=    Get Window Handles
    FOR    ${handle}    IN    @{handles}
        Switch Window    ${handle}
        ${current_url}=    Get Location
        ${match}=    Run Keyword And Return Status    Should Contain    ${current_url}    ${url_pattern}
        IF    ${match}
            RETURN
        END
    END
    Fail    Window with URL pattern '${url_pattern}' not found

Close Current Window And Switch Back
    [Documentation]    Close current window and switch to main
    Close Window
    Switch Window    MAIN

Close All Windows Except Main
    [Documentation]    Close all windows except the main one
    @{handles}=    Get Window Handles
    ${main}=    Get From List    ${handles}    0
    FOR    ${handle}    IN    @{handles}
        IF    '${handle}' != '${main}'
            Switch Window    ${handle}
            Close Window
        END
    END
    Switch Window    ${main}

Open Link In New Tab
    [Arguments]    ${locator}
    [Documentation]    Open link in new tab using Ctrl+Click
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Press Keys    ${locator}    CTRL+RETURN

"""
    
    def _get_javascript_keywords(self) -> str:
        return """# ============================================
# JavaScript Operations
# ============================================

Execute Custom JavaScript
    [Arguments]    ${javascript_code}
    [Documentation]    Execute custom JavaScript code
    ${result}=    Execute JavaScript    ${javascript_code}
    RETURN    ${result}

Set Element Attribute
    [Arguments]    ${locator}    ${attribute}    ${value}
    [Documentation]    Set attribute value using JavaScript
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Execute JavaScript
    ...    arguments[0].setAttribute('${attribute}', '${value}');
    ...    ARGUMENTS    ${locator}

Remove Element Attribute
    [Arguments]    ${locator}    ${attribute}
    [Documentation]    Remove attribute from element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Execute JavaScript
    ...    arguments[0].removeAttribute('${attribute}');
    ...    ARGUMENTS    ${locator}

Get Element Attribute Value
    [Arguments]    ${locator}    ${attribute}
    [Documentation]    Get attribute value of an element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${value}=    Get Element Attribute    ${locator}    ${attribute}
    RETURN    ${value}

Click Element With JavaScript
    [Arguments]    ${locator}
    [Documentation]    Click element using JavaScript (bypasses visibility)
    Execute JavaScript    arguments[0].click();    ARGUMENTS    ${locator}

Set Input Value With JavaScript
    [Arguments]    ${locator}    ${value}
    [Documentation]    Set input value using JavaScript
    Execute JavaScript
    ...    arguments[0].value = '${value}';
    ...    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    ...    ARGUMENTS    ${locator}

Highlight Element
    [Arguments]    ${locator}    ${color}=red    ${duration}=2s
    [Documentation]    Temporarily highlight element for debugging
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${original_style}=    Execute JavaScript    return arguments[0].style.cssText;    ARGUMENTS    ${locator}
    Execute JavaScript    arguments[0].style.border = '3px solid ${color}';    ARGUMENTS    ${locator}
    Sleep    ${duration}
    Execute JavaScript    arguments[0].style.cssText = '${original_style}';    ARGUMENTS    ${locator}

"""
    
    def _get_wait_keywords(self) -> str:
        return """# ============================================
# Advanced Wait Operations
# ============================================

Wait Until Element Contains Text
    [Arguments]    ${locator}    ${expected_text}    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait until element contains specific text
    Wait Until Element Is Visible    ${locator}    ${timeout}
    Wait Until Element Contains    ${locator}    ${expected_text}    ${timeout}

Wait Until Page Title Contains
    [Arguments]    ${expected_title}    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait until page title contains expected text
    Wait Until Keyword Succeeds    ${timeout}    1s
    ...    Title Should Contain    ${expected_title}

Wait For Element To Disappear
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait for element to disappear from page
    Wait Until Element Is Not Visible    ${locator}    ${timeout}

Wait For Page Load Complete
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait for page to fully load
    Wait Until Keyword Succeeds    ${timeout}    1s
    ...    Execute JavaScript    return document.readyState === 'complete'

Wait For Ajax Complete
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait for all AJAX requests to complete
    Wait Until Keyword Succeeds    ${timeout}    0.5s
    ...    Execute JavaScript    return (typeof jQuery === 'undefined') || (jQuery.active === 0)

Wait For Element Attribute
    [Arguments]    ${locator}    ${attribute}    ${expected_value}    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Wait until element attribute has expected value
    Wait Until Keyword Succeeds    ${timeout}    1s
    ...    Element Attribute Value Should Be    ${locator}    ${attribute}    ${expected_value}

"""
    
    def _get_table_keywords(self) -> str:
        return """# ============================================
# Table Operations
# ============================================

Get Table Cell Text
    [Arguments]    ${table_locator}    ${row}    ${column}
    [Documentation]    Get text from specific table cell
    ${cell_text}=    Get Table Cell    ${table_locator}    ${row}    ${column}
    RETURN    ${cell_text}

Get Table Row Count
    [Arguments]    ${table_locator}
    [Documentation]    Get number of rows in table
    ${row_count}=    Get Element Count    ${table_locator}//tr
    RETURN    ${row_count}

Get Table Column Count
    [Arguments]    ${table_locator}
    [Documentation]    Get number of columns in first row
    ${col_count}=    Get Element Count    ${table_locator}//tr[1]/td | ${table_locator}//tr[1]/th
    RETURN    ${col_count}

Find Row By Cell Value
    [Arguments]    ${table_locator}    ${column}    ${value}
    [Documentation]    Find row number containing specific value in column
    ${rows}=    Get Element Count    ${table_locator}//tr
    FOR    ${row}    IN RANGE    1    ${rows + 1}
        ${cell_text}=    Get Table Cell    ${table_locator}    ${row}    ${column}
        IF    '${cell_text}' == '${value}'
            RETURN    ${row}
        END
    END
    RETURN    ${-1}

Click Cell In Table
    [Arguments]    ${table_locator}    ${row}    ${column}
    [Documentation]    Click on specific table cell
    ${cell}=    Get WebElement    ${table_locator}//tr[${row}]/td[${column}]
    Click Element    ${cell}

"""
    
    def _get_form_keywords(self) -> str:
        return """# ============================================
# Form Validation Keywords
# ============================================

Verify Field Is Required
    [Arguments]    ${locator}
    [Documentation]    Verify field has required attribute
    ${is_required}=    Get Element Attribute    ${locator}    required
    Should Not Be Empty    ${is_required}    Field should be required

Verify Field Is Disabled
    [Arguments]    ${locator}
    [Documentation]    Verify field is disabled
    Element Should Be Disabled    ${locator}

Verify Field Is Enabled
    [Arguments]    ${locator}
    [Documentation]    Verify field is enabled
    Element Should Be Enabled    ${locator}

Verify Field Is Readonly
    [Arguments]    ${locator}
    [Documentation]    Verify field is readonly
    ${readonly}=    Get Element Attribute    ${locator}    readonly
    Should Not Be Empty    ${readonly}    Field should be readonly

Clear And Input Text
    [Arguments]    ${locator}    ${text}
    [Documentation]    Clear field and input new text
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Clear Element Text    ${locator}
    Input Text    ${locator}    ${text}

Submit Form
    [Arguments]    ${form_locator}
    [Documentation]    Submit form element
    Wait Until Element Is Visible    ${form_locator}    ${DEFAULT_TIMEOUT}
    Submit Form    ${form_locator}

Verify Input Value
    [Arguments]    ${locator}    ${expected_value}
    [Documentation]    Verify input field has expected value
    ${actual_value}=    Get Value    ${locator}
    Should Be Equal    ${actual_value}    ${expected_value}
"""
