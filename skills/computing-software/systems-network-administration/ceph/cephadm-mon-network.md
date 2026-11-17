---
id: computing-software.systems-network-administration.ceph.cephadm-mon-network
name: cephadm-mon-network
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, monitor, public-network, orch-daemon-add, placement]
level: advanced
status: docs-checked
description: "Place cephadm monitors on a particular subnet and move them to a different network without losing quorum."
sources:
  - https://docs.ceph.com/en/latest/cephadm/services/mon/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tell cephadm which subnets monitors may use:

```
ceph config set mon public_network 10.1.2.0/24
ceph config set mon public_network 10.1.2.0/24,192.168.0.1/24
```

Deploy on specific hosts and networks. First stop the automatic placement:

```
ceph orch apply mon --unmanaged
ceph orch daemon add mon newhost1:10.1.2.123
ceph orch daemon add mon newhost2:10.1.2.0/24
```

Then re-enable a placement and preview it:

```
ceph orch apply mon --placement="newhost1,newhost2,newhost3" --dry-run
ceph orch apply mon --placement="newhost1,newhost2,newhost3"
```

Moving monitors to a new network:

```
ceph orch daemon add mon <newhost1:ip-or-network1>
ceph orch daemon rm *mon.<oldhost1>*
ceph orch apply mon --placement="newhost1,newhost2,newhost3"
```

Add the new monitors before removing the old ones so quorum is never lost. By default cephadm deploys up to five monitors.

Defaults: bootstrap assigns the first monitor to a subnet and designates it the cluster default, and new monitors go there unless told otherwise. If all monitors share a subnet no manual action is needed, and cephadm adds up to five automatically as hosts join. The default placement is five daemons on arbitrary hosts. A typical cluster runs three or five, and five is recommended when there are five or more nodes. Placement in a spec may use `count` or `count_per_host`, which are mutually exclusive, and `unmanaged: false` is the default. A spec can also target labelled hosts, for example `count: 5` under a `label` placement.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm Monitor Service page (docs.ceph.com/en/latest/cephadm/services/mon/): public_network, specific hosts and networks, moving monitors, default placement and spec keys.

Removed: nothing; every command and number was found on the page.

Method: documentation only; no commands were run.

