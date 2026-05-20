#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_user
short_description: Manage MongoDB database users
description:
  - Create, update, or remove MongoDB database users.
  - Uses the createUser, updateUser, and dropUser database commands.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  database:
    description:
      - The database to manage the user in.
    type: str
    required: true
  user:
    description:
      - The name of the user to manage.
    type: str
    required: true
    aliases: [name]
  password:
    description:
      - The password for the user.
      - Required when I(state=present).
    type: str
  roles:
    description:
      - List of roles to grant to the user.
      - Each role can be a string or a dict with C(role) and C(db) keys.
    type: list
    elements: raw
    default: []
  state:
    description:
      - Whether the user should exist or not.
    type: str
    choices: [present, absent]
    default: present
  update_password:
    description:
      - Controls when the password is updated.
      - C(always) will always update the password.
      - C(on_create) will only set the password when creating the user.
    type: str
    choices: [always, on_create]
    default: always
"""

EXAMPLES = r"""
- name: Create a user with readWrite role
  stevefulme1.mongodb.mongodb_user:
    database: myapp
    user: appuser
    password: secret123
    roles:
      - readWrite
    state: present

- name: Create a user with roles on multiple databases
  stevefulme1.mongodb.mongodb_user:
    database: admin
    user: admin_user
    password: secret123
    roles:
      - role: readWrite
        db: myapp
      - role: dbAdmin
        db: myapp
    state: present

- name: Remove a user
  stevefulme1.mongodb.mongodb_user:
    database: myapp
    user: appuser
    state: absent
"""

RETURN = r"""
user:
  description: The name of the user managed.
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)


def user_exists(db, username):
    """Check if a user exists in the database."""
    try:
        user_info = db.command("usersInfo", username)
        return len(user_info.get("users", [])) > 0
    except Exception:
        return False


def main():
    argument_spec = mongodb_common_argument_spec()
    argument_spec.update(
        database=dict(type="str", required=True),
        user=dict(type="str", required=True, aliases=["name"]),
        password=dict(type="str", no_log=True),
        roles=dict(type="list", elements="raw", default=[]),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        update_password=dict(
            type="str", choices=["always", "on_create"], default="always"
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["password"]),
        ],
    )

    database = module.params["database"]
    username = module.params["user"]
    password = module.params["password"]
    roles = module.params["roles"]
    state = module.params["state"]
    update_password = module.params["update_password"]

    client = get_mongodb_client(module)
    changed = False

    try:
        db = client[database]
        exists = user_exists(db, username)

        if state == "present":
            if not exists:
                if not module.check_mode:
                    db.command("createUser", username, pwd=password, roles=roles)
                changed = True
            else:
                # Update existing user
                update_cmd = {}
                if update_password == "always":
                    update_cmd["pwd"] = password
                if roles:
                    update_cmd["roles"] = roles
                if update_cmd:
                    if not module.check_mode:
                        db.command("updateUser", username, **update_cmd)
                    changed = True

        elif state == "absent":
            if exists:
                if not module.check_mode:
                    db.command("dropUser", username)
                changed = True

    except Exception as exc:
        module.fail_json(
            msg="Error managing user '%s' in database '%s': %s"
            % (username, database, str(exc))
        )
    finally:
        client.close()

    module.exit_json(changed=changed, user=username)


if __name__ == "__main__":
    main()
