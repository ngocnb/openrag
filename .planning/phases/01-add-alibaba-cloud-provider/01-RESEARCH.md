# Phase 1: Add Alibaba Cloud Provider - Research

**Date:** 2026-03-25

## 1. Existing Provider Architecture Analysis

### Provider Config Pattern (config_manager.py)

Each provider has a dataclass with specific fields:

| Provider | Fields | Lines |
|----------|--------|-------|
| OpenAIConfig | `api_key`, `configured` | 14-17 |
| AnthropicConfig | `api_key`, `configured` | 20-24 |
| WatsonXConfig | `api_key`, `endpoint`, `project_id`, `configured` | 27-33 |
| OllamaConfig | `endpoint`, `resolved_endpoint`, `configured` | 36-41 |

**Pattern for Alibaba:**
- Need `api_key`, `endpoint`, `embedding_endpoint`, `configured`
- Similar to WatsonX (has multiple URLs) but with separate embedding endpoint

### ProvidersConfig Registration (config_manager.py:44-64)

- Add `alibaba: AlibabaConfig` to `ProvidersConfig` (line 50)
- Add `alibaba` case to `get_provider_config()` method (lines 52-64)
- Add `alibaba` to `OpenRAGConfig.from_dict()` (lines 129-134)

### Environment Variable Loading (config_manager.py:238-266)

Add to `_load_env_overrides()`:
- `ALIBABA_API_KEY` → `config_data["providers"]["alibaba"]["api_key"]`
- `ALIBABA_ENDPOINT` → `config_data["providers"]["alibaba"]["endpoint"]`
- `ALIBABA_EMBEDDING_ENDPOINT` → `config_data["providers"]["alibaba"]["embedding_endpoint"]`

### Credential Loading (settings.py:476-510)

In `patched_async_client` property, add:
```python
if config.providers.alibaba.api_key:
    os.environ["ALIBABA_API_KEY"] = config.providers.alibaba.api_key
if config.providers.alibaba.endpoint:
    os.environ["ALIBABA_BASE_URL"] = config.providers.alibaba.endpoint
```

## 2. Langflow Integration

### Global Variables (langflow_headers.py)

Two functions to update:
1. `add_provider_credentials_to_headers()` (lines 7-36)
2. `build_mcp_global_vars_from_config()` (lines 39-78)

Add:
- `X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY`
- `X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL`
- `X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL`

### Field Mappings (flows_service.py:1123-1141)

Add to `field_mappings`:
```python
"api_key": {
    "openai": "OPENAI_API_KEY",
    "watsonx": "WATSONX_APIKEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "alibaba": "ALIBABA_API_KEY",  # ADD
},
"api_base": {
    "ollama": "OLLAMA_BASE_URL",
    "alibaba": "ALIBABA_BASE_URL",  # ADD
},
```

## 3. Embedding Dimension Mapping

### Current Pattern (embeddings.py:114-137)

- `OPENAI_EMBEDDING_DIMENSIONS` dict in settings.py
- `WATSONX_EMBEDDING_DIMENSIONS` dict in settings.py
- `get_embedding_dimensions()` function merges them

### For Alibaba

Add to settings.py:
```python
ALIBABA_EMBEDDING_DIMENSIONS = {
    "text-embedding-v3": 1024,
    "text-embedding-v4": 2048,
}
```

Update embeddings.py:
```python
all_models = {**OPENAI_EMBEDDING_DIMENSIONS, **WATSONX_EMBEDDING_DIMENSIONS, **ALIBABA_EMBEDDING_DIMENSIONS}
```

## 4. API Settings Changes

### Provider Validation Pattern (api/settings.py:50-51)

Update regex pattern:
```python
embedding_provider: Optional[str] = Field(None, pattern="^(openai|watsonx|ollama|alibaba)$")
```

### Settings Schemas

Add fields for Alibaba:
- `alibaba_api_key: Optional[str]`
- `alibaba_endpoint: Optional[str]`
- `alibaba_embedding_endpoint: Optional[str]`

### Provider Configuration Endpoints

Update the settings save logic to handle `alibaba` provider.

## 5. Frontend Components

### Settings Page (frontend/app/settings/page.tsx)

Pattern from lines 204-226 shows embedding model grouping:
```tsx
const groupedEmbeddingModels = [
  { group: "OpenAI", provider: "openai", ... },
  { group: "Ollama", provider: "ollama", ... },
  { group: "WatsonX", provider: "watsonx", ... },
  // ADD: { group: "Alibaba", provider: "alibaba", ... }
];
```

### Settings Form Pattern

Reference `openai-settings-form.tsx` or `watsonx-settings-dialog.tsx` for form structure.

### Onboarding Pattern

Reference `openai-onboarding.tsx` for provider onboarding flow.

## 6. Key Files to Modify

| File | Changes |
|------|---------|
| `src/config/config_manager.py` | Add AlibabaConfig, update ProvidersConfig, update from_dict |
| `src/config/settings.py` | Add ALIBABA_EMBEDDING_DIMENSIONS, update patched_async_client |
| `src/utils/embeddings.py` | Add Alibaba to dimension lookup |
| `src/utils/langflow_headers.py` | Add Alibaba global variables |
| `src/services/flows_service.py` | Add Alibaba to field_mappings |
| `src/api/settings.py` | Add Alibaba validation, schemas, endpoint handling |
| `frontend/app/settings/page.tsx` | Add Alibaba to provider list |
| `frontend/app/settings/_components/` | Create alibaba-settings-form.tsx |
| `frontend/app/onboarding/_components/` | Create alibaba-onboarding.tsx |

## 7. Edge Cases & Gotchas

1. **Separate Embedding URL**: Alibaba uses different URLs for chat vs embeddings. Must handle both in config and Langflow headers.

2. **OpenAI-Compatible Mode**: No custom Langflow components needed. Use `ALIBABA_BASE_URL` to override the OpenAI client's base URL.

3. **API Key Encryption**: The `api_key` field must be encrypted/decrypted like other providers.

4. **Model Validation**: Need to validate that the specified models work with Alibaba's API.

5. **Dimension Mapping**: `text-embedding-v3` has 1024 dimensions, `text-embedding-v4` has 2048. Must be correctly mapped.

## 8. Validation Architecture

### Unit Tests
- Test `AlibabaConfig` dataclass creation and serialization
- Test `get_embedding_dimensions()` returns correct values for Alibaba models
- Test config encryption/decryption for Alibaba API key

### Integration Tests
- Test settings API accepts Alibaba configuration
- Test embedding validation endpoint works with Alibaba provider
- Test Langflow global variables are set correctly

### Manual Verification
- Verify Alibaba appears in Settings UI
- Verify API key can be saved and retrieved
- Verify embedding dimension is detected correctly
- Verify chat works with Alibaba models

---

*Research completed: 2026-03-25*