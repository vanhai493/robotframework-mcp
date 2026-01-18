"""
Robot Framework MCP Server
A Model Context Protocol server for Robot Framework test automation
"""

__version__ = "2.0.0"
__author__ = "Meenu Rani"
__email__ = "meenu.rani@sourcefuse.com"

# Export commonly used components
from .decorators import mcp_tool_handler
from .validators import ValidationError, ValidationResult, InputValidator
from .logger import get_logger, configure_logging

__all__ = [
    'mcp_tool_handler',
    'ValidationError',
    'ValidationResult',
    'InputValidator',
    'get_logger',
    'configure_logging',
]
