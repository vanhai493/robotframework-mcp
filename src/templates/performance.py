"""
Performance testing templates for Robot Framework
"""

from string import Template
from .base import BaseTemplate


class PerformanceTestTemplate(BaseTemplate):
    """Template for generating performance monitoring tests"""
    
    def generate(
        self,
        test_url: str = "${TEST_URL}",
        load_threshold_ms: int = 3000,
        dom_ready_threshold_ms: int = 2000,
        first_paint_threshold_ms: int = 1000,
        browser: str = "chrome",
    ) -> str:
        """
        Generate a comprehensive performance test
        
        Args:
            test_url: URL to test
            load_threshold_ms: Maximum acceptable page load time
            dom_ready_threshold_ms: Maximum acceptable DOM ready time
            first_paint_threshold_ms: Maximum acceptable first paint time
            browser: Browser to use for testing
        """
        result = self._get_header("Performance Monitoring Test")
        result += self._get_settings()
        result += self._get_variables(
            test_url, load_threshold_ms, dom_ready_threshold_ms, first_paint_threshold_ms
        )
        result += self._get_test_cases()
        result += self._get_keywords()
        return result
    
    def _get_settings(self) -> str:
        return """*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    DateTime
Library    OperatingSystem
Library    String

Suite Setup    Initialize Performance Test Suite
Suite Teardown    Close All Browsers
Test Teardown    Run Keyword If Test Failed    Capture Performance Failure

"""
    
    def _get_variables(
        self, test_url: str, load_threshold: int, dom_threshold: int, paint_threshold: int
    ) -> str:
        return f"""*** Variables ***
${{TEST_URL}}                        {test_url}
${{BROWSER}}                         chrome
${{PERFORMANCE_THRESHOLD_LOAD}}      {load_threshold}
${{PERFORMANCE_THRESHOLD_DOM}}       {dom_threshold}
${{PERFORMANCE_THRESHOLD_PAINT}}     {paint_threshold}
${{PERFORMANCE_THRESHOLD_TTI}}       3500
${{REPORT_DIR}}                      performance_reports

"""
    
    def _get_test_cases(self) -> str:
        return """*** Test Cases ***
Page Load Performance Test
    [Documentation]    Test page load performance against thresholds
    [Tags]    performance    load-time    critical
    Open Browser    ${TEST_URL}    ${BROWSER}
    ...    options=add_argument("--enable-precise-memory-info")
    Maximize Browser Window
    Wait For Page Load Complete
    ${metrics}=    Collect Performance Metrics
    Validate Load Time    ${metrics}
    [Teardown]    Close Browser

DOM Ready Performance Test
    [Documentation]    Test DOM ready time performance
    [Tags]    performance    dom-ready
    Open Browser    ${TEST_URL}    ${BROWSER}
    Maximize Browser Window
    Wait For Page Load Complete
    ${metrics}=    Collect Performance Metrics
    Validate DOM Ready Time    ${metrics}
    [Teardown]    Close Browser

First Paint Performance Test
    [Documentation]    Test first paint timing
    [Tags]    performance    first-paint
    Open Browser    ${TEST_URL}    ${BROWSER}
    Maximize Browser Window
    Wait For Page Load Complete
    ${metrics}=    Collect Paint Metrics
    Validate First Paint Time    ${metrics}
    [Teardown]    Close Browser

Resource Loading Performance Test
    [Documentation]    Test resource loading performance
    [Tags]    performance    resources
    Open Browser    ${TEST_URL}    ${BROWSER}
    Maximize Browser Window
    Wait For Page Load Complete
    ${resources}=    Collect Resource Metrics
    Analyze Resource Performance    ${resources}
    [Teardown]    Close Browser

Memory Usage Test
    [Documentation]    Test memory usage during page load
    [Tags]    performance    memory
    Open Browser    ${TEST_URL}    ${BROWSER}
    ...    options=add_argument("--enable-precise-memory-info")
    Maximize Browser Window
    Wait For Page Load Complete
    ${memory}=    Collect Memory Metrics
    Log Memory Usage    ${memory}
    [Teardown]    Close Browser

Scroll Performance Test
    [Documentation]    Test scroll performance
    [Tags]    performance    scroll    interaction
    Open Browser    ${TEST_URL}    ${BROWSER}
    Maximize Browser Window
    Wait For Page Load Complete
    ${scroll_time}=    Measure Scroll Performance
    Should Be True    ${scroll_time} < 500    Scroll should be smooth (< 500ms)
    [Teardown]    Close Browser

Multiple Page Load Comparison
    [Documentation]    Compare performance across multiple page loads
    [Tags]    performance    comparison    regression
    @{results}=    Create List
    FOR    ${i}    IN RANGE    3
        Open Browser    ${TEST_URL}    ${BROWSER}
        Maximize Browser Window
        Wait For Page Load Complete
        ${metrics}=    Collect Performance Metrics
        Append To List    ${results}    ${metrics}
        Close Browser
        Sleep    2s
    END
    ${avg}=    Calculate Average Metrics    ${results}
    Log    Average load time: ${avg}[avg_load_time]ms
    Generate Performance Report    ${results}    ${avg}

"""
    
    def _get_keywords(self) -> str:
        return """*** Keywords ***
Initialize Performance Test Suite
    [Documentation]    Initialize the performance test suite
    Create Directory    ${REPORT_DIR}
    Log    Performance test suite initialized

Wait For Page Load Complete
    [Arguments]    ${timeout}=30s
    [Documentation]    Wait for page to fully load
    Wait Until Keyword Succeeds    ${timeout}    1s
    ...    Execute JavaScript    return document.readyState === 'complete'

Collect Performance Metrics
    [Documentation]    Collect comprehensive performance metrics
    ${metrics}=    Execute JavaScript
    ...    var timing = performance.timing;
    ...    return {
    ...        dns_lookup: timing.domainLookupEnd - timing.domainLookupStart,
    ...        tcp_connect: timing.connectEnd - timing.connectStart,
    ...        ssl_handshake: timing.connectEnd - timing.secureConnectionStart,
    ...        request_time: timing.responseStart - timing.requestStart,
    ...        response_time: timing.responseEnd - timing.responseStart,
    ...        dom_processing: timing.domComplete - timing.domLoading,
    ...        dom_interactive: timing.domInteractive - timing.navigationStart,
    ...        dom_ready: timing.domContentLoadedEventEnd - timing.navigationStart,
    ...        load_complete: timing.loadEventEnd - timing.navigationStart,
    ...        total_time: timing.loadEventEnd - timing.fetchStart
    ...    };
    Log    Performance Metrics: ${metrics}
    RETURN    ${metrics}

Collect Paint Metrics
    [Documentation]    Collect paint timing metrics
    ${paint}=    Execute JavaScript
    ...    var paints = performance.getEntriesByType('paint');
    ...    var result = {};
    ...    paints.forEach(function(p) {
    ...        result[p.name.replace(/-/g, '_')] = Math.round(p.startTime);
    ...    });
    ...    return result;
    Log    Paint Metrics: ${paint}
    RETURN    ${paint}

Collect Resource Metrics
    [Documentation]    Collect resource loading metrics
    ${resources}=    Execute JavaScript
    ...    var resources = performance.getEntriesByType('resource');
    ...    var summary = {total: resources.length, by_type: {}, slow_resources: []};
    ...    resources.forEach(function(r) {
    ...        var type = r.initiatorType || 'other';
    ...        if (!summary.by_type[type]) summary.by_type[type] = {count: 0, total_size: 0, total_duration: 0};
    ...        summary.by_type[type].count++;
    ...        summary.by_type[type].total_size += r.transferSize || 0;
    ...        summary.by_type[type].total_duration += r.duration;
    ...        if (r.duration > 1000) summary.slow_resources.push({name: r.name, duration: r.duration});
    ...    });
    ...    return summary;
    Log    Resource Metrics: ${resources}
    RETURN    ${resources}

Collect Memory Metrics
    [Documentation]    Collect memory usage metrics
    ${memory}=    Execute JavaScript
    ...    if (performance.memory) {
    ...        return {
    ...            used_heap: Math.round(performance.memory.usedJSHeapSize / 1048576),
    ...            total_heap: Math.round(performance.memory.totalJSHeapSize / 1048576),
    ...            heap_limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
    ...        };
    ...    }
    ...    return {used_heap: 'N/A', total_heap: 'N/A', heap_limit: 'N/A'};
    RETURN    ${memory}

Validate Load Time
    [Arguments]    ${metrics}
    [Documentation]    Validate page load time against threshold
    ${load_time}=    Get From Dictionary    ${metrics}    load_complete
    Should Be True    ${load_time} < ${PERFORMANCE_THRESHOLD_LOAD}
    ...    Page load time (${load_time}ms) exceeds threshold (${PERFORMANCE_THRESHOLD_LOAD}ms)
    Log    Page load time: ${load_time}ms - PASSED

Validate DOM Ready Time
    [Arguments]    ${metrics}
    [Documentation]    Validate DOM ready time against threshold
    ${dom_ready}=    Get From Dictionary    ${metrics}    dom_ready
    Should Be True    ${dom_ready} < ${PERFORMANCE_THRESHOLD_DOM}
    ...    DOM ready time (${dom_ready}ms) exceeds threshold (${PERFORMANCE_THRESHOLD_DOM}ms)
    Log    DOM ready time: ${dom_ready}ms - PASSED

Validate First Paint Time
    [Arguments]    ${metrics}
    [Documentation]    Validate first paint time against threshold
    ${has_fp}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${metrics}    first_paint
    IF    ${has_fp}
        ${first_paint}=    Get From Dictionary    ${metrics}    first_paint
        Should Be True    ${first_paint} < ${PERFORMANCE_THRESHOLD_PAINT}
        ...    First paint time (${first_paint}ms) exceeds threshold (${PERFORMANCE_THRESHOLD_PAINT}ms)
        Log    First paint time: ${first_paint}ms - PASSED
    ELSE
        Log    First paint metric not available
    END

Analyze Resource Performance
    [Arguments]    ${resources}
    [Documentation]    Analyze and log resource performance
    ${total}=    Get From Dictionary    ${resources}    total
    ${slow}=    Get From Dictionary    ${resources}    slow_resources
    ${slow_count}=    Get Length    ${slow}
    Log    Total resources: ${total}
    Log    Slow resources (>1s): ${slow_count}
    IF    ${slow_count} > 0
        Log    Slow resources: ${slow}    WARN
    END

Log Memory Usage
    [Arguments]    ${memory}
    [Documentation]    Log memory usage information
    Log    Used JS Heap: ${memory}[used_heap] MB
    Log    Total JS Heap: ${memory}[total_heap] MB
    Log    Heap Limit: ${memory}[heap_limit] MB

Measure Scroll Performance
    [Documentation]    Measure scroll performance
    ${start}=    Get Time    epoch
    Execute JavaScript    window.scrollTo(0, document.body.scrollHeight);
    Sleep    0.3s
    Execute JavaScript    window.scrollTo(0, 0);
    ${end}=    Get Time    epoch
    ${duration}=    Evaluate    (${end} - ${start}) * 1000
    Log    Scroll performance: ${duration}ms
    RETURN    ${duration}

Calculate Average Metrics
    [Arguments]    ${results}
    [Documentation]    Calculate average metrics from multiple runs
    ${total_load}=    Set Variable    0
    ${total_dom}=    Set Variable    0
    ${count}=    Get Length    ${results}
    FOR    ${result}    IN    @{results}
        ${load}=    Get From Dictionary    ${result}    load_complete
        ${dom}=    Get From Dictionary    ${result}    dom_ready
        ${total_load}=    Evaluate    ${total_load} + ${load}
        ${total_dom}=    Evaluate    ${total_dom} + ${dom}
    END
    ${avg_load}=    Evaluate    round(${total_load} / ${count}, 2)
    ${avg_dom}=    Evaluate    round(${total_dom} / ${count}, 2)
    ${avg}=    Create Dictionary    avg_load_time=${avg_load}    avg_dom_ready=${avg_dom}
    RETURN    ${avg}

Generate Performance Report
    [Arguments]    ${results}    ${averages}
    [Documentation]    Generate performance report file
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${filename}=    Set Variable    ${REPORT_DIR}/perf_report_${timestamp}.txt
    ${content}=    Catenate    SEPARATOR=\\n
    ...    PERFORMANCE TEST REPORT
    ...    =======================
    ...    Generated: ${timestamp}
    ...    URL: ${TEST_URL}
    ...    
    ...    AVERAGE METRICS:
    ...    - Load Time: ${averages}[avg_load_time]ms
    ...    - DOM Ready: ${averages}[avg_dom_ready]ms
    ...    
    ...    THRESHOLDS:
    ...    - Load: ${PERFORMANCE_THRESHOLD_LOAD}ms
    ...    - DOM Ready: ${PERFORMANCE_THRESHOLD_DOM}ms
    ...    - First Paint: ${PERFORMANCE_THRESHOLD_PAINT}ms
    Create File    ${filename}    ${content}
    Log    Report saved to: ${filename}

Capture Performance Failure
    [Documentation]    Capture data on performance test failure
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    Capture Page Screenshot    ${REPORT_DIR}/failure_${timestamp}.png
    ${metrics}=    Collect Performance Metrics
    Log    Failure metrics: ${metrics}    WARN
"""
