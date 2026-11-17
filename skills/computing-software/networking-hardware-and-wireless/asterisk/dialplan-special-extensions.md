---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-special-extensions
name: dialplan-special-extensions
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, special-extensions, h-extension, i-extension, t-extension, s-extension, timeout]
level: practitioner
status: docs-checked
description: "Use Asterisk built-in special extensions: a, e, h, i, o, s, t and T, plus the fallback default context, for IVR errors, timeouts, voicemail escapes and hangup cleanup."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan special extensions
- `a` (assistant): reached when the caller presses `*` while recording a voicemail.
- `o` (operator): reached when the caller presses `0` during voicemail recording, if it exists.
- `e` (exception catchall): substitutes for `i`, `t` or `T` if they are missing. The `EXCEPTION` function reports the type.
- `h` (hangup): runs in the current context when the call is hung up; used for cleanup.
- `i` (invalid): used when digits from `Background()` or `WaitExten()` match no extension in the context.
- `t` (response timeout): used when the caller waits too long during `Background()` or `WaitExten()` and no priorities remain.
- `T` (absolute timeout): runs when the absolute timeout is reached; see `core show function TIMEOUT`.
- `s` (start): where analog calls and macros begin. It is not a catch-all.

A context named `default` is used if an extension context is deleted while in use, or when no starting extension handler is defined (unless the low-level channel interface overrides it).

## Checked
2026-11-04: read the cited Asterisk documentation pages (Special-Dialplan-Extensions) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
