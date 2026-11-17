---
id: computing-software.cloud-infrastructure-engineering.google-cloud.debugging-cloud-sql-connection-failures
name: debugging-cloud-sql-connection-failures
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-sql, cloud-sql-connection-errors, cloud-sql-auth-proxy, too-many-connections, private-ip, connection-pooling]
level: practitioner
status: gated
description: "Diagnose Cloud SQL connection failures: Auth Proxy and connector errors, private IP routing, SSL mode mismatches, max connections exhaustion, IAM auth, and serverless pool sizing."
sources: ["https://cloud.google.com/sql/docs/mysql/diagnose-issues", "https://cloud.google.com/sql/docs/postgres/connect-auth-proxy#troubleshooting", "https://cloud.google.com/sql/docs/postgres/manage-connections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Cloud SQL connection failures

## Classify the error
| Error | Likely cause | Fix |
|---|---|---|
| Proxy: `failed to get instance metadata: googleapi: Error 403: ... cloudsql.instances.get` | proxy identity lacks `roles/cloudsql.client` | grant on project |
| Proxy: `Cloud SQL Admin API has not been used` | API disabled in proxy's project | enable `sqladmin.googleapis.com` |
| Proxy: `dial tcp 10.x.x.x:3307: i/o timeout` with `--private-ip` | no route/firewall to private IP, wrong VPC, PSA peering missing | check VPC, Direct VPC egress/connector for serverless |
| `connection refused` on 127.0.0.1 | proxy not running / wrong port | sidecar logs |
| `SSL connection is required` / `certificate verify failed` | `ssl_mode` ENCRYPTED_ONLY/TRUSTED_CLIENT_CERTIFICATE_REQUIRED vs client settings | use proxy/connectors (handle TLS) or client certs |
| `FATAL: remaining connection slots are reserved` / `Too many connections` | max_connections reached | pool sizing, raise flag, PgBouncer/managed pooling |
| `password authentication failed for user "sa@p.iam"` | IAM auth: missing `--auto-iam-authn`, user not created, no `cloudsql.instanceUser` | create IAM user, grant roles |
| `Instance is not running` / maintenance | instance stopped or failover | check operations list |

## Commands
```bash
gcloud sql instances describe <I> --format="yaml(state,ipAddresses,settings.ipConfiguration,settings.databaseFlags)"
gcloud sql operations list --instance=<I> --limit=10
./cloud-sql-proxy --private-ip --debug-logs <P>:<R>:<I>
```
Metrics: `cloudsql.googleapis.com/database/network/connections` (gated: unconfirmed, source is paywalled or blocked) (PostgreSQL `num_backends`) vs
max_connections; `database/network/received_bytes_count`.

## Serverless pool sizing
Max connections needed ~= max_instances x per-instance pool size. Cap Cloud Run `--max-instances`
and pool size (e.g. 5) so the total stays under `max_connections` minus headroom for admin.

## Gotchas
- Cloud SQL private IP is not reachable over VPC peering from another peered VPC (no transitive peering); use PSC or proxies.
- The proxy needs egress to `sqladmin.googleapis.com` (PGA/NAT) even when connecting via private IP.
- Connection storms after failover: use backoff and pool validation.

## Verify
- [ ] Connection from the workload succeeds with the intended path (private IP) and connection count stays below 80% of max.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: nothing removed; roles were checked against the Cloud SQL IAM roles page. Gated: the metric name cloudsql.googleapis.com/database/network/connections was not found in the fetched pages.

Method: documentation only; no commands were run.
