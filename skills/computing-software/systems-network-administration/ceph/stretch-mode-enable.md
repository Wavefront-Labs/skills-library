---
id: computing-software.systems-network-administration.ceph.stretch-mode-enable
name: stretch-mode-enable
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, stretch-cluster, two-site, tiebreaker, monitor, crush]
level: sme
status: docs-checked
description: "Enable Ceph stretch mode for two data sites plus a tiebreaker monitor: set mon locations, add a CRUSH rule, then enable_stretch_mode."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/stretch-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stretch mode suits two data centres with a tiebreaker monitor in a third location. Set monitor locations:

```
ceph mon set_location a datacenter=zone1
ceph mon set_location e datacenter=zone3
```

Edit the CRUSH map to add a stretch rule:

```
ceph osd getcrushmap > crush.map.bin
crushtool -d crush.map.bin -o crush.map.txt
crushtool -c crush.map.txt -o crush2.map.bin
ceph osd setcrushmap -i crush2.map.bin
```

Enable stretch mode, naming the tiebreaker monitor, the rule and the failure domain; the cluster switches to the connectivity election strategy automatically if it is not already set:

```
ceph mon enable_stretch_mode e stretch_replicated_rule datacenter
```

Leave stretch mode with:

```
ceph mon disable_stretch_mode [{crush_rule}] --yes-i-really-mean-it
```

Replace a failed tiebreaker with `ceph mon set_new_tiebreaker mon.<new_mon_name>`. If you use `--set-crush-location` at monitor start rather than `set_location`, read the page section on that option.

Layout assumptions: two data zones plus a tiebreaker in a third location, whose monitor can be a VM. Give the tiebreaker a CRUSH `datacenter` that is neither `zone1` nor `zone2` and not predefined in your CRUSH map. An explicit tiebreaker is optional; without one, the cluster selects a monitor in a different `datacenter` from the data zones. The recommended rule uses `step choose firstn 0 type datacenter` then `step chooseleaf firstn 2 type host`, keeping two copies per datacenter, with `min_size` 2 in normal operation. New monitors cannot join without a CRUSH location. If you deploy monitors with your own tooling, use `ceph-mon --set-crush-location 'datacenter=a'` instead of `ceph mon set_location`.

## Checked

2026-11-03. Confirmed against: the Ceph Stretch Mode page (docs.ceph.com/en/latest/rados/operations/stretch-mode/): enabling, tiebreaker, CRUSH rule, disable_stretch_mode, set_new_tiebreaker, --set-crush-location.

Removed: nothing.

Method: documentation only; no commands were run.
