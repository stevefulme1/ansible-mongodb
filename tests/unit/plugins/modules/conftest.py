# -*- coding: utf-8 -*-
"""Shared fixtures for MongoDB unit tests."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_module():
    """Return a mock AnsibleModule with check_mode disabled."""
    module = MagicMock()
    module.check_mode = False
    module.params = {
        "state": "present",
        "api_public_key": "test-key",
        "api_private_key": "test-secret",
        "group_id": "proj-123",
    }
    return module


@pytest.fixture
def mock_module_check_mode():
    """Return a mock AnsibleModule with check_mode enabled."""
    module = MagicMock()
    module.check_mode = True
    module.params = {
        "state": "present",
        "api_public_key": "test-key",
        "api_private_key": "test-secret",
        "group_id": "proj-123",
    }
    return module


@pytest.fixture
def mock_client():
    """Return a mock API client."""
    client = MagicMock()
    client.get.return_value = None
    client.create.return_value = {"id": "new-123", "name": "test"}
    client.update.return_value = {"id": "123", "name": "updated"}
    client.delete.return_value = None
    client.list.return_value = []
    return client


@pytest.fixture
def mock_client_existing():
    """Return a mock API client with existing resource."""
    client = MagicMock()
    client.get.return_value = {"id": "123", "name": "existing", "stateName": "IDLE"}
    client.create.return_value = {"id": "123", "name": "existing"}
    client.update.return_value = {"id": "123", "name": "updated"}
    client.delete.return_value = None
    client.list.return_value = [{"id": "123", "name": "existing"}]
    return client
