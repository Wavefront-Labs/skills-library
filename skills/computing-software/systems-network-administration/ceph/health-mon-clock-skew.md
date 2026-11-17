---
id: computing-software.systems-network-administration.ceph.health-mon-clock-skew
name: health-mon-clock-skew
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, health, mon-clock-skew, chrony, ntp, mon-lease]
level: practitioner
status: docs-checked
description: "Fix MON_CLOCK_SKEW by synchronising monitor hosts with chrony or NTP rather than raising mon_clock_drift_allowed."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/health-checks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MON_CLOCK_SKEW` is raised when the clocks of monitor hosts differ by more than `mon_clock_drift_allowed`.

Preferred fix: synchronise the clocks with `chrony` or legacy `ntpd`.

- Configure the daemons to sync against several internal and external sources.
- Have the NTP daemons on the monitor hosts sync against each other too: monitors matter more being in agreement with each other than being correct to reference time.

Only if you really cannot keep clocks close, raise the threshold:

```
ceph config set mon mon_clock_drift_allowed <seconds>
```

The docs say this value must stay well below the `mon_lease` interval or the monitor cluster will not work properly, and that sub-millisecond sync is easy with decent NTP or PTP, so there are very few occasions to change it.

The raising condition is a skew greater than `mon_clock_drift_allowed`. For resilience, configure the NTP daemons to sync against multiple internal and external sources, because the protocol adaptively picks the best available one. The docs add that monitors being synchronised with each other matters more than being correct against reference time, so have the monitor hosts peer with each other. With quality NTP or PTP, sub-millisecond synchronisation is routine, which is why changing the threshold is rarely appropriate. If you must, keep `mon_clock_drift_allowed` significantly below `mon_lease` or the monitor cluster will not function properly.

## Checked

2026-11-03. Confirmed against: the Ceph Health checks page (docs.ceph.com/en/latest/rados/operations/health-checks/): MON_CLOCK_SKEW.

Removed: the diagnosis line naming ceph health detail and chronyc tracking (not on the page).

Method: documentation only; no commands were run.
