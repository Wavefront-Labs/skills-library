---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-subroutines-gosub-and-macro
name: dialplan-subroutines-gosub-and-macro
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, gosub, return, macro, subroutine, arg1, macro-exten]
level: practitioner
status: docs-checked
description: "Reuse dialplan code with Gosub and Return (arguments in ARG1..), and understand legacy Macro naming, s extension and MACRO_* variables; Gosub is the recommended replacement."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Subroutines/Gosub/
  - https://docs.asterisk.org/Configuration/Dialplan/Subroutines/Macros/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan subroutines: gosub and macro
`Gosub([[context,]exten,]priority[(arg1[,...][,argN])])` runs a block of dialplan. Gosub deprecates Macro and, unlike Macro, handles nesting.

- No special syntax is needed in the called code unless you want to come back, in which case end with `Return()`.
- Example: `Gosub(my-gosub,s,1(${EXTEN}))`; the subroutine reads the value as `ARG1`.
- Dial and Queue accept Gosub on the called party's channel (see the pre-dial and pre-bridge handler pages).

Macro (historical): the context must be named `macro-<name>` and use extension `s`. Call it with `Macro(name,[arg1],[argN])`. The caller's extension, context and priority are in `MACRO_EXTEN`, `MACRO_CONTEXT`, `MACRO_PRIORITY`; arguments are `ARG1`, `ARG2`, and so on. A Goto out of the macro context ends the macro.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Gosub, Macros) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
