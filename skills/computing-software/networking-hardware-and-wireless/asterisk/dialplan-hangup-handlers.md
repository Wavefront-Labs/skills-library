---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-hangup-handlers
name: dialplan-hangup-handlers
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, hangup-handler, hangup-handler-push, channel-function, cleanup]
level: advanced
status: docs-checked
description: "Attach cleanup subroutines to a channel with CHANNEL(hangup_handler_push/pop/wipe), their execution order, and warnings about Return, timing against the h extension and delays."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Subroutines/Hangup-Handlers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan hangup handlers
Hangup handlers are subroutines attached to a channel that run when it hangs up. Unlike the `h` extension they follow the channel. Several can be attached; the most recently added runs first. The page notes they were added in Asterisk 11.

Manage them with write-only `CHANNEL()` values:
- `Set(CHANNEL(hangup_handler_push)=[[context,]exten,]priority[(arg1[,...][,argN])])` pushes one.
- `Set(CHANNEL(hangup_handler_pop)=...)` pops one, optionally replacing it with a new handler.
- `Set(CHANNEL(hangup_handler_wipe)=...)` removes all, optionally pushing a new one.

Warnings:
- They are subroutines, so end with `Return`.
- Timing relative to the `h` extension is undefined; either can run first.
- Adding a handler inside the `h` extension or during a handler is undefined behaviour.
- They run in the hangup path, so keep them fast; protocols such as ISDN and SIP may not tolerate long delays.
- Transfers, pickup and parking can leave handlers on channels on both sides of a bridge.
- Attach them to other call legs with pre-dial handlers.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Hangup-Handlers) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
