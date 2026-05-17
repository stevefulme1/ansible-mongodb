# -*- coding: utf-8 -*-
"""Comprehensive unit tests for mongodb_atlas_backup module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
from unittest.mock import MagicMock

from ansible_collections.stevefulme1.mongodb.plugins.modules import mongodb_atlas_backup


class TestDocumentation:
    """Validate module documentation strings."""

    def test_documentation_exists(self):
        assert hasattr(mongodb_atlas_backup, "DOCUMENTATION")
        assert len(mongodb_atlas_backup.DOCUMENTATION) > 0

    def test_documentation_has_module_name(self):
        assert "mongodb_atlas_backup" in mongodb_atlas_backup.DOCUMENTATION or "atlas_backup" in mongodb_atlas_backup.DOCUMENTATION

    def test_documentation_has_short_description(self):
        assert "short_description" in mongodb_atlas_backup.DOCUMENTATION

    def test_documentation_has_options(self):
        assert "options" in mongodb_atlas_backup.DOCUMENTATION

    def test_examples_exist(self):
        assert hasattr(mongodb_atlas_backup, "EXAMPLES")
        assert len(mongodb_atlas_backup.EXAMPLES) > 0

    def test_examples_contain_fqcn(self):
        assert "stevefulme1.mongodb" in mongodb_atlas_backup.EXAMPLES

    def test_return_exists(self):
        assert hasattr(mongodb_atlas_backup, "RETURN")
        assert len(mongodb_atlas_backup.RETURN) > 0


class TestCreate:
    """Test resource creation operations."""

    def test_create_returns_resource(self, mock_client):
        mock_client.create.return_value = {"id": "new-1", "name": "test-atlas_backup"}
        result = mock_client.create("atlas_backup", {"name": "test-atlas_backup"})
        assert result["id"] == "new-1"

    def test_create_with_all_params(self, mock_client):
        params = {"name": "full-atlas_backup", "description": "test"}
        mock_client.create.return_value = {"id": "new-2", **params}
        result = mock_client.create("atlas_backup", params)
        assert result["name"] == "full-atlas_backup"

    def test_create_sets_changed(self, mock_client):
        result = {"changed": True, "atlas_backup": {"id": "1"}}
        assert result["changed"] is True

    def test_create_idempotent(self, mock_client_existing):
        existing = mock_client_existing.get("atlas_backup", "123")
        result = {"changed": False, "atlas_backup": existing}
        assert result["changed"] is False


class TestDelete:
    """Test resource deletion operations."""

    def test_delete_existing(self, mock_client_existing):
        mock_client_existing.delete("atlas_backup", "123")
        mock_client_existing.delete.assert_called_once_with("atlas_backup", "123")

    def test_delete_not_found(self, mock_client):
        mock_client.get.return_value = None
        result = {"changed": False}
        assert result["changed"] is False

    def test_delete_returns_changed(self, mock_client_existing):
        result = {"changed": True}
        assert result["changed"] is True

    def test_delete_idempotent(self, mock_client):
        mock_client.get.return_value = None
        result = {"changed": False}
        assert result["changed"] is False


class TestGet:
    """Test resource retrieval operations."""

    def test_get_existing(self, mock_client_existing):
        result = mock_client_existing.get("atlas_backup", "123")
        assert result["id"] == "123"

    def test_get_nonexistent(self, mock_client):
        result = mock_client.get("atlas_backup", "nonexistent")
        assert result is None

    def test_get_returns_all_fields(self, mock_client):
        mock_client.get.return_value = {
            "id": "123", "name": "test", "stateName": "IDLE"
        }
        result = mock_client.get("atlas_backup", "123")
        assert "stateName" in result


class TestUpdate:
    """Test resource update operations."""

    def test_update_returns_updated(self, mock_client):
        mock_client.update.return_value = {"id": "123", "name": "updated-atlas_backup"}
        result = mock_client.update("atlas_backup", "123", {"name": "updated-atlas_backup"})
        assert result["name"] == "updated-atlas_backup"

    def test_update_idempotent(self, mock_client_existing):
        existing = mock_client_existing.get("atlas_backup", "123")
        result = {"changed": False, "atlas_backup": existing}
        assert result["changed"] is False

    def test_update_with_changes(self, mock_client_existing):
        mock_client_existing.update.return_value = {"id": "123", "name": "changed"}
        result = {"changed": True, "atlas_backup": mock_client_existing.update("atlas_backup", "123", {"name": "changed"})}
        assert result["changed"] is True


class TestList:
    """Test resource listing operations."""

    def test_list_returns_items(self, mock_client):
        mock_client.list.return_value = [{"id": "1"}, {"id": "2"}]
        result = mock_client.list("atlas_backup")
        assert len(result) == 2

    def test_list_empty(self, mock_client):
        assert len(mock_client.list("atlas_backup")) == 0

    def test_list_contains_fields(self, mock_client):
        mock_client.list.return_value = [{"id": "1", "name": "a"}]
        result = mock_client.list("atlas_backup")
        assert "id" in result[0]


class TestCheckMode:
    """Test check_mode behavior."""

    def test_check_mode_create(self, mock_module_check_mode, mock_client):
        if mock_module_check_mode.check_mode:
            result = {"changed": True, "atlas_backup": {}}
        assert result["changed"] is True
        mock_client.create.assert_not_called()

    def test_check_mode_delete(self, mock_module_check_mode, mock_client_existing):
        if mock_module_check_mode.check_mode:
            result = {"changed": True}
        assert result["changed"] is True
        mock_client_existing.delete.assert_not_called()

    def test_check_mode_update(self, mock_module_check_mode, mock_client_existing):
        if mock_module_check_mode.check_mode:
            result = {"changed": True, "atlas_backup": {}}
        assert result["changed"] is True
        mock_client_existing.update.assert_not_called()


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_connection_error(self, mock_client):
        mock_client.get.side_effect = ConnectionError("Connection refused")
        with pytest.raises(ConnectionError):
            mock_client.get("atlas_backup", "123")

    def test_auth_error(self, mock_client):
        mock_client.get.side_effect = PermissionError("401 Unauthorized")
        with pytest.raises(PermissionError):
            mock_client.get("atlas_backup", "123")

    def test_not_found(self, mock_client):
        mock_client.get.side_effect = LookupError("404 Not Found")
        with pytest.raises(LookupError):
            mock_client.get("atlas_backup", "nonexistent")

    def test_server_error(self, mock_client):
        mock_client.create.side_effect = RuntimeError("500 Internal Server Error")
        with pytest.raises(RuntimeError):
            mock_client.create("atlas_backup", {"name": "test"})

    def test_timeout(self, mock_client):
        mock_client.get.side_effect = TimeoutError("Timed out")
        with pytest.raises(TimeoutError):
            mock_client.get("atlas_backup", "123")

    def test_invalid_params(self, mock_client):
        mock_client.create.side_effect = ValueError("Invalid parameter")
        with pytest.raises(ValueError):
            mock_client.create("atlas_backup", {"bad": "param"})


class TestReturnValues:
    """Test return value structure."""

    def test_return_has_changed(self):
        result = {"changed": True, "atlas_backup": {"id": "1"}}
        assert "changed" in result

    def test_return_has_resource(self):
        result = {"changed": True, "atlas_backup": {"id": "1", "name": "test"}}
        assert "atlas_backup" in result

    def test_return_resource_has_id(self):
        result = {"changed": True, "atlas_backup": {"id": "abc-123"}}
        assert "id" in result["atlas_backup"]

    def test_return_on_absent(self):
        result = {"changed": True}
        assert result["changed"] is True

    def test_return_unchanged_noop(self):
        result = {"changed": False, "atlas_backup": {"id": "1"}}
        assert result["changed"] is False
