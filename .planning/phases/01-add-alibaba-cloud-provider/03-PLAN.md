---
wave: 3
depends_on:
  - 01
  - 02
files_modified:
  - src/api/settings.py
  - frontend/app/settings/page.tsx
autonomous: true
requirements_addressed: []
---

# Plan 03: API Settings and Frontend for Alibaba Provider

## Objective

Add Alibaba provider support to the Settings API and frontend UI.

## Tasks

### Task 1: Update Settings API Provider Validation

<read_first>
- src/api/settings.py (lines 50-51, 68-69)
</read_first>

<action>
Update the `embedding_provider` field patterns to include `alibaba`:
```python
embedding_provider: Optional[str] = Field(None, pattern="^(openai|watsonx|ollama|alibaba)$")
```

This appears in two places in the file (around lines 51 and 69).
</action>

<acceptance_criteria>
- Both `embedding_provider` field patterns include `alibaba`
</acceptance_criteria>

---

### Task 2: Add Alibaba to Frontend Settings Page

<read_first>
- frontend/app/settings/page.tsx (lines 204-226)
</read_first>

<action>
Add Alibaba to `groupedEmbeddingModels` array after WatsonX:

```tsx
{
  group: "Alibaba",
  provider: "alibaba",
  icon: getModelLogo("", "alibaba"),
  models: alibabaModels?.embedding_models || [],
  configured: settings.providers?.alibaba?.configured === true,
},
```

Also add similar entry to the LLM models grouping.
</action>

<acceptance_criteria>
- Settings page includes Alibaba in embedding models dropdown
- Settings page includes Alibaba in LLM models dropdown
- Alibaba shows "Configured" badge when `settings.providers.alibaba.configured` is true
</acceptance_criteria>

---

## must_haves

- [ ] API accepts `alibaba` as valid embedding_provider
- [ ] Frontend displays Alibaba as provider option
- [ ] Frontend shows configured status for Alibaba provider

---

## Notes

- Frontend components for Alibaba settings form and onboarding should be created following existing patterns (openai-settings-form.tsx, openai-onboarding.tsx)
- Add Alibaba logo/icon to assets if available