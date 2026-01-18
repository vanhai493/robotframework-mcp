"""
Configuration management for Robot Framework MCP Server
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import os
import json
import logging


class BrowserType(Enum):
    """Supported browser types"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"
    CHROMIUM = "chromium"


class TemplateType(Enum):
    """Supported selector template types"""
    APP_LOCATOR = "appLocator"
    GENERIC = "generic"
    BOOTSTRAP = "bootstrap"
    MATERIAL_UI = "materialui"
    ANT_DESIGN = "antdesign"


@dataclass
class TimeoutConfig:
    """Timeout configuration"""
    implicit_wait: str = "10s"
    explicit_wait: str = "30s"
    page_load: str = "60s"
    script_timeout: str = "30s"


@dataclass
class PerformanceThresholds:
    """Performance threshold configuration"""
    page_load_ms: int = 3000
    dom_ready_ms: int = 2000
    first_paint_ms: int = 1000
    first_contentful_paint_ms: int = 1500
    time_to_interactive_ms: int = 3500


@dataclass
class RetryConfig:
    """Retry configuration for flaky tests"""
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    retry_on_failure: bool = True


@dataclass
class ScreenshotConfig:
    """Screenshot configuration"""
    on_failure: bool = True
    directory: str = "screenshots"
    format: str = "png"
    full_page: bool = False


@dataclass
class ServerConfig:
    """Main server configuration"""
    name: str = "Robot Framework MCP Server"
    version: str = "2.0.0"
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Browser settings
    default_browser: BrowserType = BrowserType.CHROME
    headless: bool = False
    
    # Timeouts
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    
    # Performance
    performance: PerformanceThresholds = field(default_factory=PerformanceThresholds)
    
    # Retry
    retry: RetryConfig = field(default_factory=RetryConfig)
    
    # Screenshots
    screenshots: ScreenshotConfig = field(default_factory=ScreenshotConfig)


# Predefined selector configurations for different UI frameworks
SELECTOR_CONFIGS: Dict[str, Dict[str, str]] = {
    "appLocator": {
        "username_field": "id=user-name",
        "password_field": "id=password",
        "login_button": "id=login-button",
        "success_indicator": "xpath=//span[@class='title']",
        "error_message": "xpath=//h3[@data-test='error']",
        "logout_button": "id=logout_sidebar_link",
        "menu_button": "id=react-burger-menu-btn",
    },
    "generic": {
        "username_field": "id=username",
        "password_field": "id=password",
        "login_button": "css=button[type='submit']",
        "success_indicator": "css=.dashboard",
        "error_message": "css=.error",
        "logout_button": "css=.logout",
        "menu_button": "css=.menu-toggle",
    },
    "bootstrap": {
        "username_field": "css=input[name='username']",
        "password_field": "css=input[name='password']",
        "login_button": "css=.btn-primary",
        "success_indicator": "css=.navbar-brand",
        "error_message": "css=.alert-danger",
        "logout_button": "css=.btn-outline-secondary",
        "menu_button": "css=.navbar-toggler",
    },
    "materialui": {
        "username_field": "css=input[name='username'], .MuiTextField-root input",
        "password_field": "css=input[name='password'], .MuiTextField-root input[type='password']",
        "login_button": "css=.MuiButton-containedPrimary",
        "success_indicator": "css=.MuiAppBar-root",
        "error_message": "css=.MuiAlert-standardError",
        "logout_button": "css=.MuiButton-outlined",
        "menu_button": "css=.MuiIconButton-root",
    },
    "antdesign": {
        "username_field": "css=.ant-input[name='username'], #username",
        "password_field": "css=.ant-input-password input, #password",
        "login_button": "css=.ant-btn-primary",
        "success_indicator": "css=.ant-layout-header",
        "error_message": "css=.ant-alert-error",
        "logout_button": "css=.ant-btn-default",
        "menu_button": "css=.ant-menu-item",
    },
}


# Browser capabilities for different browsers
BROWSER_CAPABILITIES: Dict[str, Dict] = {
    "chrome": {
        "browserName": "chrome",
        "goog:chromeOptions": {
            "args": [
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080",
            ]
        }
    },
    "firefox": {
        "browserName": "firefox",
        "moz:firefoxOptions": {
            "args": ["-width=1920", "-height=1080"]
        }
    },
    "edge": {
        "browserName": "MicrosoftEdge",
        "ms:edgeOptions": {
            "args": ["--window-size=1920,1080"]
        }
    },
    "safari": {
        "browserName": "safari"
    },
}


def get_selector_config(template_type: str) -> Dict[str, str]:
    """Get selector configuration for a template type"""
    # Try exact match first, then case-insensitive match
    if template_type in SELECTOR_CONFIGS:
        return SELECTOR_CONFIGS[template_type]
    
    # Case-insensitive lookup
    template_lower = template_type.lower()
    for key, value in SELECTOR_CONFIGS.items():
        if key.lower() == template_lower:
            return value
    
    return SELECTOR_CONFIGS["generic"]


def get_browser_capabilities(browser: str, headless: bool = False) -> Dict:
    """Get browser capabilities with optional headless mode"""
    caps = BROWSER_CAPABILITIES.get(browser.lower(), BROWSER_CAPABILITIES["chrome"]).copy()
    
    if headless:
        if browser.lower() == "chrome":
            caps["goog:chromeOptions"]["args"].append("--headless=new")
        elif browser.lower() == "firefox":
            caps["moz:firefoxOptions"]["args"].append("-headless")
        elif browser.lower() == "edge":
            caps["ms:edgeOptions"]["args"].append("--headless")
    
    return caps


def load_config_from_file(config_path: str) -> ServerConfig:
    """Load configuration from JSON file"""
    if not os.path.exists(config_path):
        return ServerConfig()
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        config = ServerConfig()
        
        # Update simple fields
        for key in ['name', 'version', 'log_level', 'log_file', 'headless']:
            if key in data:
                setattr(config, key, data[key])
        
        # Update browser
        if 'default_browser' in data:
            config.default_browser = BrowserType(data['default_browser'])
        
        # Update nested configs
        if 'timeouts' in data:
            config.timeouts = TimeoutConfig(**data['timeouts'])
        if 'performance' in data:
            config.performance = PerformanceThresholds(**data['performance'])
        if 'retry' in data:
            config.retry = RetryConfig(**data['retry'])
        if 'screenshots' in data:
            config.screenshots = ScreenshotConfig(**data['screenshots'])
        
        return config
        
    except Exception as e:
        logging.warning(f"Failed to load config from {config_path}: {e}")
        return ServerConfig()


def save_config_to_file(config: ServerConfig, config_path: str) -> bool:
    """Save configuration to JSON file"""
    try:
        data = {
            'name': config.name,
            'version': config.version,
            'log_level': config.log_level,
            'log_file': config.log_file,
            'default_browser': config.default_browser.value,
            'headless': config.headless,
            'timeouts': {
                'implicit_wait': config.timeouts.implicit_wait,
                'explicit_wait': config.timeouts.explicit_wait,
                'page_load': config.timeouts.page_load,
                'script_timeout': config.timeouts.script_timeout,
            },
            'performance': {
                'page_load_ms': config.performance.page_load_ms,
                'dom_ready_ms': config.performance.dom_ready_ms,
                'first_paint_ms': config.performance.first_paint_ms,
                'first_contentful_paint_ms': config.performance.first_contentful_paint_ms,
                'time_to_interactive_ms': config.performance.time_to_interactive_ms,
            },
            'retry': {
                'max_retries': config.retry.max_retries,
                'retry_delay_seconds': config.retry.retry_delay_seconds,
                'retry_on_failure': config.retry.retry_on_failure,
            },
            'screenshots': {
                'on_failure': config.screenshots.on_failure,
                'directory': config.screenshots.directory,
                'format': config.screenshots.format,
                'full_page': config.screenshots.full_page,
            },
        }
        
        os.makedirs(os.path.dirname(config_path) or '.', exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to save config to {config_path}: {e}")
        return False
