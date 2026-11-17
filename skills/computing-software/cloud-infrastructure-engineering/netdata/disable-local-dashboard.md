---
id: computing-software.cloud-infrastructure-engineering.netdata.disable-local-dashboard
name: disable-local-dashboard
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, web-mode-none, disable-dashboard, healthcheck-target]
level: practitioner
status: docs-checked
description: "Turn off the Agent local web server with mode = none, and avoid the trap on Parent Agents where it also blocks inbound streaming from Children."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/securing-netdata-agents.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Disable the dashboard in the `[web]` section of `netdata.conf` (use `sudo ./edit-config netdata.conf`):

```
[web]
    mode = none
```

Restart the Agent. It then stops accepting inbound connections on the web server; access goes through Netdata Cloud.

Gotchas:
- This also blocks inbound streams from Child Agents. Do not use it on Parent Agents.
- Docker: set the environment variable `NETDATA_HEALTHCHECK_TARGET=cli` so the container healthcheck does not depend on the web port.

Alternatives when you only need to limit exposure: bearer token protection, `bind to`, `allow ... from` lists, or a reverse proxy.

## Checked

2026-11-04. Confirmed against the Netdata docs page netdata-agent/securing-netdata-agents: web mode = none, restart, inbound connections no longer accepted, the warning against using it on Parents (blocks Child streams), NETDATA_HEALTHCHECK_TARGET=cli for Docker, and the alternatives. Removed the appended Verify curl line, which the page does not contain.
Method: documentation only; no commands were run.
