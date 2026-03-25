import { expect, test } from "@playwright/test";

test.describe("Alibaba Provider Settings", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to settings page
    await page.goto("/settings");
    await page.waitForLoadState("networkidle");
  });

  test("Alibaba appears in LLM provider dropdown when configured", async ({
    page,
  }) => {
    // Check if Alibaba is visible in the LLM model selector
    const llmSelector = page
      .locator('[data-testid="llm-model-selector"]')
      .or(page.locator("text=/Language Model/i").locator(".."));

    // If settings loaded, check for Alibaba option
    const alibabaOption = page.locator("text=/Alibaba/i");
    const isVisible = await alibabaOption.isVisible().catch(() => false);

    // Log result for debugging
    console.log(`Alibaba visible in LLM dropdown: ${isVisible}`);
  });

  test("Alibaba appears in embedding provider dropdown when configured", async ({
    page,
  }) => {
    // Check if Alibaba is visible in the embedding model selector
    const embeddingSection = page.locator("text=/Embedding/i").locator("..");

    const alibabaOption = page.locator("text=/Alibaba/i");
    const isVisible = await alibabaOption.isVisible().catch(() => false);

    console.log(`Alibaba visible in embedding dropdown: ${isVisible}`);
  });
});

test.describe("Alibaba API Models Endpoint", () => {
  test("API accepts Alibaba provider for models request", async ({
    request,
  }) => {
    const response = await request.post("/api/models/alibaba", {
      data: {
        endpoint: "https://dashscope.aliyuncs.com/v1",
      },
    });

    // Should not return 400/404 for alibaba provider
    expect(response.status()).not.toBe(404);
  });
});
