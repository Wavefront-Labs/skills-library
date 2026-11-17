---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-aes-key-rotation
name: txt-aes-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aes-key-rotation, txt-encrypt-aes-key, dry-run, stop-the-world, decryption-failure]
level: sme
status: docs-checked
description: "Rotate the ExternalDNS TXT encryption key safely: what happens if you just swap the flag, and the stop, re-encrypt, dry-run, restart procedure."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating the TXT AES key

Rotation is manual and stop-the-world. ExternalDNS holds one key and cannot decrypt old records while encrypting new ones.

**Why not just swap `--txt-encrypt-aes-key`:** AES-GCM authentication fails under the new key, so label parsing errors. ExternalDNS does not crash; it quietly treats the record as unowned. It then will not update or delete it, will not take ownership or re-create it, and the record drifts unmanaged. Records created afterwards encrypt fine under the new key.

**Procedure**
1. Stop ExternalDNS (scale to 0 or pause) so nothing else writes to the zone.
2. For each encrypted TXT record, using your provider's SDK (no ready-made tool exists):
   - decrypt with the old key: `endpoint.NewLabelsFromString(value, oldKey)`
   - delete the `txt-encryption-nonce` entry from the returned map so a fresh nonce is generated
   - re-encrypt: `labels.Serialize(true, true, newKey)` (`withQuotes=true`, `txtEncryptEnabled=true`)
   - write the new value back through the provider API.
3. Update `--txt-encrypt-aes-key` (or the backing secret) to the new key.
4. Run once with `--dry-run` and check the logs: no unexpected creates, updates or deletes, and no decryption errors.
5. Restart without `--dry-run`. The next reconcile decrypts every record under the new key.

**Verify:** after step 5 there are no decryption errors and no drift in the logs.

## Checked

2026-11-04. Read the TXT registry page (docs/registry/txt.md, AES Key Rotation section). Confirmed the stop-the-world rule, the unowned-record behaviour after a key change, the five-step procedure, NewLabelsFromString, Serialize(true, true, newKey) and the dry-run check. Removed nothing.

Method: documentation only; no commands were run.
