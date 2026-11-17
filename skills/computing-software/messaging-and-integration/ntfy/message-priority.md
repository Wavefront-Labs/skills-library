---
id: computing-software.messaging-and-integration.ntfy.message-priority
name: message-priority
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, priority, x-priority, urgent, headers]
level: intro
status: docs-checked
description: "Use the five ntfy priority levels via the X-Priority header and know how each behaves on the phone."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message priority

Header: `X-Priority` with aliases `Priority`, `prio`, `p`. Accepts the number or the name.

| ID | Name | Behaviour |
|---|---|---|
| 5 | `max` / `urgent` | Long vibration bursts, default sound, pop-over |
| 4 | `high` | Long vibration burst, default sound, pop-over |
| 3 | `default` | Short vibration and sound |
| 2 | `low` | No vibration or sound; shown only when the drawer is pulled down |
| 1 | `min` | No vibration or sound; under "Other notifications" |

```
curl -H "X-Priority: 5" -d "An urgent message" ntfy.sh/phil_alerts
curl -H "Priority: low" -d "Not important" ntfy.sh/phil_alerts
curl -H p:4 -d "High" ntfy.sh/phil_alerts
```

## Notes

- Supported on Android, Apple and Firefox.
- In the Android and iOS apps, priority 3 and above vibrates and makes a sound; 4 and above also pops over. Android creates a notification channel per priority (long-press the app, tap Notifications) where sound, Do Not Disturb override and pop-over can be set.
- In JSON publishing `priority` is an integer 1-5.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Message priority, JSON table) and phone page (priority behaviour, channels): table of ids, names and behaviour, header aliases, examples, platform marker, JSON integer 1-5. Removed: the Verify step.
Method: documentation only; no commands were run.
