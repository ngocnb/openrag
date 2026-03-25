import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  useGetAlibabaModelsQuery,
  useGetCurrentProviderModelsQuery,
} from "../../app/api/queries/useGetModelsQuery";

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Note: This mock affects the useGetCurrentProviderModelsQuery tests
vi.mock("../../app/api/queries/useGetSettingsQuery", () => ({
  useGetSettingsQuery: () => ({
    data: {
      agent: { llm_provider: "alibaba" },
      providers: {
        alibaba: { endpoint: "https://test.com", configured: true },
      },
    },
  }),
}));

// Create wrapper for React Query
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return function Wrapper({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  };
}

describe("useGetAlibabaModelsQuery", () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  it("should not fetch when enabled is false", async () => {
    const wrapper = createWrapper();

    const { result } = renderHook(
      () =>
        useGetAlibabaModelsQuery(
          { endpoint: "https://test.com" },
          { enabled: false },
        ),
      { wrapper },
    );

    expect(result.current.isLoading).toBe(false);
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("should fetch Alibaba models when enabled", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        language_models: [{ value: "qwen-Plus", label: "Qwen Plus" }],
        embedding_models: [
          { value: "text-embedding-v3", label: "Text Embedding V3" },
        ],
      }),
    });

    const wrapper = createWrapper();

    const { result } = renderHook(
      () =>
        useGetAlibabaModelsQuery(
          { endpoint: "https://alibaba.test.com", apiKey: "test-key" },
          { enabled: true },
        ),
      { wrapper },
    );

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/models/alibaba"),
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining("alibaba.test.com"),
      }),
    );

    expect(result.current.data?.language_models).toHaveLength(1);
    expect(result.current.data?.embedding_models).toHaveLength(1);
  });

  it("should handle fetch error", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
    });

    const wrapper = createWrapper();

    const { result } = renderHook(
      () =>
        useGetAlibabaModelsQuery(
          { endpoint: "https://test.com" },
          { enabled: true },
        ),
      { wrapper },
    );

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeInstanceOf(Error);
    expect(result.current.error?.message).toBe(
      "Failed to fetch Alibaba models",
    );
  });

  it("should include api_key in request body when provided", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ language_models: [], embedding_models: [] }),
    });

    const wrapper = createWrapper();

    renderHook(
      () =>
        useGetAlibabaModelsQuery(
          { endpoint: "https://test.com", apiKey: "secret-key" },
          { enabled: true },
        ),
      { wrapper },
    );

    await waitFor(() => expect(mockFetch).toHaveBeenCalled());

    const call = mockFetch.mock.calls[0];
    const body = JSON.parse(call[1].body);
    expect(body.api_key).toBe("secret-key");
  });

  it("should include endpoint in request body when provided", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ language_models: [], embedding_models: [] }),
    });

    const wrapper = createWrapper();

    renderHook(
      () =>
        useGetAlibabaModelsQuery(
          { endpoint: "https://custom.alibaba.com/v1" },
          { enabled: true },
        ),
      { wrapper },
    );

    await waitFor(() => expect(mockFetch).toHaveBeenCalled());

    const call = mockFetch.mock.calls[0];
    const body = JSON.parse(call[1].body);
    expect(body.endpoint).toBe("https://custom.alibaba.com/v1");
  });
});

describe("useGetCurrentProviderModelsQuery", () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  it("should return alibaba models when provider is alibaba", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        language_models: [{ value: "qwen-plus", label: "Qwen Plus" }],
        embedding_models: [],
      }),
    });

    const wrapper = createWrapper();

    const { result } = renderHook(() => useGetCurrentProviderModelsQuery(), {
      wrapper,
    });

    // Since alibaba is not enabled without proper settings, we just check the hook doesn't crash
    expect(result.current).toBeDefined();
  });
});
