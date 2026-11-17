---
id: computing-software.systems-network-administration.zfs.zfs-send-raw-encrypted
name: zfs-send-raw-encrypted
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, send, raw, encryption, replication, no-preserve-encryption]
level: advanced
status: docs-checked
description: "Replicate encrypted ZFS datasets without exposing keys using zfs send -w, avoid mixing raw and non-raw receives, and recover from IV set mismatches."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw sends of encrypted datasets

`zfs send -w` (`--raw`) sends encrypted data exactly as stored on disk. No keys are needed on the sender to send, and the receiver keeps the same encryption keys. `keylocation` defaults to `prompt` if unset. For an unencrypted dataset, `-w` is equivalent to `-Lec`.

```
zfs send -w tank/secure@a | ssh backup zfs receive pool/secure
zfs send -w -i @a tank/secure@b | ssh backup zfs receive pool/secure
```

## Why raw

Without `-w`, data is decrypted and may be re-encrypted on the receiver with a different key, which breaks raw incrementals to that system. A backup host receiving raw streams does not have the encryption keys, so it cannot read the data or alter it undetected.

## Rules on the receiving side

- Raw streams must be received as-is: no re-encryption, decryption or recompression, and encryption properties (except keylocation) cannot be overridden.
- Do not mix raw and non-raw receives into one dataset. A non-raw receive onto a raw-received dataset replaces the IV set, and later raw incrementals fail with "IV set guid mismatch".
- To resume after that, roll back to the last raw-received snapshot and send a raw incremental from it, or send a new full raw stream.

## Related flags

- `-R` with encrypted datasets requires `-w` or `-U`.
- `-U` sends an encrypted dataset as unencrypted data.
- `-p` also needs `-w` or `-U` for encrypted sends.

Raw and redacted sends cannot be combined.

## Checked

2026-11-03. Confirmed against zfs-send(8) (`-w`, `-U`, `-p`, `-R`, equivalence to `-Lec`, raw plus redacted) and zfs-receive(8) (raw streams received as-is, mixing raw and non-raw, IV set guid mismatch and recovery). Reworded the backup-host sentence to what the page states.
Method: documentation only; no commands were run.
