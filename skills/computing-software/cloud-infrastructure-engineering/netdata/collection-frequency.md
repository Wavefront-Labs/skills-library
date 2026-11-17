---
id: computing-software.cloud-infrastructure-engineering.netdata.collection-frequency
name: collection-frequency
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, update-every, sampling-interval, plugin-frequency]
level: intro
status: docs-checked
description: "Change how often Netdata collects: global update every in the db section, per-plugin overrides, and the clamp to 1 through 3600 seconds."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/collectors/REFERENCE.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/README.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/disk-requirements-and-retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global (default `1` second):

```
[db]
    update every = 2
```

Per plugin, in that plugin's section of `netdata.conf`:

```
[plugin:apps]
    update every = 5
```

Edit `netdata.conf` with `edit-config`, then restart the Agent.

Per collector: each collector has its own format; check that collector's documentation.

Gotchas:
- Valid range is 1 to 3600 seconds. Values outside are clamped to the nearest bound with a logged warning, not rejected.
- Lowering the frequency (for example 1 s to 2 s) can halve CPU usage, per the sizing docs.
- Changing `[db] update every` also shifts tier resolution, so the same tier size holds more time.

## Checked

2026-11-04. Confirmed against the Netdata Collector configuration page: the global [db] update every setting and 1 second default, the 1-3600 clamp with a logged warning, the [plugin:apps] example, edit-config plus restart, and per-collector docs. The CPU-halving figure is from the Resource utilization page and the tier-shift note from the Disk Requirements page (both added to sources). Removed the curl verification command, which no page states.

Method: documentation only; no commands were run.
