---
wave: 2
depends_on:
  - 01
files_modified:
  - src/utils/langflow_headers.py
  - src/services/flows_service.py
autonomous: true
requirements_addressed: []
---

# Plan 02: Langflow Integration for Alibaba Provider

## Objective

Integrate Alibaba provider with Langflow by adding global variables for credentials and updating field mappings.

## Tasks

### Task 1: Add Alibaba Global Variables to langflow_headers.py

<read_first>
- src/utils/langflow_headers.py (full file)
</read_first>

<action>
1. In `add_provider_credentials_to_headers()` function (lines 7-36), after the Ollama section (line 36), add:

```python
# Add Alibaba credentials
if config.providers.alibaba.api_key:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY"] = str(config.providers.alibaba.api_key)

if config.providers.alibaba.endpoint:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL"] = str(config.providers.alibaba.endpoint)

if config.providers.alibaba.embedding_endpoint:
    headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL"] = str(config.providers.alibaba.embedding_endpoint)
```

2. In `build_mcp_global_vars_from_config()` function (lines 39-78), after the Ollama section (line 72), add:

```python
# Add Alibaba credentials
if hasattr(config.providers, 'alibaba'):
    if config.providers.alibaba.api_key:
        global_vars["ALIBABA_API_KEY"] = config.providers.alibaba.api_key

    if config.providers.alibaba.endpoint:
        global_vars["ALIBABA_BASE_URL"] = config.providers.alibaba.endpoint

    if config.providers.alibaba.embedding_endpoint:
        global_vars["ALIBABA_EMBEDDING_BASE_URL"] = config.providers.alibaba.embedding_endpoint
```
</action>

<acceptance_criteria>
- `add_provider_credentials_to_headers()` adds `X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY` header when api_key is set
- `add_provider_credentials_to_headers()` adds `X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL` header when endpoint is set
- `add_provider_credentials_to_headers()` adds `X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL` header when embedding_endpoint is set
- `build_mcp_global_vars_from_config()` returns dict with `ALIBABA_API_KEY`, `ALIBABA_BASE_URL`, `ALIBABA_EMBEDDING_BASE_URL` keys
</acceptance_criteria>

---

### Task 2: Add Alibaba to Field Mappings in flows_service.py

<read_first>
- src/services/flows_service.py (lines 1120-1152)
</read_first>

<action>
In `_update_component_model()` method, update the `field_mappings` dict (lines 1123-1141):

1. Add `"alibaba": "ALIBABA_API_KEY"` to the `api_key` mapping:
```python
"api_key": {
    "openai": "OPENAI_API_KEY",
    "watsonx": "WATSONX_APIKEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "alibaba": "ALIBABA_API_KEY",
},
```

2. Add `"alibaba": "ALIBABA_BASE_URL"` to the `api_base` mapping:
```python
"api_base": {
    "ollama": "OLLAMA_BASE_URL",
    "alibaba": "ALIBABA_BASE_URL",
},
```
</action>

<acceptance_criteria>
- `field_mappings["api_key"]` contains `"alibaba": "ALIBABA_API_KEY"`
- `field_mappings["api_base"]` contains `"alibaba": "ALIBABA_BASE_URL"`
</acceptance_criteria>

---

### Task 3: Add Alibaba Provider to Component Display Names

<read_first>
- src/services/flows_service.py (lines 1178-1196)
</read_first>

<action>
In `_get_provider_component_ids()` method (lines 1178-1196), add Alibaba case after the `anthropic` case:

```python
elif provider == "alibaba":
    return ("Alibaba Embeddings", "Alibaba")
```
</action>

<acceptance_criteria>
- `_get_provider_component_ids("alibaba")` returns `("Alibaba Embeddings", "Alibaba")`
</acceptance_criteria>

---

## Verification

After all tasks:
1. Verify imports work: `python -c "from src.utils.langflow_headers import add_provider_credentials_to_headers, build_mcp_global_vars_from_config"`
2. Verify field mappings: `python -c "from src.services.flows_service import FlowsService; print('ok')"`
</acceptance_criteria>

---

## must_haves

- [ ] Langflow receives `ALIBABA_API_KEY` global variable
- [ ] Langflow receives `ALIBABA_BASE_URL` global variable
- [ ] Langflow receives `ALIBABA_EMBEDDING_BASE_URL` global variable
- [ ] Field mappings include Alibaba for api_key and api_base