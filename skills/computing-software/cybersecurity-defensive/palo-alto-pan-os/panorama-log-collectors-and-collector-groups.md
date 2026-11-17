---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.panorama-log-collectors-and-collector-groups
name: panorama-log-collectors-and-collector-groups
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [log-collector, panorama, dedicated-log-collector, collector-group, panorama-mode, logging-service, log-redundancy]
level: practitioner
status: draft
description: "Plan Panorama logging with local and dedicated log collectors, collector groups, redundancy and retention."
sources: ["https://docs.paloaltonetworks.com/panorama/11-1/panorama-admin/panorama-overview/plan-your-panorama-deployment"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: logs from many firewalls stored with enough capacity and redundancy, and still searchable.

Modes: Panorama mode (management and logging in one VM or appliance), Management Only mode, and Log Collector mode (dedicated M-series or virtual log collector). Managed collectors form Collector Groups; firewalls are assigned to a group and forward logs round-robin to its members.

Basic workflow
1. Deploy the log collector, set its mode, serial, IP, and add it as a managed collector in Panorama > Managed Collectors.
2. Create the Collector Group, add the collector(s), enable log redundancy if you need two copies, set the log storage quota/retention.
3. Assign firewalls to the group (Collector Group > Device Log Forwarding) and verify log forwarding profiles use "send to Panorama".

```
show log-collector all
show log-collector-group all
debug log-collector log-collection-stats show incoming-logs
```
(Confirm command names per release.)

Gotchas
- Log redundancy doubles storage use.
- Mixed-version collectors and Panorama can disconnect; keep versions aligned.
- Disk additions on M-series need collector group rebalancing; plan capacity before logs fill.
- Local firewall logs are not automatically migrated to the collector.

## Verify
```
show logging-status
```
On the firewall, forwarding to the collector shows connected; on Panorama, new logs appear and the collector group shows `In Sync` with healthy disk pairs.
