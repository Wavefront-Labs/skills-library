---
id: computing-software.systems-network-administration.keepalived.persistence-settings
name: persistence-settings
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, persistence, persistence-timeout, persistence-granularity, virtual-server]
level: practitioner
status: docs-checked
description: "persistence_timeout and persistence_granularity in virtual_server for sticky client connections, with case-study timeouts of 50 and 360 seconds."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistence

Two virtual_server keywords:
- `persistence_timeout`: timeout for persistent connections (numeric).
- `persistence_granularity`: granularity mask for persistent connections (an @IP).

Case-study values: HTTP 50, SSL 360, SMTP 50 seconds. SSL gets the longest value in the examples.

```
virtual_server 192.168.200.15 443 {
    persistence_timeout 360
    ...
}
```
The synopsis states no default for either keyword.

Verify: repeated requests from one client keep landing on the same real server within the timeout.

## Checked

2026-11-04. Confirmed both keywords on the configuration synopsis page, and the 50, 360 and 50 second values on the Healthcheck case study page. Replaced the unstated units caveat with seconds and removed the IPVS connection table reference, which the pages do not mention.

Method: documentation only; no commands were run.
