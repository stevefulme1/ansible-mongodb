# Changelog

## [0.2.0] - 2026-05-20

### Added
- 8 self-hosted modules using pymongo: mongodb_database, mongodb_database_info, mongodb_user, mongodb_user_info, mongodb_index, mongodb_index_info, mongodb_replicaset, mongodb_replicaset_info
- 8 Atlas API modules: mongodb_atlas_cluster, mongodb_atlas_cluster_info, mongodb_atlas_project, mongodb_atlas_project_info, mongodb_atlas_user, mongodb_atlas_user_info, mongodb_atlas_network, mongodb_atlas_network_info
- Module utils: mongodb_client.py (pymongo wrapper with auth/SSL/replica set), atlas_client.py (Atlas REST client with digest auth)
- Doc fragments: mongodb.py (shared connection params), atlas.py (shared Atlas API params)
- All modules include DOCUMENTATION, EXAMPLES, RETURN blocks and check_mode support

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
