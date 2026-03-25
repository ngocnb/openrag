# Project Structure

**Analysis Date:** 2026-03-20

## Directory Layout

```
openrag/
├── src/                           # Core Python backend
│   ├── main.py                    # FastAPI app entry point
│   ├── agent.py                   # Agent conversation logic with MCP support
│   ├── session_manager.py         # JWT session and user management
│   ├── auth_context.py            # Thread-local auth context
│   ├── dependencies.py            # FastAPI dependency injection
│   ├── api/                       # REST API endpoints
│   │   ├── v1/                    # Public v1 API (API key auth)
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── chat.py                # Chat interaction endpoints
│   │   ├── search.py              # Search endpoints
│   │   ├── documents.py           # Document management endpoints
│   │   ├── connectors.py          # Connector management and sync
│   │   ├── settings.py            # Configuration and onboarding endpoints
│   │   ├── langflow_files.py      # Langflow file upload endpoints
│   │   ├── knowledge_filter.py    # Knowledge filter endpoints
│   │   ├── tasks.py               # Async task status endpoints
│   │   ├── models.py              # LLM provider models endpoint
│   │   ├── nudges.py              # Smart suggestions endpoint
│   │   ├── oidc.py                # OIDC discovery and JWKS
│   │   ├── provider_health.py     # Provider connectivity checks
│   │   ├── flows.py               # Langflow management endpoints
│   │   └── router.py              # Connector routing endpoint
│   ├── services/                  # Business logic services
│   │   ├── document_service.py    # Document processing and chunking
│   │   ├── chat_service.py        # Chat orchestration
│   │   ├── search_service.py      # Search operations
│   │   ├── task_service.py        # Async task management
│   │   ├── auth_service.py        # Authentication and OAuth
│   │   ├── flows_service.py       # Langflow flow management
│   │   ├── langflow_file_service.py # Langflow file operations
│   │   ├── knowledge_filter_service.py # Knowledge filter logic
│   │   ├── models_service.py      # LLM model discovery
│   │   ├── monitor_service.py     # System monitoring
│   │   ├── api_key_service.py     # API key management
│   │   ├── conversation_persistence_service.py # Chat history storage
│   │   └── langflow_mcp_service.py # MCP server management
│   ├── connectors/                # External source integrations
│   │   ├── base.py                # Abstract connector interface
│   │   ├── service.py             # Traditional connector service (OpenRAG ingestion)
│   │   ├── langflow_connector_service.py # Langflow-based ingestion
│   │   ├── connector_router.py    # Routes between connector implementations
│   │   ├── connection_manager.py  # Manages persistent connector connections
│   │   ├── aws_s3/                # AWS S3 connector
│   │   ├── ibm_cos/               # IBM Cloud Object Storage connector
│   │   ├── google_drive/          # Google Drive connector
│   │   ├── onedrive/              # Microsoft OneDrive connector
│   │   └── sharepoint/            # Microsoft SharePoint connector
│   ├── models/                    # Data models and processors
│   │   ├── processors.py          # DocumentFileProcessor for ingestion
│   │   ├── tasks.py               # Task model definitions
│   │   └── url.py                 # URL model
│   ├── config/                    # Configuration management
│   │   ├── settings.py            # Environment settings and clients
│   │   ├── config_manager.py      # Persisted config file handling
│   │   └── model_constants.py     # Model dimension constants
│   ├── utils/                     # Utility functions
│   │   ├── embeddings.py          # Embedding model utilities
│   │   ├── opensearch_utils.py    # OpenSearch connection and queries
│   │   ├── opensearch_queries.py  # Query building utilities
│   │   ├── document_processing.py # Text extraction and chunking
│   │   ├── docling_client.py      # Docling OCR integration
│   │   ├── encryption.py          # Config file encryption
│   │   ├── langflow_utils.py      # Langflow API helpers
│   │   ├── langflow_headers.py    # Langflow global variable management
│   │   ├── file_utils.py          # File operations
│   │   ├── hash_utils.py          # File hashing
│   │   ├── logging_config.py      # Structured logging setup
│   │   ├── gpu_detection.py       # GPU availability detection
│   │   ├── version_utils.py       # Version management
│   │   ├── env_utils.py           # Environment variable parsing
│   │   ├── container_utils.py     # Docker detection
│   │   ├── telemetry/             # Event telemetry client
│   │   └── acl_utils.py           # Access control utilities
│   └── tui/                       # Terminal user interface
│       ├── main.py                # TUI entry point
│       ├── cli.py                 # CLI command definitions
│       ├── screens/               # TUI screens (welcome, config, logs, etc.)
│       ├── managers/              # TUI component managers
│       ├── widgets/               # Textual UI components
│       ├── config_fields.py       # Configuration field definitions
│       └── _assets/               # Sample flows and documents
├── frontend/                      # Next.js web UI
│   ├── package.json               # Frontend dependencies
│   ├── components/                # React components
│   ├── hooks/                     # React hooks (chat streaming, file drag, etc.)
│   ├── pages/                     # Next.js pages
│   └── app/                       # Next.js app directory (if using App Router)
├── sdks/                          # Official SDKs
│   ├── typescript/                # TypeScript/JavaScript SDK
│   ├── python/                    # Python SDK (openrag-sdk)
│   └── mcp/                       # MCP server integration
├── kubernetes/                    # Kubernetes deployment configs
├── scripts/                       # Build and deployment scripts
├── docs/                          # Documentation
├── flows/                         # Sample Langflow workflows
├── openrag-documents/             # Sample documents for onboarding
├── .planning/                     # GSD codebase documentation
├── keys/                          # JWT RSA key pair (generated at startup)
├── Dockerfile                     # Backend container image
├── Dockerfile.backend             # Backend-specific build
├── Dockerfile.frontend            # Frontend-specific build
├── docker-compose.yml             # Production stack definition
├── docker-compose.dev.yml         # Development stack definition
├── docker-compose.gpu.yml         # GPU-enabled stack
├── pyproject.toml                 # Python package definition
├── Makefile                       # Build and development commands
└── README.md                      # Project overview
```

## Source Code Organization

### API Module (`src/api/`)

**Internal Endpoints:**
- `auth.py`: OAuth login/logout, user info
- `chat.py`: Chat interface (both MCP agent and Langflow flows)
- `search.py`: Semantic search endpoint
- `documents.py`: Document metadata operations
- `connectors.py`: Connector OAuth, sync, webhook endpoints
- `settings.py`: Configuration retrieval/update, onboarding, settings management
- `langflow_files.py`: Langflow-specific file operations
- `knowledge_filter.py`: Create/update/delete/subscribe to knowledge filters
- `tasks.py`: Async task status and cancellation
- `upload.py`: File upload and context management
- `models.py`: Available LLM models for each provider
- `nudges.py`: Smart suggestions based on knowledge
- `oidc.py`: OIDC discovery, JWKS, token introspection
- `provider_health.py`: Provider connectivity status
- `flows.py`: Langflow flow reset/management
- `keys.py`: API key management for public API
- `docling.py`: Docling health check

**Public v1 API (`src/api/v1/`)**
- `chat.py`: Chat creation, listing, deletion (API key auth)
- `search.py`: Semantic search (API key auth)
- `documents.py`: Document ingestion, task status, deletion (API key auth)
- `settings.py`: Public settings endpoints
- `models.py`: Public models endpoint
- `knowledge_filters.py`: Public knowledge filter endpoints

### Services Module (`src/services/`)

**Core Services:**
- `document_service.py`: Document chunking, embedding, OpenSearch storage
- `chat_service.py`: Chat request handling and response orchestration
- `search_service.py`: Semantic search with optional knowledge filter
- `task_service.py`: Async task creation, tracking, and cleanup
- `auth_service.py`: OAuth flow handling, JWT generation, user session management
- `flows_service.py`: Langflow flow discovery, backup, reset detection
- `langflow_file_service.py`: File upload to Langflow, ingestion task creation
- `knowledge_filter_service.py`: Filter CRUD and subscription management
- `models_service.py`: LLM model discovery for OpenAI, Anthropic, IBM, Ollama
- `monitor_service.py`: Container/host resource monitoring
- `api_key_service.py`: API key generation, validation, revocation
- `conversation_persistence_service.py`: Chat history storage to disk
- `langflow_mcp_service.py`: MCP server lifecycle and execution
- `session_ownership_service.py`: Track document ownership by session

### Connectors Module (`src/connectors/`)

**Architecture:**
- `base.py`: Abstract `BaseConnector` interface (list, retrieve, sync, cleanup)
- `service.py`: Traditional connector service for OpenRAG ingestion pipeline
- `langflow_connector_service.py`: Langflow-based ingestion service
- `connection_manager.py`: CRUD for connector connections, OAuth token persistence
- `connector_router.py`: Selects between connector services based on config

**Provider Implementations:**
Each provider (AWS S3, IBM COS, Google Drive, OneDrive, SharePoint) has:
- `connector.py`: Core connector logic
- `auth.py`: OAuth and credential handling
- `api.py`: Provider-specific API wrappers (S3/IBM COS only)
- `models.py`: Data models for buckets/folders
- `support.py`: Helper utilities

### Models Module (`src/models/`)

- `processors.py`: `DocumentFileProcessor` class for file ingestion pipeline
- `tasks.py`: Task model definitions for async operations
- `url.py`: URL-related models

### Config Module (`src/config/`)

- `settings.py`: Environment variable loading, client initialization, API credentials
- `config_manager.py`: Encrypted config file persistence, onboarding state
- `model_constants.py`: Embedding model dimension mappings

### Utils Module (`src/utils/`)

**Document Processing:**
- `document_processing.py`: Text extraction, relevance scoring
- `docling_client.py`: Docling service integration for PDF/DOCX parsing
- `embeddings.py`: Embedding provider abstraction, dimension resolution

**OpenSearch Integration:**
- `opensearch_utils.py`: Connection pooling, health checks
- `opensearch_queries.py`: Query building (BM25, vector, knowledge filter)

**Langflow Integration:**
- `langflow_utils.py`: API key generation, flow execution
- `langflow_headers.py`: Global variable construction for flows

**System Utilities:**
- `encryption.py`: Config file encryption/decryption
- `logging_config.py`: Structured logging via Structlog
- `version_utils.py`: Version constants and management
- `env_utils.py`: Type-safe environment variable parsing
- `container_utils.py`: Docker/Podman detection
- `gpu_detection.py`: GPU availability checking
- `file_utils.py`: File I/O operations
- `hash_utils.py`: Document hashing
- `acl_utils.py`: Access control checks

**Telemetry:**
- `telemetry/client.py`: Event tracking (community builds disable this)
- `telemetry/category.py`: Event category definitions
- `telemetry/message_id.py`: Event ID definitions

### TUI Module (`src/tui/`)

- `main.py`: Entry point for terminal UI
- `cli.py`: CLI command parsing and execution
- `screens/`: Textual UI screens (welcome, config, logs, diagnostics, monitor)
- `managers/`: Component managers (container, docling, environment)
- `widgets/`: Custom Textual widgets
- `_assets/`: Sample flows and bundled documentation

## Configuration Files

**Python Package:**
- `pyproject.toml`: Package metadata, dependencies, entry points

**Environment:**
- `.env.example`: Template for required environment variables
- `.python-version`: Python version specification
- `.pre-commit-config.yaml`: Pre-commit hooks configuration

**Docker:**
- `docker-compose.yml`: Production/standard deployment
- `docker-compose.dev.yml`: Development environment with hot-reload
- `docker-compose.gpu.yml`: GPU-enabled deployment
- `Dockerfile`: Backend multi-stage build
- `.dockerignore`: Docker build exclusions

**Build:**
- `Makefile`: Development and build commands
- `MANIFEST.in`: Package distribution manifest
- `patch-netty.sh`: Netty patching utility

## Key File Locations

**Entry Points:**
- Backend REST API: `src/main.py` (starts FastAPI on port 8000)
- Terminal UI: `src/tui/main.py` (entry point `openrag` command)
- Frontend: `frontend/app/` or `frontend/pages/` (Next.js app)

**Configuration:**
- Settings: `src/config/settings.py` (environment-based)
- Persisted config: `openrag-config.toml` (in user home directory, encrypted)
- Flow IDs: Environment variables (LANGFLOW_CHAT_FLOW_ID, LANGFLOW_INGEST_FLOW_ID, etc.)

**Core Logic:**
- Document processing: `src/models/processors.py`
- Chat orchestration: `src/services/chat_service.py`, `src/agent.py`
- Search: `src/services/search_service.py`, `src/utils/opensearch_queries.py`
- Authentication: `src/services/auth_service.py`, `src/session_manager.py`

**Testing:**
- Test files: Colocated with source or in `tests/` directory (if present)
- Unit test markers: `*.test.py`, `*_test.py` conventions

## Naming Conventions

**Files:**
- Python modules: `snake_case.py` (e.g., `document_service.py`, `opensearch_utils.py`)
- API route files: `snake_case.py` matching endpoint domain (e.g., `langflow_files.py`)
- Service classes: `CamelCase` (e.g., `DocumentService`, `ChatService`)
- Utility functions: `snake_case` (e.g., `get_embedding_model()`)

**Directories:**
- Package/module directories: `snake_case/` (e.g., `src/connectors/`, `src/services/`)
- Provider packages: `provider_name/` (e.g., `aws_s3/`, `google_drive/`)
- Logical groupings: `snake_case/` (e.g., `screens/`, `managers/`, `widgets/`)

**Classes:**
- Service classes: `{Domain}Service` (e.g., `DocumentService`, `ChatService`)
- Connector classes: `{Provider}Connector` (e.g., `S3Connector`)
- Data classes: `{Entity}` (e.g., `User`, `Document`)

**Functions:**
- Async functions: `async def {verb}_{noun}()` (e.g., `async def chat()`, `async def process_document()`)
- Helper functions: `_private_helper()` for internal utilities
- Public API functions: `public_function()` without underscore prefix

## Where to Add New Code

**New API Endpoint:**
1. Handler function in `src/api/{domain}.py`
2. Route registration in `src/main.py` (add_api_route)
3. Optional service method in `src/services/{domain}_service.py`
4. Test file: colocated or in `tests/api/test_{domain}.py`

**New Service/Business Logic:**
1. Service class in `src/services/{domain}_service.py`
2. Initialization in `initialize_services()` in `src/main.py`
3. Injection via FastAPI Depends in API handlers
4. Test file: `tests/services/test_{domain}_service.py`

**New Connector/External Integration:**
1. Connector class in `src/connectors/{provider}/connector.py`
2. Auth logic in `src/connectors/{provider}/auth.py`
3. Models in `src/connectors/{provider}/models.py`
4. Register in `connection_manager.py`
5. Add routes in `src/api/connectors.py`

**New Utility Function:**
1. Utility module in `src/utils/{domain}.py`
2. Public functions at module level
3. Internal helpers prefixed with `_`
4. Test file: `tests/utils/test_{domain}.py`

**Frontend Component:**
1. New component in `frontend/components/{ComponentName}/`
2. Follow Next.js conventions (React components, hooks)
3. Colocate tests with component or in `__tests__/`

## Special Directories

**Generated Directories:**
- `keys/`: RSA key pair for JWT signing (generated at startup if missing)
- `.planning/`: GSD codebase documentation (generated by analysis)

**Excluded from Build:**
- `node_modules/`: NPM dependencies (frontend)
- `.venv/`, `venv/`: Python virtual environments
- `__pycache__/`: Python compiled files
- `.git/`: Git repository data

**Volume-Mounted (Docker):**
- `openrag-documents/`: User-uploaded documents and sample data
- `openrag-config.toml`: User configuration (encrypted)
- OpenSearch data volume: Vector database persistence

**Configuration Storage:**
- User home directory: `~/.openrag/` (config files, cache)
- Docker volume: `/app/openrag-documents` (mounted path)
- Local relative: `./openrag-documents/` (development)

---

*Structure analysis: 2026-03-20*
