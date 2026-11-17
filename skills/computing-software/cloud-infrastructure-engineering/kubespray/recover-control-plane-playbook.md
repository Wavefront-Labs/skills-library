---
id: computing-software.cloud-infrastructure-engineering.kubespray.recover-control-plane-playbook
name: recover-control-plane-playbook
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [recovery, control-plane, etcd, quorum, recover-control-plane, snapshot]
level: advanced
status: docs-checked
description: "Recover a broken Kubespray control plane with recover-control-plane.yml: broken_etcd and broken_kube_control_plane groups, group order, etcd_retries and snapshot restore."
sources:
  - https://kubespray.io/docs/operations/recover-control-plane.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use the `recover-control-plane.yml` playbook when control plane nodes are lost (hardware failure, failed patching or upgrade, etcd corruption). At least one functional node must remain.

Runbook:
1. Back up what you can.
2. Provision new nodes to replace broken ones.
3. Copy broken etcd nodes into the `broken_etcd` group and make sure `etcd_member_name` is set.
4. Copy broken control plane nodes into `broken_kube_control_plane`.
5. Place the surviving nodes first in the `etcd` and `kube_control_plane` groups.
6. Add the new nodes below the survivors in those groups.

Then run the playbook with `--limit etcd,kube_control_plane` and raise the etcd retries with `-e etcd_retries=10` or higher; the needed number is hard to predict.

If quorum is lost, the playbook detects it, takes a snapshot from the first node in the `etcd` group and restores from it. To restore from another snapshot, pass its path:

```
-e etcd_snapshot=/tmp/etcd_snapshot
```

Caveats stated on the page: it has only been tested with fairly small etcd databases, disruptions are possible and there are no guarantees. Reproduce the same failure on a test cluster and rehearse the recovery before touching the real one.

## Checked

2026-11-04. The runbook order, variables and caveats were confirmed on the Recovering the control plane page.

Method: documentation only; no commands were run.
