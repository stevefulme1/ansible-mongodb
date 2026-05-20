# Changelog

## [0.1.0] - 2026-05-20

### Removed
- Deleted 54 fabricated modules that used fake REST API endpoints instead of real pymongo/Atlas API
- Deleted fabricated api_client.py module_utils (generic REST wrapper)
- Deleted fabricated mongodb_inventory dynamic inventory plugin
- Deleted fabricated EDA event source plugins (change_stream, oplog_tail)
- Deleted associated unit tests for removed modules

### Retained
- 10 placeholder roles for common MongoDB operational workflows
- Collection scaffolding (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, MAINTAINERS)
- CI/CD workflow configuration

### Notes
- Version reset to 0.1.0 to reflect pre-release status
- Future modules will use pymongo for self-hosted and Atlas Administration API v2 for cloud
