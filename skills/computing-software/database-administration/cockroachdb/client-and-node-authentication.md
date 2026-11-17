---
id: computing-software.database-administration.cockroachdb.client-and-node-authentication
name: client-and-node-authentication
category: computing-software
field: database-administration
product: cockroachdb
tags: [authentication, node-authentication, client-authentication, custom-ca, accept-sql-without-tls]
level: practitioner
status: docs-checked
description: "How CockroachDB authenticates nodes and clients with certificates or passwords, custom or public CA layouts, and the accept-sql-without-tls option."
sources:
  - https://www.cockroachlabs.com/docs/stable/authentication
  - https://www.cockroachlabs.com/docs/stable/cockroach-start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and configure the authentication method for self-hosted clusters.

Model: nodes authenticate each other and clients using TLS certificates; clients can instead authenticate with a SQL password while still holding `ca.crt` to verify the node.

Certificate rules:
- Node certificate: `CN=node`, with all IPs and DNS names (from `--listen-addr`/`--advertise-addr` or hostnames, plus `localhost` for loopback connections) in the Subject Alternative Name.
- Client certificate: `client.<user>.crt` with `CN=<user>`, signed by the CA behind `ca.crt`.
- Client connects with a cert: `cockroach sql --certs-dir=certs --user=<user>`.

Custom or public CA: the node needs `ca.crt`, `node.crt`/`node.key` (used when it acts as a server) and `client.node.crt`/`client.node.key` (used when it acts as a client of another node; `CN=node`, signed by the same CA). The default `node.crt` is multi-functional only when it carries `CN=node` and the SANs. A public CA certificate for the DB Console goes in as `ui.crt` and `ui.key` in `--certs-dir`.

SQL without TLS: the preview flag `--accept-sql-without-tls` on `cockroach start` lets SQL clients open a session without a TLS handshake. They still must present valid credentials such as a password, and other authentication schemes can apply. Connect with `cockroach sql --user=<user> --insecure`. The page intends it for deployments where transport security is already handled by the infrastructure (its example is IPSec with a DMZ).

Insecure mode (`--insecure`) skips both TLS and authentication and is for non-production testing only.

Verify: connect as a named user with `cockroach sql --certs-dir=certs --user=<user>`; the client still needs `ca.crt` to validate the node certificate.

## Checked
2026-11-03. Confirmed on the authentication and cockroach start pages: node certificate rules (`CN=node`, SANs including `localhost` for loopback), `client.<user>.crt` with `CN=<user>`, `client.node.crt`/`client.node.key` for custom or public CA layouts, `ui.crt`/`ui.key`, password authentication without TLS via the preview `--accept-sql-without-tls` (credentials still required), and `--insecure` skipping TLS and authentication for non-production testing only. Removed: the invented `SHOW USERS`/`current_user` verify step.
Method: documentation only; no commands were run.
