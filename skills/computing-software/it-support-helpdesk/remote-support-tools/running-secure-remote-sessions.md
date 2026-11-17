---
id: computing-software.it-support-helpdesk.remote-support-tools.running-secure-remote-sessions
name: running-secure-remote-sessions
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, remote-support, remote-desktop, teamviewer, anydesk, quick-assist, rdp, mstsc, chrome-remote-desktop, screenconnect, connectwise, attended-access, unattended-access, user-verification, tech-support-scam, social-engineering, uac, secure-desktop, elevation, nla, rd-gateway, vpn, port-3389, mfa, session-recording, audit-log, file-transfer, bandwidth, uac-in-remote-session, caller-verification]
level: practitioner
status: draft
description: "Run remote support sessions safely in Quick Assist, TeamViewer, AnyDesk, ScreenConnect, RDP or Chrome Remote Desktop: verify both sides, handle UAC, lock down RDP, log and clean up."
sources:
  - "https://learn.microsoft.com/en-us/windows/client-management/client-tools/quick-assist"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running secure remote support sessions

**Goal:** fix the problem on someone else's screen without becoming the attack vector:
both parties know who the other is, the user stays in control, privilege is used only
when needed, and nothing is left listening after you leave.

## 1. Pick the right mode
- **Attended** (user present, gives a code/accepts a prompt): Quick Assist, TeamViewer
  QuickSupport, AnyDesk, ScreenConnect support session, Chrome Remote Desktop *Support*
  (remotedesktop.google.com/support). Default for end-user help.
- **Unattended** (agent installed, no one present): ScreenConnect access agents,
  TeamViewer/AnyDesk with assigned devices, RMM tools, RDP to servers. Use only on
  corporate-managed devices, governed by policy, never on personal machines.
- **RDP** is for admins reaching servers or their own desktop, not for helping a user
  see what you do (on client Windows an RDP connection locks the person at the console out).

## 2. Verify both directions
**You verify the user** before acting on their account: ticket number, plus a check from
your identity process (call back on the directory number, manager confirmation, or a
push/verified ID tool). Never ask for their password or MFA code.
**The user verifies you:** the session should be initiated from an existing ticket, via
an official channel, and you quote the ticket number. Train users that IT never cold-calls
asking them to install remote software, and that a pop-up with a phone number is a scam
(see computing-software.general-digital-literacy.basic-troubleshooting.everyday-troubleshooting-method).
Quick Assist and AnyDesk are the tools most abused in callback/"refund" scams and
help-desk impersonation; many organisations block Quick Assist where an approved tool
exists.

## 3. Session etiquette
- Ask permission before taking control; narrate what you're about to do.
- Ask the user to close email, chat, banking and personal documents first.
- Prefer *view only* while diagnosing; take control only for the fix.
- Don't browse beyond the task.
- File transfer: use the tool's built-in transfer, scan files, and delete what you copied
  (both ends) at the end. No personal USB or webmail as a relay.

## 4. Elevation and the UAC trap
UAC prompts render on the **secure desktop**, which most attended tools cannot see or
click. In Quick Assist the helper usually sees a paused or black screen until the user
answers the prompt themselves; if the user isn't an admin, you can't type admin
credentials into it. Options (confirm against your tool's current docs):
- Have the user approve if they hold rights (rare in a well-run estate).
- Use the tool's elevation feature — TeamViewer, AnyDesk and ScreenConnect can run
  elevated or via their service/agent so the secure desktop is reachable.
- Use your org's privilege-management tool (e.g. Endpoint Privilege Management/LAPS
  account) and type credentials yourself, never read them out.
Never set UAC to "never notify" as a workaround.

## 5. RDP hardening
- **Never expose TCP 3389 to the internet.** Reach it through a VPN, RD Gateway,
  Azure Bastion or a zero-trust access broker.
- Require **Network Level Authentication**; limit the *Remote Desktop Users* group;
  enforce account lockout.
- For admin hops prefer Remote Credential Guard or Restricted Admin mode so credentials
  aren't left on the target.
- Shadowing a user session (`mstsc /shadow:<SESSION_ID> /control`) should keep the
  consent prompt; don't use `/noConsentPrompt` without a written policy.

## 6. Secure the tools themselves
- SSO + **MFA on every support-tool account**; no shared technician logins.
- Restrict console access by IP or conditional access; role-based permissions (L1
  attended only, unattended for L2+).
- Patch self-hosted servers promptly: on-prem ScreenConnect had a critical
  authentication-bypass vulnerability in 2024 that was exploited at scale.
- Enable **session logging/recording** and keep it per retention policy; recordings can
  contain personal data, so restrict who can view them.

## 7. Bandwidth tips
Choose "optimise for speed"/lower colour quality, hide the remote wallpaper, show one
monitor at lower resolution, and close video calls on the user side.

## 8. Ending the session
Summarise what you changed, confirm the issue is fixed with the user, disconnect
explicitly, and confirm the tool shows *ended*. For one-off sessions ensure the
QuickSupport/AnyDesk client wasn't left installed with unattended access or a permanent
password. Record the session ID and changes in the ticket.

## Gotchas
- Some tools stay running in the tray after "close"; check the user can see it's gone.
- A reboot during an attended session drops it; unattended agents survive, attended
  ones generally don't (some tools offer "reconnect after reboot").

## Verify
- [ ] Identity verified both ways and recorded in the ticket.
- [ ] Session started from a known channel with user consent.
- [ ] No credentials were spoken, typed into chat or stored.
- [ ] No unattended agent or permanent password left behind (unless policy).
- [ ] RDP not reachable from the internet; NLA on; tool accounts use MFA.
