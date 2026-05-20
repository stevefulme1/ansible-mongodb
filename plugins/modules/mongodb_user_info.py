#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_user_info
short_description: Gather information about MongoDB users
description:
  - Return user information from a MongoDB database.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  database:
    description:
      - The database to query users from.
    type: str
    required: true
  user:
    description:
      - Limit output to a specific user.
      - If not specified, all users in the database are returned.
    type: str
    aliases: [name]
"""

EXAMPLES = r"""
- name: List all users in a database
  stevefulme1.mongodb.mongodb_user_info:
    database: admin
  register: result

- name: Get info for a specific user
  stevefulme1.mongodb.mongodb_user_info:
    database: admin
    user: appuser
  register: result
"""

RETURN = r"""
users:
  description: List of user information dicts.
  type: list
  elements: dict
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)


def main():
    argument_spec = mongodb_common_argument_spec()
    argument_spec.update(
        database=dict(type="str", required=True),
        user=dict(type="str", aliases=["name"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    database = module.params["database"]
    username = module.params.get("user")
    client = get_mongodb_client(module)

    try:
        db = client[database]
        if username:
            user_info = db.command("usersInfo", username)
        else:
            user_info = db.command("usersInfo", 1)

        users = user_info.get("users", [])
        # Convert to serializable format
        result_users = []
        for user in users:
            entry = {
                "user": user.get("user"),
                "db": user.get("db"),
                "roles": user.get("roles", []),
            }
            result_users.append(entry)

    except Exception as exc:
        module.fail_json(
            msg="Error retrieving user info from '%s': %s" % (database, str(exc))
        )
    finally:
        client.close()

    module.exit_json(changed=False, users=result_users)


if __name__ == "__main__":
    main()
