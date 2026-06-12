from __future__ import absolute_import, division, print_function
__metaclass__ = type

#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or
#  https://www.gnu.org/licenses/gpl-3.0.txt)
"""Manage MongoDB Atlas cluster auto-scaling settings."""

    AtlasClient,
    atlas_common_argument_spec,
)
DOCUMENTATION = r"""
---
module: mongodb_auto_scaling
short_description: Manage MongoDB Atlas cluster auto-scaling settings
description:
  - Configure auto-scaling settings for MongoDB Atlas clusters.
  - Uses the C(/api/atlas/v2/groups/{groupId}/clusters/
    {clusterName}/processArgs) endpoint.
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
  cluster_name:
    description:
      - The name of the cluster to configure auto-scaling for.
    type: str
    required: true
  compute_enabled:
    description:
      - Whether to enable compute auto-scaling.
    type: bool
    default: false
  compute_scale_down_enabled:
    description:
      - Whether to enable scaling down compute resources.
    type: bool
    default: false
  compute_min_instance_size:
    description:
      - Minimum instance size for compute auto-scaling.
    type: str
  compute_max_instance_size:
    description:
      - Maximum instance size for compute auto-scaling.
    type: str
  disk_gb_enabled:
    description:
      - Whether to enable disk auto-scaling.
    type: bool
    default: false
  state:
    description:
      - Whether the auto-scaling configuration should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Enable auto-scaling for a cluster
  stevefulme1.mongodb.mongodb_auto_scaling:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    cluster_name: my-cluster
    compute_enabled: true
    compute_scale_down_enabled: true
    compute_min_instance_size: M10
    compute_max_instance_size: M30
    disk_gb_enabled: true
    state: present

- name: Disable auto-scaling for a cluster
  stevefulme1.mongodb.mongodb_auto_scaling:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    cluster_name: my-cluster
    state: absent
"""

RETURN = r"""
auto_scaling:
  description: The auto-scaling configuration returned by the Atlas API.
  type: dict
  returned: when state is present
"""

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.atlas_client import (
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = atlas_common_argument_spec()
    argument_spec.update(
        group_id=dict(type="str", required=True),
        cluster_name=dict(type="str", required=True),
        compute_enabled=dict(type="bool", default=False),
        compute_scale_down_enabled=dict(type="bool", default=False),
        compute_min_instance_size=dict(type="str"),
        compute_max_instance_size=dict(type="str"),
        disk_gb_enabled=dict(type="bool", default=False),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    group_id = module.params["group_id"]
    cluster_name = module.params["cluster_name"]
    state = module.params["state"]
    client = AtlasClient(module)

    path = "/groups/%s/clusters/%s/processArgs" % (group_id, cluster_name)
    changed = False
    auto_scaling = {}

    # Check if auto-scaling config exists
    exists = False
    try:
        status, resp = client.get(path)
        if status == 200:
            exists = True
            auto_scaling = resp
    except Exception:
        pass

    if state == "present":
        payload = {
            "autoScaling": {
                "compute": {
                    "enabled": module.params["compute_enabled"],
                    "scaleDownEnabled": module.params["compute_scale_down_enabled"],
                },
                "diskGBEnabled": module.params["disk_gb_enabled"],
            }
        }

        if module.params.get("compute_min_instance_size"):
            payload["autoScaling"]["compute"]["minInstanceSize"] = module.params["compute_min_instance_size"]
        if module.params.get("compute_max_instance_size"):
            payload["autoScaling"]["compute"]["maxInstanceSize"] = module.params["compute_max_instance_size"]

        if not exists:
            if not module.check_mode:
                status, auto_scaling = client.post(path, payload)
            changed = True
        else:
            # Check if update needed
            current = auto_scaling.get("autoScaling", {})
            if (current.get("compute", {}).get("enabled") != module.params["compute_enabled"] or  # noqa: W504
                    current.get("diskGBEnabled") != module.params["disk_gb_enabled"]):
                if not module.check_mode:
                    status, auto_scaling = client.patch(path, payload)
                changed = True

    elif state == "absent":
        if exists:
            if not module.check_mode:
                # Disable auto-scaling by setting enabled flags to false
                payload = {
                    "autoScaling": {
                        "compute": {"enabled": False},
                        "diskGBEnabled": False,
                    }
                }
                client.patch(path, payload)
            changed = True

    module.exit_json(changed=changed, auto_scaling=auto_scaling)


if __name__ == "__main__":
    main()
