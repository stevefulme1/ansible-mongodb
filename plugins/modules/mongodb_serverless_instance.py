#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_serverless_instance
short_description: Manage MongoDB Atlas serverless instances
description:
  - Create, update, or delete MongoDB Atlas serverless instances.
  - Uses the C(/api/atlas/v2/groups/{groupId}/serverless) endpoint.
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
      - The name of the serverless instance.
    type: str
    required: true
  provider_name:
    description:
      - The cloud provider for the serverless instance.
    type: str
    choices: [AWS, GCP, AZURE]
    default: AWS
  region_name:
    description:
      - The cloud provider region.
    type: str
    default: US_EAST_1
  continuous_backup_enabled:
    description:
      - Whether to enable continuous backup for the serverless instance.
    type: bool
    default: false
  state:
    description:
      - Whether the serverless instance should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create a serverless instance
  stevefulme1.mongodb.mongodb_serverless_instance:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    name: my-serverless-instance
    provider_name: AWS
    region_name: US_EAST_1
    continuous_backup_enabled: true
    state: present

- name: Delete a serverless instance
  stevefulme1.mongodb.mongodb_serverless_instance:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    name: my-serverless-instance
    state: absent
"""

RETURN = r"""
serverless_instance:
  description: The serverless instance details returned by the Atlas API.
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
        provider_name=dict(
            type="str",
            choices=["AWS", "GCP", "AZURE"],
            default="AWS",
        ),
        region_name=dict(type="str", default="US_EAST_1"),
        continuous_backup_enabled=dict(type="bool", default=False),
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

    path = "/groups/%s/serverless/%s" % (group_id, name)
    changed = False
    serverless_instance = {}

    # Check if serverless instance exists
    exists = False
    try:
        status, resp = client.get(path)
        if status == 200:
            exists = True
            serverless_instance = resp
    except Exception:
        pass

    if state == "present":
        payload = {
            "name": name,
            "providerSettings": {
                "providerName": module.params["provider_name"],
                "regionName": module.params["region_name"],
            },
            "continuousBackupEnabled": module.params["continuous_backup_enabled"],
        }

        if not exists:
            if not module.check_mode:
                status, serverless_instance = client.post(
                    "/groups/%s/serverless" % group_id, payload
                )
            changed = True
        else:
            # Check if update needed
            current_backup = serverless_instance.get("continuousBackupEnabled", False)
            if current_backup != module.params["continuous_backup_enabled"]:
                if not module.check_mode:
                    status, serverless_instance = client.patch(path, payload)
                changed = True

    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.delete(path)
            changed = True

    module.exit_json(changed=changed, serverless_instance=serverless_instance)


if __name__ == "__main__":
    main()
