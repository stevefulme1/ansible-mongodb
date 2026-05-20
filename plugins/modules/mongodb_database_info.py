#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_database_info
short_description: Gather information about MongoDB databases
description:
  - Return a list of databases on the MongoDB server.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  name:
    description:
      - Limit output to a specific database.
      - If not specified, all databases are returned.
    type: str
"""

EXAMPLES = r"""
- name: List all databases
  stevefulme1.mongodb.mongodb_database_info:
  register: result

- name: Get info for a specific database
  stevefulme1.mongodb.mongodb_database_info:
    name: myapp
  register: result
"""

RETURN = r"""
databases:
  description: List of database information dicts.
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
        name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    name = module.params.get("name")
    client = get_mongodb_client(module)

    try:
        db_list = client.list_databases()
        databases = []
        for db_info in db_list:
            if name and db_info["name"] != name:
                continue
            databases.append(db_info)

    except Exception as exc:
        module.fail_json(msg="Error listing databases: %s" % str(exc))
    finally:
        client.close()

    module.exit_json(changed=False, databases=databases)


if __name__ == "__main__":
    main()
