#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_user
short_description: Manage MongoDB Atlas database users
description:
  - Create, update, or delete MongoDB Atlas database users.
  - Uses the C(/api/atlas/v2/groups/{groupId}/databaseUsers) endpoint.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.atlas
options:
  group_id:
    description:
      - The Atlas project (group) ID.
    type: str
    required: true
  database_name:
    description:
      - The authentication database for the user.
      - Usually C(admin) for SCRAM users or C($external) for LDAP/X.509.
    type: str
    default: admin
  username:
    description:
      - The username for the database user.
    type: str
    required: true
  password:
    description:
      - The password for the user.
      - Required when creating a SCRAM user.
    type: str
  roles:
    description:
      - List of roles to grant.
      - Each role is a dict with C(roleName) and C(databaseName) keys.
    type: list
    elements: dict
    default: []
  scopes:
    description:
      - List of scopes limiting the user to specific clusters or data lakes.
      - Each scope is a dict with C(name) and C(type) keys.
    type: list
    elements: dict
    default: []
  state:
    description:
      - Whether the user should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create an Atlas database user
  stevefulme1.mongodb.mongodb_atlas_user:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    username: appuser
    password: secret123
    roles:
      - roleName: readWrite
        databaseName: myapp
    state: present

- name: Remove an Atlas database user
  stevefulme1.mongodb.mongodb_atlas_user:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    username: appuser
    state: absent
"""

RETURN = r"""
user:
  description: The database user details returned by the Atlas API.
  type: dict
  returned: when state is present
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.atlas_client import (
    AtlasClient,
    atlas_common_argument_spec,
)


def main():
    argument_spec = atlas_common_argument_spec()
    argument_spec.update(
        group_id=dict(type="str", required=True),
        database_name=dict(type="str", default="admin"),
        username=dict(type="str", required=True),
        password=dict(type="str", no_log=True),
        roles=dict(type="list", elements="dict", default=[]),
        scopes=dict(type="list", elements="dict", default=[]),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    group_id = module.params["group_id"]
    database_name = module.params["database_name"]
    username = module.params["username"]
    password = module.params.get("password")
    roles = module.params["roles"]
    scopes = module.params["scopes"]
    state = module.params["state"]
    client = AtlasClient(module)

    base_path = "/groups/%s/databaseUsers" % group_id
    user_path = "%s/%s/%s" % (base_path, database_name, username)
    changed = False
    user = {}

    # Check if user exists
    exists = False
    try:
        status, resp = client.get(user_path)
        if status == 200 and resp:
            exists = True
            user = resp
    except Exception:
        pass

    if state == "present":
        payload = {
            "databaseName": database_name,
            "username": username,
            "roles": roles,
            "scopes": scopes,
        }
        if password:
            payload["password"] = password

        if not exists:
            if not module.check_mode:
                status, user = client.post(base_path, payload)
            changed = True
        else:
            # Update roles/scopes if different
            current_roles = sorted(
                [str(r) for r in user.get("roles", [])]
            )
            new_roles = sorted([str(r) for r in roles])
            if current_roles != new_roles or password:
                if not module.check_mode:
                    status, user = client.patch(user_path, payload)
                changed = True

    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.delete(user_path)
            changed = True

    module.exit_json(changed=changed, user=user)


if __name__ == "__main__":
    main()
