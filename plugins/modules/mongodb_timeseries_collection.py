#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.stevefulme1.mongodb.plugins.module_utils.mongodb_client import (
    get_mongodb_client,
    mongodb_common_argument_spec,
)
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mongodb_timeseries_collection
short_description: Manage MongoDB time series collections
description:
  - Create, update, or delete MongoDB time series collections.
  - Time series collections efficiently store sequences of measurements over a period of time.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.mongodb.connection
options:
  database:
    description:
      - The database name containing the collection.
    type: str
    required: true
  name:
    description:
      - The name of the time series collection.
    type: str
    required: true
  time_field:
    description:
      - The name of the field which contains the time for each measurement.
    type: str
    required: true
  meta_field:
    description:
      - The name of the field which contains metadata in each measurement.
    type: str
  granularity:
    description:
      - The granularity of measurements in the collection.
    type: str
    choices: [seconds, minutes, hours]
    default: seconds
  expire_after_seconds:
    description:
      - The number of seconds after which documents in the collection expire.
    type: int
  state:
    description:
      - Whether the time series collection should exist or not.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Create a time series collection for temperature data
  stevefulme1.mongodb.mongodb_timeseries_collection:
    mongodb_uri: "mongodb://localhost:27017"
    database: weather
    name: temperatures
    time_field: timestamp
    meta_field: sensor_id
    granularity: minutes
    state: present

- name: Create a time series collection with expiration
  stevefulme1.mongodb.mongodb_timeseries_collection:
    mongodb_uri: "mongodb://localhost:27017"
    database: metrics
    name: system_metrics
    time_field: timestamp
    meta_field: hostname
    granularity: seconds
    expire_after_seconds: 2592000  # 30 days
    state: present

- name: Delete a time series collection
  stevefulme1.mongodb.mongodb_timeseries_collection:
    mongodb_uri: "mongodb://localhost:27017"
    database: weather
    name: temperatures
    state: absent
"""

RETURN = r"""
timeseries_collection:
  description: The time series collection details.
  type: dict
  returned: when state is present
"""


def main():
    argument_spec = mongodb_common_argument_spec()
    argument_spec.update(
        database=dict(type="str", required=True),
        name=dict(type="str", required=True),
        time_field=dict(type="str", required=True),
        meta_field=dict(type="str"),
        granularity=dict(
            type="str",
            choices=["seconds", "minutes", "hours"],
            default="seconds",
        ),
        expire_after_seconds=dict(type="int"),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    database = module.params["database"]
    name = module.params["name"]
    state = module.params["state"]
    client = get_mongodb_client(module)

    changed = False
    timeseries_collection = {}

    # Check if collection exists
    db = client.get_database(database)
    exists = name in db.list_collection_names()

    if state == "present":
        if not exists:
            if not module.check_mode:
                timeseries_options = {
                    "timeField": module.params["time_field"],
                    "granularity": module.params["granularity"],
                }
                if module.params.get("meta_field"):
                    timeseries_options["metaField"] = module.params["meta_field"]

                create_options = {"timeseries": timeseries_options}

                if module.params.get("expire_after_seconds"):
                    create_options["expireAfterSeconds"] = module.params["expire_after_seconds"]

                db.create_collection(name, **create_options)

                timeseries_collection = {
                    "name": name,
                    "database": database,
                    "options": create_options,
                }
            changed = True
        else:
            # Collection exists, return current info
            timeseries_collection = {
                "name": name,
                "database": database,
                "exists": True,
            }

    elif state == "absent":
        if exists:
            if not module.check_mode:
                db.drop_collection(name)
            changed = True

    client.close()
    module.exit_json(
        changed=changed, timeseries_collection=timeseries_collection)


if __name__ == "__main__":
    main()
