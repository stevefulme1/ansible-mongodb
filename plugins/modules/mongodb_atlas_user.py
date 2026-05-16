#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""mongodb_atlas_user module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_user
short_description: Manage MongoDB Atlas database users
description:
    - Manage MongoDB Atlas database users.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the resource.
        type: str
        default: present
        choices: [present, absent]
    host:
        description: API host address.
        type: str
        required: true
    username:
        description: Unique identifier of the atlas user.
        type: str
    name:
        description: Display name.
        type: str
    db_username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
    api_key:
        description: API key for authentication.
        type: str
    validate_certs:
        description: Validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Create a atlas user
  stevefulme1.mongodb.mongodb_atlas_user:
    host: api.example.com
    name: my-atlas-user
    state: present

- name: Delete a atlas user
  stevefulme1.mongodb.mongodb_atlas_user:
    host: api.example.com
    db_username: "example-id"
    state: absent
"""

RETURN = r"""
atlas_user:
    description: Resource details.
    returned: on success
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.mongodb.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            username=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            