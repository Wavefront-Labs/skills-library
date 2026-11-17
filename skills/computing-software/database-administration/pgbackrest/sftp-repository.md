---
id: computing-software.database-administration.pgbackrest.sftp-repository
name: sftp-repository
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, sftp, repo-sftp, ssh-keys, known-hosts]
level: advanced
status: docs-checked
description: "Use an SFTP host as repository: key pair, host key checking, and why to raise process-max."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep the repository on a host reachable by SFTP.

SFTP transfer is relatively slow, so raise `process-max` to parallelise.

```
[global]
process-max=4
repo4-type=sftp
repo4-path=/demo-repo
repo4-bundle=y
repo4-sftp-host=sftp-server
repo4-sftp-host-user=pgbackrest
repo4-sftp-host-key-hash-type=sha1
repo4-sftp-private-key-file=/path/to/id_rsa_sftp
repo4-sftp-public-key-file=/path/to/id_rsa_sftp.pub
```

Setup in the guide: generate a key pair (PEM format RSA) for the PostgreSQL user, append the public key to the repository user's authorized_keys on the SFTP server, and add the server to known_hosts, because `repo-sftp-host-key-check-type` defaults to `strict`.

Check types: `strict` (never auto-adds host keys, refuses changed or unknown), `accept-new` (adds new, refuses changed), `fingerprint` (compare with `repo-sftp-host-fingerprint`, which must match the hash type) and `none`. Hash type is `md5`, `sha1` or `sha256` (sha256 needs a newer libssh2).

The public key file is optional if pgBackRest is compiled against OpenSSL, and required if compiled against a different library. `repo-sftp-private-key-passphrase` covers protected keys; `repo-sftp-known-host` overrides the searched known-hosts files; `repo-sftp-host-port` defaults to 22.

Without `repo4-retention-full` set, backup warns the repository may run out of space.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (SFTP Support). Removed: the libssh2/OpenSSH public key wording (the page says OpenSSL). 

Method: documentation only; no commands were run.
