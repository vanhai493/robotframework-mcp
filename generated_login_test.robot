*** Settings ***
Library    SeleniumLibrary
Library    Collections

Suite Setup    Log    Starting Login Test Suite
Suite Teardown    Close All Browsers
Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot

*** Variables ***
${URL}                  https://www.saucedemo.com
${USERNAME}             standard_user
${PASSWORD}             secret_sauce
${BROWSER}              Chrome
${TIMEOUT}              10s

# Selector Variables
${USERNAME_FIELD}       id=user-name
${PASSWORD_FIELD}       id=password
${LOGIN_BUTTON}         id=login-button
${SUCCESS_INDICATOR}    xpath=//span[@class='title']
${ERROR_MESSAGE}        xpath=//h3[@data-test='error']

*** Test Cases ***
Valid Login Test
    [Documentation]    Test successful login with valid credentials
    [Tags]    smoke    login    positive    appLocator
    Open Browser    ${URL}    ${BROWSER}    
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_FIELD}    ${TIMEOUT}
    Input Text    ${USERNAME_FIELD}    ${USERNAME}
    Input Text    ${PASSWORD_FIELD}    ${PASSWORD}
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${SUCCESS_INDICATOR}    ${TIMEOUT}
    Page Should Contain    Dashboard
    [Teardown]    Close Browser

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
