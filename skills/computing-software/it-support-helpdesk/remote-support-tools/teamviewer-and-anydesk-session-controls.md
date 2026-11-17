---
id: computing-software.it-support-helpdesk.remote-support-tools.teamviewer-and-anydesk-session-controls
name: teamviewer-and-anydesk-session-controls
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, teamviewer-session, teamviewer, anydesk, attended-access, unattended-access, black-screen, reboot-and-reconnect]
level: practitioner
status: draft
description: "Drive TeamViewer and AnyDesk sessions properly: QuickSupport vs full client, permission toggles, reboot-and-reconnect, black screen, unattended passwords and policies."
sources:
  - "https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-remote/"
  - "https://support.anydesk.com/docs/unattended-access"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# teamviewer-and-anydesk-session-controls

## Attended sessions
- **TeamViewer**: user runs QuickSupport (no install, no admin) and reads the ID and
  password. Prefer a custom QuickSupport module from the Management Console so the user
  sees your company name and the session is tied to your licence.
- **AnyDesk**: user reads the 9-digit address; an accept window appears with permission
  toggles. Ask the user to accept, then confirm in the toolbar which permissions you have.

## Controls you will use
| Need | TeamViewer | AnyDesk |
|---|---|---|
| Send Ctrl+Alt+Del | Actions > Ctrl+Alt+Del | Actions > Ctrl+Alt+Del |
| Reboot and come back | Actions > Restart > Restart (reconnect) or Restart in safe mode | Actions > Restart (needs the restart permission) |
| Hide screen from bystanders | Actions > Show black screen (installs a driver) | Privacy mode (permission toggle) |
| Block user input | Actions > Disable remote input | Block user input toggle |
| Files | File Transfer window or drag and drop | File manager / clipboard file transfer |
| Swap roles | Switch sides with partner | Switch sides |

## Unattended access
- TeamViewer: assign the device to your company account (Easy Access) via deployment
  with an assignment ID; never rely on a static personal password.
- AnyDesk: set an unattended access password under Security, ideally with a permission
  profile that limits what an unattended login can do. Custom clients can enforce this.
- Both: enforce two-factor on technician accounts and log sessions to a central report.

## Gotchas
- Restarting without the reconnect option drops the session; the user must reopen the
  client.
- Black screen needs the driver; on first use the session may drop once while it loads.
- UAC prompts need the full client running as a service; QuickSupport cannot see the
  secure desktop unless the user starts it elevated.
- Free/personal TeamViewer use triggers "commercial use suspected" lockouts; use the
  licensed client.
- Both are top scam tools. Verify the caller before any user installs either.

## Verify
Session appears in the console connection report with technician, device, duration and a
ticket reference in the comment field; unattended devices show under the company group.
