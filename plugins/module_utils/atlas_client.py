# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.urls import open_url


def atlas_common_argument_spec():
    """Return common argument spec for Atlas modules."""
    return dict(
        atlas_public_key=dict(type="str", required=True),
        atlas_private_key=dict(type="str", required=True, no_log=True),
        atlas_base_url=dict(
            type="str", default="https://cloud.mongodb.com/api/atlas/v2"
        ),
    )


class AtlasClient(object):
    """Client for the MongoDB Atlas REST API with Digest authentication."""

    def __init__(self, module):
        self.module = module
        self.public_key = module.params["atlas_public_key"]
        self.private_key = module.params["atlas_private_key"]
        self.base_url = module.params["atlas_base_url"].rstrip("/")

    def _url(self, path):
        """Build full URL from path."""
        return "%s%s" % (self.base_url, path)

    def request(self, method, path, data=None):
        """Make an API request to Atlas.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE).
            path: API path (e.g. /api/atlas/v2/groups).
            data: Request body dict (will be JSON-encoded).

        Returns:
            Tuple of (status_code, response_dict).
        """
        url = self._url(path)
        headers = {
            "Accept": "application/vnd.atlas.2023-01-01+json",
            "Content-Type": "application/json",
        }

        body = None
        if data is not None:
            body = json.dumps(data)

        try:
            resp = open_url(
                url,
                method=method,
                data=body,
                headers=headers,
                url_username=self.public_key,
                url_password=self.private_key,
                force_basic_auth=False,
                validate_certs=True,
            )
            status = resp.getcode()
            content = resp.read()
            if content:
                return status, json.loads(content)
            return status, {}
        except Exception as exc:
            error_body = ""
            if hasattr(exc, "read"):
                try:
                    error_body = exc.read()
                except Exception:
                    pass
            status_code = getattr(exc, "code", 0)
            self.module.fail_json(
                msg="Atlas API error: %s %s -> %s %s"
                % (method, url, str(exc), error_body),
                status_code=status_code,
            )
        return None, None  # unreachable, satisfies linters

    def get(self, path):
        """Make a GET request."""
        return self.request("GET", path)

    def post(self, path, data):
        """Make a POST request."""
        return self.request("POST", path, data)

    def patch(self, path, data):
        """Make a PATCH request."""
        return self.request("PATCH", path, data)

    def delete(self, path):
        """Make a DELETE request."""
        return self.request("DELETE", path)
