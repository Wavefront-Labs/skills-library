---
id: computing-software.systems-network-administration.incus.trust-pki-ca-mode
name: trust-pki-ca-mode
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, authentication, pki, ca, client-ca, server-ca, crl, trust-ca-certificates]
level: advanced
status: docs-checked
description: "Run Incus in PKI mode: client.ca and server.ca placement, core.trust_ca_certificates, ca.crl revocation, and CA entries in the trust store."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKI mode

1. Put `client.ca` in `~/.config/incus` on clients and `server.ca` in `/var/lib/incus` on the server.
2. Replace the generated certificates with CA-issued ones and restart the server.

- CA-issued certificates are not trusted automatically; add them to the trust store, unless you set `core.trust_ca_certificates=true`, which grants full access to any valid CA-issued client certificate (unless added as restricted). Use a CA dedicated to Incus.
- Revocation: list certificates in `ca.crl` in the server configuration directory and they are rejected.
- Alternative: put a CA certificate in the trust store so any client certificate it issued authenticates. Intermediates must be presented; `clientAuth` extended key usage is required if specified; directly stored certificates take precedence. CRLs are not checked, so remove the CA entry to revoke all it issued.
- A changed server certificate makes clients refuse to connect; verify with the administrator first.

## Checked

2026-11-09. Confirmed against the Incus Remote API authentication page: client.ca and server.ca locations, restart, generated certificates not auto-trusted, core.trust_ca_certificates behaviour and caution, ca.crl, CA entries in the trust store (intermediates, clientAuth, precedence, no CRL check), changed server certificate failure. Nothing removed.
Method: documentation only; no commands were run.
