# Timing and Logging Quick Reference

## Overview

The `mcp_tool_handler` decorator automatically provides timing and logging for all MCP tools.

## Quick Start

```python
from src.decorators import mcp_tool_handler

@mcp.tool()
@mcp_tool_handler("my_tool")
def my_tool(param1: str, param2: int) -> str:
    # Your tool implementation
    return result
```

## What Gets Logged

### 1. Tool Call (INFO level)
```
Tool called: my_tool(param1='value', param2=42)
```

### 2. Tool Result (INFO level)
```
Tool result: my_tool - SUCCESS (45.23ms)
Tool result: my_tool - FAILED (2.15ms)
```

### 3. Validation Errors (WARNING level)
```
Validation error: url - Invalid URL format
```

### 4. Unexpected Errors (ERROR level)
```
Unexpected error in my_tool: division by zero
[Full stack trace]
```

## Timing Information

- **Precision**: Milliseconds (ms)
- **Overhead**: < 1ms per call
- **Captured on**: All code paths (success and errors)
- **Format**: `(45.23ms)` in log output

## Configuration

### Set Log Level
```python
from src.logger import configure_logging

# Development - see everything
configure_logging(level="DEBUG")

# Production - normal operations
configure_logging(level="INFO")

# Production - errors only
configure_logging(level="WARNING")
```

### Set Log File
```python
configure_logging(level="INFO", log_file="logs/mcp_server.log")
```

## Log Levels by Operation

| Operation | Log Level | When Logged |
|-----------|-----------|-------------|
| Tool call | INFO | Every invocation |
| Successful result | INFO | On success |
| Failed result | INFO | On any error |
| Validation error | WARNING | On ValidationError |
| Unexpected error | ERROR | On Exception |

## Example Log Output

### Successful Execution
```
2024-01-15 10:30:45 | INFO | Tool called: create_test_case(url='https://example.com', test_name='Login')
2024-01-15 10:30:45 | INFO | Tool result: create_test_case - SUCCESS (45.23ms)
```

### Validation Error
```
2024-01-15 10:31:20 | INFO | Tool called: validate_config(config_file='config.txt')
2024-01-15 10:31:20 | WARNING | Validation error: config_file - Config must be JSON file
2024-01-15 10:31:20 | INFO | Tool result: validate_config - FAILED (2.15ms)
```

### Unexpected Error
```
2024-01-15 10:32:10 | INFO | Tool called: process_data(data={'key': 'value'})
2024-01-15 10:32:10 | ERROR | Unexpected error in process_data: 'required_key'
Traceback (most recent call last):
  File "src/decorators.py", line 35, in wrapper
    result = func(*args, **kwargs)
  File "src/tools.py", line 42, in process_data
    result = data['required_key']
KeyError: 'required_key'
2024-01-15 10:32:10 | INFO | Tool result: process_data - FAILED (1.87ms)
```

## Performance Tips

1. **Use appropriate log level**: WARNING in production reduces overhead
2. **Monitor timing**: Use logged durations to identify slow operations
3. **Set timeouts**: Based on typical timing measurements
4. **Rotate logs**: Configure log rotation for long-running servers

## Best Practices

### ✅ DO
- Use INFO level for development and testing
- Monitor timing for performance optimization
- Check logs when debugging issues
- Use WARNING level in production for better performance

### ❌ DON'T
- Log sensitive data (passwords, tokens) - mask them first
- Ignore timing warnings for slow operations
- Disable logging completely - at least use WARNING level
- Forget to rotate logs in production

## Troubleshooting

### No logs appearing?
- Check log level: `configure_logging(level="DEBUG")`
- Verify logger is configured: `from src.logger import get_logger; logger = get_logger()`

### Logs too verbose?
- Increase log level: `configure_logging(level="WARNING")`
- This will only log errors, not every tool call

### Need to analyze performance?
- Grep for timing: `grep "ms)" logs/mcp_server.log`
- Find slow operations: `grep -E "\([0-9]{3,}\.[0-9]{2}ms\)" logs/mcp_server.log`

### Want structured logs?
- The logger uses structured format: `timestamp | level | logger | message`
- Easy to parse with log analysis tools

## Integration with Monitoring

The timing and logging data can be used with:
- **Log aggregation**: Splunk, ELK, Datadog
- **Metrics**: Extract timing for dashboards
- **Alerting**: Alert on error rates or slow operations
- **Debugging**: Full context for issue reproduction

## Related Documentation

- Full details: `docs/task_2.1.2_timing_and_logging.md`
- Decorator usage: `docs/decorator_usage.md`
- Test examples: `tests/test_timing_and_logging.py`

## Summary

The timing and logging functionality provides:
- ✅ Automatic timing for all tools
- ✅ Comprehensive logging at all stages
- ✅ Minimal performance overhead (< 1ms)
- ✅ Configurable log levels
- ✅ Production-ready implementation

No additional code needed - just use the `@mcp_tool_handler` decorator!
