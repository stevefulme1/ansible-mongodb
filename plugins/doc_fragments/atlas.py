# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  atlas_public_key:
    description:
      - The public key for MongoDB Atlas API authentication.
    type: str
    required: true
  atlas_private_key:
    description:
      - The private key for MongoDB Atlas API authentication.
    type: str
    required: true
  atlas_base_url:
    description:
      - The base URL for the MongoDB Atlas API.
    type: str
    default: https://cloud.mongodb.com/api/atlas/v2
"""
