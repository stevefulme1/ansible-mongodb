# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  login_host:
    description:
      - The host running the MongoDB instance to connect to.
    type: str
    default: localhost
  login_port:
    description:
      - The port on which MongoDB is listening.
    type: int
    default: 27017
  login_user:
    description:
      - The username used to authenticate with MongoDB.
    type: str
  login_password:
    description:
      - The password used to authenticate with MongoDB.
    type: str
  login_database:
    description:
      - The database where login credentials are stored.
    type: str
    default: admin
  ssl:
    description:
      - Whether to use SSL/TLS for the connection.
    type: bool
    default: false
  ssl_certfile:
    description:
      - The path to the client certificate file for SSL.
    type: str
  ssl_keyfile:
    description:
      - The path to the client private key file for SSL.
      - This is a filesystem path, not a secret value.
    type: str
  ssl_ca_certs:
    description:
      - The path to the CA certificate file for SSL.
    type: str
  connection_options:
    description:
      - Additional connection options passed to pymongo.MongoClient.
    type: dict
    default: {}
requirements:
  - pymongo
"""
