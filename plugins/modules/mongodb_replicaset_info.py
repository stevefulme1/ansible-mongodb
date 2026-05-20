#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_replicaset_info
short_description: Gather information about a MongoDB replica set
description:
  - Return the status and configuration of a MongoDB replica set.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
"""

EXAMPLES = r"""
- name: Get replica set status
  stevefulme1.mongodb.mongodb_replicaset_info:
  register: result
"""

RETURN = r"""
replicaset:
  description: Replica set status information.
  type: dict
  returned: always
  contains:
    set:
      description: Name of the replica set.
      type: str
    members:
      description: List of replica set members and their states.
      type: list
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)


def main():
    argument_spec = mongodb_common_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    client = get_mongodb_client(module)

    try:
        rs_status = client.admin.command("replSetGetStatus")
        # Convert to serializable format
        result = {
            "set": rs_status.get("set"),
            "myState": rs_status.get("myState"),
            "members": [],
        }
        for member in rs_status.get("members", []):
            result["members"].append(
                {
                    "_id": member.get("_id"),
                    "name": member.get("name"),
                    "stateStr": member.get("stateStr"),
                    "health": member.get("health"),
                }
            )
    except Exception as exc:
        module.fail_json(msg="Error retrieving replica set status: %s" % str(exc))
    finally:
        client.close()

    module.exit_json(changed=False, replicaset=result)


if __name__ == "__main__":
    main()
