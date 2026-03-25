"""Unit tests for Alibaba embedding dimensions."""

import pytest

from config.settings import ALIBABA_EMBEDDING_DIMENSIONS


class TestAlibabaEmbeddingDimensions:
    """Tests for ALIBABA_EMBEDDING_DIMENSIONS mapping."""

    def test_text_embedding_v3_dimension(self):
        """text-embedding-v3 should have 1024 dimensions."""
        assert ALIBABA_EMBEDDING_DIMENSIONS["text-embedding-v3"] == 1024

    def test_text_embedding_v4_dimension(self):
        """text-embedding-v4 should have 2048 dimensions."""
        assert ALIBABA_EMBEDDING_DIMENSIONS["text-embedding-v4"] == 2048

    def test_dimensions_dict_exists(self):
        """ALIBABA_EMBEDDING_DIMENSIONS should be a dict."""
        assert isinstance(ALIBABA_EMBEDDING_DIMENSIONS, dict)

    def test_dimensions_dict_not_empty(self):
        """ALIBABA_EMBEDDING_DIMENSIONS should have at least one entry."""
        assert len(ALIBABA_EMBEDDING_DIMENSIONS) >= 1

    def test_all_dimensions_are_positive_integers(self):
        """All dimension values should be positive integers."""
        for model, dim in ALIBABA_EMBEDDING_DIMENSIONS.items():
            assert isinstance(dim, int), f"Dimension for {model} should be int, got {type(dim)}"
            assert dim > 0, f"Dimension for {model} should be positive, got {dim}"

    def test_model_names_are_strings(self):
        """All model names should be strings."""
        for model in ALIBABA_EMBEDDING_DIMENSIONS.keys():
            assert isinstance(model, str), f"Model name should be str, got {type(model)}"

    def test_no_duplicate_models(self):
        """There should be no duplicate model names (keys are unique)."""
        models = list(ALIBABA_EMBEDDING_DIMENSIONS.keys())
        assert len(models) == len(set(models)), "Duplicate model names found"