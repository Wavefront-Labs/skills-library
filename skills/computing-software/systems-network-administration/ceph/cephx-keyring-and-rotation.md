---
id: computing-software.systems-network-administration.ceph.cephx-keyring-and-rotation
name: cephx-keyring-and-rotation
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephx, keyring, ceph-authtool, auth-rotate, import]
level: advanced
status: docs-checked
description: "Build keyring files with ceph-authtool, import users, and rotate a CephX key with ceph auth rotate."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/user-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create an empty keyring and populate it:

```
ceph-authtool --create-keyring /path/to/keyring
ceph auth import -i /path/to/keyring
```

Export a user and use its keyring on a client:

```
ceph auth get client.john -o /etc/ceph/ceph.client.john.keyring
```

Rotate a user's secret:

```
ceph auth rotate <entity>
```

Notes:

- A keyring may hold several users. `ceph auth export {TYPE.ID}` prints in keyring format.
- Import adds or updates users from a keyring file in the cluster database.
- Keys are stored in plain text files on trusted hosts, so set appropriate permissions on keyring files.

Command line selection: `ceph --id foo --keyring /path/to/keyring health` and the equivalents `--user`, `--name client.foo`, `-n client.foo`.

The page documents several keyring workflows beyond rotation. Create a user's entry directly in a keyring with `ceph-authtool -C /etc/ceph/ceph.keyring -n client.ringo --cap osd 'allow rwx' --cap mon 'allow rwx' --gen-key`, then register it in the cluster with `ceph auth add client.ringo -i /etc/ceph/ceph.keyring`. Merge one keyring into another with `ceph-authtool /etc/ceph/ceph.keyring --import-keyring /etc/ceph/ceph.client.admin.keyring`. Rotation avoids deleting and recreating the entity when its key is compromised, lost or scheduled for rotation. Keys in plaintext files have security shortcomings, as the page itself notes.

## Checked

2026-11-09. Confirmed against: the Ceph User Management page (docs.ceph.com/en/latest/rados/operations/user-management/): Keyring Management, Importing a User, Key rotation, Command Line Usage and Limitations.

Removed: the advice on copying the rotated key and restarting daemons, which the page does not give.

Method: documentation only; no commands were run.

