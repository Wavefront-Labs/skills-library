---
id: computing-software.digital-privacy-hygiene.vpn-tools.end-to-end-encrypted-video-calls
name: end-to-end-encrypted-video-calls
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, encrypted-video-calls, zoom-e2ee, jitsi, facetime]
level: practitioner
status: draft
description: "Choose and configure end-to-end encrypted video calls in Signal, FaceTime, WhatsApp, Zoom E2EE and Jitsi, and know which meeting features E2EE disables."
sources:
  - "https://support.zoom.com/"
  - "https://jitsi.org/e2ee-in-jitsi/"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://signal.org/blog/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Encrypted video calls

**Goal:** a call where only the participants, not the platform, can see and hear it.

## Options
| Service | E2EE | Notes |
|---|---|---|
| Signal | Always, 1:1 and groups | Phone number or username needed |
| FaceTime | Always | Apple devices; FaceTime links let Android/Windows users join via web |
| WhatsApp | Always, 1:1 and groups | Meta collects metadata |
| Zoom | Optional E2EE mode | Host enables; disables cloud recording, live transcripts, join before host, breakout rooms and some apps |
| Jitsi Meet | Optional E2EE toggle | Browser-based; check all clients support it |
| Google Meet / Teams | Client-side encryption only on certain business/enterprise tiers; Teams offers E2EE for 1:1 calls when enabled | Standard meetings are encrypted in transit, not end to end |

## Zoom E2EE
Settings > Meeting > **Allow use of end-to-end encryption**, then schedule with "End-to-end encryption" selected.
In meeting, the shield icon shows a security code; participants can read it aloud to check it matches.

## Good practice
- Verify the call is E2EE in the UI (shield/lock, safety number) rather than trusting marketing.
- Use unique meeting links and waiting rooms; E2EE does not stop an invited attacker.
- Recordings, AI notetakers and transcripts break E2EE by design; agree on them before the call.

## Gotchas
- Dial-in phone participants cannot join E2EE meetings.
- "Encrypted" without "end-to-end" means the provider can access content.
