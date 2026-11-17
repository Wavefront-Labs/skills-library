---
id: computing-software.cloud-infrastructure-engineering.netdata.extreme-cardinality-protection
name: extreme-cardinality-protection
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, extreme-cardinality, ephemerality, meta-db]
level: advanced
status: docs-checked
description: "Tune Netdata extreme cardinality protection for churning instances: settings, cleanup rules, history-loss caveats, SQLite vacuum behaviour and log verification."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/extreme-cardinality-protection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Settings in `[db]` of `netdata.conf`:
- `extreme cardinality protection`: default `yes` for multi-tier `dbengine`, otherwise `no`.
- `extreme cardinality keep instances`: default 1000 (1 to 1000000); higher is less aggressive.
- `extreme cardinality min ephemerality`: default 50 percent (0 to 100); higher is less aggressive.

```
[db]
    extreme cardinality keep instances = 2000
    extreme cardinality min ephemerality = 75
```

Restart the Agent.

Rules:
- Ephemerality is the percentage of a context's retained instances with no tier-0 retention.
- Cleanup runs about two minutes after the first real rotation in any dbengine tier.
- Netdata keeps the larger of the keep-instances value or the ephemerality percentage of instances; only eligible ones above that are cleared. Example: 3,000 instances, 2,000 eligible (66%) keeps 1,500, clears up to 500.
- Instances currently collected are never selected.

Gotchas:
- Some long-term history becomes inaccessible immediately; review thresholds before lowering them.
- `netdata-meta.db` is not cleaned synchronously: first scan about 30 minutes after startup, dimensions rescanned weekly. With `[sqlite] auto vacuum = INCREMENTAL` (default) vacuum is requested only when free pages exceed 5%.

Verify:

```
sudo journalctl --namespace=netdata MESSAGE_ID=d1f59606dd4d41e3b217a0cfcae8e632
```

or filter the Logs tab on MESSAGE_ID "Netdata extreme cardinality".

## Checked

2026-11-04. Confirmed against the Netdata Extreme cardinality protection page: the three settings with defaults and ranges, the example, restart note, ephemerality definition, two-minute scan, keep rule and 3,000-instance example, collected-instance exclusion, the history-loss warning, the 30-minute and weekly metadata scans, the 5% auto vacuum rule, and the journalctl message ID. Nothing removed.

Method: documentation only; no commands were run.
