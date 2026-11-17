---
id: computing-software.data-engineering.kestra.system-requirements
name: system-requirements
category: computing-software
field: data-engineering
product: kestra
tags: [requirements, postgresql, mysql, read-committed, java, sizing]
level: intro
status: docs-checked
description: "Kestra software and hardware requirements: Java, supported databases and storage, the MySQL READ COMMITTED rule, and minimum standalone sizing."
sources:
  - https://kestra.io/docs/administrator-guide/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Software:

- Java: runtime JDK 25 (Eclipse Temurin default); source and target 21, built with `--release 21`.
- Open source queue and repository: PostgreSQL 14 or later, or MySQL 8 or later excluding 8.0.31.
- Enterprise adds Apache Kafka 3+, Elasticsearch 7+ and OpenSearch 2+ for large deployments.
- Internal storage: Google Cloud Storage, AWS S3, Azure Blob Storage, or S3-compatible via the `minio` type.

MySQL:

- Kestra requires `READ COMMITTED`; the MySQL default `REPEATABLE READ` can deadlock the JDBC queue and raises an `IllegalStateException`.
- Set `transaction_isolation=READ-COMMITTED` under `[mysqld]` in `my.cnf`, or the parameter group or database flags on managed services.
- If you cannot change the server, set `transaction-isolation: TRANSACTION_READ_COMMITTED` in the Kestra datasource configuration.
- Load the MySQL time zone tables, or the scheduler may misfire or skip runs.

Hardware: a standalone server needs at least 4 GiB memory and 2 vCPUs. Script tasks require Docker-in-Docker support, so platforms without it (the page cites AWS ECS Fargate) are unsupported.

## Checked

2026-11-04. Confirmed against "Prerequisites: software and hardware requirements before deploying Kestra" (administrator-guide/requirements): Java runtime and release target, PostgreSQL and MySQL versions, Enterprise Kafka, Elasticsearch and OpenSearch minimums, internal storage providers and minio type, MySQL READ COMMITTED guidance and settings, time zone tables, 4 GiB and 2 vCPU standalone minimum, Docker-in-Docker and ECS Fargate note. No claims removed.
Method: documentation only; no commands were run.
