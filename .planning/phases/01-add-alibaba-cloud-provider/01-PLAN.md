---
wave: 1
depends_on: []
files_modified:
  - src/config/config_manager.py
  - src/config/settings.py
  - src/utils/embeddings.py
autonomous: true
requirements_addressed: []
---

# Plan 01: Backend Configuration for Alibaba Provider

## Objective

Add Alibaba provider configuration infrastructure to the backend, including config dataclass, dimension mappings, and credential loading.

## Tasks

### Task 1: Add AlibabaConfig Dataclass

<read_first>
- src/config/config_manager.py (lines 13-41, 44-64)
</read_first>

<action>
1. After line 41 (after `OllamaConfig`), add a new dataclass:

```python
@dataclass
class AlibabaConfig:
    """Alibaba Cloud provider configuration."""
    api_key: str = ""
    endpoint: str = "https://coding-intl.dashscope.aliyuncs.com/v1"
    embedding_endpoint: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    configured: bool = False
```

2. In `ProvidersConfig` class (line 44-50), add `alibaba: AlibabaConfig` field after `ollama: OllamaConfig`.

3. In `get_provider_config()` method (lines 52-64), add:
```python
elif provider_lower == "alibaba":
    return self.alibaba
```

4. In `OpenRAGConfig.from_dict()` method (lines 129-134), add to the `ProvidersConfig` initialization:
```python
alibaba=AlibabaConfig(**_decrypt_provider(providers_data.get("alibaba", {}))),
```

5. In `load_config()` method (lines 180-191), add `"alibaba": {}` to the providers dict.

6. In the file config merge loop (line 204), add `"alibaba"` to the provider list.
</action>

<acceptance_criteria>
- `config_manager.py` contains `class AlibabaConfig` with fields: api_key, endpoint, embedding_endpoint, configured
- `ProvidersConfig` class has `alibaba: AlibabaConfig` field
- `get_provider_config("alibaba")` returns the alibaba config
- `OpenRAGConfig.from_dict()` creates AlibabaConfig from dict
- Config loading includes `"alibaba": {}` default
</acceptance_criteria>

---

### Task 2: Add Environment Variable Loading for Alibaba

<read_first>
- src/config/config_manager.py (lines 238-296)
</read_first>

<action>
In `_load_env_overrides()` method, after the Ollama provider settings (around line 266), add:

```python
# Alibaba provider settings
if os.getenv("ALIBABA_API_KEY"):
    config_data["providers"]["alibaba"]["api_key"] = os.getenv("ALIBABA_API_KEY")
if os.getenv("ALIBABA_ENDPOINT"):
    config_data["providers"]["alibaba"]["endpoint"] = os.getenv("ALIBABA_ENDPOINT")
if os.getenv("ALIBABA_EMBEDDING_ENDPOINT"):
    config_data["providers"]["alibaba"]["embedding_endpoint"] = os.getenv("ALIBABA_EMBEDDING_ENDPOINT")
```
</action>

<acceptance_criteria>
- `_load_env_overrides()` method handles `ALIBABA_API_KEY`, `ALIBABA_ENDPOINT`, `ALIBABA_EMBEDDING_ENDPOINT` env vars
- Env vars map to `config_data["providers"]["alibaba"]` fields
</acceptance_criteria>

---

### Task 3: Add Alibaba Embedding Dimensions

<read_first>
- src/config/settings.py (lines 118-140)
- src/utils/embeddings.py (lines 114-137)
</read_first>

<action>
1. In `settings.py`, after `WATSONX_EMBEDDING_DIMENSIONS` (around line 140), add:

```python
ALIBABA_EMBEDDING_DIMENSIONS = {
    "text-embedding-v3": 1024,
    "text-embedding-v4": 2048,
}
```

2. In `embeddings.py`, update the `get_embedding_dimensions()` function (line 125):
```python
all_models = {**OPENAI_EMBEDDING_DIMENSIONS, **WATSONX_EMBEDDING_DIMENSIONS, **ALIBABA_EMBEDDING_DIMENSIONS}
```

3. Add import at top of `embeddings.py`:
```python
from config.settings import KNN_EF_CONSTRUCTION, KNN_M, OPENAI_EMBEDDING_DIMENSIONS, VECTOR_DIM, WATSONX_EMBEDDING_DIMENSIONS, ALIBABA_EMBEDDING_DIMENSIONS
```
</action>

<acceptance_criteria>
- `settings.py` contains `ALIBABA_EMBEDDING_DIMENSIONS` dict with `text-embedding-v3: 1024` and `text-embedding-v4: 2048`
- `embeddings.py` imports `ALIBABA_EMBEDDING_DIMENSIONS`
- `get_embedding_dimensions()` includes Alibaba models in lookup
</acceptance_criteria>

---

### Task 4: Add Alibaba Credential Loading in settings.py

<read_first>
- src/config/settings.py (lines 476-510)
</read_first>

<action>
In `patched_async_client` property, after the Ollama endpoint loading (around line 510), add:

```python
# Set Alibaba credentials
if config.providers.alibaba.api_key:
    os.environ["ALIBABA_API_KEY"] = config.providers.alibaba.api_key
    logger.debug("Loaded Alibaba API key from config")
if config.providers.alibaba.endpoint:
    os.environ["ALIBABA_BASE_URL"] = config.providers.alibaba.endpoint
if config.providers.alibaba.embedding_endpoint:
    os.environ["ALIBABA_EMBEDDING_BASE_URL"] = config.providers.alibaba.embedding_endpoint
```
</action>

<acceptance_criteria>
- `patched_async_client` property sets `ALIBABA_API_KEY`, `ALIBABA_BASE_URL`, `ALIBABA_EMBEDDING_BASE_URL` env vars from config
- Debug log message is logged when API key is loaded
</acceptance_criteria>

---

## Verification

After all tasks:
1. Run `python -c "from src.config.config_manager import AlibabaConfig; c = AlibabaConfig(api_key='test'); print(c)"`
2. Verify no import errors
3. Verify dimension lookup: `python -c "from src.utils.embeddings import get_embedding_dimensions; import asyncio; print(asyncio.run(get_embedding_dimensions('text-embedding-v3')))"`