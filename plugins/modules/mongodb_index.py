#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_index
short_description: Manage MongoDB collection indexes
description:
  - Create or drop indexes on MongoDB collections.
  - Uses pymongo create_index and drop_index methods.
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
      - The collection to manage indexes on.
    type: str
    required: true
  name:
    description:
      - The name of the index.
      - Required when I(state=absent).
    type: str
  keys:
    description:
      - The index keys as a dict mapping field names to sort order.
      - Use C(1) for ascending and C(-1) for descending.
      - Required when I(state=present).
    type: dict
  unique:
    description:
      - Whether the index should enforce uniqueness.
    type: bool
    default: false
  sparse:
    description:
      - Whether the index should be sparse.
    type: bool
    default: false
  state:
    description:
      - Whether the index should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create an ascending index on email field
  stevefulme1.mongodb.mongodb_index:
    database: myapp
    collection: users
    keys:
      email: 1
    unique: true

- name: Create a compound index
  stevefulme1.mongodb.mongodb_index:
    database: myapp
    collection: orders
    keys:
      customer_id: 1
      created_at: -1

- name: Drop an index by name
  stevefulme1.mongodb.mongodb_index:
    database: myapp
    collection: users
    name: email_1
    state: absent
"""

RETURN = r"""
name:
  description: The name of the index that was created or dropped.
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)


def index_exists(collection, index_name):
    """Check if an index exists on a collection."""
    indexes = collection.index_information()
    return index_name in indexes


def main():
    argument_spec = mongodb_common_argument_spec()
    argument_spec.update(
        database=dict(type="str", required=True),
        collection=dict(type="str", required=True),
        name=dict(type="str"),
        keys=dict(type="dict", no_log=False),
        unique=dict(type="bool", default=False),
        sparse=dict(type="bool", default=False),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["keys"]),
            ("state", "absent", ["name"]),
        ],
    )

    database = module.params["database"]
    collection_name = module.params["collection"]
    index_name = module.params.get("name")
    keys = module.params.get("keys")
    unique = module.params["unique"]
    sparse = module.params["sparse"]
    state = module.params["state"]

    client = get_mongodb_client(module)
    changed = False
    result_name = index_name or ""

    try:
        db = client[database]
        collection = db[collection_name]

        if state == "present":
            # Convert keys dict to list of tuples for pymongo
            key_list = [(k, int(v)) for k, v in keys.items()]

            kwargs = {}
            if index_name:
                kwargs["name"] = index_name
            if unique:
                kwargs["unique"] = True
            if sparse:
                kwargs["sparse"] = True

            if not module.check_mode:
                result_name = collection.create_index(key_list, **kwargs)
            else:
                # Generate expected name
                if index_name:
                    result_name = index_name
                else:
                    result_name = "_".join(
                        "%s_%s" % (k, v) for k, v in keys.items()
                    )
            changed = True

        elif state == "absent":
            if index_exists(collection, index_name):
                if not module.check_mode:
                    collection.drop_index(index_name)
                changed = True
            result_name = index_name

    except Exception as exc:
        module.fail_json(
            msg="Error managing index on '%s.%s': %s"
            % (database, collection_name, str(exc))
        )
    finally:
        client.close()

    module.exit_json(changed=changed, name=result_name)


if __name__ == "__main__":
    main()
