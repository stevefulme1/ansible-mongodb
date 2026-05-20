#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_cluster
short_description: Manage MongoDB Atlas clusters
description:
  - Create, update, or delete MongoDB Atlas clusters via the Atlas REST API.
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
      - The name of the cluster.
    type: str
    required: true
  cluster_type:
    description:
      - The type of cluster to create.
    type: str
    choices: [REPLICASET, SHARDED, GEOSHARDED]
    default: REPLICASET
  provider_name:
    description:
      - The cloud provider for the cluster.
    type: str
    choices: [AWS, GCP, AZURE, TENANT]
    default: AWS
  region_name:
    description:
      - The cloud provider region.
    type: str
    default: US_EAST_1
  instance_size:
    description:
      - The Atlas instance size name.
    type: str
    default: M10
  disk_size_gb:
    description:
      - Disk size in GB for the cluster.
    type: float
  mongo_db_major_version:
    description:
      - The MongoDB major version for the cluster.
    type: str
  state:
    description:
      - Whether the cluster should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create an Atlas cluster
  stevefulme1.mongodb.mongodb_atlas_cluster:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    name: my-cluster
    cluster_type: REPLICASET
    provider_name: AWS
    region_name: US_EAST_1
    instance_size: M10
    state: present

- name: Delete an Atlas cluster
  stevefulme1.mongodb.mongodb_atlas_cluster:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    name: my-cluster
    state: absent
"""

RETURN = r"""
cluster:
  description: The cluster details returned by the Atlas API.
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
        name=dict(type="str", required=True),
        cluster_type=dict(
            type="str",
            choices=["REPLICASET", "SHARDED", "GEOSHARDED"],
            default="REPLICASET",
        ),
        provider_name=dict(
            type="str",
            choices=["AWS", "GCP", "AZURE", "TENANT"],
            default="AWS",
        ),
        region_name=dict(type="str", default="US_EAST_1"),
        instance_size=dict(type="str", default="M10"),
        disk_size_gb=dict(type="float"),
        mongo_db_major_version=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    group_id = module.params["group_id"]
    name = module.params["name"]
    state = module.params["state"]
    client = AtlasClient(module)

    path = "/groups/%s/clusters/%s" % (group_id, name)
    changed = False
    cluster = {}

    # Check if cluster exists
    exists = False
    try:
        status, resp = client.get(path)
        if status == 200:
            exists = True
            cluster = resp
    except Exception:
        pass

    if state == "present":
        payload = {
            "name": name,
            "clusterType": module.params["cluster_type"],
            "replicationSpecs": [
                {
                    "numShards": 1,
                    "regionConfigs": [
                        {
                            "providerName": module.params["provider_name"],
                            "regionName": module.params["region_name"],
                            "electableSpecs": {
                                "instanceSize": module.params["instance_size"],
                                "nodeCount": 3,
                            },
                            "priority": 7,
                        }
                    ],
                }
            ],
        }
        if module.params.get("disk_size_gb"):
            payload["diskSizeGB"] = module.params["disk_size_gb"]
        if module.params.get("mongo_db_major_version"):
            payload["mongoDBMajorVersion"] = module.params["mongo_db_major_version"]

        if not exists:
            if not module.check_mode:
                status, cluster = client.post(
                    "/groups/%s/clusters" % group_id, payload
                )
            changed = True
        else:
            # Update if instance size changed
            current_size = ""
            for spec in cluster.get("replicationSpecs", []):
                for rc in spec.get("regionConfigs", []):
                    es = rc.get("electableSpecs", {})
                    current_size = es.get("instanceSize", "")
                    break
            if current_size != module.params["instance_size"]:
                if not module.check_mode:
                    status, cluster = client.patch(path, payload)
                changed = True

    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.delete(path)
            changed = True

    module.exit_json(changed=changed, cluster=cluster)


if __name__ == "__main__":
    main()
