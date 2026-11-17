---
id: computing-software.cloud-infrastructure-engineering.netdata.debug-collector
name: debug-collector
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, plugins-d, go-d-plugin, collector-debug]
level: practitioner
status: docs-checked
description: "Debug a failing Netdata collector by running its plugin by hand as the netdata user in debug mode for go.d, python.d or charts.d collectors."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/collectors/REFERENCE.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Go to the plugins directory (if absent, check the `plugins directory` setting in `netdata.conf`):

```
cd /usr/libexec/netdata/plugins.d/
```

2. Become the netdata user:

```
sudo su -s /bin/bash netdata
```

3. Run debug for your collector type:

```
./go.d.plugin -d -m <MODULE_NAME>
./python.d.plugin <MODULE_NAME> debug trace
./charts.d.plugin debug 1 <MODULE_NAME>
```

4. Read the output for configuration issues, connection problems and permission errors.

For Dynamic Configuration jobs in a Failed state, use Restart to see the failure message.

## Checked

2026-11-04: the plugins directory, the switch to the netdata user, the three debug commands and the output categories confirmed against the Netdata collector configuration reference; the Restart behaviour confirmed against the Dynamic Configuration Manager page. Removed the root, restart-Agent and verify lines (not on the pages).

Method: documentation only; no commands were run.
