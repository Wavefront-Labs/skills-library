---
id: computing-software.networking-hardware-and-wireless.asterisk.auto-attendant-ivr-menus
name: auto-attendant-ivr-menus
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ivr, auto-attendant, background, waitexten, goto, record, directory, dialplan]
level: intro
status: docs-checked
description: "Build a dialplan auto-attendant: Background and WaitExten, Goto forms and labels, Record for custom prompts, and i and t extensions for invalid entries and timeouts."
sources:
  - https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Creating-a-Simple-IVR-Menu/
  - https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Background-and-WaitExten-Applications/
  - https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Goto-Application-and-Priority-Labels/
  - https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Record-Application/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# auto-attendant ivr menus
Put a menu in its own context. Pattern from the docs:
```
[demo-menu]
exten => s,1,Answer(500)
 same => n(loop),Background(press-1&or&press-2)
 same => n,WaitExten()
exten => 1,1,Playback(you-entered)
 same => n,Goto(s,loop)
```
- `Background(prompt1&prompt2)` plays prompts (no file extension, joined with `&`) while listening for DTMF and jumps to a matching extension in the current context.
- `WaitExten(N)` waits N seconds for an extension; with no argument it uses the built-in response timeout (changeable with `TIMEOUT()`). Use the `t` extension for timeouts and `i` for invalid entries.
- `Goto()` takes one parameter (priority or label in this extension), two (extension, priority or label) or three (context, extension, priority or label).
- `Record(en/custom-menu.gsm)` beeps and records until `#`; the extension must be a format shown by `core show file formats`. Play it back with `Playback(custom-menu)`.
- Menu options can send callers to extensions, `Directory(vm-demo,users,fe)`, or `VoiceMailMain(@vm-demo)`.

Some sample prompts come from the extra sounds packages.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Creating-a-Simple-IVR-Menu, Background-and-WaitExten-Applications, Goto-Application-and-Priority-Labels, Record-Application) and confirmed the commands, options, defaults and names stated above. Unconfirmed WaitExten timeout wording replaced with the documented behaviour.

Method: documentation only; no commands were run.
