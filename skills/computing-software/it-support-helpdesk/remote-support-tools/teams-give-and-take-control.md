---
id: computing-software.it-support-helpdesk.remote-support-tools.teams-give-and-take-control
name: teams-give-and-take-control
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, teams-give-control, teams-screen-sharing, request-control, external-participants, meeting-policy, remote-support]
level: intro
status: draft
description: "Use Microsoft Teams give/take control for quick support: requesting control, policy settings that block it, external users, elevation limits, when to switch tools."
sources:
  - "https://support.microsoft.com/en-us/office/give-and-take-control-of-shared-content-in-microsoft-teams-meetings-6fe8d5c0-2c4a-4b84-8d8f-dbd2f3c30c40"
  - "https://learn.microsoft.com/en-us/microsoftteams/meeting-policies-content-sharing"
  - "https://learn.microsoft.com/en-us/microsoftteams/meeting-policies-participants-and-guests"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# teams-give-and-take-control

For a quick "show me" fix, a Teams call with screen sharing and control is often faster
than launching a remote tool. Know its limits.

## How it works
1. Start a Teams call or meeting with the user; the user clicks **Share** and shares their
   **screen** (control is only available on full screen sharing, not a single window in
   all clients, and not PowerPoint Live).
2. Either the user clicks **Give control** in the sharing toolbar and picks you, or you
   click **Request control** and the user accepts.
3. Either side can stop: user clicks **Take back control**; you click **Release control**.
4. Works on Windows and macOS desktop Teams. Browser and mobile clients can share but not
   give control in the same way. macOS users must grant Teams Screen Recording and
   Accessibility permissions.

## Policy settings (Teams admin center > Meetings > Meeting policies > Content sharing)
- **Screen sharing mode**: Entire screen / Single application / Disabled.
- **Participants can give or request control**: on/off.
- **External participants can give or request control**: off by default in many tenants;
  supporting a federated partner needs it on.
- 1:1 calls follow similar settings in calling/meeting policy.

## Limits that matter for support
- **No elevation**: UAC prompts appear on the secure desktop, which Teams can't show or
  click. You'll see a black/paused screen. Use Intune Remote Help or an RMM tool.
- Session ends if Teams restarts, the user signs out, or the PC reboots.
- No file transfer, no unattended access, no session audit trail beyond the meeting record.
- Multi-monitor: the user chooses which screen to share; ask for the right one.

## Etiquette and safety
- Tell the user before you take control and narrate what you click.
- Never accept control requests from unknown external users (common scam vector);
  advise users the same.
- Close sensitive windows before sharing (email, HR documents).

## Verify
You can move the pointer and type in the user's session, the user can take back control
instantly, and for tasks needing elevation you've switched to a tool that supports it.
