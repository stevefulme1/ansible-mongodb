#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_replicaset
short_description: Configure MongoDB replica sets
description:
  - Initialize a MongoDB replica set or manage its members.
  - Uses rs.initiate() and rs.reconfig() commands via pymongo.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  replica_set:
    description:
      - The name of the replica set.
    type: str
    required: true
  members:
    description:
      - List of replica set members.
      - Each member can be a host string or a dict with C(host) and optional C(priority) and C(arbiterOnly) keys.
    type: list
    elements: raw
    required: true
  validate:
    description:
      - Whether to wait for all members to be healthy after configuration.
    type: bool
    default: true
"""

EXAMPLES = r"""
- name: Initialize a replica set
  stevefulme1.mongodb.mongodb_replicaset:
    replica_set: rs0
    members:
      - mongo1.example.com:27017
      - mongo2.example.com:27017
      - host: mongo3.example.com:27017
        arbiterOnly: true

- name: Reconfigure replica set members
  stevefulme1.mongodb.mongodb_replicaset:
    replica_set: rs0
    members:
      - mongo1.example.com:27017
      - mongo2.example.com:27017
      - mongo3.example.com:27017
"""

RETURN = r"""
replica_set:
  description: The name of the replica set.
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)


def get_rs_status(client):
    """Get replica set status, return None if not initialized."""
    try:
        return client.admin.command("replSetGetStatus")
    except Exception:
        return None


def build_member_config(members):
    """Build replica set member configuration list."""
    config_members = []
    for idx, member in enumerate(members):
        if isinstance(member, str):
            config_members.append({"_id": idx, "host": member})
        elif isinstance(member, dict):
            entry = {"_id": idx, "host": member["host"]}
            if member.get("priority") is not None:
                entry["priority"] = member["priority"]
            if member.get("arbiterOnly"):
                entry["arbiterOnly"] = True
            config_members.append(entry)
    return config_members


def main():
    argument_spec = mongodb_common_argument_spec()
    argument_spec.update(
        replica_set=dict(type="str", required=True),
        members=dict(type="list", elements="raw", required=True),
        validate=dict(type="bool", default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    replica_set = module.params["replica_set"]
    members = module.params["members"]
    client = get_mongodb_client(module)
    changed = False

    try:
        rs_status = get_rs_status(client)
        member_config = build_member_config(members)

        if rs_status is None:
            # Replica set not initialized - initiate
            config = {
                "_id": replica_set,
                "members": member_config,
            }
            if not module.check_mode:
                client.admin.command("replSetInitiate", config)
            changed = True
        else:
            # Replica set exists - reconfig if members changed
            current_config = client.admin.command("replSetGetConfig")["config"]
            current_hosts = sorted(
                [m["host"] for m in current_config["members"]]
            )
            new_hosts = sorted([m["host"] for m in member_config])

            if current_hosts != new_hosts:
                new_config = current_config.copy()
                new_config["members"] = member_config
                new_config["version"] = current_config["version"] + 1
                if not module.check_mode:
                    client.admin.command("replSetReconfig", new_config)
                changed = True

    except Exception as exc:
        module.fail_json(
            msg="Error configuring replica set '%s': %s" % (replica_set, str(exc))
        )
    finally:
        client.close()

    module.exit_json(changed=changed, replica_set=replica_set)


if __name__ == "__main__":
    main()
