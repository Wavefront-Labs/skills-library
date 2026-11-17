---
id: computing-software.cloud-infrastructure-engineering.minio.lifecycle-management
name: lifecycle-management
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, lifecycle-management, ilm, mc-ilm-rule-add, expiration, transition, s3-lifecycle-compatibility, lifecycle-scanner]
level: practitioner
status: docs-checked
description: "MinIO object lifecycle management rules for time-based expiry and tiering, S3 rule compatibility, and why the low-priority scanner can apply rules after the rule period."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-lifecycle-management.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO object lifecycle management

Lifecycle rules automate time or date based **transition** (move to a remote tier) or **expiry** (delete) of objects. Syntax and behaviour follow S3 lifecycle, so rules can be exported from S3 and imported into MinIO or the reverse; MinIO describes rules in JSON, so XML to JSON conversion may be needed. Rules are created with `mc ilm rule add`.

## Where rules run
MinIO's built-in scanner checks objects against all lifecycle rules. It is a low-priority process that yields to heavy I/O to avoid spikes at rule times, so an object may not be detected as eligible until after the rule period has passed (`computing-software.cloud-infrastructure-engineering.minio.scanner`).

## Versioned buckets
MinIO adopts S3 behaviour:
- Rules apply to the **current** version by default.
- Expiry of the current version creates a `DeleteMarker`; non-current versions need `--noncurrent-expire-days`.
- Delete markers are not expired, even if no other versions exist, unless `--expire-delete-marker` is set.
- `--expire-all-object-versions` together with `--expire-days` permanently deletes all versions of objects (since RELEASE.2024-05-01T01-11-10Z only objects with no delete marker as latest).
- Transition applies to the current version unless `--noncurrent-transition-days` and `--noncurrent-transition-tier` are given.

## Replication
Objects deleted by a lifecycle expiration rule are not replicated as deletes on buckets with replication configured.

Related: `computing-software.cloud-infrastructure-engineering.minio.lifecycle-expiration-rules`, `computing-software.cloud-infrastructure-engineering.minio.tiering`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: object-lifecycle-management page: transition and expiry, scanner behaviour, versioned bucket rules, replication note. Removed or fixed: nothing.

Method: documentation only; no commands were run.
