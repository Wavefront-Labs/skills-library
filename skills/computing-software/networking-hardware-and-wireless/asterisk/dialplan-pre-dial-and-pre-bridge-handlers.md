---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-pre-dial-and-pre-bridge-handlers
name: dialplan-pre-dial-and-pre-bridge-handlers
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, pre-dial, pre-bridge, gosub, dial-options, queue]
level: advanced
status: docs-checked
description: "Run subroutines around Dial: pre-dial b and B options, pre-bridge M (macro) and U (gosub) options after answer, plus the Queue macro and gosub arguments."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Subroutines/Pre-Dial-Handlers/
  - https://docs.asterisk.org/Configuration/Dialplan/Subroutines/Pre-Bridge-Handlers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan pre-dial and pre-bridge handlers
**Pre-dial** (Dial and FollowMe): runs after the channels exist but before the call is placed.
- `B([[context^]exten^]priority[(arg1[^...][^argN])])` runs on the caller channel before callee channels are created.
- `b(...)` runs on each callee channel after creation.
- Missing context or exten default to the caller channel's values. Handlers are Gosub subroutines, so end with `Return`. Keep them short; actions that move the channel into other applications give undefined behaviour.

**Pre-bridge**: runs after answer, before the parties are connected.
- Dial `M(macro[^arg[^...]])`: macro name without the `macro-` prefix; `MACRO_RESULT` can steer behaviour afterwards.
- Dial `U(x[^arg[^...]])`: a gosub (call `Return`); `GOSUB_RESULT` likewise.
- `Queue(queuename[,options[,URL[,announceoverride[,timeout[,AGI[,macro[,gosub[,rule[,position]]]]]]]]])`: `macro` and `gosub` run on the called party's channel.

Example: `Dial(PJSIP/ALICE,30,M(announcement))` runs `[macro-announcement]` on Alice's channel when she answers. Check `core show application Dial` for the full option semantics.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Pre-Dial-Handlers, Pre-Bridge-Handlers) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
