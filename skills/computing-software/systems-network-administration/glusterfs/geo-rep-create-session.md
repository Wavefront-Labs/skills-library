---
id: computing-software.systems-network-administration.glusterfs.geo-rep-create-session
name: geo-rep-create-session
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, push-pem, no-verify, ssh-port]
level: advanced
status: docs-checked
description: "Create a GlusterFS geo-replication session with push-pem or no-verify, the force flag for a smaller Secondary, and using a custom SSH port."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a geo-replication session

```
gluster volume geo-replication <primary_volume> \
    <secondary_user>@<secondary_host>::<secondary_volume> \
    create [ssh-port <port>] push-pem|no-verify [force]
```

- `push-pem` distributes keys to the Secondary nodes automatically.
- `no-verify` skips key distribution and Secondary checks; you must make sure the SSH port is open, passwordless login works, the Secondary volume is empty and it has enough memory.
- `force` is needed when the Secondary has less total space than the Primary.

Custom SSH port:

```
gluster volume geo-replication gvol-primary \
    geoaccount@snode1.example.com::gvol-secondary config ssh_port 50022
gluster volume geo-replication gvol-primary \
    geoaccount@snode1.example.com::gvol-secondary create ssh-port 50022 push-pem
```

Prerequisites are in geo-rep-prerequisites and unprivileged-user setup in geo-rep-mountbroker-setup. After create, run `set_geo_rep_pem_keys.sh` as root on a Secondary node (see geo-rep-mountbroker-setup), then start the session (geo-rep-lifecycle-commands).

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: the create syntax, push-pem and no-verify behaviour and its four external checks, force for a smaller Secondary, the ssh_port config plus create ssh-port example, and the post-creation set_geo_rep_pem_keys.sh step. Nothing removed.

Method: documentation only; no commands were run.
