# TESTING

## Framework

| Layer | Framework | Version | Config |
|-------|-----------|---------|--------|
| Backend unit tests | pytest | 9.0.2 | `pyproject.toml` |
| Frontend unit tests | Vitest | 4.1.1 | `frontend/vitest.config.ts` |
| Frontend E2E tests | Playwright | 1.57.0 | `frontend/playwright.config.ts` |
| SDK integration tests | Vitest | 1.0.0 | `sdks/typescript/vitest.config.ts` |

## Test Structure

```
tests/
  unit/                    # pytest unit tests
    test_*.py              # Backend unit tests
  integration/             # pytest integration tests
    sdk/                   # SDK integration tests
    core/                  # Core integration tests

frontend/tests/
  unit/                    # Vitest unit tests
    *.test.ts(x)           # Frontend unit tests
  core/                    # Playwright E2E specs
    *.spec.ts              # Feature-level end-to-end tests

sdks/typescript/tests/
  integration.test.ts      # SDK integration tests against real OpenRAG instance
```

## Naming Conventions

- Backend unit tests: `tests/unit/test_*.py`
- Frontend unit tests: `frontend/tests/unit/*.test.ts(x)`
- E2E tests: `frontend/tests/core/*.spec.ts`
- Integration tests: `*.test.ts` (SDK)

## Test Patterns

### Backend Unit Tests (pytest)
- Test individual functions and classes in isolation
- Use fixtures for common setup (`tests/unit/conftest.py`)
- Mock external dependencies (APIs, databases)
- Run: `source .venv/bin/activate && python -m pytest tests/unit/ -v`

### Frontend Unit Tests (Vitest)
- React Testing Library for component and hook testing
- Mock fetch and external APIs
- React Query wrapper for hook tests
- Run: `cd frontend && npm run test`

### Integration Tests (Vitest)
- Hit a real OpenRAG instance — **no mocking**
- 60-second timeout per test
- Conditional skipping via `describe.skipIf()` and `test.skip()`

### E2E Tests (Playwright)
- API mocking via Playwright route interception (`page.route()`)
- Infrastructure auto-startup via `webServer` config
- 5-minute timeout for E2E suites
- Tests organized by feature in `frontend/tests/core/`

## Running Tests

```bash
# Backend unit tests
source .venv/bin/activate && python -m pytest tests/unit/ -v

# Frontend unit tests
cd frontend && npm run test

# Frontend E2E tests
cd frontend && npx playwright test

# SDK integration tests
cd sdks/typescript && npm test
```

## Night Shift Test Generation

**CRITICAL:** Tests MUST be written BEFORE implementation (Step 5 of AGENT_LOOPS.md).

When implementing a new feature, generate tests in this order:

1. **Backend Unit Tests** (`tests/unit/test_{feature}.py`)
   - Test dataclasses, utility functions, configuration
   - Test API validation patterns
   - Mock external dependencies

2. **Frontend Unit Tests** (`frontend/tests/unit/{feature}.test.tsx`)
   - Test React hooks with React Query wrapper
   - Test TypeScript types/interfaces
   - Mock fetch for API calls

3. **E2E Tests** (`frontend/tests/core/{feature}.spec.ts`)
   - Test user workflows in browser
   - Use Playwright route mocking for API responses
   - Test visibility and interaction

### Test Template Files

- Backend: `tests/unit/test_alibaba_config.py` (reference)
- Frontend hooks: `frontend/tests/unit/alibaba-models-query.test.tsx` (reference)
- E2E: `frontend/tests/core/alibaba-provider.spec.ts` (reference)

## Key Observations

- **Unit tests are required** — not just integration/E2E
- Backend tests use pytest with fixtures in `conftest.py`
- Frontend tests use Vitest with React Testing Library
- E2E tests can run in isolation (Playwright manages server startup)
- No code coverage configuration found — coverage not enforced