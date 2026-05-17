# stevefulme1.mongodb

Ansible Collection for MongoDB -- Atlas cluster/backup/networking/alerts, self-hosted replication/sharding/users, and EDA change stream integration.

## Overview

This collection provides **55 modules** for automating MongoDB infrastructure (both Atlas and self-hosted), along with 10 operational roles, a dynamic inventory plugin, and CI/CD workflows.

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
ansible-galaxy collection install stevefulme1-mongodb-2.0.0.tar.gz
```

## Included Content

### Modules (55)

CRUD and info modules covering:

- **Atlas** -- clusters, backups, networking, alerts, users, teams
- **Self-hosted** -- replication, sharding, users, roles, indexes
- **Time-series** -- time-series collection management
- **Serverless** -- serverless instance management
- **Auto-scaling** -- auto-scaling configuration
- **Monitoring** -- profiling, metrics, diagnostics

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

### Inventory Plugin

- `mongodb_inventory` -- Dynamic inventory from MongoDB clusters

## Usage

```yaml
- name: Create an Atlas cluster
  stevefulme1.mongodb.mongodb_atlas_cluster:
    api_public_key: "{{ atlas_public_key }}"
    api_private_key: "{{ atlas_private_key }}"
    project_id: "{{ atlas_project_id }}"
    name: production
    cluster_type: REPLICASET
    provider_name: AWS
    region: US_EAST_1
    instance_size: M30
    state: present
```

## License

Apache-2.0
