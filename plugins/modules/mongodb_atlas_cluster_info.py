#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_cluster_info
short_description: Gather information about MongoDB Atlas clusters
description:
  - Return cluster information from MongoDB Atlas.
  - Uses the C(/api/atlas/v2/groups/{groupId}/clusters) endpoint.
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
  name:
    description:
      - Limit output to a specific cluster.
    type: str
"""

EXAMPLES = r"""
- name: List all clusters in a project
  stevefulme1.mongodb.mongodb_atlas_cluster_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
  register: result

- name: Get info for a specific cluster
  stevefulme1.mongodb.mongodb_atlas_cluster_info:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    name: my-cluster
  register: result
"""

RETURN = r"""
clusters:
  description: List of cluster information dicts.
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
        name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    group_id = module.params["group_id"]
    name = module.params.get("name")
    client = AtlasClient(module)

    if name:
        path = "/groups/%s/clusters/%s" % (group_id, name)
        status, resp = client.get(path)
        clusters = [resp] if resp else []
    else:
        path = "/groups/%s/clusters" % group_id
        status, resp = client.get(path)
        clusters = resp.get("results", [])

    module.exit_json(changed=False, clusters=clusters)


if __name__ == "__main__":
    main()
