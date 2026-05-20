#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_project
short_description: Manage MongoDB Atlas projects
description:
  - Create or delete MongoDB Atlas projects (groups).
  - Uses the C(/api/atlas/v2/groups) endpoint.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.atlas
options:
  name:
    description:
      - The name of the Atlas project.
    type: str
    required: true
  org_id:
    description:
      - The Atlas organization ID.
      - Required when I(state=present).
    type: str
  group_id:
    description:
      - The Atlas project (group) ID.
      - Required when I(state=absent) to identify the project to delete.
    type: str
  state:
    description:
      - Whether the project should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create an Atlas project
  stevefulme1.mongodb.mongodb_atlas_project:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    name: my-project
    org_id: 5e2211c17a3e5a48f5497000
    state: present

- name: Delete an Atlas project
  stevefulme1.mongodb.mongodb_atlas_project:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    name: my-project
    group_id: 5e2211c17a3e5a48f5497de3
    state: absent
"""

RETURN = r"""
project:
  description: The project details returned by the Atlas API.
  type: dict
  returned: when state is present
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.atlas_client import (
    AtlasClient,
    atlas_common_argument_spec,
)


def find_project_by_name(client, name):
    """Find an Atlas project by name."""
    status, resp = client.get("/groups/byName/%s" % name)
    if status == 200 and resp:
        return resp
    return None


def main():
    argument_spec = atlas_common_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        org_id=dict(type="str"),
        group_id=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["org_id"]),
        ],
    )

    name = module.params["name"]
    org_id = module.params.get("org_id")
    group_id = module.params.get("group_id")
    state = module.params["state"]
    client = AtlasClient(module)
    changed = False
    project = {}

    existing = find_project_by_name(client, name)

    if state == "present":
        if not existing:
            payload = {"name": name, "orgId": org_id}
            if not module.check_mode:
                status, project = client.post("/groups", payload)
            changed = True
        else:
            project = existing

    elif state == "absent":
        target_id = group_id or (existing.get("id") if existing else None)
        if target_id and existing:
            if not module.check_mode:
                client.delete("/groups/%s" % target_id)
            changed = True

    module.exit_json(changed=changed, project=project)


if __name__ == "__main__":
    main()
