---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-directory-layout
name: swanctl-directory-layout
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl-dir, credentials, x509, private-keys, swanctl-dir-env]
level: intro
status: docs-checked
description: "The swanctl configuration directory layout for strongSwan: x509, x509ca, x509crl, rsa, ecdsa, pkcs8, pkcs12, private, pubkey and conf.d, plus relocating it with SWANCTL_DIR."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlDir.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl directory layout
The swanctl directory (usually `/etc/swanctl`) holds `swanctl.conf` and a fixed set of sub-directories read by `swanctl --load-creds`. All files may be DER or PEM encoded.

| Directory | Contents |
|---|---|
| `conf.d` | snippets included via `include conf.d/*.conf` in the default swanctl.conf |
| `x509` | trusted X.509 end entity certificates |
| `x509ca` | trusted CA certificates |
| `x509aa` | trusted Attribute Authority certificates |
| `x509ocsp` | trusted OCSP signer certificates |
| `x509crl` | certificate revocation lists |
| `x509ac` | attribute certificates |
| `rsa` | PKCS#1 RSA private keys |
| `ecdsa` | plain ECDSA private keys |
| `pkcs8` | PKCS#8 private keys of any type |
| `pkcs12` | PKCS#12 containers |
| `private` | private keys in any format |
| `pubkey` | raw public keys |

The directories are accessed relative to the loaded `swanctl.conf`, so loading it from a custom place with `--file` moves the whole tree (the page says since 5.7.2). The location can also be set at runtime with the `SWANCTL_DIR` environment variable.

Relative paths in `certs`, `cacerts` and `pubkeys` resolve against `x509`, `x509ca` and `pubkey` respectively.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl Directory page (directory table, DER or PEM, relative to loaded swanctl.conf since 5.7.2, SWANCTL_DIR, conf.d) and the swanctl.conf reference (relative path rules for certs, cacerts, pubkeys). Nothing removed.

Method: documentation only; no commands were run.
