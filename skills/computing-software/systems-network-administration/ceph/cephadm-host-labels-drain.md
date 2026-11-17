---
id: computing-software.systems-network-administration.ceph.cephadm-host-labels-drain
name: cephadm-host-labels-drain
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, host, label, drain, maintenance]
level: practitioner
status: docs-checked
description: "Add, label, drain and remove hosts in a cephadm cluster."
sources:
  - https://docs.ceph.com/en/latest/cephadm/host-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List and add:

```
ceph orch host ls --detail
ceph orch host add <newhost> [<ip>] [--labels <label1>[,<label2>...]]
ceph orch host add host4 10.10.0.104 --labels _admin
```

Labels steer placement and the special `_admin` label makes cephadm keep `ceph.conf` and the admin keyring on the host:

```
ceph orch host label add host1 my_label
ceph orch host label rm host1 my_label
```

Remove a host by draining it first, which removes its daemons and moves OSDs off:

```
ceph orch host drain <host>
ceph orch host drain <host> --keep-conf-keyring
ceph orch host drain <host> --zap-osd-devices
ceph orch osd rm status
ceph orch ps <host>
ceph orch host rm <host>
```

Wait until `ceph orch ps <host>` shows no daemons. For a host that is gone:

```
ceph orch host rm <host> --offline --force
```

Special labels all start with an underscore. `_no_schedule` stops cephadm deploying daemons on a host and, if added to a host with daemons, moves them elsewhere except OSDs. `_no_conf_keyring` does the same for managed `ceph.conf` and keyrings, and `_no_autotune_memory` prevents memory autotuning. Drain applies `_no_schedule` and `_no_conf_keyring` and schedules all OSDs on the host for removal; `--zap-osd-devices` additionally erases their devices, which is destructive. Maintenance mode stops all Ceph daemons on a host: `ceph orch host maintenance enter <hostname>` and `exit <hostname>`. Forcing entry with `--force --yes-i-really-mean-it` can cause loss of data availability or break the monitor quorum, and the flag is rejected without `--force`.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm Host Management page (docs.ceph.com/en/latest/cephadm/host-management/): adding and listing hosts, labels and special labels, draining, removing offline hosts and maintenance mode.

Removed: nothing; one maintenance-mode warning was reworded to match the page.

Method: documentation only; no commands were run.

