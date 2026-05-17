#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""mongodb_atlas_alert module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_alert
short_description: Manage MongoDB Atlas alert configurations
description:
    - Manage MongoDB Atlas alert configurations.
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
    alert_config_id:
        description: Unique identifier of the atlas alert.
        type: str
    name:
        description: Display name.
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
"""

EXAMPLES = r"""
- name: Create a atlas alert
  stevefulme1.mongodb.mongodb_atlas_alert:
    host: api.example.com
    name: my-atlas-alert
    state: present

- name: Delete a atlas alert
  stevefulme1.mongodb.mongodb_atlas_alert:
    host: api.example.com
    alert_config_id: "example-id"
    state: absent
"""

RETURN = r"""
atlas_alert:
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
            alert_config_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[("state", "absent", ("alert_config_id",))],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("alert_config_id")

    if state == "present":
        existing = None
        if resource_id:
            existing = client.get("atlas_alert", resource_id)
        elif module.params.get("name"):
            name_filter = module.params.get("name", "")
            candidates = client.list("atlas_alert", {"name": name_filter})
            if candidates:
                existing = candidates[0]

        if existing:
            if module.check_mode:
                module.exit_json(changed=False, atlas_alert=existing)
            result = client.update("atlas_alert", resource_id or existing.get("id", ""), module.params)
            module.exit_json(changed=True, atlas_alert=result)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("atlas_alert", module.params)
            module.exit_json(changed=True, atlas_alert=result)
    else:
        existing = None
        if resource_id:
            existing = client.get("atlas_alert", resource_id)
        if not existing:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("atlas_alert", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
