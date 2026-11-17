---
id: computing-software.cybersecurity-defensive.cosign.registry-auth-flags
name: registry-auth-flags
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, registry-auth, registry-mtls, registry-username, tls, private-registry]
level: practitioner
status: docs-checked
description: "Authenticate cosign to registries with basic or bearer credentials and mTLS flags, plus the insecure-registry options and why not to use them."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry authentication and TLS flags

By default cosign uses the default keychain. Explicit flags on sign, verify, attest, tree, clean, download, save and load:

- `--registry-username` / `--registry-password` basic auth
- `--registry-token` bearer token
- `--registry-cacert` CA certificate (PEM) for the registry connection
- `--registry-client-cert` and `--registry-client-key` client certificate pair for mTLS
- `--registry-server-name` SAN used as the TLS ServerName to verify the mTLS connection

The sign page lists no stdin option for the password. `cosign login` has `--password-stdin` (see registry-login).

Testing-only flags, flagged "Don't use this for anything but testing":
- `--allow-http-registry` allows plain HTTP.
- `--allow-insecure-registry` allows expired or self-signed TLS certificates.

Related: k8s-keychain for workload identity in clusters.

## Checked

2026-11-04. Confirmed on the cosign sign, verify, attest, tree, clean, download, save, load and login reference pages: the `--registry-*` flags with their descriptions, the two testing-only flags with the quoted warning, and `--password-stdin`. Removed: the claim that the default keychain reads credentials from a container login and the advice to prefer `--registry-cacert` (not on the pages).

Method: documentation only; no commands were run.
