---
id: computing-software.systems-network-administration.netbird.traffic-events-logging
name: traffic-events-logging
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, traffic-events, flow-logs, kernel-reporting, siem-correlation]
level: advanced
status: docs-checked
description: "Enable and read NetBird traffic events: requirements, group scoping, aggregation, retention, SIEM streaming, correlation and traffic that is not recorded."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/activity/traffic-events-logging.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Records who connected to what, when, from where, and whether a policy allowed it. Beta. Requires Cloud Business or licensed self-hosted Enterprise with traffic flow enabled, and client 0.39+.

Enable: Settings > Networks > Experimental > Enable Traffic Events (off by default). Userspace reporting is always on; Traffic Reporting (Kernel) adds packet sizes but can raise client CPU. Scope to selected groups (none selected means all peers). Changes apply without a restart and are audited.

Reporting: from v0.75 clients aggregate by source address, direction, protocol, destination and port (or ICMP type), with start/end/drop counts and byte/packet totals. P2P is logged on both peers; blocked on the refusing peer; routed on the initiating and routing peers.

Retention: seven days in experimental mode; API returns up to 50,000 flow records; events can take up to ten minutes to appear.

SIEM: streamed in real time; in rare cases (such as a server restart) an event can be streamed twice, so deduplicate on event ID; user name and email are omitted.

Correlate both sides with reporter, source, destination, direction, protocol and destination port. Blocked events and policy IDs are not reported when the destination or routing peer runs in kernel mode; on Linux force userspace with `NB_WG_KERNEL_DISABLED`, `NB_FORCE_USERSPACE_FIREWALL`, `NB_FORCE_USERSPACE_ROUTER`.

Not recorded: UDP DNS on ports 53, 5353, 22054 (including mDNS); exit-node `0.0.0.0/0` traffic; connections dropped by a failed posture check.

## Checked

2026-11-04. Confirmed against the NetBird traffic events logging page: availability and beta note, client 0.39, enable path, kernel reporting, group scope, v0.75 aggregation, retention and 50,000 limit, ten-minute delay, streaming fields, correlation, kernel-mode limitation and the three environment variables, unrecorded traffic. Reworded the streaming delivery line, because the page does not say at-least-once.
Method: documentation only; no commands were run.
