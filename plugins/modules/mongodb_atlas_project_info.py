#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_project_info
short_description: Gather information about MongoDB Atlas projects
description:
  - Return project information from MongoDB Atlas.
  - Uses the C(/api/atlas/v2/groups) endpoint.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.atlas
options:
  name:
    description:
      - Limit output to a project with this name.
    type: str
  group_id:
    description:
      - Limit output to a project with this ID.
    type: str
"""

EXAMPLES = r"""
- name: List all Atlas projects
  stevefulme1.mongodb.mongodb_atlas_project_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
  register: result

- name: Get project by name
  stevefulme1.mongodb.mongodb_atlas_project_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    name: my-project
  register: result
"""

RETURN = r"""
projects:
  description: List of project information dicts.
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
        name=dict(type="str"),
        group_id=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[("name", "group_id")],
    )

    name = module.params.get("name")
    group_id = module.params.get("group_id")
    client = AtlasClient(module)

    if group_id:
        status, resp = client.get("/groups/%s" % group_id)
        projects = [resp] if resp else []
    elif name:
        status, resp = client.get("/groups/byName/%s" % name)
        projects = [resp] if resp else []
    else:
        status, resp = client.get("/groups")
        projects = resp.get("results", [])

    module.exit_json(changed=False, projects=projects)


if __name__ == "__main__":
    main()
