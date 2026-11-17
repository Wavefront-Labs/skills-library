---
id: computing-software.networking-hardware-and-wireless.opnsense.normalization-scrub-rules
name: normalization-scrub-rules
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [normalization, scrub, mss, fragments]
level: practitioner
status: docs-checked
description: "Configure OPNsense traffic normalization rules: max MSS, TOS/DSCP, minimum TTL, do-not-fragment, random ID and default interface scrub."
sources: ["https://docs.opnsense.org/manual/firewall_scrub.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Traffic normalization

Normalization protects internal hosts from protocol inconsistencies. By default, unless Disable interface scrub is set, every interface is scrubbed for all traffic with fragment reassemble on, and max-mss applied when an MSS value is set on the interface. Custom normalization rules are available for finer needs and use the same matching as ordinary firewall rules.

Options a matching rule can set:

- Max mss: enforce a maximum MSS on TCP packets (can also be a general rule on the interface).
- TOS / DSCP: force a TOS or DSCP value on IP packets.
- Minimum TTL: enforce a minimum TTL.
- Do not fragment: clears the dont-fragment bit of a matching IP packet, which disables IP fragmentation when set.
- Random ID: replaces the IP identification field with random values to counter predictable generators; only applies to packets not fragmented after optional reassembly.

When rules overlap the first match wins, and per-interface options are sorted after user-configured rules, so a custom rule overrides an interface MSS setting. Some protocols such as NFS need particular fragment handling, which may require options like IP Do-Not-Fragment to be set.

## Checked

2026-11-03. Read the Normalization manual page (firewall_scrub.html) on docs.opnsense.org and confirmed the claims above against them. Removed: the menu path Firewall > Settings > Normalization (the page does not state it) and an unsupported explanation of the Do not fragment option.
Method: documentation only; no commands were run.
