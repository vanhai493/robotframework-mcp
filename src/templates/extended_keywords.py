"""
Extended Selenium keywords for screenshots, performance, and window management
"""

from .base import BaseTemplate


class ExtendedSeleniumKeywords(BaseTemplate):
    """Template for extended Selenium operations"""
    
    def generate(self) -> str:
        """Generate extended Selenium keywords"""
        result = self._get_header("Extended Selenium Keywords")
        result += self._get_settings()
        result += self._get_screenshot_keywords()
        result += self._get_text_retrieval_keywords()
        result += self._get_window_management_keywords()
        result += self._get_performance_keywords()
        result += self._get_browser_info_keywords()
        return result
    
    def _get_settings(self) -> str:
        return """*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String
Library    DateTime
Library    OperatingSystem

*** Variables ***
${DEFAULT_TIMEOUT}       10s
${SCREENSHOT_DIR}        screenshots

"""
    
    def _get_screenshot_keywords(self) -> str:
        return """*** Keywords ***
# ============================================
# Screenshot Capabilities
# ============================================

Capture Full Page Screenshot
    [Arguments]    ${filename}=page_screenshot.png
    [Documentation]    Capture screenshot of entire page
    Capture Page Screenshot    ${filename}
    Log    Screenshot saved as: ${filename}
    RETURN    ${filename}

Capture Element Screenshot
    [Arguments]    ${locator}    ${filename}=element_screenshot.png
    [Documentation]    Capture screenshot of specific element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    Capture Element Screenshot    ${locator}    ${filename}
    Log    Element screenshot saved as: ${filename}
    RETURN    ${filename}

Capture Screenshot With Timestamp
    [Documentation]    Capture screenshot with current timestamp in filename
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${filename}=    Set Variable    screenshot_${timestamp}.png
    Capture Page Screenshot    ${filename}
    RETURN    ${filename}

Set Screenshot Directory
    [Arguments]    ${directory_path}
    [Documentation]    Set custom directory for screenshots
    Set Screenshot Directory    ${directory_path}
    Log    Screenshot directory set to: ${directory_path}

Take Screenshot On Failure
    [Documentation]    Take screenshot when test fails (for teardown use)
    ${test_name}=    Get Variable Value    ${TEST_NAME}    unknown_test
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${safe_name}=    Replace String    ${test_name}    ${SPACE}    _
    ${filename}=    Set Variable    failure_${safe_name}_${timestamp}.png
    Capture Page Screenshot    ${filename}
    Log    Failure screenshot saved: ${filename}
    RETURN    ${filename}

Take Element Screenshot With Highlight
    [Arguments]    ${locator}    ${filename}=highlighted_element.png    ${color}=red
    [Documentation]    Take screenshot of element with visual highlight
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    # Add visual highlight
    Execute JavaScript    arguments[0].style.border = '3px solid ${color}';    ARGUMENTS    ${locator}
    Sleep    0.3s
    Capture Element Screenshot    ${locator}    ${filename}
    # Remove highlight
    Execute JavaScript    arguments[0].style.border = '';    ARGUMENTS    ${locator}
    Log    Highlighted element screenshot saved: ${filename}
    RETURN    ${filename}

"""
    
    def _get_text_retrieval_keywords(self) -> str:
        return """# ============================================
# Text Retrieval Operations
# ============================================

Get Element Text Value
    [Arguments]    ${locator}
    [Documentation]    Get text content from an element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${text}=    Get Text    ${locator}
    RETURN    ${text}

Get Input Field Value
    [Arguments]    ${locator}
    [Documentation]    Get value from input field
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${value}=    Get Value    ${locator}
    RETURN    ${value}

Get Page Title
    [Documentation]    Get current page title
    ${title}=    Get Title
    RETURN    ${title}

Get Current URL
    [Documentation]    Get current page URL
    ${url}=    Get Location
    RETURN    ${url}

Get Page Source
    [Documentation]    Get complete page source HTML
    ${source}=    Get Source
    RETURN    ${source}

Get All Text From Page
    [Documentation]    Get all visible text from page body
    ${text}=    Get Text    css=body
    RETURN    ${text}

Get Element Inner HTML
    [Arguments]    ${locator}
    [Documentation]    Get inner HTML of element
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${html}=    Execute JavaScript    return arguments[0].innerHTML;    ARGUMENTS    ${locator}
    RETURN    ${html}

Get Element Outer HTML
    [Arguments]    ${locator}
    [Documentation]    Get outer HTML of element (including element itself)
    Wait Until Element Is Visible    ${locator}    ${DEFAULT_TIMEOUT}
    ${html}=    Execute JavaScript    return arguments[0].outerHTML;    ARGUMENTS    ${locator}
    RETURN    ${html}

"""
    
    def _get_window_management_keywords(self) -> str:
        return """# ============================================
# Window Management Operations
# ============================================

Get Current Window Position
    [Documentation]    Get current window position coordinates
    ${position}=    Get Window Position
    Log    Current window position: ${position}
    RETURN    ${position}

Set Window Position
    [Arguments]    ${x}    ${y}
    [Documentation]    Set window position to specific coordinates
    Set Window Position    ${x}    ${y}
    Log    Window position set to: ${x}, ${y}

Get Current Window Size
    [Documentation]    Get current window size dimensions
    ${size}=    Get Window Size
    Log    Current window size: ${size}
    RETURN    ${size}

Set Window Size
    [Arguments]    ${width}    ${height}
    [Documentation]    Set window size to specific dimensions
    Set Window Size    ${width}    ${height}
    Log    Window size set to: ${width}x${height}

Center Window On Screen
    [Documentation]    Center the browser window on screen
    ${screen_width}=    Execute JavaScript    return screen.width;
    ${screen_height}=    Execute JavaScript    return screen.height;
    ${window_width}=    Set Variable    1200
    ${window_height}=    Set Variable    800
    ${x}=    Evaluate    (${screen_width} - ${window_width}) // 2
    ${y}=    Evaluate    (${screen_height} - ${window_height}) // 2
    Set Window Size    ${window_width}    ${window_height}
    Set Window Position    ${x}    ${y}

Set Responsive Viewport
    [Arguments]    ${device}=desktop
    [Documentation]    Set viewport size for responsive testing
    ${sizes}=    Create Dictionary
    ...    mobile=375x667
    ...    tablet=768x1024
    ...    desktop=1920x1080
    ...    laptop=1366x768
    ${size}=    Get From Dictionary    ${sizes}    ${device}
    @{dimensions}=    Split String    ${size}    x
    Set Window Size    ${dimensions}[0]    ${dimensions}[1]
    Log    Viewport set to ${device}: ${size}

Restore Window Size
    [Arguments]    ${width}=1024    ${height}=768
    [Documentation]    Restore window to default size
    Set Window Size    ${width}    ${height}
    Maximize Browser Window

"""
    
    def _get_performance_keywords(self) -> str:
        return """# ============================================
# Performance and Logging Operations
# ============================================

Get Browser Console Logs
    [Documentation]    Retrieve browser console logs
    ${logs}=    Execute JavaScript    
    ...    if (window.console && window.console.logs) { return window.console.logs; }
    ...    return [];
    Log Many    @{logs}
    RETURN    ${logs}

Log Performance Metrics
    [Documentation]    Log browser performance metrics
    ${navigation_timing}=    Execute JavaScript    
    ...    return JSON.stringify(performance.getEntriesByType('navigation')[0]);
    ${paint_timing}=    Execute JavaScript    
    ...    return JSON.stringify(performance.getEntriesByType('paint'));
    Log    Navigation Timing: ${navigation_timing}
    Log    Paint Timing: ${paint_timing}

Measure Page Load Time
    [Documentation]    Measure and return page load time in milliseconds
    ${load_time}=    Execute JavaScript    
    ...    var nav = performance.getEntriesByType('navigation')[0];
    ...    return nav ? nav.loadEventEnd - nav.startTime : 0;
    Log    Page load time: ${load_time} ms
    RETURN    ${load_time}

Get Page Performance Metrics
    [Documentation]    Get comprehensive page performance metrics
    ${metrics}=    Execute JavaScript
    ...    var timing = performance.timing;
    ...    return {
    ...        dns_lookup: timing.domainLookupEnd - timing.domainLookupStart,
    ...        tcp_connect: timing.connectEnd - timing.connectStart,
    ...        request_response: timing.responseEnd - timing.requestStart,
    ...        dom_processing: timing.domComplete - timing.domLoading,
    ...        load_complete: timing.loadEventEnd - timing.navigationStart,
    ...        dom_ready: timing.domContentLoadedEventEnd - timing.navigationStart
    ...    };
    RETURN    ${metrics}

Get Network Performance
    [Documentation]    Get network performance information
    ${network_info}=    Execute JavaScript    
    ...    return JSON.stringify({
    ...        connection: navigator.connection || navigator.mozConnection || navigator.webkitConnection,
    ...        onLine: navigator.onLine,
    ...        cookieEnabled: navigator.cookieEnabled
    ...    });
    Log    Network Info: ${network_info}
    RETURN    ${network_info}

Monitor Page Resources
    [Documentation]    Monitor and log page resource loading
    ${resources}=    Execute JavaScript    
    ...    var resources = performance.getEntriesByType('resource');
    ...    return resources.map(function(r) {
    ...        return {name: r.name, type: r.initiatorType, size: r.transferSize, duration: r.duration};
    ...    });
    Log    Page Resources: ${resources}
    RETURN    ${resources}

Clear Browser Performance Data
    [Documentation]    Clear browser performance timing data
    Execute JavaScript    performance.clearResourceTimings();
    Execute JavaScript    performance.clearMarks();
    Execute JavaScript    performance.clearMeasures();
    Log    Browser performance data cleared

"""
    
    def _get_browser_info_keywords(self) -> str:
        return """# ============================================
# Browser Information
# ============================================

Log Browser Information
    [Documentation]    Log comprehensive browser information
    ${user_agent}=    Execute JavaScript    return navigator.userAgent;
    ${viewport}=    Execute JavaScript    return window.innerWidth + 'x' + window.innerHeight;
    ${screen_resolution}=    Execute JavaScript    return screen.width + 'x' + screen.height;
    ${color_depth}=    Execute JavaScript    return screen.colorDepth;
    ${language}=    Execute JavaScript    return navigator.language;
    ${platform}=    Execute JavaScript    return navigator.platform;
    
    Log    User Agent: ${user_agent}
    Log    Viewport Size: ${viewport}
    Log    Screen Resolution: ${screen_resolution}
    Log    Color Depth: ${color_depth}
    Log    Language: ${language}
    Log    Platform: ${platform}

Get Browser Name
    [Documentation]    Get browser name from user agent
    ${user_agent}=    Execute JavaScript    return navigator.userAgent;
    ${is_chrome}=    Run Keyword And Return Status    Should Contain    ${user_agent}    Chrome
    ${is_firefox}=    Run Keyword And Return Status    Should Contain    ${user_agent}    Firefox
    ${is_safari}=    Run Keyword And Return Status    Should Contain    ${user_agent}    Safari
    ${is_edge}=    Run Keyword And Return Status    Should Contain    ${user_agent}    Edg
    
    IF    ${is_edge}
        RETURN    Edge
    ELSE IF    ${is_chrome}
        RETURN    Chrome
    ELSE IF    ${is_firefox}
        RETURN    Firefox
    ELSE IF    ${is_safari}
        RETURN    Safari
    ELSE
        RETURN    Unknown
    END

Set Browser Implicit Wait
    [Arguments]    ${timeout}=${DEFAULT_TIMEOUT}
    [Documentation]    Set implicit wait timeout for element finding
    Set Browser Implicit Wait    ${timeout}
    Log    Browser implicit wait set to: ${timeout}

Get Cookies As Dictionary
    [Documentation]    Get all cookies as dictionary
    ${cookies}=    Get Cookies
    ${cookie_dict}=    Create Dictionary
    FOR    ${cookie}    IN    @{cookies}
        Set To Dictionary    ${cookie_dict}    ${cookie.name}    ${cookie.value}
    END
    RETURN    ${cookie_dict}

Clear All Browser Data
    [Documentation]    Clear cookies, local storage, and session storage
    Delete All Cookies
    Execute JavaScript    localStorage.clear();
    Execute JavaScript    sessionStorage.clear();
    Log    All browser data cleared
"""
