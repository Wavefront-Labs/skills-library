---
id: computing-software.systems-network-administration.ceph.auth-caps-modify
name: auth-caps-modify
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephx, caps, modify, namespace, pool]
level: practitioner
status: docs-checked
description: "Change existing CephX capabilities safely: ceph auth caps replaces the whole capability set for the user."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/user-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `ceph auth caps` to modify an existing user:

```
ceph auth caps USERTYPE.USERID {daemon} 'allow [r|w|x|*|...] [pool={pool-name}] [namespace={namespace-name}]' [{daemon} 'allow ...']
```

The new caps replace what the user had before, so show the old ones first and include everything you want to keep:

```
ceph auth get client.john
ceph auth caps client.john mon 'allow r' osd 'allow rw pool=liverpool'
ceph auth caps client.paul mon 'allow rw' osd 'allow rwx pool=liverpool'
ceph auth caps client.brian-manager mon 'allow *' osd 'allow *'
```

Capability letters: `r` read, `w` write, `x` call class methods (and auth operations on monitors), `*` all. Restrict by `pool=` and, within the pool, by `namespace=`.

To change caps by editing, export the entity (`ceph auth export {TYPE.ID}`), edit the caps and `ceph auth import -i /path/to/keyring`.

Two warnings from the user management page apply here. First, `ceph auth caps` overwrites every capability the user has, so always include the ones you keep. Second, running `ceph auth caps client.admin mgr 'allow*'` removes necessary capabilities from `client.admin`; the page gives a repair procedure that must be run from inside the `/var/lib/ceph/mon/<monitor_name>` directory, so never experiment on the admin user.

## Checked

2026-11-09. Confirmed against: the Ceph User Management page (docs.ceph.com/en/latest/rados/operations/user-management/): Modifying User Capabilities, capability letters and profiles, the client.admin warning and repair command, and the keyring export/import workflow.

Removed: the pool-rename advice (not on the page).

Method: documentation only; no commands were run.
 Capability profiles, for example `profile rbd` for Manager, Monitor and OSD, are shorthand for the minimal privileges an application needs, and `profile crash` gives read-only monitor access for the crash module.
