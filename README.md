# stevefulme1.mongodb

Ansible Collection for MongoDB -- Atlas cloud management and self-hosted database automation.

**Status: Pre-release (0.2.0). Under active development.**

## Overview

This collection provides modules for automating MongoDB infrastructure using real MongoDB drivers and APIs:

- **Atlas** (cloud) -- via MongoDB Atlas Administration API v2
- **Self-hosted** -- via `pymongo` Python driver

Placeholder roles are included for common operational workflows.

## Requirements

- ansible-core >= 2.16
- Python >= 3.11
- `pymongo` (for self-hosted modules)

## Installation

```bash
ansible-galaxy collection install stevefulme1.mongodb
```

Or from source:

```bash
ansible-galaxy collection build
ansible-galaxy collection install stevefulme1-mongodb-0.2.0.tar.gz
```

## Included Content

### Modules (16)

#### Self-hosted (pymongo-based)

| Module | Description |
|--------|-------------|
| `mongodb_database` | Create or drop MongoDB databases |
| `mongodb_database_info` | Gather information about MongoDB databases |
| `mongodb_user` | Manage MongoDB database users (createUser/updateUser/dropUser) |
| `mongodb_user_info` | Gather information about MongoDB users |
| `mongodb_index` | Manage collection indexes (create_index/drop_index) |
| `mongodb_index_info` | Gather information about collection indexes |
| `mongodb_replicaset` | Configure replica sets (replSetInitiate/replSetReconfig) |
| `mongodb_replicaset_info` | Gather replica set status information |

#### Atlas API (REST-based)

| Module | Description |
|--------|-------------|
| `mongodb_atlas_cluster` | Manage Atlas clusters |
| `mongodb_atlas_cluster_info` | Gather information about Atlas clusters |
| `mongodb_atlas_project` | Manage Atlas projects (groups) |
| `mongodb_atlas_project_info` | Gather information about Atlas projects |
| `mongodb_atlas_user` | Manage Atlas database users |
| `mongodb_atlas_user_info` | Gather information about Atlas database users |
| `mongodb_atlas_network` | Manage Atlas IP access lists |
| `mongodb_atlas_network_info` | Gather information about Atlas IP access lists |

### Module Utils

| Utility | Description |
|---------|-------------|
| `mongodb_client` | pymongo wrapper with auth, SSL, and replica set support |
| `atlas_client` | Atlas REST API client with digest authentication |

### Doc Fragments

| Fragment | Description |
|----------|-------------|
| `mongodb` | Shared params: login_host, login_port, login_user, login_password, login_database, ssl |
| `atlas` | Shared params: atlas_public_key, atlas_private_key, atlas_base_url |

### Roles (10)

| Role | Description |
|------|-------------|
| `mongodb_atlas_setup` | Provision Atlas clusters |
| `mongodb_backup` | Configure backup policies |
| `mongodb_cluster_setup` | Deploy self-hosted clusters |
| `mongodb_index_optimization` | Index analysis and optimization |
| `mongodb_monitoring` | Set up monitoring and alerting |
| `mongodb_restore` | Database restore operations |
| `mongodb_security_hardening` | Security baseline configuration |
| `mongodb_sharding_setup` | Configure sharded clusters |
| `mongodb_upgrade` | Version upgrade procedures |
| `mongodb_user_management` | User and role management |

## License

GPL-3.0-or-later

## Community

- [Contributing](CONTRIBUTING.md) - How to contribute to this project
- [Code of Conduct](CODE_OF_CONDUCT.md) - Ansible Community Code of Conduct
- [Security Policy](SECURITY.md) - How to report security vulnerabilities
