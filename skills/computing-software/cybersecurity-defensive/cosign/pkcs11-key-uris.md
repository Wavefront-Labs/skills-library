---
id: computing-software.cybersecurity-defensive.cosign.pkcs11-key-uris
name: pkcs11-key-uris
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, pkcs11, list-keys-uris, hsm, cosign-pkcs11-pin]
level: advanced
status: docs-checked
description: "Discover PKCS11 tokens and key URIs with cosign pkcs11-tool list-tokens and list-keys-uris."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_pkcs11-tool.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_pkcs11-tool_list-keys-uris.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pkcs11-tool

"Provides utilities for retrieving information from a PKCS11 token." Subcommands: `list-tokens` (list all PKCS11 tokens linked to a module) and `list-keys-uris` (list URIs of all keys in a PKCS11 token).

```
cosign pkcs11-tool list-keys-uris --module-path /usr/lib/libp11kit.so --slot-id 0
```

Flags for list-keys-uris:
- `--module-path`: absolute path to the PKCS11 module.
- `--slot-id`: id of the PKCS11 slot, uses 0 if empty.
- `--pin`: pin of the PKCS11 slot, uses environment variable `COSIGN_PKCS11_PIN` if empty.
- `-f, --no-input` (inherited from `pkcs11-tool`): skip warnings and confirmations.

The docs pages do not show the URI format; copy it from the tool output rather than composing it.

## Checked

2026-11-04. Confirmed against the cosign docs pages cosign_pkcs11-tool and cosign_pkcs11-tool_list-keys-uris: purpose, subcommand descriptions, example, flags and defaults, `COSIGN_PKCS11_PIN`. Removed: the workflow claim that the URI is passed to `--key` in `cosign sign` (the sign page documents key path, KMS URI or Kubernetes Secret and does not mention PKCS11), advice to prefer the environment variable over `--pin`, and a generic closing check line.
Method: documentation only; no commands were run.
