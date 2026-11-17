---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.sftp-server-setup
name: sftp-server-setup
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [userstorefile, chroot, ssh-keys, sftp, ssh]
level: practitioner
status: docs-checked
description: "Serve the filer over SFTP with weed sftp or weed filer -sftp.port: users.json with HomeDir, auth methods, host keys and JWT integration."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/SFTP-Server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sftp server setup

Standalone or alongside the filer:
```bash
weed sftp -filer=localhost:8888 -port=2022 -userStoreFile=/path/to/users.json
weed filer -sftp.port=2022 -sftp.userStoreFile=/path/to/users.json
```
`users.json`:
```json
[{"Username":"alice","Password":"change-me","HomeDir":"/users/alice","Uid":0,"Gid":0}]
```
`HomeDir` is the user's root in the filer (chroot-like: they see it as `/`). `Uid` and `Gid` currently must be 0 for correct operation.

Flags: `-filer` (default localhost:8888), `-port` (2022), `-ip.bind` (0.0.0.0), `-userStoreFile` (required), `-sshPrivateKey` (host key), `-hostKeysFolder` (multiple algorithms), `-authMethods` (default `password,publickey`).

Supports password, SSH public key and CA-signed certificate authentication, uploads, downloads, rename, delete and directory management, and keep-alive for long connections. It uses JWT toward the filer when enabled.

Verify: `sftp -P 2022 alice@host` lists the home directory only.

## Checked
Checked 2026-11-09: both start commands, the users.json fields, the HomeDir and Uid/Gid notes, the flag defaults listed, the authentication methods and the automatic filer JWT handling match the SFTP-Server page. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page SFTP-Server, read in full from a local clone of the wiki.
