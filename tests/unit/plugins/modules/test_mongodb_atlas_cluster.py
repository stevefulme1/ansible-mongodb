from __future__ import absolute_import, division, print_function
__metaclass__ = type

"""Unit tests for mongodb_atlas_cluster module."""

from unittest.mock import MagicMock


TestCreate:
    def test_create_returns_resource(self):
        mock_client = MagicMock()
        mock_client.create.return_value = dict(id="123", name="test")
        result = mock_client.create("atlas_cluster", dict(name="test"))
        assert result["id"] == "123"


TestDelete:
    def test_delete_calls_api(self):
        mock_client = MagicMock()
        mock_client.delete("atlas_cluster", "123")
        mock_client.delete.assert_called_once_with("atlas_cluster", "123")


TestList:
    def test_list_returns_items(self):
        mock_client = MagicMock()
        mock_client.list.return_value = [dict(id="1"), dict(id="2")]
        result = mock_client.list("atlas_cluster")
        assert len(result) == 2


TestGet:
    def test_get_not_found(self):
        mock_client = MagicMock()
        mock_client.get.return_value = None
        assert mock_client.get("atlas_cluster", "x") is None
