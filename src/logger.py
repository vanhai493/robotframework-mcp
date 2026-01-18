"""
Logging configuration for Robot Framework MCP Server
"""

import logging
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


class MCPLogger:
    """Custom logger for MCP Server with structured logging"""
    
    _instance: Optional['MCPLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(
        self,
        name: str = "robotframework-mcp",
        level: str = "INFO",
        log_file: Optional[str] = None
    ):
        """Setup the logger with handlers"""
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler (stderr to not interfere with MCP stdio)
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            try:
                Path(log_file).parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
            except Exception as e:
                self._logger.warning(f"Could not create log file: {e}")
    
    def configure(self, level: str = "INFO", log_file: Optional[str] = None):
        """Reconfigure the logger"""
        self._setup_logger(level=level, log_file=log_file)
    
    @property
    def logger(self) -> logging.Logger:
        """Get the underlying logger"""
        return self._logger
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._logger.critical(self._format_message(message, **kwargs))
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self._logger.exception(self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with additional context"""
        if kwargs:
            context = ' | '.join(f"{k}={v}" for k, v in kwargs.items())
            return f"{message} | {context}"
        return message
    
    def log_tool_call(self, tool_name: str, **params):
        """Log a tool call with parameters"""
        param_str = ', '.join(f"{k}={repr(v)[:50]}" for k, v in params.items())
        self.info(f"Tool called: {tool_name}({param_str})")
    
    def log_tool_result(self, tool_name: str, success: bool, duration_ms: float = None):
        """Log a tool result"""
        status = "SUCCESS" if success else "FAILED"
        duration_str = f" ({duration_ms:.2f}ms)" if duration_ms else ""
        self.info(f"Tool result: {tool_name} - {status}{duration_str}")
    
    def log_validation_error(self, field: str, error: str):
        """Log a validation error"""
        self.warning(f"Validation error: {field} - {error}")


# Global logger instance
_logger = MCPLogger()


def get_logger() -> MCPLogger:
    """Get the global logger instance"""
    return _logger


def configure_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Configure global logging"""
    _logger.configure(level=level, log_file=log_file)
