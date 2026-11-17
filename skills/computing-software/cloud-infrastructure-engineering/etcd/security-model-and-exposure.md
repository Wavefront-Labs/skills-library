---
id: computing-software.cloud-infrastructure-engineering.etcd.security-model-and-exposure
name: security-model-and-exposure
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [security, exposure, metrics-endpoint, health-endpoint, access-control, network, secrets, trust]
level: advanced
status: docs-checked
description: "Security model of etcd: insecure defaults, TLS and client or peer certificate auth, endpoints outside RBAC and unencrypted disk data."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/security/"
  - "https://etcd.io/docs/v3.5/op-guide/authentication/rbac/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults: etcd does not enable RBAC or transport-layer authentication by default, to reduce friction (changing that would be a breaking change). A cluster that does not enable security features can expose its data to any clients.

Transport security:

- TLS and client certificate authentication are supported for both client-to-server and peer (server-to-server) traffic. Client flags: `--cert-file`, `--key-file` (unencrypted), `--client-cert-auth`, `--trusted-ca-file`, `--auto-tls`. Peer equivalents have the `--peer-` prefix. A key must be set whenever a certificate is supplied.
- Create and sign a new key pair for every member.
- With `--client-cert-auth` and authentication enabled, the certificate Common Name gives the user name.
- `--auto-tls` and `--peer-auto-tls` give encryption without authentication: self-signed certificates do not authenticate identity. Their validity is one year unless `--self-signed-cert-validity` sets years.
- `--peer-cert-allowed-cn` (v3.3.0 and later) restricts peers by exact Common Name match.
- Since v3.2.0, TLS certificates are reloaded on every client connection, so expiring certs can be replaced without stopping servers, and peer certs with a mismatched IP SAN are denied.
- `--cipher-suites`, `--tls-min-version` and `--tls-max-version` constrain TLS.

Gaps to cover yourself:

- Authentication protects the V3 gRPC API. `/metrics` and `/health` use a separate handler and are not protected by RBAC; secure them with mTLS (`--cert-file`, `--key-file`, `--client-cert-auth`), by binding metrics to a private interface with `--listen-metrics-urls`, or with network policy or firewall rules.
- etcd does not encrypt key/value data stored on disk. Options: encrypt and decrypt in client applications, or use storage-layer encryption such as dm-crypt.
- `--host-whitelist` (default empty, allowing all hostnames) protects insecure servers from DNS rebinding: if the connection is HTTPS any hostname is allowed; otherwise, with a non-empty whitelist, only listed Host values are accepted. Loopback addresses are not added automatically.
- When etcd creates directories it sets permission 700, and logs a warning if an existing directory has different permissions.

## Checked

2026-11-08. Read in full: etcd v3.5 Transport security model page and Role-based access control page. Confirmed every item above. Removed: port-role descriptions, the Kubernetes Secrets remark, prefix-scoped-role and private-interface advice for listen URLs, the snapshot-encryption and etcdutl access advice, the --enable-v2 default claim and the audit log claim (not on the pages read).
Method: documentation only; no commands were run.
