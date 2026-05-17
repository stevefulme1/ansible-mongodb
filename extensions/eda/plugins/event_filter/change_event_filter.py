"""Filter MongoDB change stream events by operation type."""

DOCUMENTATION = r"""
---
event_filter: change_event_filter
short_description: Filter MongoDB change events by operation type
description:
  - Filters MongoDB change stream or oplog events by operation type
    (insert, update, replace, delete, drop, invalidate).
  - Optionally filters by database name and collection name.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  operations:
    description: List of operation types to include.
    type: list
    elements: str
    default: [insert, update, delete]
  databases:
    description:
      - List of database names to include. Empty means all databases.
    type: list
    elements: str
    default: []
  collections:
    description:
      - List of collection names to include. Empty means all collections.
    type: list
    elements: str
    default: []
  exclude_system:
    description: Whether to exclude system collections (those starting with C(system.)).
    type: bool
    default: true
"""

EXAMPLES = r"""
- stevefulme1.mongodb.change_event_filter:
    operations: [insert, update]
    databases: [production]
    exclude_system: true
"""


def main(event, operations=None, databases=None, collections=None, exclude_system=True):
    """Filter MongoDB change events."""
    if not isinstance(event, dict):
        return event
    if operations is None:
        operations = ["insert", "update", "delete"]
    if databases is None:
        databases = []
    if collections is None:
        collections = []

    payload = event.get("payload", event)

    # Get operation type
    op_type = str(payload.get("operationType", payload.get("op", ""))).lower()
    # Map oplog single-char ops to full names
    op_map = {"i": "insert", "u": "update", "d": "delete", "c": "command"}
    op_type = op_map.get(op_type, op_type)

    if op_type not in [o.lower() for o in operations]:
        return None

    # Get namespace
    ns = payload.get("ns", {})
    if isinstance(ns, dict):
        db = ns.get("db", "")
        coll = ns.get("coll", "")
    else:
        parts = str(ns).split(".", 1)
        db = parts[0] if parts else ""
        coll = parts[1] if len(parts) > 1 else ""

    if exclude_system and coll.startswith("system."):
        return None

    if databases and db not in databases:
        return None

    if collections and coll not in collections:
        return None

    return event
