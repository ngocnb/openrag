# Architecture

**Analysis Date:** 2026-03-20

## System Overview

OpenRAG is a comprehensive Retrieval-Augmented Generation (RAG) platform that enables intelligent document search and AI-powered conversations. It is an open-source package for building agentic RAG systems that integrates with orchestration tools, vector databases, and LLM providers. The system utilizes Langflow for document ingestion workflows, OpenSearch for semantic search, and Docling for intelligent document processing.

**Architectural Style:** Layered service-oriented architecture with a clear separation between API layer, business logic (services), data persistence, and external integrations.

## Architectural Layers

The system follows a classic layered architecture with five main layers:

**1. API Layer (`src/api/`)**
- REST endpoints that handle HTTP requests
- Two API versions: internal endpoints and public v1 API
- Internal endpoints: chat, search, documents, connectors, settings, authentication
- Public v1 endpoints: require API key authentication
- Framework: FastAPI (async-first)

**2. Service Layer (`src/services/`)**
- Business logic implementation
- Services: `DocumentService`, `ChatService`, `SearchService`, `TaskService`, `AuthService`, `FlowsService`, `ModelsService`, `KnowledgeFilterService`, `LangflowFileService`, `MonitorService`
- Handles orchestration between API layer and data layer
- Manages workflow coordination (e.g., document ingestion, chat interactions)

**3. Model/Data Processing Layer (`src/models/`, `src/config/`)**
- Data models and processors
- `DocumentFileProcessor`: handles document ingestion and chunking
- Configuration management via `ConfigManager`
- Task definitions for async operations

**4. Integration Layer (`src/connectors/`, `src/utils/`)**
- External service integrations
- Connectors: AWS S3, IBM COS, Google Drive, OneDrive, SharePoint
- Utilities: embeddings, OpenSearch queries, encryption, telemetry, document processing (Docling)
- Langflow integration for advanced ingestion workflows

**5. Data Storage Layer**
- OpenSearch: vector database for semantic search and knowledge storage
- File storage: local filesystem, AWS S3, IBM COS
- Session management: in-memory user sessions and JWT token handling
- Conversation persistence: disk-based storage for chat history

## Key Components

**FastAPI Application** (`src/main.py`)
- Entry point for the REST API
- Initializes all services and dependencies
- Registers API routes for both internal and public endpoints
- Manages startup/shutdown lifecycle and background tasks

**Authentication & Session Management** (`src/session_manager.py`)
- JWT token management with RSA key signing
- User session tracking
- Support for OAuth (Google, Azure/Microsoft, custom OIDC)
- Anonymous user support for no-auth mode
- Per-user OpenSearch client isolation for multi-tenancy

**Document Ingestion Pipeline**
- **Traditional Path**: `DocumentService` → `DocumentFileProcessor` → OpenSearch (embeddings via configured provider)
- **Langflow Path**: `LangflowFileService` → Langflow flow execution → OpenSearch via Langflow component
- Supports multiple embedding providers: OpenAI, IBM WatsonX, Ollama, Anthropic
- Document processing via Docling with OCR support

**Chat & Conversation System**
- **Agent-driven chat**: `agent.py` with MCP (Model Context Protocol) support
- **Langflow-based chat**: Direct integration with Langflow chat flows
- **Conversation persistence**: In-memory thread storage with disk-based metadata
- Conversation branching via `previous_response_id`
- Knowledge filter integration for context-aware responses

**Connector System** (`src/connectors/`)
- Abstract base: `ConnectorService` (traditional ingestion) and `LangflowConnectorService`
- Provider implementations: AWS S3, IBM COS, Google Drive, OneDrive, SharePoint
- Connection management with OAuth flows
- Webhook-based sync for real-time document updates
- Router pattern: `ConnectorRouter` selects between Langflow and traditional connector service

**Configuration Management** (`src/config/`)
- Runtime configuration via `ConfigManager` (persisted to config file)
- Environment-based settings (embeddings model, providers, flow IDs)
- Onboarding state tracking (embedding model selection, sample data ingestion)
- Provider credentials management

## Data Flow

### Document Ingestion Flow

```
User Upload
    ↓
API Endpoint (/upload_context, /upload_path)
    ↓
ConnectorRouter decides: Langflow or Traditional?
    ↓
[Langflow Path]                    [Traditional Path]
  ↓                                  ↓
LangflowFileService              DocumentFileProcessor
  ↓                                  ↓
Upload to Langflow               Docling (PDF parsing/OCR)
  ↓                                  ↓
Langflow Ingest Flow            Document Chunking
  ↓                                  ↓
Embedding via Flow Component    Get Embeddings (OpenAI/IBM/Ollama)
  ↓                                  ↓
OpenSearch Index                 OpenSearch Index
```

### Chat/Query Flow

```
User Query
    ↓
API: /chat or /langflow (Langflow-based)
    ↓
ChatService.chat() or ChatService.langflow_chat()
    ↓
[MCP Agent Path]                 [Langflow Direct Path]
  ↓                                  ↓
agent.async_chat()              async_langflow() request
  ↓                                  ↓
OpenAI/Anthropic LLM            Langflow Flow Execution
+ MCP tools (search, etc)          ↓
  ↓                                  ↓
Tool Results (OpenSearch)       Langflow Components
  ↓                                  ↓
Generate Response                Response
```

### Search Flow

```
Search Query
    ↓
API: /search (internal) or /v1/search (public)
    ↓
SearchService.search()
    ↓
OpenSearch Semantic Search
(vector + BM25 hybrid search)
    ↓
Filter by Knowledge Filter (if specified)
    ↓
Return Results + Sources
```

## Design Patterns

**Service Locator Pattern**
- Centralized `clients` object (`config.settings.clients`) provides access to:
  - OpenSearch client
  - Langflow HTTP client
  - OpenAI/Anthropic LLM client (with MCP patching)

**Dependency Injection**
- FastAPI's `Depends()` system injects authenticated user context
- Services receive dependencies via constructor injection

**Router/Strategy Pattern**
- `ConnectorRouter`: routes between `LangflowConnectorService` and `ConnectorService`
- Selects ingestion strategy based on configuration

**Factory Pattern**
- Dynamic index body creation via `create_dynamic_index_body()` based on embedding model dimensions

**Observer Pattern**
- Webhook subscriptions for connector syncs (OneDrive, Google Drive, SharePoint)

**Session/Context Pattern**
- Thread-local `auth_context` for passing authentication info through the call stack
- Per-user OpenSearch clients for data isolation

**Background Task Processing**
- Async task queue via `TaskService` with progress tracking
- Cleanup scheduler for expired tasks
- Periodic flow backup every 5 minutes

## Module Boundaries

**API Module** → **Service Module**
- API endpoints call service methods via FastAPI dependency injection
- Services provide single-responsibility methods (chat, search, ingestion, etc.)
- Request validation and error handling at API boundary

**Service Module** → **Integration Layer**
- Services use utilities for domain logic (document processing, OpenSearch queries)
- Connectors provide external source abstraction
- Config provides runtime configuration

**Integration Layer → Data Storage**
- OpenSearch client calls go through async connection pool
- File uploads stored in configured provider (local/S3/IBM COS)
- Session data serialized to disk as needed

**Session Management** → All Layers
- JWT tokens validated at API layer via `dependencies.py`
- User context available to all services via `session_manager`
- OpenSearch queries automatically scoped to user's data

## External Dependencies

**LLM Providers**
- OpenAI: primary chat/embedding provider
- Anthropic: alternative chat provider
- IBM WatsonX: embedding and chat models
- Ollama: local embedding inference

**Search & Vector Store**
- OpenSearch: vector database (KNN search via disk_ann algorithm)
- Supports multi-embedding model indexes (dynamic field mapping)

**Orchestration & Workflows**
- Langflow: advanced document ingestion, chat flows, MCP server generation
- Direct API integration via HTTP (customizable with global variables)

**Document Processing**
- Docling: PDF/DOCX/PPTX parsing with OCR via Tesseract
- Rich document understanding for accurate chunking

**Cloud Storage**
- AWS S3: file storage and connector source
- IBM COS: alternative cloud object storage
- Local filesystem: default file storage

**Authentication & OAuth**
- Google OAuth: user authentication
- Azure/Microsoft: OneDrive and SharePoint OAuth
- OIDC: custom identity provider support
- JWT: internal token generation and validation

**Telemetry**
- Custom telemetry client for event tracking (disabled by default in community builds)
- Event categories: application startup, document ingestion, OpenSearch operations, etc.

**Additional Libraries**
- FastAPI/Uvicorn: HTTP server framework
- Textual: TUI (terminal UI) for local installation
- Structlog: structured logging
- Cryptography: encryption for configuration files
- IBM Secrets Manager SDK: enterprise credential management

---

*Architecture analysis: 2026-03-20*
