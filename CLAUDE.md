# MCP Server Development Guidelines

## Project Overview
Building an MCP (Model Context Protocol) Server in Python that enables LLMs to interact with external systems and tools.

## Code Standards

### Python Best Practices
- Use Python 3.10+ features and type hints consistently
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Keep functions focused and single-purpose
- Handle errors gracefully with proper exception handling

### MCP Server Specific
- Implement proper JSON-RPC 2.0 protocol handling
- Use async/await for non-blocking operations
- Validate all inputs and outputs according to MCP schemas
- Provide clear, descriptive tool descriptions
- Include proper error messages with context

### Project Structure
```
mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main server implementation
│   ├── handlers/          # Request handlers
│   ├── tools/            # Tool implementations
│   └── utils/            # Utility functions
├── tests/                # Test files
├── pyproject.toml       # Project configuration
├── README.md            # Documentation
└── .env.example         # Environment variables template
```

### Dependencies
- Use `mcp` package for MCP protocol implementation
- Prefer well-maintained, lightweight libraries
- Pin dependency versions for reproducibility
- Use virtual environments for isolation

### Testing
- Write unit tests for all tool implementations
- Test error handling and edge cases
- Mock external dependencies
- Use pytest as the testing framework

### Security
- Never hardcode credentials or secrets
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Implement rate limiting where appropriate
- Follow principle of least privilege

### Documentation
- Document all tools with clear descriptions
- Include usage examples in docstrings
- Maintain up-to-date README with setup instructions
- Document environment variables and configuration

### Error Handling
- Return proper MCP error codes
- Include helpful error messages
- Log errors appropriately (not sensitive data)
- Fail gracefully without crashing the server

### Performance
- Use connection pooling for database/API connections
- Implement caching where appropriate
- Consider memory usage for large responses
- Use streaming for large data transfers when possible

## Development Workflow
1. Define tool schemas first
2. Implement handlers with proper validation
3. Write tests alongside implementation
4. Document as you code
5. Test with an MCP client before finalizing

## Commands to Run
- Linting: `ruff check .`
- Type checking: `mypy src/`
- Tests: `pytest`
- Format code: `ruff format .`