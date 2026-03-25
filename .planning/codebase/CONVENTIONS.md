# Coding Conventions

**Analysis Date:** 2026-03-20

## Naming Patterns

**Files:**
- TypeScript SDK: kebab-case for files (`client.ts`, `chat.ts`, `search.ts`, `knowledge-filters.ts`, `documents.ts`)
- React components: kebab-case (e.g., `chat-renderer.tsx`, `label-wrapper.tsx`, `protected-route.tsx`)
- Hooks: kebab-case with `use-` prefix (e.g., `use-file-drag.ts`, `use-mobile.tsx`, `useChatStreaming.ts`)
- Test files: `.test.ts` or `.spec.ts` suffix (e.g., `integration.test.ts`, `onboarding.spec.ts`)

**Functions:**
- camelCase for exported functions (e.g., `createTestFile()`, `ensureOnboarding()`, `createApiKey()`)
- camelCase for methods within classes (e.g., `query()`, `get()`, `update()`, `delete()`)
- Private methods use `_` prefix (e.g., `_request()`, `_getHeaders()`, `_handleError()`)
- Async functions use async/await syntax without callback pattern

**Variables:**
- camelCase for local variables and parameters (e.g., `streamingMessage`, `isLoading`, `chatId`)
- UPPER_SNAKE_CASE for constants (e.g., `DEFAULT_BASE_URL`, `SKIP_TESTS`, `BASE_URL`)
- Reference prefix for refs: `*Ref` suffix (e.g., `streamAbortRef`, `streamIdRef`, `timeoutId`)
- State variables use `is` prefix for booleans (e.g., `isLoading`, `isDragging`, `isMobile`, `showLayout`)

**Types:**
- PascalCase for interfaces and types (e.g., `ChatResponse`, `SearchResult`, `OpenRAGClientOptions`)
- Interfaces describe objects/contracts (e.g., `ChatCreateOptions`, `SettingsUpdateOptions`)
- Type unions for discriminated unions (e.g., `StreamEvent = ContentEvent | SourcesEvent | DoneEvent`)
- Classes use PascalCase (e.g., `OpenRAGClient`, `ChatClient`, `SearchClient`)

**Enum-like patterns:**
- String literals for discriminated types (e.g., `type StreamEventType = "content" | "sources" | "done"`)
- Use type discriminants: `type: "content"`, `type: "sources"`, etc.

## Code Style

**Formatting:**
- Tool: Biome (frontend), ESLint + Next.js config (frontend), ESLint (SDK)
- Indentation: 2 spaces (enforced in biome.json)
- Line length: No explicit limit configured, but code follows readability patterns
- Quote style: Double quotes (enforced in biome.json for JavaScript)

**Linting:**
- Tool: Biome (frontend primary) + ESLint (Next.js rules)
- Rules configured in `biome.json` at `/home/baongoc/workspaces/openrag/frontend/`
- Rules configured in `eslint.config.mjs` at `/home/baongoc/workspaces/openrag/frontend/`
- Key rules enforced:
  - No console except error/warn (configured in `noConsole` rule)
  - No unused variables (warn level)
  - No explicit any (warn level)
  - ESLint rules: next/core-web-vitals

**Semicolons:**
- Semicolons are used to terminate statements (both TypeScript SDK and frontend)
- Optional semicolon omission not observed

**Trailing commas:**
- Used in multi-line declarations (e.g., function parameters, object properties)

## Import Organization

**Order:**
1. Built-in/Node modules (`import * as fs from "fs"`, `import * as path from "path"`, `import { describe, it } from "vitest"`)
2. External packages (`import { useQueryClient } from "@tanstack/react-query"`, `import { motion } from "framer-motion"`)
3. Relative imports from same project (`import { ChatClient } from "./chat"`, `import { useChat } from "@/contexts/chat-context"`)
4. Type imports separated with `import type` keyword

**Path Aliases:**
- Frontend: `@/*` maps to root directory (configured in tsconfig.json)
- Example usage: `@/components/`, `@/hooks/`, `@/contexts/`, `@/lib/`, `@/app/`
- Promotes clean relative paths in nested components

**Example pattern:**
```typescript
// Built-in imports
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

// External packages
import { describe, it, expect, beforeAll } from "vitest";
import type { OpenRAGClient } from "./client";

// Local imports
import { getEnv } from "./utils";
```

## Error Handling

**Patterns:**
- Custom error classes extend Error base class with name assignment
- Error messages are descriptive and user-facing when appropriate
- Errors include status codes when from HTTP responses (e.g., `OpenRAGError`, `AuthenticationError`)
- Error responses differentiated by HTTP status code:
  - 401/403 → `AuthenticationError`
  - 404 → `NotFoundError`
  - 400 → `ValidationError`
  - 429 → `RateLimitError`
  - 500+ → `ServerError`
  - Other → `OpenRAGError`

**Example from `client.ts`:**
```typescript
export class OpenRAGError extends Error {
  constructor(
    message: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = "OpenRAGError";
  }
}

export class AuthenticationError extends OpenRAGError {
  constructor(message: string, statusCode?: number) {
    super(message, statusCode);
    this.name = "AuthenticationError";
  }
}
```

**Try-catch patterns:**
- Try-finally used to ensure cleanup (e.g., timeout clearing, reader cleanup)
- Specific error handling for known error types
- Generic error handling for unknown errors
- Error messages transformed for user display when appropriate

## Logging

**Framework:** Console object (with Biome enforcement allowing only `error` and `warn` in production)

**Patterns:**
- `console.log()` with descriptive prefixes for debugging (e.g., `"[SDK Tests]"`, `"[useChatStreaming]"`, `"[Tool Detection]"`)
- `console.error()` for actual errors
- `console.warn()` for warnings
- Structured logging with context labels (e.g., `console.log("[Tool Detection] Found tool-related keys:", toolRelatedKeys, chunk)`)
- Prefix patterns aid in log filtering and debugging

## Comments

**When to Comment:**
- Function/class documentation: JSDoc-style comments on public APIs
- Complex logic: Inline comments explaining non-obvious implementations
- TODO comments used sparingly in integration tests where known issues exist (e.g., "TODO: Fix Langflow ingestion flow")
- Comments placed above the code they describe

**JSDoc/TSDoc:**
- Comprehensive JSDoc on public class/function definitions
- Parameter descriptions with `@param` tags
- Return type descriptions with `@returns` tags
- Example usage in `@example` blocks (particularly in SDK client code)

**Example from `client.ts`:**
```typescript
/**
 * OpenRAG API client.
 *
 * The client can be configured via constructor arguments or environment variables:
 * - OPENRAG_API_KEY: API key for authentication
 * - OPENRAG_URL: Base URL for the OpenRAG frontend (default: http://localhost:3000)
 *
 * @example
 * ```typescript
 * const client = new OpenRAGClient();
 * const response = await client.chat.create({ message: "Hello" });
 * ```
 */
export class OpenRAGClient {
```

## Function Design

**Size:** Functions are focused and concise, ranging 20-150 lines for complex operations
- Small utility functions: 5-10 lines
- Hooks with state management: 30-100 lines
- Streaming handlers: Can extend to 150+ lines due to protocol handling complexity

**Parameters:**
- Options objects used instead of multiple positional parameters
- Destructuring common pattern: `{ endpoint = "/api/langflow", onComplete, onError } = {}`
- Type annotations required for all parameters

**Return Values:**
- Explicit return types specified
- Functions returning Promises use `async`/`await`
- Generator functions use `async *` for AsyncIterator implementations
- Null returns used to indicate missing data (e.g., `filter: KnowledgeFilter | null`)

**Example from `useChatStreaming.ts`:**
```typescript
export function useChatStreaming({
  endpoint = "/api/langflow",
  onComplete,
  onError,
}: UseChatStreamingOptions = {}) {
  // Implementation
}
```

## Module Design

**Exports:**
- Named exports preferred for functions and classes
- Default export used in some cases (e.g., SDK index file may have default client)
- Type exports use `export type` keyword (e.g., `export type StreamEventType = ...`)

**Barrel Files:**
- Single index file pattern in `/src/index.ts` for SDK exports
- Aggregate imports from sub-modules (e.g., client, types)
- Frontend uses path aliases instead of barrel files at component level

**Encapsulation:**
- Private fields use `private` keyword in classes
- Internal methods use `_` prefix (e.g., `_request()`, `_init()`)
- `@internal` JSDoc tag used to mark internal API methods

## Class Structure

**Constructor:**
- Private fields initialized in constructor with readonly modifiers
- Constructor pattern: `constructor(options: OptionsType = {})`
- All dependencies injected through constructor or options

**Properties:**
- Readonly properties when values don't change: `readonly chat: ChatClient`
- Private properties for internal state: `private _apiKey: string`
- Getter functions for computed properties: `get text(): string`

**Example from `client.ts`:**
```typescript
export class OpenRAGClient {
  private static readonly DEFAULT_BASE_URL = "http://localhost:3000";

  private readonly _apiKey: string;
  private readonly _baseUrl: string;
  private readonly _timeout: number;

  readonly chat: ChatClient;
  readonly search: SearchClient;

  constructor(options: OpenRAGClientOptions = {}) {
    // Implementation
  }
}
```

## Conditional Logic

**Pattern:**
- Guard clauses early in functions to reduce nesting
- Ternary operators for simple binary conditions
- If-else for multi-branch logic
- Optional chaining (`?.`) for safe property access
- Nullish coalescing (`??`) for default values

**Example:**
```typescript
const value = options.timeout ?? 30000;  // Default if undefined/null
const headers = this._getHeaders(options.isMultipart);  // Guard with early return
```

---

*Convention analysis: 2026-03-20*
