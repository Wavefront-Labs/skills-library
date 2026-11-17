---
id: computing-software.cybersecurity-defensive.suricata.tag-keyword
name: tag-keyword
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [tag, tagged-packets, conditional-pcap]
level: practitioner
status: docs-checked
description: "Tag packets after an alert with the tag keyword: scope, metric, defaults, and logging to eve or conditional pcap."
sources: ["https://docs.suricata.io/en/latest/rules/tag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tag

`tag:<scope>[,<count>,<metric>[,<direction>]];`

- Scope: `session` or `host`. Metric: `packets`, `bytes`, `seconds`. Direction (`src` or `dst`) only with host scope and an explicit count and metric.
- Defaults without a count: 256 packets for session, and 256 packets for the alert's destination IP for host.

Examples: `tag:session;`, `tag:host,100,packets,src;`, `tag:host,3600,seconds,dst;`. A rule may hold several tags.

Logging:
- eve-log: enable `tagged-packets` under the alert output; records have event_type `packet`.
- pcap-log: set `conditional` to `tag`.

Session tags live on the flow; a packet with no flow is not tagged, silently. Host tags live in the host table, whose size may need tuning.

## Checked

2026-11-08. Read in full the raw Suricata user guide source behind the cited URL (doc/userguide/rules/tag.rst): syntax, scope, metric and direction values, the 256-packet defaults, examples, EVE tagged-packets and event_type packet, pcap-log conditional tag, and flow and host table notes. Nothing removed.

Method: documentation only; no commands were run.
