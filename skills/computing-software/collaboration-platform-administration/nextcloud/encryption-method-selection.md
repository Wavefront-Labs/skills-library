---
id: computing-software.collaboration-platform-administration.nextcloud.encryption-method-selection
name: encryption-method-selection
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [encryption, sse, e2ee, luks, threat-model]
level: advanced
status: draft
description: "Choose between Nextcloud server-side encryption, end-to-end encryption and disk encryption by who can decrypt and which threat each one actually covers."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: match the encryption method to the threat before enabling anything.

Definitions from the docs:
- Server-Side Encryption (SSE): done by the server, protects files at rest on local and external storage, keys stay on the server.
- End-to-End Encryption (E2EE): done by desktop or mobile clients before upload. Only the client can decrypt, so server admins and external storage providers cannot read data.
- Disk or block device encryption, for example LUKS: encrypts the whole device, readable only once unlocked.

Comparison, by who can decrypt and what it protects against:
- SSE master key: admins and users; protects against external storage providers.
- SSE user keys: users and malicious admins; same protection against storage providers.
- SSE user keys with recovery: users and admins holding the recovery key.
- E2EE: users only; protects against admins and external storage providers.
- Disk encryption: the OS admin; protects against physical tampering and theft.

Rules of thumb stated in the docs:
- The methods are not interchangeable.
- SSE is mainly for protecting files on external third-party storage.
- If administrators must not read data, use E2EE.
- For local storage, disk encryption such as LUKS addresses server theft, which SSE does not aim at.
- SSE does not protect data from a compromised Nextcloud server or a malicious admin.


Check: write the threat down first, then confirm the chosen method appears against it in the comparison above.
