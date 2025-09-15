# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Agent OS Docker application - a production-ready platform for serving Agentic Applications as an API. The project uses the Agno framework to create and manage AI agents with FastAPI as the web framework and PostgreSQL with pgvector for data storage.

## Development Commands

### Environment Setup
```bash
# Install uv package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up development environment
./scripts/dev_setup.sh

# Activate virtual environment
source .venv/bin/activate
```

### Code Quality and Validation
```bash
# Format code with ruff
./scripts/format.sh

# Lint and type check
./scripts/validate.sh

# Run individual commands
ruff format .
ruff check .
mypy . --config-file pyproject.toml
```

### Testing
```bash
# Run all tests (requires Docker)
./scripts/run_tests.sh

# Run specific test types
./scripts/run_tests.sh health    # Health check tests only
./scripts/run_tests.sh agents    # Agent tests only
./scripts/run_tests.sh fast      # Fast tests (exclude slow tests)

# Run tests manually (after starting containers)
pytest tests/ -v
pytest tests/ -v -m "not slow"  # Skip slow tests
```

### Application Deployment

#### Local Development
```bash
# Start application with Docker Compose
docker compose up -d --build

# Stop application
docker compose down

# Using ag CLI (if available)
ag infra up
ag infra down
```

#### Production Build
```bash
# Build and push production image
./scripts/build_image.sh
```

### Dependency Management
```bash
# Add dependencies to pyproject.toml, then regenerate requirements.txt
./scripts/generate_requirements.sh

# Upgrade all dependencies
./scripts/generate_requirements.sh upgrade
```

## Architecture

### Core Components

**Application Entry Point**: `app/main.py`
- Creates AgentOS instance with configured agents
- Uses `app/config.yaml` for UI configuration (quick prompts)
- Serves FastAPI application on port 8000

**Agent Definitions**: `agents/`
- `web_agent.py` - Web search capabilities using DDGS
- `agno_assist.py` - Agno documentation assistant
- Each agent uses GPT-5 by default (configurable)

**Infrastructure**: `compose.yaml`
- `pgvector` service: PostgreSQL with vector extensions on port 5432
- `api` service: FastAPI application with hot reload in development

### Configuration

**Environment Variables**:
- `OPENAI_API_KEY` - Required for GPT models
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_DATABASE` - Database connection
- Database defaults: user=ai, password=ai, database=ai

**Python Configuration**: `pyproject.toml`
- Ruff linting with 120 character line length
- MyPy type checking with strict settings
- Pytest configuration in `pytest.ini`

### Data Storage

**Database**: PostgreSQL with pgvector extension
- Used for agent sessions, knowledge, and memories
- Vector search capabilities for agent knowledge bases
- Persistent storage via Docker volume `pgdata`

## Development Workflow

1. **Code Changes**: Edit Python files in `app/` or `agents/`
2. **Format**: Run `./scripts/format.sh` before committing
3. **Validate**: Run `./scripts/validate.sh` to check linting and types
4. **Test**: Run appropriate test suite with `./scripts/run_tests.sh`
5. **Dependencies**: Update `pyproject.toml` and regenerate `requirements.txt`

## Key Files

- `app/main.py` - Application entry point and agent configuration
- `pyproject.toml` - Python project configuration and dependencies
- `compose.yaml` - Docker services definition
- `pytest.ini` - Test configuration with coverage reporting
- `scripts/` - Development automation scripts