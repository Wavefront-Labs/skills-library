---
id: computing-software.database-administration.cockroachdb.cockroach-cert-certificates
name: cockroach-cert-certificates
category: computing-software
field: database-administration
product: cockroachdb
tags: [cockroach-cert, tls-certificates, certificate-authority, node-certificate, client-certificate]
level: practitioner
status: docs-checked
description: "Generate and lay out CockroachDB TLS certificates with cockroach cert: CA, node and client certs, required files, CN and SAN rules, lifetime and key permissions."
sources:
  - https://www.cockroachlabs.com/docs/stable/cockroach-cert
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a certificate set for a secure cluster.

Subcommands: `create-ca`, `create-node`, `create-client`, `list`.

Files in `--certs-dir`:
- Node: `ca.crt`, `node.crt` (signed by the CA, `CN=node`, every IP and DNS name in the Subject Alternative Name, wildcards in DNS names supported), `node.key`.
- Client: `ca.crt`, `client.<user>.crt` with `CN=<user>`, `client.<user>.key`.
- Optional `ui.crt` and `ui.key` for a public CA certificate on the DB Console.
`node.crt` is multi-functional: used both for incoming connections and for the node's outgoing connections to other nodes.

Typical flow:
```shell
cockroach cert create-ca --certs-dir=certs --ca-key=my-safe-directory/ca.key
cockroach cert create-node <node hostname> <other addresses> --certs-dir=certs --ca-key=my-safe-directory/ca.key
cockroach cert create-client root --certs-dir=certs --ca-key=my-safe-directory/ca.key
cockroach cert list --certs-dir=certs
```
Flags: `--certs-dir` (default under the user's `.cockroach-certs` directory), `--ca-key` (required for all `create-*`), `--allow-ca-key-reuse`, `--overwrite`, `--lifetime` (default `87840h0m0s`, about 10 years), `--key-size` (default 2048), and `--tenant-name-scope` for client certs.

Gotchas:
- The CA key is never loaded automatically by `cockroach` commands; keep it in a separate directory and pass `--ca-key`.
- Key files must have restricted permissions; the check can be disabled with environment variable `COCKROACH_SKIP_KEY_PERMISSION_CHECK=true` (not advised). On Kubernetes set `fsGroup`.

Verify: `cockroach cert list` shows the expected files and expiry for each.

## Checked
2026-11-03. Confirmed on the cockroach cert page: subcommands, node and client file names, `CN=node`, SAN with wildcard DNS names, optional `ui.crt`/`ui.key`, multi-functional `node.crt`, flags and defaults (`--certs-dir`, `--ca-key` required for create-*, `--allow-ca-key-reuse`, `--lifetime` 87840h0m0s, `--key-size` 2048, `--tenant-name-scope`), the CA key never loaded automatically, `COCKROACH_SKIP_KEY_PERMISSION_CHECK`, Kubernetes `fsGroup`. Removed: the uncited SAN failure-mode claim.
Method: documentation only; no commands were run.
