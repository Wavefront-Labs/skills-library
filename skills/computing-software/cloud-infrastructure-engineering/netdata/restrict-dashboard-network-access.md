---
id: computing-software.cloud-infrastructure-engineering.netdata.restrict-dashboard-network-access
name: restrict-dashboard-network-access
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, bind-to, allow-connections-from, access-lists]
level: practitioner
status: docs-checked
description: "Limit who can reach the Agent web server on port 19999 with bind to and per-feature allow ... from access lists in the web section of netdata.conf."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/securing-netdata-agents.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bind the Agent to a private interface (multiple IPs and ports supported):

```
[web]
    bind to = 10.1.1.1:19999 localhost:19999
```

Access lists in `[web]` (default is `localhost *`, so external connections are allowed):

```
[web]
    allow connections from = localhost
    allow connections from = 10.*
    allow connections from = example*
```

Feature-specific lists (values are shown in the docs as examples):

```
[web]
    allow connections from = localhost *
    allow dashboard from = localhost *
    allow mcp from = localhost *
    allow badges from = *
    allow streaming from = *
    allow management from = localhost
```

There is also `allow netdata.conf from`, defaulting in the example to localhost and private ranges.

Steps: `sudo ./edit-config netdata.conf` in the config directory, edit `[web]`, restart the Agent.

Gotchas:
- Cloud connections are always TLS-encrypted; enable SSL separately to encrypt local dashboard traffic.
- Outbound access is still needed for ACLK, telemetry and updates.

## Checked

2026-11-04. Confirmed against the Netdata docs page netdata-agent/securing-netdata-agents: bind to with multiple addresses, allow connections from examples, the localhost * default, the feature-specific allow lists (dashboard, mcp, badges, streaming, netdata.conf, management), Cloud connections always TLS-encrypted, SSL needed separately for local traffic, and outbound access for ACLK, telemetry and updates. Removed the appended Verify line, which the page does not contain.
Method: documentation only; no commands were run.
