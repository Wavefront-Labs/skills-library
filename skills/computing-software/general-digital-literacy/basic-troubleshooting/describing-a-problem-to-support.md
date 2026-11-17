---
id: computing-software.general-digital-literacy.basic-troubleshooting.describing-a-problem-to-support
name: describing-a-problem-to-support
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-method, support-ticket, bug-report, help-desk]
level: intro
status: draft
description: "Write a support request or help desk ticket that gets solved first time: what you expected, what happened, exact error text, steps, device details and screenshots."
sources:
  - https://support.microsoft.com/en-us/windows/get-help-in-windows-1aa10ac6-a1d5-8c11-c2b4-f4d3c8afe0de
  - https://getsupport.apple.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Describe a problem to support

Support spends most time asking for information you could have given. One complete message beats five replies.

## Template
```
Summary: Outlook on my laptop won't send email since this morning (receiving works).
Expected: Messages send from Outbox.
Actual: Stuck in Outbox; error "0x800CCC0F The connection to the server was interrupted".
Steps: Open Outlook > New email to anyone > Send > sits in Outbox. Same with attachments or not.
Since: Today 09:10, after Windows restarted for updates.
Scope: Only this laptop; phone sends fine. Colleague on same Wi-Fi is fine.
Tried: Restarted, removed and re-added the account, webmail sends OK.
Device: Dell Latitude 5440, Windows 11 24H2, Outlook classic (Microsoft 365, Version 2409).
Attached: screenshot of the error, time of last failure 10:42.
Impact: I can't send invoices; deadline 3pm.
```

## Collecting the details
- **Exact error text**: copy it (`Ctrl+C` works on many Windows dialogs) or screenshot (`Win+Shift+S`, Mac `Cmd+Shift+4`). Error codes matter more than descriptions.
- **Versions**: Windows `winver`; Mac Apple menu › About This Mac; app Help › About.
- **Serial number** for hardware: sticker, BIOS, or `wmic bios get serialnumber`; Mac About This Mac.
- Short **screen recording** for intermittent or multi-step problems (`Win+Alt+R` in Game Bar, Mac `Cmd+Shift+5`).

## Etiquette and safety
- One problem per ticket. Reply in the same thread.
- Never send passwords or full card numbers. Genuine support doesn't ask for them; remote-access sessions should be ones you started from the official site.

## Verify
- [ ] Someone who has never seen your computer could reproduce the problem from the message.
