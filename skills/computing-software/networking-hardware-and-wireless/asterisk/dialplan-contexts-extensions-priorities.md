---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-contexts-extensions-priorities
name: dialplan-contexts-extensions-priorities
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, extensions-conf, contexts, priorities, labels, include, switch]
level: intro
status: docs-checked
description: "Structure extensions.conf: contexts, exten => number,priority,application, the n priority and same => prefix, labels, and the search order of extensions and includes."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Contexts-Extensions-and-Priorities/
  - https://docs.asterisk.org/Configuration/Dialplan/Include-Statements/Include-Statements-Basics/
  - https://docs.asterisk.org/Configuration/Dialplan/Include-Statements/Using-Include-Statements-to-Create-Classes-of-Service/
  - https://docs.asterisk.org/Configuration/Dialplan/Switch-Statements/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan contexts, extensions and priorities
Contexts are bracketed sections of `extensions.conf`. An extension line is `exten => number,priority,application(params)`, e.g. `exten => 6001,1,Dial(PJSIP/demo-alice,20)`.

- Priorities run in sequence from 1; a missing number ends the call. `n` means previous priority plus one, and `same =>` avoids repeating the extension.
- Labels: `n(repeat)` or `same => n(repeat),...` for jumping back later.
- Search order inside a context: explicit extensions, pattern extensions, includes, switches. Includes are processed depth-first.
- `include => features` pulls another context in. Avoid overlapping patterns or duplicate extensions across included contexts because processing does not stop at the first match.
- Classes of service: chain contexts (for example local, then longdistance including local, then international including longdistance) and point each phone at the context matching its privilege.
- `switch => IAX2/user:password@myserver/mycontext` shares a dialplan with another server. Reciprocal switches are not allowed and an offline switched server can delay dialing. `lswitch` skips load-time variable substitution; `eswitch` evaluates it at run time.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Contexts-Extensions-and-Priorities, Include-Statements-Basics, Using-Include-Statements-to-Create-Classes-of-Service, Switch-Statements) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
