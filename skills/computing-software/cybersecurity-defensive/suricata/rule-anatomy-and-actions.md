---
id: computing-software.cybersecurity-defensive.suricata.rule-anatomy-and-actions
name: rule-anatomy-and-actions
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-structure, rule-actions, alert, drop-reject]
level: intro
status: docs-checked
description: "Read a Suricata rule: action, header and options, plus what alert, pass, drop, reject, rejectsrc, rejectdst and rejectboth do."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rule anatomy and actions

A rule has an action, a header (protocol, addresses, ports, direction) and options in parentheses separated by semicolons.

`alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"..."; classtype:bad-unknown; sid:123; rev:1;)`

## Actions

- `alert`: generate an alert.
- `pass`: stop further inspection of the packet.
- `drop`: drop the packet and alert.
- `reject` / `rejectsrc`: send RST or ICMP unreachable to the sender of the matching packet.
- `rejectdst`: send it to the receiver.
- `rejectboth`: send it to both sides.

In IPS mode every reject action also drops.

Option order matters: changing it changes the rule's meaning.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/intro) read in full; the claims, names, values and examples left in this skill match the page text. Removed the pointer to action ordering, which was not read.

Method: documentation only; no commands were run.
