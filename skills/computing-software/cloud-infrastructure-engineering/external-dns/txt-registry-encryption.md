---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-registry-encryption
name: txt-registry-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, txt-encrypt-enabled, txt-encrypt-aes-key, aes-gcm, label-filter, sensitive-metadata]
level: advanced
status: docs-checked
description: "Encrypt ExternalDNS registry TXT records with AES-256-GCM: key generation, best-effort caveat, scoping with label filters and a recovery plan."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypting TXT registry records

Registry TXT values can reveal internal ingress names and namespaces. Enable encryption with `--txt-encrypt-enabled` and a 32-byte AES-256-GCM key via `--txt-encrypt-aes-key=<key>`, as URL-safe base64 (recommended) or plain text.

Generate a key:

```sh
openssl rand -base64 32
```

**Caveats**
- Encryption is best-effort: the stored bytes (AES-GCM over a gzip payload) are not guaranteed stable across Go or dependency upgrades. Updating or deleting existing encrypted records could break on providers that match by value; decrypting written records is not expected to break.
- It adds CPU per reconcile.
- Encrypted TXT records always use the new record-type format.

**Recommended practice**
- Do not encrypt by default. Run two instances: one plain, one with encryption scoped by `--label-filter` (for example `--label-filter=external-dns/txt-encrypt=true`).
- Give the plain instance the inverse selector, such as `--label-filter='external-dns/txt-encrypt notin (true)'`, so both do not claim a resource.
- Keep the label convention stable: moving a resource between filters forces an ownership handoff and a TXT rewrite.
- Back up zone contents including TXT records and document a recovery procedure. Lost or corrupted TXT records can orphan or recreate records.

**Manual edit:** the docs show Go code using `endpoint.EncryptText` and `endpoint.DecryptText` from `sigs.k8s.io/external-dns/endpoint` for editing a registry value by hand.

For changing the key, see the key rotation skill.

## Checked

2026-11-04. Read the TXT registry page (Encryption, Recommended Practices, key generation). Confirmed the flags, the 32-byte AES-256-GCM key, the best-effort note, the two-instance advice, the label-filter examples and the EncryptText/DecryptText example. Removed nothing.

Method: documentation only; no commands were run.
