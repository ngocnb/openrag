"""Unit tests for Alibaba provider configuration."""

import base64
import pytest

from config.config_manager import (
    AlibabaConfig,
    ProvidersConfig,
    OpenAIConfig,
    AnthropicConfig,
    WatsonXConfig,
    OllamaConfig,
    ConfigManager,
)


@pytest.fixture(autouse=True)
def setup_encryption_env(monkeypatch):
    """Set up encryption key for tests that need it."""
    import utils.encryption
    utils.encryption._cached_master_secret = None
    monkeypatch.setenv("OPENRAG_ENCRYPTION_KEY", base64.b64encode(b"0123456789abcdef0123456789abcdef").decode("ascii"))


class TestAlibabaConfig:
    """Tests for AlibabaConfig dataclass."""

    def test_alibaba_config_defaults(self):
        """AlibabaConfig should have correct default values."""
        config = AlibabaConfig()

        assert config.api_key == ""
        assert config.endpoint == "https://coding-intl.dashscope.aliyuncs.com/v1"
        assert config.embedding_endpoint == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        assert config.configured is False

    def test_alibaba_config_custom_values(self):
        """AlibabaConfig should accept custom values."""
        config = AlibabaConfig(
            api_key="test-api-key",
            endpoint="https://custom.endpoint.com/v1",
            embedding_endpoint="https://custom.embed.com/v1",
            configured=True,
        )

        assert config.api_key == "test-api-key"
        assert config.endpoint == "https://custom.endpoint.com/v1"
        assert config.embedding_endpoint == "https://custom.embed.com/v1"
        assert config.configured is True

    def test_alibaba_config_partial_values(self):
        """AlibabaConfig should work with partial values."""
        config = AlibabaConfig(api_key="my-key")

        assert config.api_key == "my-key"
        assert config.endpoint == "https://coding-intl.dashscope.aliyuncs.com/v1"
        assert config.configured is False


class TestProvidersConfigAlibaba:
    """Tests for ProvidersConfig with Alibaba support."""

    def test_providers_config_includes_alibaba(self):
        """ProvidersConfig should include alibaba field."""
        providers = ProvidersConfig(
            openai=OpenAIConfig(),
            anthropic=AnthropicConfig(),
            watsonx=WatsonXConfig(),
            ollama=OllamaConfig(),
            alibaba=AlibabaConfig(),
        )

        assert hasattr(providers, 'alibaba')
        assert isinstance(providers.alibaba, AlibabaConfig)

    def test_get_provider_config_alibaba(self):
        """get_provider_config should return Alibaba config."""
        alibaba_config = AlibabaConfig(api_key="test-key")
        providers = ProvidersConfig(
            openai=OpenAIConfig(),
            anthropic=AnthropicConfig(),
            watsonx=WatsonXConfig(),
            ollama=OllamaConfig(),
            alibaba=alibaba_config,
        )

        result = providers.get_provider_config("alibaba")
        assert result is alibaba_config
        assert result.api_key == "test-key"

    def test_get_provider_config_alibaba_case_insensitive(self):
        """get_provider_config should handle Alibaba case-insensitively."""
        alibaba_config = AlibabaConfig(api_key="test-key")
        providers = ProvidersConfig(
            openai=OpenAIConfig(),
            anthropic=AnthropicConfig(),
            watsonx=WatsonXConfig(),
            ollama=OllamaConfig(),
            alibaba=alibaba_config,
        )

        assert providers.get_provider_config("Alibaba") is alibaba_config
        assert providers.get_provider_config("ALIBABA") is alibaba_config
        assert providers.get_provider_config("AlIbAbA") is alibaba_config

    def test_get_provider_config_unknown_provider_raises(self):
        """get_provider_config should raise for unknown provider."""
        providers = ProvidersConfig(
            openai=OpenAIConfig(),
            anthropic=AnthropicConfig(),
            watsonx=WatsonXConfig(),
            ollama=OllamaConfig(),
            alibaba=AlibabaConfig(),
        )

        with pytest.raises(ValueError, match="Unknown provider"):
            providers.get_provider_config("unknown")


class TestConfigManagerAlibaba:
    """Tests for ConfigManager with Alibaba provider."""

    def test_config_manager_loads_alibaba_default(self, tmp_path):
        """ConfigManager should load empty Alibaba config by default."""
        test_yaml = tmp_path / "test_config.yaml"
        test_yaml.write_text("providers: {}\n")

        cm = ConfigManager(str(test_yaml))
        config = cm.get_config()

        assert config.providers.alibaba is not None
        assert config.providers.alibaba.api_key == ""
        assert config.providers.alibaba.configured is False

    def test_config_manager_saves_alibaba_config(self, tmp_path):
        """ConfigManager should save Alibaba config with encryption."""
        import yaml

        test_yaml = tmp_path / "test_config.yaml"
        cm = ConfigManager(str(test_yaml))
        config = cm.get_config()

        config.providers.alibaba.api_key = "alibaba-secret-key"
        config.providers.alibaba.endpoint = "https://custom.alibaba.com/v1"
        config.providers.alibaba.configured = True

        cm.save_config_file(config)

        # Verify saved with encryption
        with open(test_yaml, "r") as f:
            saved_data = yaml.safe_load(f)

        assert "alibaba" in saved_data["providers"]
        # API key should be encrypted (dict, not plain string)
        assert isinstance(saved_data["providers"]["alibaba"]["api_key"], dict)
        assert saved_data["providers"]["alibaba"]["api_key"]["algorithm"] == "AES-256-GCM"
        assert saved_data["providers"]["alibaba"]["endpoint"] == "https://custom.alibaba.com/v1"
        assert saved_data["providers"]["alibaba"]["configured"] is True

    def test_config_manager_roundtrip_alibaba(self, tmp_path):
        """ConfigManager should load Alibaba config correctly after save."""
        test_yaml = tmp_path / "test_config.yaml"

        # First save
        cm = ConfigManager(str(test_yaml))
        config = cm.get_config()
        config.providers.alibaba.api_key = "roundtrip-key"
        config.providers.alibaba.embedding_endpoint = "https://embed.alibaba.com/v1"
        cm.save_config_file(config)

        # Then load in new manager
        cm2 = ConfigManager(str(test_yaml))
        config2 = cm2.get_config()

        assert config2.providers.alibaba.api_key == "roundtrip-key"
        assert config2.providers.alibaba.embedding_endpoint == "https://embed.alibaba.com/v1"

    def test_config_manager_env_override_alibaba(self, tmp_path, monkeypatch):
        """ConfigManager should load Alibaba config from environment variables."""
        monkeypatch.setenv("ALIBABA_API_KEY", "env-api-key")
        monkeypatch.setenv("ALIBABA_ENDPOINT", "https://env.alibaba.com/v1")
        monkeypatch.setenv("ALIBABA_EMBEDDING_ENDPOINT", "https://env-embed.alibaba.com/v1")

        test_yaml = tmp_path / "test_config.yaml"
        test_yaml.write_text("providers: {}\n")

        cm = ConfigManager(str(test_yaml))
        config = cm.get_config()

        assert config.providers.alibaba.api_key == "env-api-key"
        assert config.providers.alibaba.endpoint == "https://env.alibaba.com/v1"
        assert config.providers.alibaba.embedding_endpoint == "https://env-embed.alibaba.com/v1"