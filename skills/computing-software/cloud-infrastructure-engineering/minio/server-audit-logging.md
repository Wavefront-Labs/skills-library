---
id: computing-software.cloud-infrastructure-engineering.minio.server-audit-logging
name: server-audit-logging
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, server-audit-logging, logger-webhook, audit-webhook, http-webhook, minio-logger-webhook-endpoint, auth-token, journalctl]
level: practitioner
status: docs-checked
description: "Publish MinIO server and audit logs to an HTTP webhook with MINIO_LOGGER_WEBHOOK and MINIO_AUDIT_WEBHOOK variables or mc admin config set logger_webhook, with auth token format."
sources: ["https://github.com/minio/docs/blob/main/source/operations/monitoring/minio-logging.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO server and audit logs to HTTP webhooks

MinIO writes `minio server` operations to the console. Under systemd read them with `journalctl -u SERVICENAME.service`. It can also publish two log streams to an HTTP webhook as a JSON document in a `PUT` request to each endpoint; nothing is published unless you configure it, and the endpoint must process each document.
- **Server logs**: the same operations as the console, for monitoring and troubleshooting.
- **Audit logs**: granular per-operation records for security standards and regulations.

## Server log webhook, environment variables
Required: `MINIO_LOGGER_WEBHOOK_ENABLE` and `MINIO_LOGGER_WEBHOOK_ENDPOINT`.
```
export MINIO_LOGGER_WEBHOOK_ENABLE_<IDENTIFIER>="on"
export MINIO_LOGGER_WEBHOOK_ENDPOINT_<IDENTIFIER>="https://webhook-1.example.net"
export MINIO_LOGGER_WEBHOOK_AUTH_TOKEN_<IDENTIFIER>="TOKEN"
```
- `<IDENTIFIER>` names the endpoint and must match across its variables; reusing an existing identifier overrides that endpoint. Review with `mc admin config get ALIAS logger_webhook`.
- The token is placed in the auth header **exactly as written**, so prefix `Bearer ` or a custom scheme yourself. Omit it if the endpoint needs no auth.
- Restart and set identical variables on all servers.

## Server log webhook, config
```
mc admin config set ALIAS/ logger_webhook:IDENTIFIER \
   endpoint="https://webhook-1.example.net" auth_token="TOKEN"
```
Only `endpoint` is required. Restart the deployment afterwards.

## Audit logs
The same pattern uses `MINIO_AUDIT_WEBHOOK_ENABLE` and `MINIO_AUDIT_WEBHOOK_ENDPOINT` as the required variables, with optional `MINIO_AUDIT_WEBHOOK_AUTH_TOKEN`, `MINIO_AUDIT_WEBHOOK_CLIENT_CERT` and `MINIO_AUDIT_WEBHOOK_CLIENT_KEY` (certificate and key for client authentication), each suffixed with `_<IDENTIFIER>`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: minio-logging page: PUT of JSON per endpoint, server and audit webhook variables including AUTH_TOKEN, CLIENT_CERT and CLIENT_KEY, token used as written. Removed or fixed: nothing.

Method: documentation only; no commands were run.
