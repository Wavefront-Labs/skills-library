---
id: computing-software.it-support-helpdesk.remote-support-tools.working-over-low-bandwidth-connections
name: working-over-low-bandwidth-connections
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, low-bandwidth-session, bandwidth, view-only, rdp, teamviewer, latency, rdp-performance]
level: practitioner
status: draft
description: "Keep a remote session usable on poor links: measure latency and loss, cut colour depth and visuals, force TCP for RDP, go view-only or fall back to command line."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/rdp-error-general-troubleshooting"
  - "https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/troubleshooting/how-to-improve-the-connection-quality/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# working-over-low-bandwidth-connections

## Measure first
- From the user's side: `ping -n 20 8.8.8.8` (loss and jitter) and `pathping <gateway>` to
  see where loss starts. Over 150 ms RTT or 2% loss makes full-screen control painful.
- Check what else is using the link: a sync client, video call, or a family streaming.
  Ask the user to pause OneDrive sync for the session.

## Reduce what you send
- TeamViewer: Quality = Optimize speed, remove remote wallpaper, disable display of
  remote cursor animation; scale to fit rather than original.
- AnyDesk: Display > Optimise reaction time; lower colour depth.
- RDP: on the Experience tab choose a low connection speed; disable wallpaper, font
  smoothing, animations; one monitor only.
- RDP over lossy Wi-Fi or some VPNs: UDP transport can stutter. Force TCP on the client
  with policy "Turn Off UDP On Client" (registry value `fClientDisableUDP=1` under
  `HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\Client`).

## Change how you work
- **View only** and talk the user through clicks; input lag is usually worse than
  screen lag.
- Do the work over a command channel instead: PowerShell remoting, RMM script, or SSH
  move kilobytes rather than frames.
- Push large installers from your side through RMM/Intune rather than file transfer.
- If nothing holds, phone plus screenshots/photos sent to the ticket is a valid method.

## Gotchas
- Mobile hotspots throttle after a data cap; speed tests early in a session lie.
- Satellite links have 600 ms+ latency regardless of bandwidth; expect view-only work.
- Do not run Windows Update or big installs during the session on a capped link without
  telling the user about data cost.

## Verify
The user can follow your actions in real time with under a second of lag, and the ticket
records the link conditions and the method used.
