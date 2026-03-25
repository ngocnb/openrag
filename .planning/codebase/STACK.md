# Technology Stack

**Analysis Date:** 2026-03-20

## Languages

**Primary:**
- Python 3.13 - Backend services, connectors, and TUI
- TypeScript/JavaScript - Frontend and SDKs
- Node.js 20.20.0 - Frontend runtime

**Secondary:**
- Bash - Docker entrypoints, utility scripts, Makefiles

## Runtime

**Environment:**
- Python 3.13 (specified in `.python-version`)
- Node.js 20.20.0+ (specified in `frontend/package.json`)
- Docker/Docker Compose for containerized deployment

**Package Manager:**
- **Python:** uv (Astral package manager) - with lockfile `uv.lock`
- **JavaScript/Node:** npm - with `package-lock.json` files in `frontend/`

## Frameworks

**Backend:**
- FastAPI 0.115.0+ - Web framework for REST API endpoints (`src/main.py`, `src/api/`)
- Uvicorn 0.35.0+ - ASGI server
- Agentd 0.2.2+ - Agent framework for OpenAI/Claude integration with MCP support (`agentd.patch`)

**Frontend:**
- Next.js 15.5.9+ - React framework for web UI (`frontend/`)
- React 19.0.0 - UI component library
- TailwindCSS 3.4.17 - Utility-first CSS framework
- Biome 2.3.5 - Code formatter and linter (replaces Prettier/ESLint)

**TUI/CLI:**
- Textual 0.45.0+ - Terminal UI framework (`src/tui/`)
- Rich 13.0.0+ - Terminal formatting and tables

**Testing:**
- pytest 8+ - Python test runner
- pytest-asyncio 0.21.0+ - Async test support
- pytest-mock 3.12.0+ - Mocking support
- pytest-cov 4.0.0+ - Coverage reporting
- Playwright 1.57.0+ - Browser automation (Frontend E2E tests)

**Build/Dev:**
- Docker/Buildkit - Container builds (BuildKit enabled in `Dockerfile.backend`)
- Husky 9.0.0+ - Git hooks (`frontend/.husky/`)
- Lint-staged 15.0.0+ - Run linters on staged files
- Knip 5.73.1+ - Unused code detection (frontend)

## Key Dependencies

**Critical Infrastructure:**
- opensearch-py 3.0.0[async] - Async OpenSearch client for vector search (`src/config/settings.py`, `src/utils/opensearch_utils.py`)
- httpx 0.27.0+ - Async HTTP client for API calls and webhooks
- aiofiles 24.1.0+ - Async file I/O

**Authentication & Security:**
- cryptography 45.0.6+ - Encryption utilities (`src/utils/encryption.py`)
- PyJWT 2.8.0+ - JWT token generation and validation
- google-api-python-client 2.143.0+ - Google APIs client
- google-auth-httplib2 0.2.0+ - Google HTTP authentication
- google-auth-oauthlib 1.2.0+ - Google OAuth2 support (`src/connectors/google_drive/oauth.py`)
- msal 1.29.0+ - Microsoft ADAL for Azure/Office 365 authentication
- ibm-secrets-manager-sdk 2.1.19+ - IBM Secrets Manager integration

**Cloud Storage:**
- boto3 1.35.0+ - AWS S3 SDK (`src/connectors/aws_s3/`)
- ibm-cos-sdk 2.13.0+ - IBM Cloud Object Storage SDK (`src/connectors/ibm_cos/`)

**Data Processing:**
- python-multipart 0.0.20+ - Multipart form data parsing
- structlog 25.4.0+ - Structured logging configuration (`src/utils/logging_config.py`)
- python-dotenv 1.0.0+ - Environment variable loading

**Frontend UI:**
- @radix-ui/* - Unstyled, accessible components (accordion, avatar, dialog, dropdown, label, popover, select, separator, slider, switch, tabs, tooltip)
- @tanstack/react-query 5.86.0+ - Data fetching and caching
- ag-grid-react 34.2.0+ - Advanced data grid
- lucide-react 0.525.0+ - Icon library
- react-hook-form 7.65.0+ - Form state management
- react-markdown 10.1.0+ - Markdown rendering
- react-syntax-highlighter 16.1.0+ - Code syntax highlighting
- zustand 5.0.8+ - Lightweight state management
- sonner 2.0.6+ - Toast notifications
- motion 12.23.12+ - Animation library
- next-themes 0.4.6+ - Dark mode support

**Validation & Utilities:**
- zxcvbn 4.5.0+ - Password strength validation
- psutil 7.0.0+ - System resource monitoring

**SDK/Client Libraries:**
- openai (AsyncOpenAI) - OpenAI API client (imported dynamically in `src/config/settings.py`)
- anthropic - Anthropic Claude API client (referenced in model constants)
- ollama - Local Ollama integration (via OLLAMA_ENDPOINT)
- watsonx - IBM Watson X API access

## Configuration

**Environment Variables:**
- See `.env.example` for full list (~200+ configuration options)
- Critical variables for operations:
  - `OPENSEARCH_PASSWORD` - OpenSearch admin password (required)
  - `LANGFLOW_SECRET_KEY` - Langflow authentication key
  - `OPENAI_API_KEY` - OpenAI API credentials
  - `ANTHROPIC_API_KEY` - Anthropic API credentials
  - `GOOGLE_OAUTH_CLIENT_ID/SECRET` - Google Drive/Docs integration
  - `MICROSOFT_GRAPH_OAUTH_CLIENT_ID/SECRET` - SharePoint/OneDrive
  - `AWS_ACCESS_KEY_ID/SECRET` - S3 access
  - `IBM_COS_*` - IBM Cloud Object Storage credentials
  - `OPENRAG_ENCRYPTION_KEY` - Base64 AES-256-GCM master encryption key for credentials
  - `LANGFLOW_CHAT_FLOW_ID`, `LANGFLOW_INGEST_FLOW_ID` - Langflow flow identifiers

**Encryption:**
- Master encryption key configured via `OPENRAG_ENCRYPTION_KEY` environment variable
- Tenant identifier via `OPENRAG_TENANT_ID` (default: "openrag")
- Prerequisite enforcement via `OPENRAG_ENFORCE_PREREQUISITES`

**Logging:**
- Structured logging via `structlog` with `LOG_LEVEL` (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FORMAT` configurable (default: json)
- Colored output disabled with `NO_COLOR` flag
- HTTP access logging controlled by `ACCESS_LOG` flag

**Build Configuration:**
- `pyproject.toml` - Python project metadata and dependencies
- `frontend/package.json` - Node dependencies and scripts
- `Dockerfile.backend`, `Dockerfile.frontend`, `Dockerfile.langflow` - Multi-stage Docker builds
- `docker-compose.yml` - Orchestration of all services
- `uv.lock` - Python dependency lock file
- Husky pre-commit hooks in `frontend/.husky/`

## Platform Requirements

**Development:**
- Python 3.13
- Node.js 20.20.0+
- Docker Engine with BuildKit support
- Docker Compose 2.0+
- Git (for submodules and hooks)

**Production:**
- Docker/Docker Compose environment
- OpenSearch 3.0.0+ (containerized in docker-compose.yml)
- External API keys for LLM providers (OpenAI, Anthropic, WatsonX, Ollama)
- File storage: OpenSearch (vector index) + S3/IBM COS optional
- Network: Outbound HTTPS for external APIs, webhook base URL (optional)

**Hardware Recommendations:**
- Minimum 4GB RAM for single-node OpenSearch
- CPU cores: Configure `MAX_WORKERS` for concurrent ingestion (default: min(4, CPU_COUNT // 2))
- Storage: Depends on ingested document volume (persisted in `opensearch-data` volume)

---

*Stack analysis: 2026-03-20*
