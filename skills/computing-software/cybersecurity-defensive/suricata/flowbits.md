---
id: computing-software.cybersecurity-defensive.suricata.flowbits
name: flowbits
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [flowbits, flow-state, multi-packet-detection]
level: practitioner
status: docs-checked
description: "Link rules across packets with flowbits: set, isset, isnotset, unset, noalert, OR syntax with pipe, case-sensitive names."
sources: ["https://docs.suricata.io/en/latest/rules/flow-keywords.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# flowbits

State is kept in memory per flow, so an alert fires only when conditions across packets are met.

- `set,name`: set the bit.
- `isset,name`: match only if set.
- `isnotset,name`: match only if not set.
- `unset,name`: clear it.
- `noalert`: suppress this rule's alert; typical for state-only rules.

Names are case-sensitive. `|` ORs names: `flowbits:isset,user1|user2`. `noalert;` alone is equivalent to `flowbits:noalert;`.

Differences from Snort: Suricata supports setting and checking the same flowbit within one packet or stream, and checks `isset` after the fast pattern match but before other `content` matches, rather than in left-to-right rule order. Chains of dependent flowbits across rules can depend on rule order or `sid` order.

## Checked

2026-11-08. Read the flowbits section of the raw Suricata user guide source (doc/userguide/rules/flow-keywords.rst, lines 9-67) and the Flowbits and flowbits:noalert sections of differences-from-snort.rst. Removed the `detect.flowbits.max-per-signature` default, which neither page states. Partial read: the rest of both pages was not read.

Method: documentation only; no commands were run.
