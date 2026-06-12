# -*- coding: utf-8 -*-
"""Unit tests for mongodb_serverless_instance module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

try:
    from ansible_collections.stevefulme1.mongodb.plugins.modules import mongodb_serverless_instance
    HAS_MODULE = True
except ImportError:
    HAS_MODULE = False


@pytest.mark.skipif(not HAS_MODULE, reason="mongodb_serverless_instance not importable outside collection")
class TestDocumentation:
    """Validate module documentation strings."""

    def test_documentation_exists(self):
        assert len(mongodb_serverless_instance.DOCUMENTATION) > 0

    def test_documentation_has_module_name(self):
        assert "mongodb_serverless_instance" in mongodb_serverless_instance.DOCUMENTATION or "serverless_instance" in mongodb_serverless_instance.DOCUMENTATION

    def test_documentation_has_short_description(self):
        assert "short_description" in mongodb_serverless_instance.DOCUMENTATION

    def test_documentation_has_options(self):
        assert "options" in mongodb_serverless_instance.DOCUMENTATION


@pytest.mark.skipif(not HAS_MODULE, reason="mongodb_serverless_instance not importable outside collection")
class TestExamples:
    """Validate module examples."""

    def test_examples_exist(self):
        assert len(mongodb_serverless_instance.EXAMPLES) > 0


@pytest.mark.skipif(not HAS_MODULE, reason="mongodb_serverless_instance not importable outside collection")
class TestReturn:
    """Validate module return documentation."""

    def test_return_exists(self):
        assert len(mongodb_serverless_instance.RETURN) > 0


@pytest.mark.skipif(not HAS_MODULE, reason="mongodb_serverless_instance not importable outside collection")
class TestMain:
    """Validate main function."""

    def test_main_callable(self):
        assert callable(mongodb_serverless_instance.main)
