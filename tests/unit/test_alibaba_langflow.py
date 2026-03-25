"""Unit tests for Alibaba Langflow integration."""

import pytest

from config.config_manager import (
    AlibabaConfig,
    ProvidersConfig,
    OpenAIConfig,
    AnthropicConfig,
    WatsonXConfig,
    OllamaConfig,
    OpenRAGConfig,
    KnowledgeConfig,
    AgentConfig,
    OnboardingState,
)
from utils.langflow_headers import (
    add_provider_credentials_to_headers,
    build_mcp_global_vars_from_config,
)


class MockConfig:
    """Mock OpenRAGConfig for testing."""

    def __init__(self, alibaba_config=None):
        self.providers = ProvidersConfig(
            openai=OpenAIConfig(),
            anthropic=AnthropicConfig(),
            watsonx=WatsonXConfig(),
            ollama=OllamaConfig(),
            alibaba=alibaba_config or AlibabaConfig(),
        )
        self.knowledge = KnowledgeConfig()
        self.agent = AgentConfig()


class TestAlibabaLangflowHeaders:
    """Tests for Alibaba credentials in Langflow headers."""

    @pytest.mark.asyncio
    async def test_add_provider_credentials_includes_alibaba_api_key(self):
        """add_provider_credentials_to_headers should include Alibaba API key."""
        config = MockConfig(alibaba_config=AlibabaConfig(api_key="test-alibaba-key"))
        headers = {}

        await add_provider_credentials_to_headers(headers, config)

        assert "X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY" in headers
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY"] == "test-alibaba-key"

    @pytest.mark.asyncio
    async def test_add_provider_credentials_includes_alibaba_base_url(self):
        """add_provider_credentials_to_headers should include Alibaba base URL."""
        config = MockConfig(alibaba_config=AlibabaConfig(endpoint="https://alibaba.example.com/v1"))
        headers = {}

        await add_provider_credentials_to_headers(headers, config)

        assert "X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL" in headers
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL"] == "https://alibaba.example.com/v1"

    @pytest.mark.asyncio
    async def test_add_provider_credentials_includes_alibaba_embedding_url(self):
        """add_provider_credentials_to_headers should include Alibaba embedding URL."""
        config = MockConfig(alibaba_config=AlibabaConfig(embedding_endpoint="https://embed.alibaba.com/v1"))
        headers = {}

        await add_provider_credentials_to_headers(headers, config)

        assert "X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL" in headers
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL"] == "https://embed.alibaba.com/v1"

    @pytest.mark.asyncio
    async def test_add_provider_credentials_skips_empty_api_key(self):
        """add_provider_credentials_to_headers should skip empty Alibaba API key but include default endpoints."""
        config = MockConfig(alibaba_config=AlibabaConfig())  # Empty config (has default endpoints)
        headers = {}

        await add_provider_credentials_to_headers(headers, config)

        # API key should not be added when empty
        assert "X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY" not in headers
        # Default endpoints ARE added (they're not empty strings)
        assert "X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL" in headers
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL"] == "https://coding-intl.dashscope.aliyuncs.com/v1"

    @pytest.mark.asyncio
    async def test_add_provider_credentials_all_alibaba_fields(self):
        """add_provider_credentials_to_headers should include all Alibaba fields."""
        config = MockConfig(alibaba_config=AlibabaConfig(
            api_key="full-key",
            endpoint="https://full.alibaba.com/v1",
            embedding_endpoint="https://full-embed.alibaba.com/v1",
        ))
        headers = {}

        await add_provider_credentials_to_headers(headers, config)

        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_API_KEY"] == "full-key"
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_BASE_URL"] == "https://full.alibaba.com/v1"
        assert headers["X-LANGFLOW-GLOBAL-VAR-ALIBABA_EMBEDDING_BASE_URL"] == "https://full-embed.alibaba.com/v1"


class TestAlibabaMcpGlobalVars:
    """Tests for Alibaba credentials in MCP global variables."""

    @pytest.mark.asyncio
    async def test_build_mcp_global_vars_includes_alibaba_api_key(self):
        """build_mcp_global_vars_from_config should include Alibaba API key."""
        config = MockConfig(alibaba_config=AlibabaConfig(api_key="mcp-alibaba-key"))

        global_vars = await build_mcp_global_vars_from_config(config)

        assert "ALIBABA_API_KEY" in global_vars
        assert global_vars["ALIBABA_API_KEY"] == "mcp-alibaba-key"

    @pytest.mark.asyncio
    async def test_build_mcp_global_vars_includes_alibaba_base_url(self):
        """build_mcp_global_vars_from_config should include Alibaba base URL."""
        config = MockConfig(alibaba_config=AlibabaConfig(endpoint="https://mcp.alibaba.com/v1"))

        global_vars = await build_mcp_global_vars_from_config(config)

        assert "ALIBABA_BASE_URL" in global_vars
        assert global_vars["ALIBABA_BASE_URL"] == "https://mcp.alibaba.com/v1"

    @pytest.mark.asyncio
    async def test_build_mcp_global_vars_includes_alibaba_embedding_url(self):
        """build_mcp_global_vars_from_config should include Alibaba embedding URL."""
        config = MockConfig(alibaba_config=AlibabaConfig(embedding_endpoint="https://mcp-embed.alibaba.com/v1"))

        global_vars = await build_mcp_global_vars_from_config(config)

        assert "ALIBABA_EMBEDDING_BASE_URL" in global_vars
        assert global_vars["ALIBABA_EMBEDDING_BASE_URL"] == "https://mcp-embed.alibaba.com/v1"

    @pytest.mark.asyncio
    async def test_build_mcp_global_vars_skips_empty_api_key(self):
        """build_mcp_global_vars_from_config should skip empty Alibaba API key but include default endpoints."""
        config = MockConfig(alibaba_config=AlibabaConfig())  # Empty config (has default endpoints)

        global_vars = await build_mcp_global_vars_from_config(config)

        # API key should not be included when empty
        assert "ALIBABA_API_KEY" not in global_vars
        # Default endpoints ARE included (they're not empty strings)
        assert "ALIBABA_BASE_URL" in global_vars
        assert global_vars["ALIBABA_BASE_URL"] == "https://coding-intl.dashscope.aliyuncs.com/v1"
        assert "ALIBABA_EMBEDDING_BASE_URL" in global_vars