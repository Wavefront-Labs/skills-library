---
id: computing-software.systems-network-administration.healthchecks.config-email-and-s3
name: config-email-and-s3
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, s3-object-storage, ping-body-storage, email-settings, secret-files]
level: advanced
status: docs-checked
description: "Self-hosted Healthchecks S3-compatible storage for ping bodies (S3_* variables) and the email variables, with _FILE secret variants taking precedence."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
S3-compatible storage keeps ping bodies (those larger than 100 bytes) outside the database:
- `S3_ACCESS_KEY`, `S3_SECRET_KEY` (or `S3_SECRET_KEY_FILE`)
- `S3_ENDPOINT`: URL of the S3-compatible service
- `S3_REGION`, `S3_BUCKET`
- `S3_TIMEOUT` (default 60 seconds per operation)
- `S3_SECURE` (default True): use TLS

If the storage is unreachable, the API ping-body endpoint returns 503. Clean orphaned objects with `pruneobjects`.

Email (outgoing): `EMAIL_HOST`, `EMAIL_PORT` (587), `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` (True), `EMAIL_USE_SSL` (False), `EMAIL_USE_VERIFICATION` (True), `DEFAULT_FROM_EMAIL`. See self-hosted-email-sending for the port 465 and 587 combinations.

Secrets via files: for variables such as `DB_PASSWORD_FILE`, `EMAIL_HOST_PASSWORD_FILE`, `SECRET_KEY_FILE` and `S3_SECRET_KEY_FILE`, the file contents become the variable's value and take precedence over it.

Ping address domain: `PING_EMAIL_DOMAIN` (default `localhost`).

## Checked

2026-11-04. Confirmed against the Healthchecks server configuration page and README: S3_* variables and defaults (S3_TIMEOUT 60, S3_SECURE True), the 100-byte threshold for external storage, pruneobjects, EMAIL_* defaults, _FILE variables taking precedence, PING_EMAIL_DOMAIN default, and the API ping-body 503 when object storage is unavailable. Nothing removed.

Method: documentation only; no commands were run.
