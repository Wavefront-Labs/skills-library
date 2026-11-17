---
id: computing-software.it-support-helpdesk.remote-support-tools.quick-assist-session-setup-and-limits
name: quick-assist-session-setup-and-limits
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, quick-assist-session, quick-assist, attended-access, remote-help, windows]
level: practitioner
status: draft
description: "Run a Windows Quick Assist session end to end: code exchange, view vs full control, UAC and restart limits, and when to move to Intune Remote Help instead."
sources:
  - "https://learn.microsoft.com/en-us/windows/client-management/client-tools/quick-assist"
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/remote-help"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# quick-assist-session-setup-and-limits

Quick Assist is the free attended tool built into Windows 10/11 (now delivered as the
"Quick Assist" Microsoft Store app). It is fine for ad-hoc help; it is not an
enterprise tool, and the limits below decide when to switch.

## Running a session
1. Helper opens Quick Assist (Start > Quick Assist, or `Ctrl`+`Win`+`Q`) and signs in with
   a Microsoft account or work account. The sharer never signs in.
2. Helper selects **Help someone** and reads out the 6-character security code. The code
   expires after 10 minutes; generate a new one rather than rushing the user.
3. Sharer enters the code under **Get help** and reviews the helper's name on the consent
   screen. Tell them to check the name matches you; this is the scam checkpoint.
4. Sharer clicks **Allow** to share screen. The helper starts in view-only and clicks
   **Request control**; the sharer approves a second prompt.
5. Use the toolbar: monitor selector, laser pointer, annotate, chat, pause, end.

## Limits that bite
- **UAC prompts**: the secure desktop is not shared. The helper sees a paused or black
  screen; the user must click Yes or type admin credentials themselves. Plan elevation
  (LAPS password read out by phone, or an admin-run tool) before the session.
- **Restarts end the session**. There is no reconnect; the user must start a new code.
- No file transfer, no unattended access, no session recording, no tenant audit log.
- Blocked when outbound HTTPS to the Quick Assist and Azure Communication Services
  endpoints is filtered; proxies with SSL inspection often break the WebSocket.
- Organisations can remove it: `Get-AppxPackage *QuickAssist* -AllUsers` shows whether it is
  present; Intune or AppLocker policies may block it deliberately.

## When to use Intune Remote Help instead
Remote Help (Intune add-on licence) gives RBAC, Entra sign-in on both ends, the helper's
identity verified by the tenant, elevation on the remote device, and session reports in
Intune. Use it for any managed corporate device where audit or elevation matters.

## Gotchas
- Users run old Win+R `quickassist` shortcuts; the inbox version was retired, so install
  the Store app if it fails to launch.
- Scammers use Quick Assist too. Never ask a user to enter a code a caller gave them
  unless they initiated the ticket.

## Verify
The sharer sees your name on consent, you have full control after the second prompt,
and the ticket notes the session start/end time and actions taken.
