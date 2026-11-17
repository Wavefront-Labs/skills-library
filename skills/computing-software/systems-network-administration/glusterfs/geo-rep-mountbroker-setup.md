---
id: computing-software.systems-network-administration.glusterfs.geo-rep-mountbroker-setup
name: geo-rep-mountbroker-setup
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, mountbroker, gluster-mountbroker, unprivileged]
level: advanced
status: docs-checked
description: "Set up an unprivileged geo-replication Secondary user with gluster-mountbroker, create the group and account, generate SSH keys with gluster-georep-sshkey, then restart glusterd."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-replication mountbroker setup

On all Secondary nodes create the group and user:

```
sudo groupadd geogroup
useradd -s /bin/bash -d /path/to/geoaccount/ -G geogroup geoaccount
```

On any one Secondary node:

```
gluster-mountbroker setup /var/mountbroker-root geogroup
gluster-mountbroker add gvol-secondary geoaccount
gluster-mountbroker status
```

`gluster-mountbroker remove` removes a user. Then restart `glusterd` on all Secondary nodes.

On the Primary host that will run `create`, set up passwordless SSH and keys:

```
ssh-keygen
ssh-copy-id geoaccount@snode1.example.com
gluster-georep-sshkey generate
```

By default each public key in `common_secret.pem.pub` gets a prefix that stops the key running extra commands; `gluster-georep-sshkey generate --no-prefix` disables the prefix.

After the session is created (see geo-rep-create-session), run as root on one Secondary node:

```
/usr/libexec/glusterfs/set_geo_rep_pem_keys.sh <secondary_user> <primary_volume> <secondary_volume>
```

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: group and user creation, gluster-mountbroker setup, add, status and remove, the glusterd restart, ssh-keygen and ssh-copy-id, gluster-georep-sshkey generate with and without --no-prefix, and set_geo_rep_pem_keys.sh. The home directory in the useradd example is a placeholder path. Nothing removed.

Method: documentation only; no commands were run.
