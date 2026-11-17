---
id: computing-software.web-development.directus.self-host-requirements
name: self-host-requirements
category: computing-software
field: web-development
product: directus
tags: [self-host-requirements, supported-databases, storage-adapters, redis-scaling]
level: intro
status: docs-checked
description: "Check Directus self-hosting requirements: Docker, compute sizing, supported databases, storage adapters, and Redis for caching and horizontal scaling."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/self-hosting/2.requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Directus ships as a Docker image, so the host must run Docker and let you edit environment variables.

- **Compute**: minimum 1 instance of 0.25 vCPU / 512 MB; recommended minimum 2 instances of 1 vCPU / 2 GB. Under-provisioning is easy.
- **Database**: the image bundles all optional drivers. Supported are long-term-support versions of PostgreSQL, MySQL, SQLite, MS SQL Server, MariaDB, CockroachDB and OracleDB. One database with multiple schemas is not supported.
- **Storage**: a storage adapter pattern; configure an adapter through variables or mount a local directory as a volume.
- **Redis**: optional for caching but recommended, and required to scale horizontally.
- **Also consider**: backups for database and assets, a CDN, a load balancer across instances, and monitoring.

Checklist:
1. Pick the database and confirm LTS version.
2. Decide asset storage (volume or adapter).
3. Add Redis if you plan more than one instance.
4. Size containers per the recommended minimum.

## Checked

2026-11-04: Docker image, compute minimum and recommended sizes, supported databases, the multiple-schemas limitation, storage adapter pattern, Redis for caching and horizontal scaling and the recommendations confirmed against the Directus Self-Hosting Requirements page. Removed an unsupported Verify line.

Method: documentation only; no commands were run.
