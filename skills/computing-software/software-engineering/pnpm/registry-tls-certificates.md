---
id: computing-software.software-engineering.pnpm.registry-tls-certificates
name: registry-tls-certificates
category: computing-software
field: software-engineering
product: pnpm
tags: [ca-certificate, cafile, client-certificate, node-extra-ca-certs, tls-registry, keyfile, certfile]
level: advanced
status: docs-checked
description: "Set pnpm TLS trust and client certificates: ca, cafile, per-registry ca/cert/key files, NODE_EXTRA_CA_CERTS and the system trust store fallback."
sources:
  - https://pnpm.io/npmrc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set in `.npmrc` or `auth.ini`.

```ini
ca="-----BEGIN CERTIFICATE-----\nXXXX\n-----END CERTIFICATE-----"
ca[]="..."
ca[]="..."
cafile=/path/to/ca.pem
//registry.npmjs.org/:cafile=ca-cert.pem
//registry.npmjs.org/:certfile=server-cert.pem
//registry.npmjs.org/:keyfile=server-key.pem
```

- `ca` (PEM text, array with `ca[]`) or `cafile` (path) replaces the default trusted CAs. When null, pnpm trusts the operating system store; if it cannot load that, it uses the Mozilla set built into pnpm.
- `NODE_EXTRA_CA_CERTS` (environment): PEM file of extra CAs added to the trusted set (system store, or `ca`/`cafile` when set). A missing or unreadable file is ignored.
- `cert` and `key`: client certificate and key as PEM values, not paths. `<URL>:cert`, `<URL>:key` per registry; file variants are `<URL>:certfile` and `<URL>:keyfile`; CA variants `<URL>:ca` and `<URL>:cafile`.
- See also `strictSsl` in network settings.

## Checked

2026-11-04. Confirmed ca, cafile, NODE_EXTRA_CA_CERTS, cert, key and the per-registry ca, cafile, cert, certfile, key and keyfile forms and the system-store fallback against pnpm.io/npmrc. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
