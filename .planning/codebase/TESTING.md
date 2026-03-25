# TESTING

## Framework

| Layer | Framework | Version | Config |
|-------|-----------|---------|--------|
| SDK integration tests | Vitest | 1.0.0 | `sdks/typescript/vitest.config.ts` |
| Frontend E2E tests | Playwright | 1.57.0 | `frontend/playwright.config.ts` |

## Test Structure

```
sdks/typescript/tests/
  integration.test.ts       # SDK integration tests against real OpenRAG instance

frontend/tests/
  core/                     # Playwright E2E specs
    *.spec.ts               # Feature-level end-to-end tests
```

## Naming Conventions

- Integration tests: `*.test.ts`
- E2E tests: `*.spec.ts`
- Tests organized in separate `tests/` directories per package

## Test Patterns

### Integration Tests (Vitest)
- Hit a real OpenRAG instance — **no mocking**
- 60-second timeout per test
- Conditional skipping via `describe.skipIf()` and `test.skip()`
- State management across suites using shared variables
- File: `sdks/typescript/tests/integration.test.ts`

### E2E Tests (Playwright)
- API mocking via Playwright route interception (`page.route()`)
- Infrastructure auto-startup via `webServer` config in `frontend/playwright.config.ts`
- 5-minute timeout for E2E suites
- Tests organized by feature in `frontend/tests/core/`

## Running Tests

```bash
# SDK integration tests
cd sdks/typescript && npm test

# Frontend E2E tests
cd frontend && npx playwright test
```

## Key Observations

- **No unit tests** — testing strategy focuses on integration and E2E
- Integration tests require a running OpenRAG instance
- E2E tests can run in isolation (Playwright manages server startup)
- Test files use `.test.ts` (Vitest) and `.spec.ts` (Playwright) extensions consistently
- No code coverage configuration found — coverage not enforced
