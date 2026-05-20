# stevefulme1.mongodb

Ansible Collection for MongoDB -- Atlas cloud management and self-hosted database automation.

**Status: Pre-release (0.1.0). Under active development.**

## Overview

This collection will provide modules for automating MongoDB infrastructure using real MongoDB drivers and APIs:

- **Atlas** (cloud) -- via MongoDB Atlas Administration API
- **Self-hosted** -- via `pymongo` Python driver

Placeholder roles are included for common operational workflows.

## Requirements

- ansible-core >= 2.16
- Python >= 3.11

## Installation

```bash
ansible-galaxy collection install stevefulme1.mongodb
```

Or from source:

```bash
ansible-galaxy collection build
ansible-galaxy collection install stevefulme1-mongodb-0.1.0.tar.gz
```

## Included Content

### Modules

No modules yet. Modules will use:

- `pymongo` for self-hosted MongoDB operations
- MongoDB Atlas Administration API v2 for cloud resources

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
