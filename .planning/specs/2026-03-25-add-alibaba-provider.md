# What

Add Alibaba Cloud as a new LLM provider with separate embedding configuration.

## Chat/LLM Provider

- Uses OpenAI-compatible API
- Base URL: `https://coding-intl.dashscope.aliyuncs.com/v1`
- Models: `glm-5`, `kimi-k2.5`, `qwen3.5-plus`, `MiniMax-M2.5`

## Embedding Provider

- Uses OpenAI-compatible API
- Base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- Models: `text-embedding-v3` (1024 dimensions), `text-embedding-v4` (2048 dimensions)

---

# Why OpenAI-Compatible Mode Works

Alibaba's DashScope API is OpenAI-compatible. This means:

- **No custom Langflow components needed**
- Existing OpenAI-compatible flow components work with `ALIBABA_API_KEY` and `ALIBABA_BASE_URL` global variables
- LiteLLM can route requests based on model name or explicit configuration

---

# Research

## Current Provider Architecture

| Component | File | Purpose |
|-----------|------|---------|
| Config dataclass | `config/config_manager.py` | `OpenAIConfig`, `AnthropicConfig`, `WatsonXConfig`, `OllamaConfig` |
| Credential loading | `config/settings.py:476-510` | Sets env vars for LiteLLM routing |
| Dimension lookup | `utils/embeddings.py` | Hardcoded dimension mappings |
| Langflow headers | `utils/langflow_headers.py` | Passes credentials as global vars |
| Field mappings | `services/flows_service.py:1123-1141` | Maps provider fields to global vars |

## Embedding Configuration Flow

```
Frontend Settings → config.yaml → config_manager.py → patched_async_client (LiteLLM)
                                    ↓
                        langflow_headers.py (global vars for flows)
```

## Langflow Global Variables Needed

| Variable | Purpose |
|----------|---------|
| `ALIBABA_API_KEY` | API authentication |
| `ALIBABA_BASE_URL` | Custom endpoint for chat |
| `ALIBABA_EMBEDDING_BASE_URL` | Separate endpoint for embeddings |

---

# How

## Backend Changes

### 1. Add AlibabaConfig (`config/config_manager.py`)

```python
@dataclass
class AlibabaConfig:
    """Alibaba Cloud provider configuration."""
    api_key: str = ""
    endpoint: str = "https://coding-intl.dashscope.aliyuncs.com/v1"
    embedding_endpoint: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    configured: bool = False
```

### 2. Add to ProvidersConfig (`config/config_manager.py`)

```python
@dataclass
class ProvidersConfig:
    openai: OpenAIConfig
    anthropic: AnthropicConfig
    watsonx: WatsonXConfig
    ollama: OllamaConfig
    alibaba: AlibabaConfig  # ADD
```

### 3. Add credential loading (`config/settings.py:patched_async_client`)

```python
# Set Alibaba credentials
if config.providers.alibaba.api_key:
    os.environ["ALIBABA_API_KEY"] = config.providers.alibaba.api_key
if config.providers.alibaba.endpoint:
    os.environ["ALIBABA_BASE_URL"] = config.providers.alibaba.endpoint
```

### 4. Add dimension mappings (`config/settings.py`)

```python
ALIBABA_EMBEDDING_DIMENSIONS = {
    "text-embedding-v3": 1024,
    "text-embedding-v4": 2048,
}
```

### 5. Update embeddings.py

- Add `ALIBABA_EMBEDDING_DIMENSIONS` to dimension lookup
- Update `get_embedding_dimensions()` to include Alibaba

### 6. Update langflow_headers.py

```python
# Add Alibaba credentials
if config.providers.alibaba.api_key:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY"] = str(config.providers.alibaba.api_key)
if config.providers.alibaba.endpoint:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL"] = str(config.providers.alibaba.endpoint)
if config.providers.alibaba.embedding_endpoint:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL"] = str(config.providers.alibaba.embedding_endpoint)
```

### 7. Update flows_service.py field mappings

```python
field_mappings = {
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
    # ...
}
```

### 8. Update api/settings.py

- Add `alibaba` to embedding provider validation pattern
- Add Alibaba API key/endpoint fields to settings schemas
- Handle Alibaba provider in provider configuration endpoints

## Frontend Changes

### 1. Add Alibaba to settings page (`frontend/app/settings/page.tsx`)

```tsx
const groupedEmbeddingModels = [
  // ... existing providers
  {
    group: "Alibaba",
    provider: "alibaba",
    icon: getModelLogo("", "alibaba"),
    models: alibabaModels?.embedding_models || [],
    configured: settings.providers?.alibaba?.configured === true,
  },
];
```

### 2. Create Alibaba settings form (`frontend/app/settings/_components/alibaba-settings-form.tsx`)

- API key input
- Endpoint URL (pre-filled with default)
- Embedding endpoint URL (pre-filled with default)

### 3. Add Alibaba to onboarding (`frontend/app/onboarding/_components/`)

- Add Alibaba as provider option
- Create `alibaba-onboarding.tsx` component

### 4. Add Alibaba logo/icon

### 5. Update model helpers (`frontend/app/settings/_helpers/model-helpers.tsx`)

- Add Alibaba model lists
- Add provider detection logic

## Configuration Files

### config.yaml

```yaml
providers:
  alibaba:
    api_key: ""
    endpoint: "https://coding-intl.dashscope.aliyuncs.com/v1"
    embedding_endpoint: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    configured: false
```

### .env.example

```bash
# Alibaba Cloud (DashScope)
ALIBABA_API_KEY=
ALIBABA_ENDPOINT=https://coding-intl.dashscope.aliyuncs.com/v1
ALIBABA_EMBEDDING_ENDPOINT=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

---

# Acceptance Criteria

## Onboarding

- [ ] Alibaba appears as a provider option in onboarding
- [ ] User can enter API key
- [ ] User can select from models: `qwen3.5-plus`, `kimi-k2.5`, `glm-5`, `MiniMax-M2.5`
- [ ] API key validation works before proceeding

## Settings

- [ ] Alibaba section appears in Settings page
- [ ] User can update API key
- [ ] User can modify endpoint URLs (advanced)
- [ ] "Configured" badge shows when API key is set

## Embedding

- [ ] Alibaba appears in embedding provider dropdown
- [ ] User can select embedding models: `text-embedding-v3`, `text-embedding-v4`
- [ ] Embedding dimension is correctly detected (1024 or 2048)
- [ ] Documents ingest successfully with Alibaba embeddings

## Chat/LLM

- [ ] Chat works with Alibaba models
- [ ] Model selection dropdown includes Alibaba models
- [ ] Error messages are clear when API key is missing/invalid

## Langflow Integration

- [ ] Global variables `ALIBABA_API_KEY`, `ALIBABA_BASE_URL`, `ALIBABA_EMBEDDING_BASE_URL` are set
- [ ] Flows using OpenAI-compatible components work with Alibaba

---

# Test Cases

## Unit Tests

- [ ] `AlibabaConfig` dataclass serializes/deserializes correctly
- [ ] `get_embedding_dimensions()` returns correct values for Alibaba models
- [ ] Config encryption/decryption works for Alibaba API key

## Integration Tests

- [ ] Settings API accepts and saves Alibaba configuration
- [ ] Embedding validation endpoint works with Alibaba
- [ ] Chat endpoint works with Alibaba models (mock or real API)

## E2E Tests

- [ ] Full onboarding flow with Alibaba provider
- [ ] Document ingestion with Alibaba embeddings
- [ ] Chat conversation with Alibaba LLM

---

# Out of Scope

- Custom Langflow components (not needed — OpenAI-compatible)
- Fine-tuning or custom model support
- Alibaba-specific features beyond OpenAI compatibility