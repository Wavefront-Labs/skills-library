---
id: computing-software.cloud-infrastructure-engineering.netdata.disable-plugins-and-collectors
name: disable-plugins-and-collectors
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, go-d-conf, plugins-section, disable-collector]
level: intro
status: docs-checked
description: "Turn off a whole Netdata plugin in netdata.conf or a single go.d collector in go.d.conf, and know which file each belongs in."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/collectors/REFERENCE.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Disable a plugin: `sudo ./edit-config netdata.conf`, then in `[plugins]` uncomment the line and set it to `no`:

```
[plugins]
    proc = yes
    python.d = no
```

Disable one collector: open the plugin config and uncomment the collector line set to `no`:

```
sudo ./edit-config go.d.conf
```

```
modules:
    xyz_collector: no
```

Restart the Agent after either change.

Gotchas:
- Plugins are disabled in `netdata.conf`; Go collectors are disabled in `go.d.conf`.
- Go collectors can also be enabled and configured in the UI through the Dynamic Configuration Manager.

Find collectors in the Collecting Metrics guide or the Integrations page.

## Checked

2026-11-04: the `[plugins]` and `go.d.conf` examples, edit-config usage, restart step, Dynamic Configuration note and the pointers to the Collecting Metrics guide and Integrations page confirmed against the Netdata collector configuration reference. Removed a resource-cost claim and an unsourced verify line.

Method: documentation only; no commands were run.
