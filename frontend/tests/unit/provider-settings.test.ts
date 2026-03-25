import { describe, expect, it } from "vitest";
import type { ProviderSettings } from "../../app/api/queries/useGetSettingsQuery";

describe("ProviderSettings type", () => {
  it("should allow alibaba provider configuration", () => {
    const settings: ProviderSettings = {
      alibaba: {
        has_api_key: true,
        endpoint: "https://dashscope.aliyuncs.com/v1",
        embedding_endpoint: "https://dashscope.aliyuncs.com/compatible-mode/v1",
        configured: true,
      },
    };

    expect(settings.alibaba?.configured).toBe(true);
    expect(settings.alibaba?.endpoint).toBe(
      "https://dashscope.aliyuncs.com/v1",
    );
  });

  it("should allow partial alibaba configuration", () => {
    const settings: ProviderSettings = {
      alibaba: {
        configured: false,
      },
    };

    expect(settings.alibaba?.configured).toBe(false);
    expect(settings.alibaba?.endpoint).toBeUndefined();
  });

  it("should allow alibaba without api key", () => {
    const settings: ProviderSettings = {
      alibaba: {
        endpoint: "https://custom.endpoint.com/v1",
        configured: true,
      },
    };

    expect(settings.alibaba?.has_api_key).toBeUndefined();
    expect(settings.alibaba?.endpoint).toBe("https://custom.endpoint.com/v1");
  });

  it("should allow all providers together", () => {
    const settings: ProviderSettings = {
      openai: { has_api_key: true, configured: true },
      anthropic: { has_api_key: true, configured: true },
      watsonx: {
        has_api_key: true,
        endpoint: "https://us-south.ml.cloud.ibm.com",
        project_id: "test-project",
        configured: true,
      },
      ollama: { endpoint: "http://localhost:11434", configured: true },
      alibaba: {
        has_api_key: true,
        endpoint: "https://dashscope.aliyuncs.com/v1",
        embedding_endpoint: "https://dashscope.aliyuncs.com/compatible-mode/v1",
        configured: true,
      },
    };

    expect(settings.openai?.configured).toBe(true);
    expect(settings.anthropic?.configured).toBe(true);
    expect(settings.watsonx?.configured).toBe(true);
    expect(settings.ollama?.configured).toBe(true);
    expect(settings.alibaba?.configured).toBe(true);
  });

  it("should have optional alibaba field", () => {
    const settings: ProviderSettings = {
      openai: { configured: true },
    };

    expect(settings.alibaba).toBeUndefined();
  });

  it("should support embedding_endpoint field", () => {
    const settings: ProviderSettings = {
      alibaba: {
        endpoint: "https://chat.api.com/v1",
        embedding_endpoint: "https://embed.api.com/v1",
        configured: true,
      },
    };

    expect(settings.alibaba?.embedding_endpoint).toBe(
      "https://embed.api.com/v1",
    );
    expect(settings.alibaba?.endpoint).not.toBe(
      settings.alibaba?.embedding_endpoint,
    );
  });
});
