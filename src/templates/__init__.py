"""
Robot Framework code templates
"""

from .base import BaseTemplate
from .login import LoginTestTemplate, LoginPageObjectTemplate
from .selenium_keywords import AdvancedSeleniumKeywords
from .extended_keywords import ExtendedSeleniumKeywords
from .performance import PerformanceTestTemplate
from .api import APITestTemplate
from .data_driven import DataDrivenTestTemplate
from .mobile import MobileTestTemplate
from .visual import VisualRegressionTemplate
from .database import DatabaseTestTemplate
from .cicd import CICDTemplate

__all__ = [
    'BaseTemplate',
    'LoginTestTemplate',
    'LoginPageObjectTemplate',
    'AdvancedSeleniumKeywords',
    'ExtendedSeleniumKeywords',
    'PerformanceTestTemplate',
    'APITestTemplate',
    'DataDrivenTestTemplate',
    'MobileTestTemplate',
    'VisualRegressionTemplate',
    'DatabaseTestTemplate',
    'CICDTemplate',
]
