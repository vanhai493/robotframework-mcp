"""
Visual regression testing templates for Robot Framework
"""

from .base import BaseTemplate


class VisualRegressionTemplate(BaseTemplate):
    """Template for generating visual regression tests"""
    
    def generate(
        self,
        base_url: str = "${BASE_URL}",
        baseline_dir: str = "baselines",
        diff_dir: str = "diffs",
        threshold: float = 0.95,
    ) -> str:
        """
        Generate visual regression test template
        
        Args:
            base_url: Base URL for testing
            baseline_dir: Directory for baseline images
            diff_dir: Directory for diff images
            threshold: Similarity threshold (0-1)
        """
        result = self._get_header("Visual Regression Test")
        result += self._get_settings()
        result += self._get_variables(base_url, baseline_dir, diff_dir, threshold)
        result += self._get_test_cases()
        result += self._get_keywords()
        return result
    
    def _get_settings(self) -> str:
        return """*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    Collections
Library    String
Library    DateTime

Suite Setup    Initialize Visual Test Suite
Suite Teardown    Close All Browsers
Test Teardown    Run Keyword If Test Failed    Capture Failure Screenshot

"""
    
    def _get_variables(
        self, base_url: str, baseline_dir: str, diff_dir: str, threshold: float
    ) -> str:
        return f"""*** Variables ***
${{BASE_URL}}              {base_url}
${{BROWSER}}               chrome
${{BASELINE_DIR}}          {baseline_dir}
${{DIFF_DIR}}              {diff_dir}
${{SCREENSHOT_DIR}}        screenshots
${{SIMILARITY_THRESHOLD}}  {threshold}
${{TIMEOUT}}               10s

# Viewport sizes for responsive testing
@{{VIEWPORTS}}             1920x1080    1366x768    768x1024    375x667

"""
    
    def _get_test_cases(self) -> str:
        return """*** Test Cases ***
Homepage Visual Test
    [Documentation]    Visual regression test for homepage
    [Tags]    visual    homepage    regression
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    css=body    ${TIMEOUT}
    Sleep    1s    # Wait for animations
    ${result}=    Compare Page To Baseline    homepage
    Should Be True    ${result}    Homepage visual regression detected

Login Page Visual Test
    [Documentation]    Visual regression test for login page
    [Tags]    visual    login    regression
    Open Browser    ${BASE_URL}/login    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    css=form    ${TIMEOUT}
    Sleep    1s
    ${result}=    Compare Page To Baseline    login_page
    Should Be True    ${result}    Login page visual regression detected
    [Teardown]    Close Browser

Responsive Visual Test
    [Documentation]    Visual regression test across viewports
    [Tags]    visual    responsive    regression
    Open Browser    ${BASE_URL}    ${BROWSER}
    FOR    ${viewport}    IN    @{VIEWPORTS}
        Set Viewport Size    ${viewport}
        Sleep    0.5s
        ${name}=    Set Variable    homepage_${viewport}
        ${result}=    Compare Page To Baseline    ${name}
        Should Be True    ${result}    Visual regression at ${viewport}
    END
    [Teardown]    Close Browser

Element Visual Test
    [Documentation]    Visual regression test for specific element
    [Tags]    visual    element    regression
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    css=.header    ${TIMEOUT}
    ${result}=    Compare Element To Baseline    css=.header    header_element
    Should Be True    ${result}    Header element visual regression detected
    [Teardown]    Close Browser

Full Page Screenshot Test
    [Documentation]    Capture and compare full page screenshot
    [Tags]    visual    fullpage    regression
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    css=body    ${TIMEOUT}
    ${result}=    Compare Full Page To Baseline    homepage_full
    Should Be True    ${result}    Full page visual regression detected
    [Teardown]    Close Browser

Create Baseline Images
    [Documentation]    Create baseline images for visual testing
    [Tags]    visual    baseline    setup
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    css=body    ${TIMEOUT}
    Sleep    1s
    Create Baseline Screenshot    homepage
    Go To    ${BASE_URL}/login
    Wait Until Page Contains Element    css=form    ${TIMEOUT}
    Sleep    1s
    Create Baseline Screenshot    login_page
    [Teardown]    Close Browser

"""
    
    def _get_keywords(self) -> str:
        return """*** Keywords ***
Initialize Visual Test Suite
    [Documentation]    Initialize directories for visual testing
    Create Directory    ${BASELINE_DIR}
    Create Directory    ${DIFF_DIR}
    Create Directory    ${SCREENSHOT_DIR}
    Log    Visual test suite initialized

Set Viewport Size
    [Arguments]    ${size}
    [Documentation]    Set browser viewport to specific size
    @{dimensions}=    Split String    ${size}    x
    ${width}=    Convert To Integer    ${dimensions}[0]
    ${height}=    Convert To Integer    ${dimensions}[1]
    Set Window Size    ${width}    ${height}

Create Baseline Screenshot
    [Arguments]    ${name}
    [Documentation]    Create baseline screenshot for comparison
    ${filename}=    Set Variable    ${BASELINE_DIR}/${name}.png
    Capture Page Screenshot    ${filename}
    Log    Baseline created: ${filename}

Compare Page To Baseline
    [Arguments]    ${name}
    [Documentation]    Compare current page to baseline
    ${current}=    Set Variable    ${SCREENSHOT_DIR}/${name}_current.png
    ${baseline}=    Set Variable    ${BASELINE_DIR}/${name}.png
    
    # Capture current screenshot
    Capture Page Screenshot    ${current}
    
    # Check if baseline exists
    ${baseline_exists}=    Run Keyword And Return Status    File Should Exist    ${baseline}
    IF    not ${baseline_exists}
        Log    Baseline not found, creating new baseline    WARN
        Copy File    ${current}    ${baseline}
        RETURN    ${True}
    END
    
    # Compare images (simplified - in real implementation use image comparison library)
    ${result}=    Compare Images    ${baseline}    ${current}    ${name}
    RETURN    ${result}

Compare Element To Baseline
    [Arguments]    ${locator}    ${name}
    [Documentation]    Compare specific element to baseline
    ${current}=    Set Variable    ${SCREENSHOT_DIR}/${name}_current.png
    ${baseline}=    Set Variable    ${BASELINE_DIR}/${name}.png
    
    Wait Until Element Is Visible    ${locator}    ${TIMEOUT}
    Capture Element Screenshot    ${locator}    ${current}
    
    ${baseline_exists}=    Run Keyword And Return Status    File Should Exist    ${baseline}
    IF    not ${baseline_exists}
        Log    Baseline not found, creating new baseline    WARN
        Copy File    ${current}    ${baseline}
        RETURN    ${True}
    END
    
    ${result}=    Compare Images    ${baseline}    ${current}    ${name}
    RETURN    ${result}

Compare Full Page To Baseline
    [Arguments]    ${name}
    [Documentation]    Compare full page screenshot (with scrolling)
    ${current}=    Set Variable    ${SCREENSHOT_DIR}/${name}_current.png
    ${baseline}=    Set Variable    ${BASELINE_DIR}/${name}.png
    
    # Capture full page by scrolling
    ${page_height}=    Execute JavaScript    return document.body.scrollHeight
    ${viewport_height}=    Execute JavaScript    return window.innerHeight
    Set Window Size    1920    ${page_height}
    Sleep    0.5s
    Capture Page Screenshot    ${current}
    
    ${baseline_exists}=    Run Keyword And Return Status    File Should Exist    ${baseline}
    IF    not ${baseline_exists}
        Copy File    ${current}    ${baseline}
        RETURN    ${True}
    END
    
    ${result}=    Compare Images    ${baseline}    ${current}    ${name}
    RETURN    ${result}

Compare Images
    [Arguments]    ${baseline}    ${current}    ${name}
    [Documentation]    Compare two images and generate diff
    # Note: This is a placeholder. In real implementation, use PIL/Pillow or similar
    # For actual image comparison, you would need to:
    # 1. Load both images
    # 2. Calculate pixel-by-pixel difference
    # 3. Calculate similarity percentage
    # 4. Generate diff image if different
    
    ${baseline_size}=    Get File Size    ${baseline}
    ${current_size}=    Get File Size    ${current}
    
    # Simple size comparison (placeholder for actual image comparison)
    ${size_diff}=    Evaluate    abs(${baseline_size} - ${current_size})
    ${threshold}=    Evaluate    ${baseline_size} * 0.1
    
    IF    ${size_diff} > ${threshold}
        Log    Visual difference detected for ${name}    WARN
        Generate Diff Image    ${baseline}    ${current}    ${name}
        RETURN    ${False}
    END
    
    Log    Visual comparison passed for ${name}
    RETURN    ${True}

Generate Diff Image
    [Arguments]    ${baseline}    ${current}    ${name}
    [Documentation]    Generate diff image highlighting differences
    ${diff_file}=    Set Variable    ${DIFF_DIR}/${name}_diff.png
    # Placeholder - actual implementation would use image processing
    Log    Diff image would be saved to: ${diff_file}

Capture Failure Screenshot
    [Documentation]    Capture screenshot on test failure
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${test_name}=    Get Variable Value    ${TEST_NAME}    unknown
    ${safe_name}=    Replace String    ${test_name}    ${SPACE}    _
    Capture Page Screenshot    ${SCREENSHOT_DIR}/failure_${safe_name}_${timestamp}.png

Hide Dynamic Elements
    [Documentation]    Hide elements that change between runs
    Execute JavaScript
    ...    var elements = document.querySelectorAll('.timestamp, .dynamic-content, .ad');
    ...    elements.forEach(function(el) { el.style.visibility = 'hidden'; });

Remove Animations
    [Documentation]    Disable CSS animations for consistent screenshots
    Execute JavaScript
    ...    var style = document.createElement('style');
    ...    style.innerHTML = '*, *::before, *::after { animation: none !important; transition: none !important; }';
    ...    document.head.appendChild(style);

Wait For Images To Load
    [Documentation]    Wait for all images to fully load
    Wait Until Keyword Succeeds    30s    1s
    ...    Execute JavaScript    return Array.from(document.images).every(img => img.complete)
"""
