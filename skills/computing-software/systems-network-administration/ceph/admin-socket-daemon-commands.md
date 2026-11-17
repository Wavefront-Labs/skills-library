---
id: computing-software.systems-network-administration.ceph.admin-socket-daemon-commands
name: admin-socket-daemon-commands
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, admin-socket, daemon, cephadm, asok, debug]
level: practitioner
status: docs-checked
description: "Query a running Ceph daemon through its admin socket with ceph daemon, including entering the container on cephadm hosts."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The admin socket gives direct access to one daemon on its own host.

```
ceph daemon {daemon-name} {command}
ceph daemon {path-to-socket-file} {command}
ceph daemon osd.0 version
```

On cephadm deployments the daemon runs in a container, so enter it first:

```
cephadm enter --name {daemon-name}
```

Then run `ceph daemon ...` inside.

Typical uses:

- `ceph daemon {daemon-name} help` lists the commands a daemon supports.
- `ceph daemon /var/run/ceph/ceph-mgr.x.asok dump_osd_network 0` to dump OSD network ping times from the manager.

Compared with `ceph tell {daemon-type}.{id}`, `ceph daemon` bypasses the monitor and assumes a direct login to the daemon's host, while `ceph tell` sends the command over the network (the `ceph` tool needs the monitors to find the daemon) and needs no access to the host.

Use the socket when the daemon is the only thing you can reach. `ceph daemon osd.0 version` shows the daemon version, and `ceph daemon {path-to-socket-file} {command}` addresses a socket directly, for example one under `/var/run/ceph/`. Because cephadm runs daemons in containers, run `cephadm enter --name {daemon-name}` first. In packages installs the sockets are in `/var/run/ceph`; under cephadm they are in `/var/run/ceph/<fsid>` on the host and appear under `/var/run/ceph` inside the container.

## Checked

2026-11-09. Confirmed against: the Ceph Monitoring a Cluster page (docs.ceph.com/en/latest/rados/operations/monitoring/): Using the admin socket, dump_osd_network and the ceph daemon versus ceph tell comparison.

Removed: the config show/diff/get, connection scores and ceph config show examples (not on the page).

Method: documentation only; no commands were run.

