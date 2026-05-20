#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_atlas_network
short_description: Manage MongoDB Atlas IP access lists
description:
  - Add or remove entries from the MongoDB Atlas IP access list.
  - Uses the C(/api/atlas/v2/groups/{groupId}/accessList) endpoint.
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
  ip_address:
    description:
      - An IP address to add or remove from the access list.
      - Mutually exclusive with I(cidr_block) and I(aws_security_group).
    type: str
  cidr_block:
    description:
      - A CIDR block to add or remove from the access list.
      - Mutually exclusive with I(ip_address) and I(aws_security_group).
    type: str
  aws_security_group:
    description:
      - An AWS security group ID to add or remove.
      - Mutually exclusive with I(ip_address) and I(cidr_block).
    type: str
  comment:
    description:
      - A comment describing the access list entry.
    type: str
    default: Managed by Ansible
  state:
    description:
      - Whether the access list entry should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Allow an IP address
  stevefulme1.mongodb.mongodb_atlas_network:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    ip_address: 203.0.113.10
    comment: Office IP
    state: present

- name: Allow a CIDR block
  stevefulme1.mongodb.mongodb_atlas_network:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    cidr_block: 10.0.0.0/8
    state: present

- name: Remove an IP from the access list
  stevefulme1.mongodb.mongodb_atlas_network:
    atlas_public_key: "{{ atlas_pub_key }}"
    atlas_private_key: "{{ atlas_priv_key }}"
    group_id: 5e2211c17a3e5a48f5497de3
    ip_address: 203.0.113.10
    state: absent
"""

RETURN = r"""
entry:
  description: The access list entry details.
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
        ip_address=dict(type="str"),
        cidr_block=dict(type="str"),
        aws_security_group=dict(type="str"),
        comment=dict(type="str", default="Managed by Ansible"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("ip_address", "cidr_block", "aws_security_group"),
        ],
        required_one_of=[
            ("ip_address", "cidr_block", "aws_security_group"),
        ],
    )

    group_id = module.params["group_id"]
    ip_address = module.params.get("ip_address")
    cidr_block = module.params.get("cidr_block")
    aws_sg = module.params.get("aws_security_group")
    comment = module.params["comment"]
    state = module.params["state"]
    client = AtlasClient(module)

    base_path = "/groups/%s/accessList" % group_id
    changed = False
    entry = {}

    # Determine the entry identifier for lookup/delete
    if ip_address:
        # Atlas stores single IPs as /32 CIDR
        entry_id = ip_address.replace("/", "%%2F")
        payload_entry = {"ipAddress": ip_address, "comment": comment}
    elif cidr_block:
        entry_id = cidr_block.replace("/", "%%2F")
        payload_entry = {"cidrBlock": cidr_block, "comment": comment}
    else:
        entry_id = aws_sg
        payload_entry = {"awsSecurityGroup": aws_sg, "comment": comment}

    # Check if entry exists
    exists = False
    try:
        status, resp = client.get("%s/%s" % (base_path, entry_id))
        if status == 200 and resp:
            exists = True
            entry = resp
    except Exception:
        pass

    if state == "present":
        if not exists:
            if not module.check_mode:
                status, resp = client.post(base_path, [payload_entry])
                if resp and resp.get("results"):
                    entry = resp["results"][0]
            changed = True

    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.delete("%s/%s" % (base_path, entry_id))
            changed = True

    module.exit_json(changed=changed, entry=entry)


if __name__ == "__main__":
    main()
