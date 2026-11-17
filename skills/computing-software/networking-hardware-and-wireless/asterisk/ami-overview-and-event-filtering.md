---
id: computing-software.networking-hardware-and-wireless.asterisk.ami-overview-and-event-filtering
name: ami-overview-and-event-filtering
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ami, manager-conf, event-filter, eventfilter, actions, events, class-authorizations]
level: practitioner
status: docs-checked
description: "Use AMI on TCP 5038 with manager.conf read and write classes, and trim event streams with advanced eventfilter(action,name,header,method) or the deprecated regex form."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/The-Asterisk-Manager-TCP-IP-API/
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/AMI-Event-Filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMI overview and event filtering
AMI is a client/server protocol over TCP, configured in `manager.conf`; when enabled it listens on port 5038. Clients send **actions**, get **responses**, and receive **events**. Some actions return an initial response followed by a list of events so large reports do not block the manager. Headers are local to each message; reuse existing header names where possible.

Users get `read` (which event classes they receive) and `write` (which action classes they may run). Classes can overlap: the `command` write permission lets a client run CLI commands that overlap other classes.

**Advanced filtering** (recommended), per user in `manager.conf`:
`eventfilter(<criteria>) = [<match_expression>]`
- `action(include|exclude)` (default include)
- `name(<event_name>)`, exact and case-sensitive (check with `manager show events`)
- `header(<header_name>)`, restricts matching to that header
- `method(regex|exact|starts_with|ends_with|contains|none)` (default none)

Order: no filters means all events; include only means any match is sent; exclude only means any match is blocked; both means includes first, then excludes. An empty right side is intentional for name-only filters.
```
eventfilter(action(exclude),header(Channel),method(starts_with)) = Local/
```
**Legacy** filters (`eventfilter=Event: Newchannel`, `!` prefix excludes) run a regex over the whole payload; they are deprecated for performance.

## Checked
2026-11-04: read the cited Asterisk documentation pages (The-Asterisk-Manager-TCP-IP-API, AMI-Event-Filtering) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
