---
id: computing-software.systems-network-administration.ceph.cephadm-upgrade
name: cephadm-upgrade
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, upgrade, orch-upgrade, image, noautoscale]
level: practitioner
status: docs-checked
description: "Run a cephadm upgrade with ceph orch upgrade start, monitor it, stop it, and handle the PG autoscaler during the upgrade."
sources:
  - https://docs.ceph.com/en/latest/cephadm/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start from a healthy cluster, then give a version or an image:

```
ceph orch upgrade start --ceph-version <version>
ceph orch upgrade start --image quay.io/ceph/ceph:v20.2.3
```

Monitor and cancel:

```
ceph orch upgrade status
ceph -W cephadm
ceph orch upgrade stop
```

Autoscaler: by default cephadm pauses and resumes PG autoscaling during an upgrade itself. To opt out and leave the autoscaler as it is, set:

```
ceph config set mgr mgr/cephadm/pg_autoscale_during_upgrade true
ceph config get mgr mgr/cephadm/pg_autoscale_during_upgrade
```

With that option true, autoscaling is not turned on if it was already off. You can also pause it yourself with `ceph osd pool set noautoscale` and release it with `ceph osd pool unset noautoscale`.

For CephFS, `ceph config set mgr mgr/orchestrator/fail_fs true` is documented as a setting before upgrading. Limit gateway upgrades per pass with `ceph config set mgr mgr/cephadm/max_gateway_upgrades_per_pass 8`.

If a host is offline, cephadm pauses the upgrade and raises `UPGRADE_OFFLINE_HOST`.

Upgrade refuses to start while any host is offline or in maintenance mode. If a host goes offline mid-upgrade, cephadm pauses and raises `UPGRADE_OFFLINE_HOST`; after fixing it, run `ceph orch upgrade resume`. Staggered upgrades limit scope: `ceph orch upgrade start --image <image-name> --daemon-types mgr,mon --hosts host1,host2` or `--services rgw.example1,rgw.example2 --limit 2`. Cephadm strictly enforces an upgrade order for daemons. If you opt out of autoscaler pausing, existing pool modes `off`, `on` or `warn` are expected to remain, and unsetting `noautoscale` after the upgrade may split or merge PGs if the target changed.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm Upgrade page (docs.ceph.com/en/latest/cephadm/upgrade/): upgrade start forms, offline-host behaviour, autoscaler pausing, fail_fs, max_gateway_upgrades_per_pass and staggered-upgrade options.

Removed: nothing; every command and option was found on the page.

Method: documentation only; no commands were run.

