---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-sql-ssl-modes-and-client-certificates
name: cloud-sql-ssl-modes-and-client-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-sql, cloud-sql-ssl, server-ca, client-certificates, tls, cloud-sql-auth-proxy, ca-rotation]
level: practitioner
status: docs-checked
description: "Enforce encrypted Cloud SQL connections: SSL modes, server CA modes and rotation, client certificates for direct connections, and why connectors/Auth Proxy are usually simpler."
sources: ["https://docs.cloud.google.com/sql/docs/postgres/configure-ssl-instance", "https://docs.cloud.google.com/sql/docs/postgres/manage-ssl-instance", "https://docs.cloud.google.com/sql/docs/mysql/authorize-ssl", "https://docs.cloud.google.com/sql/docs/postgres/sql-proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SQL SSL modes and client certificates

## 1. Require encryption
```bash
gcloud sql instances patch db1 --ssl-mode=ENCRYPTED_ONLY
# or mutual TLS for direct connections:
gcloud sql instances patch db1 --ssl-mode=TRUSTED_CLIENT_CERTIFICATE_REQUIRED
```
| `--ssl-mode` | Effect |
|---|---|
| `ALLOW_UNENCRYPTED_AND_ENCRYPTED` | default; allows non-TLS; avoid |
| `ENCRYPTED_ONLY` | TLS required, client cert not verified |
| `TRUSTED_CLIENT_CERTIFICATE_REQUIRED` | TLS + valid client cert |
The **Cloud SQL Auth Proxy** obtains an ephemeral SSL certificate (expires in about an hour, refreshed by the proxy) and the docs name the proxy or connectors as the way to enforce client identity for IAM database authentication under `TRUSTED_CLIENT_CERTIFICATE_REQUIRED`.

## 2. Server CA
```bash
gcloud sql instances describe db1    # look for serverCaMode
gcloud sql ssl server-ca-certs list --instance=db1
gcloud sql instances describe db1 --format='value(serverCaCert.cert)' > server-ca.pem
psql "host=<IP> dbname=app user=app sslmode=verify-ca sslrootcert=server-ca.pem"
```
CA modes (`--server-ca-mode`): per-instance CA (the default; Cloud SQL creates a server CA per instance), `GOOGLE_MANAGED_CAS_CA` (shared CA) or `CUSTOMER_MANAGED_CAS_CA` (needs a valid CA pool and CA). Shared CA needs Auth Proxy 2.13.0+ and customer-managed CA needs 2.14.3+. For hostname checks, use a DNS name from the instance's `dnsNames` as host with `sslmode=verify-full`.
**Rotation** (per-instance CA only): add the upcoming CA, distribute the bundle to clients, then rotate:
```bash
gcloud sql ssl server-ca-certs create --instance=db1
gcloud sql ssl server-ca-certs list --instance=db1 --format='value(cert)' > ca-bundle.pem   # deploy to clients
gcloud sql ssl server-ca-certs rotate --instance=db1
```

## 3. Client certificates
```bash
gcloud sql ssl client-certs create app-client client-key.pem --instance=db1
gcloud sql ssl client-certs describe app-client --instance=db1 --format='value(cert)' > client-cert.pem
psql "host=<IP> sslmode=verify-ca sslrootcert=server-ca.pem sslcert=client-cert.pem sslkey=client-key.pem dbname=app user=app"
```
You cannot retrieve the private key later; if lost, create a new certificate. Track expiry and delete unused ones (`client-certs delete`).

## Gotchas
- Use `sslmode=verify-ca` or `verify-full` so the client verifies the server.
- Rotating the server CA without distributing the new one first breaks every direct client at once.
- Private IP doesn't mean encrypted; enforce SSL mode anyway.

## Checked
2026-10-31. Confirmed against the Cloud SQL configure-ssl-instance, manage-ssl-instance and sql-proxy pages: `--ssl-mode` values and the default, per-instance CA as default CA mode, `GOOGLE_MANAGED_CAS_CA` and `CUSTOMER_MANAGED_CAS_CA`, proxy minimum versions, ephemeral cert lifetime, private key not retrievable, `dnsNames` with `sslmode=verify-full`, rotate and rollback. gcloud commands checked against the reference. Removed: certificate lifetime in years, claim that only the two newer CA modes allow verify-full, `serverCaMode` format path.
Method: documentation only; no commands were run.

## Verify
- [ ] A non-TLS connection attempt is rejected.
- [ ] `gcloud sql ssl server-ca-certs list` shows expiry dates tracked in your cert inventory.
