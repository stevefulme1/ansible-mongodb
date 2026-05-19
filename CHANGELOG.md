# Changelog

## [2.1.2] - 2026-05-18

### Security
- Added `no_log: true` to all `password` and `api_key` role arguments to prevent credential exposure in logs
- Changed EDA webhook default listen address from `0.0.0.0` to `127.0.0.1` to prevent unintended network exposure
- Added payload size limit (1 MB) to EDA webhook event source

## [2.0.1] - 2026-05-18

### Security
- Prevent credential leak in API request bodies: connection params (password,
  api_key, username, host, validate_certs) are now stripped before POST/PUT
- Added request timeout (30 s) to all HTTP methods to prevent hung connections
- Hardened .gitignore against accidental credential commits

## [2.0.0] - 2026-05-17

### Added
- Idempotency: get-before-write with state comparison in 27 modules
- Pagination support (limit/offset/max_results) for all 24 info modules
- Time-series, serverless instance, and auto-scaling modules
- EDA event filter plugin
- Comprehensive test suites for 15 MongoDB modules
- Pre-commit and linting configuration
- Sanity tests for ansible-core 2.16/2.17/2.18/2.20

### Fixed
- Pylint unhashable-member false positives resolved
- Stale sanity ignore files removed
- Long assert lines broken for E501 compliance
- Role README files added for Galaxy compliance
- Galaxy import validation issues resolved
- Python 3.13 unit test compatibility
- CI failures resolved

## [1.2.0] - 2026-05-15

### Added
- 48 modules covering full MongoDB platform (Atlas and self-hosted)
- 10 Day-2 operation roles
- EDA source plugins
- Dynamic inventory plugin

## [1.0.0] - 2026-05-15

### Added
- Initial release with Atlas and self-hosted MongoDB modules
- EDA change stream integration
- Unit tests and CI pipeline
