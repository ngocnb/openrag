# Phase 1: Add Alibaba Cloud Provider - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning
**Source:** Spec file `.planning/specs/2026-03-25-add-alibaba-provider.md`

<domain>
## Phase Boundary

Add Alibaba Cloud as a new LLM provider with separate embedding configuration using OpenAI-compatible API mode.

**In scope:**
- Backend: config_manager.py, settings.py, embeddings.py, langflow_headers.py, flows_service.py, api/settings.py
- Frontend: settings page, onboarding, model helpers
- Configuration: config.yaml, .env.example

**Out of scope:**
- Custom Langflow components (not needed — OpenAI-compatible)
- Fine-tuning or custom model support
- Alibaba-specific features beyond OpenAI compatibility

</domain>

<decisions>
## Implementation Decisions

### Provider Configuration
- Use OpenAI-compatible API mode for both chat and embeddings
- Chat base URL: `https://coding-intl.dashscope.aliyuncs.com/v1`
- Embedding base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- Chat models: `glm-5`, `kimi-k2.5`, `qwen3.5-plus`, `MiniMax-M2.5`
- Embedding models: `text-embedding-v3` (1024 dims), `text-embedding-v4` (2048 dims)

### Backend Architecture
- Add `AlibabaConfig` dataclass to `config/config_manager.py`
- Add `alibaba` field to `ProvidersConfig`
- Load credentials in `settings.py:patched_async_client` property
- Add dimension mappings to `embeddings.py`
- Pass credentials via `langflow_headers.py` global variables
- Update field mappings in `flows_service.py`
- Add provider validation in `api/settings.py`

### Frontend Components
- Add Alibaba to settings page provider list
- Create Alibaba settings form component
- Add Alibaba to onboarding flow
- Add Alibaba logo/icon
- Update model helpers with Alibaba models

### Langflow Integration
- NO custom components needed (OpenAI-compatible)
- Pass `ALIBABA_API_KEY`, `ALIBABA_BASE_URL`, `ALIBABA_EMBEDDING_BASE_URL` as global variables

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Provider Pattern References
- `src/config/config_manager.py` — Existing provider config pattern (OpenAIConfig, AnthropicConfig, WatsonXConfig, OllamaConfig)
- `src/config/settings.py` — Credential loading pattern (lines 476-510)
- `src/utils/embeddings.py` — Dimension lookup pattern
- `src/utils/langflow_headers.py` — Global variable passing pattern
- `src/services/flows_service.py` — Field mapping pattern (lines 1123-1141)
- `src/api/settings.py` — Settings API pattern

### Frontend References
- `frontend/app/settings/page.tsx` — Settings page pattern
- `frontend/app/settings/_components/openai-settings-form.tsx` — Provider settings form pattern
- `frontend/app/onboarding/_components/openai-onboarding.tsx` — Onboarding pattern

### Spec Document
- `.planning/specs/2026-03-25-add-alibaba-provider.md` — Full implementation spec

</canonical_refs>

<specifics>
## Specific Ideas

### API Endpoints
- Chat: `https://coding-intl.dashscope.aliyuncs.com/v1`
- Embeddings: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

### Models to Support
- Chat: `glm-5`, `kimi-k2.5`, `qwen3.5-plus`, `MiniMax-M2.5`
- Embeddings: `text-embedding-v3` (1024), `text-embedding-v4` (2048)

### Config Structure
```yaml
providers:
  alibaba:
    api_key: ""
    endpoint: "https://coding-intl.dashscope.aliyuncs.com/v1"
    embedding_endpoint: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    configured: false
```

### Langflow Global Variables
- `ALIBABA_API_KEY` — API authentication
- `ALIBABA_BASE_URL` — Chat endpoint
- `ALIBABA_EMBEDDING_BASE_URL` — Embedding endpoint

</specifics>

<deferred>
## Deferred Ideas

None — spec covers phase scope completely.

</deferred>

---

*Phase: 01-add-alibaba-cloud-provider*
*Context gathered: 2026-03-25 via spec extraction*