---
id: computing-software.collaboration-platform-administration.nextcloud.sse-limitations-and-key-loss-risks
name: sse-limitations-and-key-loss-risks
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [server-side-encryption, key-loss, filenames, quota, external-storage]
level: advanced
status: draft
description: "Know the Nextcloud server-side encryption limits before enabling it: filenames stay readable, no web UI undo, key loss means data loss, and sharing and quota effects."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: decide whether server-side encryption (SSE) is acceptable, before you turn it on.

Limitations the docs list:
- SSE encrypts file contents only. Filenames and folder structure are not encrypted. Do not confuse it with S3 SSE-C, which is also supported.
- It cannot be reversed through the Nextcloud web interface.
- Troubleshooting generally needs `occ` access, so make sure you have it first.
- Losing the encryption keys or the instance secret means permanent data loss.
- Quotas are based on unencrypted size. Encrypted files may be about 1% larger (it was 35% before Nextcloud 25).
- TLS terminates before SSE encrypts, so files can be exposed in memory between the two.
- Files on external storage encrypted with SSE cannot be shared from the storage provider, only through Nextcloud, because the key never leaves the server.

Before enabling:
1. Read the whole guide and understand the risks.
2. Back up the instance configuration and all keys somewhere safe.
3. Pick a key management mode (see sse-key-management-modes).

Hardening tip from the docs: configure external storage with "Check for changes: Never". Nextcloud then ignores files not added through it, which stops the storage admin adding files. Do not use this if the storage legitimately changes outside Nextcloud.

Check: a documented restore test exists, using the key backup, before any real data is encrypted.
