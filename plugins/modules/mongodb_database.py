#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_database
short_description: Manage MongoDB databases
description:
  - Create or drop MongoDB databases.
  - A database is created implicitly when a collection is created in it.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  name:
    description:
      - The name of the database to manage.
    type: str
    required: true
  state:
    description:
      - Whether the database should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create a database by ensuring a collection exists
  stevefulme1.mongodb.mongodb_database:
    name: myapp
    state: present

- name: Drop a database
  stevefulme1.mongodb.mongodb_database:
    name: myapp
    state: absent
"""

RETURN = r"""
name:
  description: The name of the database.
  type: str
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
        name=dict(type="str", required=True),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    name = module.params["name"]
    state = module.params["state"]
    client = get_mongodb_client(module)
    changed = False

    try:
        existing_dbs = client.list_database_names()
        db_exists = name in existing_dbs

        if state == "present":
            if not db_exists:
                if not module.check_mode:
                    # Create database by inserting into a placeholder collection
                    db = client[name]
                    db.create_collection("_ansible_placeholder")
                changed = True

        elif state == "absent":
            if db_exists:
                if not module.check_mode:
                    client.drop_database(name)
                changed = True

    except Exception as exc:
        module.fail_json(msg="Error managing database '%s': %s" % (name, str(exc)))
    finally:
        client.close()

    module.exit_json(changed=changed, name=name)


if __name__ == "__main__":
    main()
