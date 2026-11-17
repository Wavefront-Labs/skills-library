---
id: computing-software.systems-network-administration.glusterfs.geo-rep-prerequisites
name: geo-rep-prerequisites
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, prerequisites, meta-volume, ntp]
level: practitioner
status: docs-checked
description: "Checklist before creating a GlusterFS geo-replication session: matching versions, passwordless SSH, synchronised clocks, and the optional gluster_shared_storage meta volume."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-replication prerequisites

Geo-replication is asynchronous and periodic, unlike synchronous replicated volumes.

Requirements:

- Primary and Secondary must both be Gluster volumes.
- Both clusters run the same GlusterFS version.
- Passwordless SSH from the host that runs `create` to one Secondary node, for the unprivileged account.
- Clocks on Primary bricks are synchronised (NTP or similar); skew can cause changes to be missed.
- Optional meta volume: a shared replica 3 volume named `gluster_shared_storage`, mounted at `/var/run/gluster/shared_storage/`. Enable its use per session with `config use-meta-volume true`. Without it, the Active worker is chosen by `node-uuid`.

Related:

- For a non-root Secondary user, see geo-rep-mountbroker-setup.
- Session creation is in geo-rep-create-session.
- Logs: `/var/log/glusterfs/geo-replication` on Primary nodes and `/var/log/glusterfs/geo-replication-secondary` on Secondary nodes.
- A Secondary with less total space than the Primary needs `force` at create time.

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: Gluster volumes on both sides, same GlusterFS version, passwordless SSH requirement, NTP and clock skew, the gluster_shared_storage replica 3 meta volume and mount path, node-uuid default, log directories and force for a smaller Secondary. Nothing removed.

Method: documentation only; no commands were run.
