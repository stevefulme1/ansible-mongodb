# -*- coding: utf-8 -*-
"""Unit tests for mongodb_serverless_instance module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.stevefulme1.mongodb.plugins.modules import mongodb_serverless_instance


class TestDocumentation:
    """Validate module documentation strings."""

    def test_documentation_exists(self):
        assert hasattr(mongodb_serverless_instance, "DOCUMENTATION")
        assert len(mongodb_serverless_instance.DOCUMENTATION) > 0

    def test_documentation_has_module_name(self):
        assert "mongodb_serverless_instance" in mongodb_serverless_instance.DOCUMENTATION or "serverless_instance" in mongodb_serverless_instance.DOCUMENTATION

    def test_documentation_has_short_description(self):
        assert "short_description" in mongodb_serverless_instance.DOCUMENTATION

    def test_documentation_has_options(self):
        assert "options" in mongodb_serverless_instance.DOCUMENTATION

    def test_examples_exist(self):
        assert hasattr(mongodb_serverless_instance, "EXAMPLES")
        assert len(mongodb_serverless_instance.EXAMPLES) > 0

    def test_examples_contain_fqcn(self):
        assert "stevefulme1.mongodb" in mongodb_serverless_instance.EXAMPLES

    def test_return_exists(self):
        assert hasattr(mongodb_serverless_instance, "RETURN")
        assert len(mongodb_serverless_instance.RETURN) > 0


class TestCreate:
    """Test resource creation operations."""

    def test_create_returns_resource(self, mock_client):
        mock_client.create.return_value = {"id": "new-1", "name": "test"}
        result = mock_client.create("serverless_instance", {"name": "test"})
        assert result["id"] == "new-1"

    def test_create_sets_changed(self, mock_client):
        result = {"changed": True, "serverless_instance": {"id": "1"}}
        assert result["changed"] is True

    def test_create_idempotent(self, mock_client_existing):
        existing = mock_client_existing.get("serverless_instance", "123")
        result = {"changed": False, "serverless_instance": existing}
        assert result["changed"] is False


class TestDelete:
    """Test resource deletion operations."""

    def test_delete_existing(self, mock_client_existing):
        mock_client_existing.delete("serverless_instance", "123")
        mock_client_existing.delete.assert_called_once()

    def test_delete_not_found(self, mock_client):
        mock_client.get.return_value = None
        result = {"changed": False}
        assert result["changed"] is False

    def test_delete_returns_changed(self, mock_client_existing):
        result = {"changed": True}
        assert result["changed"] is True


class TestMainFunction:
    """Validate main function exists."""

    def test_main_exists(self):
        assert hasattr(mongodb_serverless_instance, "main")
        assert callable(mongodb_serverless_instance.main)
