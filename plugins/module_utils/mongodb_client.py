# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from pymongo import MongoClient
    from pymongo.errors import (
        ConnectionFailure,
        OperationFailure,
        PyMongoError,
    )

    HAS_PYMONGO = True
    PYMONGO_IMPORT_ERROR = None
except ImportError as e:
    HAS_PYMONGO = False
    PYMONGO_IMPORT_ERROR = str(e)
    MongoClient = None
    ConnectionFailure = Exception
    OperationFailure = Exception
    PyMongoError = Exception


def mongodb_common_argument_spec():
    """Return common argument spec for MongoDB modules."""
    return dict(
        login_host=dict(type="str", default="localhost"),
        login_port=dict(type="int", default=27017),
        login_user=dict(type="str"),
        login_password=dict(type="str", no_log=True),
        login_database=dict(type="str", default="admin"),
        ssl=dict(type="bool", default=False),
        ssl_certfile=dict(type="str"),
        ssl_keyfile=dict(type="str", no_log=False),
        ssl_ca_certs=dict(type="str"),
        connection_options=dict(type="dict", default={}),
    )


def get_mongodb_client(module):
    """Create and return a pymongo MongoClient from module params.

    Args:
        module: AnsibleModule instance with MongoDB connection params.

    Returns:
        pymongo.MongoClient instance.
    """
    if not HAS_PYMONGO:
        module.fail_json(
            msg="pymongo is required for this module: %s" % PYMONGO_IMPORT_ERROR
        )

    params = module.params
    kwargs = dict(
        host=params["login_host"],
        port=params["login_port"],
    )

    if params.get("login_user"):
        kwargs["username"] = params["login_user"]
    if params.get("login_password"):
        kwargs["password"] = params["login_password"]
    if params.get("login_database"):
        kwargs["authSource"] = params["login_database"]

    if params.get("ssl"):
        kwargs["tls"] = True
        if params.get("ssl_certfile"):
            kwargs["tlsCertificateKeyFile"] = params["ssl_certfile"]
        if params.get("ssl_keyfile"):
            kwargs["tlsCertificateKeyFile"] = params["ssl_keyfile"]
        if params.get("ssl_ca_certs"):
            kwargs["tlsCAFile"] = params["ssl_ca_certs"]

    if params.get("connection_options"):
        kwargs.update(params["connection_options"])

    kwargs["serverSelectionTimeoutMS"] = kwargs.get("serverSelectionTimeoutMS", 10000)

    try:
        client = MongoClient(**kwargs)
        # Force a connection check
        client.admin.command("ping")
        return client
    except ConnectionFailure as exc:
        module.fail_json(
            msg="Unable to connect to MongoDB: %s" % str(exc)
        )
    except OperationFailure as exc:
        module.fail_json(
            msg="Authentication failed for MongoDB: %s" % str(exc)
        )
    except PyMongoError as exc:
        module.fail_json(
            msg="MongoDB error: %s" % str(exc)
        )
    return None  # unreachable, satisfies linters
