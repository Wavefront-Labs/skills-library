---
id: computing-software.systems-network-administration.ceph.auth-get-or-create-user
name: auth-get-or-create-user
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephx, auth, user, caps, keyring]
level: practitioner
status: docs-checked
description: "Create CephX users with ceph auth get-or-create and friends, scoping mon and osd capabilities to a pool."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/user-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CephX users are named `TYPE.ID`, such as `client.paul`. Capabilities per daemon type restrict what the user can do.

```
ceph auth get-or-create client.paul mon 'allow r' osd 'allow rw pool=liverpool'
ceph auth get-or-create client.george mon 'allow r' osd 'allow rw pool=liverpool' -o george.keyring
ceph auth get-or-create-key client.ringo mon 'allow r' osd 'allow rw pool=liverpool' -o ringo.key
```

Differences:

- `ceph auth add` is the canonical way to add a user: it creates the user, generates a key and adds any specified capabilities.
- `get-or-create` returns the keyring-format key, creating the user only if needed.
- `get-or-create-key` returns just the key.
- `-o file` saves the output.

Inspect and remove:

```
ceph auth ls
ceph auth get client.admin
ceph auth print-key client.paul
ceph auth del client.paul
```

Run a command as that user with `ceph --id foo --keyring /path/to/keyring health` (or `--user`, `--name client.foo`, `-n client.foo`). Prefer pool-scoped caps over `allow *`.

`ceph auth add` is described as the canonical way to add a user, and `get-or-create` as often the most convenient. The docs warn that any user with capabilities on OSDs can reach all pools in the cluster unless access is restricted to a proper subset, which is why the examples carry `pool=liverpool`. Use `ceph auth print-key client.paul` to feed a key to another tool, for example `mount -t ceph serverhost:/ mountpoint -o name=client.user,secret=`ceph auth print-key client.user``. Named profiles such as `profile rbd` and `profile bootstrap-osd` exist for common roles, so prefer them to hand-written capability strings where they fit.

## Checked

2026-11-09. Confirmed against: the Ceph User Management page (docs.ceph.com/en/latest/rados/operations/user-management/): Add a User, Deleting a User, Printing a User's Key, Command Line Usage, capability profiles, and the warning that OSD capabilities reach all pools unless restricted.

Removed: the claim that `ceph auth add` fails when the user exists (the page does not state it).

Method: documentation only; no commands were run.

