#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""mongodb_atlas_whitelist_info module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_whitelist_info
short_description: Retrieve atlas whitelist information
description:
    - Retrieve details about atlas whitelists.
    - Read-only module.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    host:
        description: API host address.
        type: str
        required: true
    entry_id:
        description: ID of a specific resource.
        type: str
    name:
        description: Filter by name.
        type: str
    username:
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
    limit:
        description:
          - Maximum number of results per page (maps to Atlas itemsPerPage).
        type: int
        default: 100
    offset:
        description:
          - Page number to return (maps to Atlas pageNum, 1-indexed).
        type: int
        default: 1
    max_results:
        description:
          - Maximum total results to return.
        type: int
        default: 1000
"""

EXAMPLES = r"""
- name: List all atlas whitelists
  stevefulme1.mongodb.mongodb_atlas_whitelist_info:
    host: api.example.com
  register: result

- name: Get a specific atlas whitelist
  stevefulme1.mongodb.mongodb_atlas_whitelist_info:
    host: api.example.com
    entry_id: "example-id"
  register: result
"""

RETURN = r"""
atlas_whitelists:
    description: List of resource details.
    returned: always
    type: list
    elements: dict
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
            entry_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
            limit=dict(type="int", default=100),
            offset=dict(type="int", default=1),
            max_results=dict(type="int", default=1000),
        ),
        supports_check_mode=True,
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    resource_id = module.params.get("entry_id")

    if resource_id:
        result = client.get("atlas_whitelist", resource_id)
        resources = [result] if result else []
    else:
        _params = dict(module.params)
        if module.params.get("limit"):
            _params["limit"] = module.params["limit"]
        if module.params.get("offset"):
            _params["offset"] = module.params["offset"]
        resources = client.list("atlas_whitelist", module.params)

    module.exit_json(changed=False, atlas_whitelists=resources)


if __name__ == "__main__":
    main()
