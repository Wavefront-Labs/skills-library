---
id: computing-software.cryptography-implementation.key-management.private-key-file-permissions
name: private-key-file-permissions
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-file-permissions, file-permissions, private-keys, chmod, icacls, systemd-credentials, key-storage, linux, windows]
level: practitioner
status: docs-checked
description: "Set and verify filesystem ownership and permissions for private keys used by PostgreSQL and systemd services on Linux, and deliver keys through systemd credentials."
sources: ["https://www.postgresql.org/docs/current/ssl-tcp.html", "https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#Credentials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private key file permissions

## Linux baselines
```
install -d -m 0700 -o root -g root /etc/pki/app
install -m 0600 -o root -g root server.key /etc/pki/app/server.key
stat -c '%a %U:%G %n' /etc/pki/app/*
```
| Consumer | Requirement |
|---|---|
| PostgreSQL `server.key` | Must disallow all group and world access (`chmod 0600`); or owned by root with group read (0640), with the postgres user in that group |
| Other services: no root-owned master process | Give the service account only the access it needs (for example 0640 root:svcgroup), or deliver via systemd credentials |

## systemd credentials (avoid long-lived key files readable by the service user)
```ini
[Service]
LoadCredential=tls.key:/etc/pki/app/server.key
# or an encrypted credential: LoadCredentialEncrypted=tls.key:/etc/credstore.encrypted/tls.key
ExecStart=/usr/bin/app --key ${CREDENTIALS_DIRECTORY}/tls.key
```
The service reads the key from `$CREDENTIALS_DIRECTORY`. A failed decryption of a `LoadCredentialEncrypted=`
credential fails the service.

## Gotchas
- Config management that templates keys can reset permissions to 0644 on each run; set mode explicitly.
- Backups and container volume mounts often lose permissions; check after restore.

## Checked

2026-11-01. Confirmed against the PostgreSQL SSL/TCP page (server.key must disallow group and world access; 0600, or
root-owned 0640 with group membership) and the systemd.exec credentials section (`LoadCredential=`,
`LoadCredentialEncrypted=`, `$CREDENTIALS_DIRECTORY`, failed decryption fails the service). Removed: OpenSSH,
sshd, nginx and Apache rows, the Windows icacls section, the TPM-bound encryption command and the SELinux
restorecon line, none of which the cited pages confirm.

Method: documentation only; no commands were run.

## Verify
- [ ] `find / -name "*.key" -perm /044 2>/dev/null` returns nothing unexpected.
- [ ] Services start with keys at 0600/0640 and fail closed if permissions are looser where enforced.
