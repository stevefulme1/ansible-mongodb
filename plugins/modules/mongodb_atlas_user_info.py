#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_user_info
short_description: Gather information about MongoDB Atlas database users
description:
  - Return database user information from MongoDB Atlas.
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
  username:
    description:
      - Limit output to a specific user.
    type: str
  database_name:
    description:
      - The authentication database.
      - Used with I(username) to identify a specific user.
    type: str
    default: admin
"""

EXAMPLES = r"""
- name: List all Atlas database users
  stevefulme1.mongodb.mongodb_atlas_user_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
  register: result

- name: Get info for a specific user
  stevefulme1.mongodb.mongodb_atlas_user_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    username: appuser
  register: result
"""

RETURN = r"""
users:
  description: List of database user dicts.
  type: list
  elements: dict
  returned: always
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
        username=dict(type="str"),
        database_name=dict(type="str", default="admin"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    group_id = module.params["group_id"]
    username = module.params.get("username")
    database_name = module.params["database_name"]
    client = AtlasClient(module)

    if username:
        path = "/groups/%s/databaseUsers/%s/%s" % (
            group_id,
            database_name,
            username,
        )
        status, resp = client.get(path)
        users = [resp] if resp else []
    else:
        path = "/groups/%s/databaseUsers" % group_id
        status, resp = client.get(path)
        users = resp.get("results", [])

    module.exit_json(changed=False, users=users)


if __name__ == "__main__":
    main()
