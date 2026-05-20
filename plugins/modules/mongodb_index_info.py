#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_index_info
short_description: Gather information about MongoDB collection indexes
description:
  - Return index information for a MongoDB collection.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.mongodb
options:
  database:
    description:
      - The database containing the collection.
    type: str
    required: true
  collection:
    description:
      - The collection to list indexes for.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: List all indexes on a collection
  stevefulme1.mongodb.mongodb_index_info:
    database: myapp
    collection: users
  register: result
"""

RETURN = r"""
indexes:
  description: Dict of index names to their definitions.
  type: dict
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
        collection=dict(type="str", required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    database = module.params["database"]
    collection_name = module.params["collection"]
    client = get_mongodb_client(module)

    try:
        db = client[database]
        collection = db[collection_name]
        indexes = collection.index_information()

    except Exception as exc:
        module.fail_json(
            msg="Error listing indexes on '%s.%s': %s"
            % (database, collection_name, str(exc))
        )
    finally:
        client.close()

    module.exit_json(changed=False, indexes=indexes)


if __name__ == "__main__":
    main()
