---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.projector-and-meeting-room-av
name: projector-and-meeting-room-av
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, projector-troubleshooting, meeting-room, hdmi, miracast, hdcp, edid, teams-rooms]
level: practitioner
status: draft
description: "Get presentations on screen fast in meeting rooms: Win+P modes, inputs and adapters, wireless casting, HDCP and EDID problems, HDMI audio, and room readiness checks."
sources:
  - "https://support.microsoft.com/en-us/windows/how-to-use-multiple-monitors-in-windows-329c6962-5a4d-b481-7baa-bec9671f728a"
  - "https://support.microsoft.com/en-us/windows/screen-mirroring-and-projecting-to-your-pc-or-wireless-display-5af9f371-c704-1c7f-8f0d-fa607551d09c"
  - "https://learn.microsoft.com/en-us/microsoftteams/rooms/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# projector-and-meeting-room-av

## The 60-second fix (user waiting, meeting starting)
1. Projector/display on and on the right input (HDMI 1/2, USB-C, wireless).
2. Cable firmly in, then press `Win`+`P` > **Duplicate**.
3. Still nothing: unplug and replug the cable with the laptop awake; try the other cable
   or adapter from the room kit.
4. Laptop picture wrong size: set the display to 1920x1080 in Display settings when
   duplicating to an older projector.

## Adapters and ports
- USB-C ports must support DisplayPort Alt Mode (DP or Thunderbolt logo). Charge-only
  ports output nothing.
- Cheap HDMI adapters fail at 4K or with HDCP; keep tested adapters in the room.
- Long HDMI runs and extenders/switchers cause dropouts; bypass the switcher to test.

## HDCP and EDID
- Black screen only when playing protected video (streaming, some players): HDCP failure
  along the chain (switcher, old projector). Use a non-protected source or bypass.
- Wrong resolutions offered or none: EDID from the switcher/extender is bad; power-cycle
  the AV chain in order (display, switcher, then laptop).

## Wireless
- `Win`+`K` casts to Miracast receivers on the same network; Teams Rooms and other room
  systems have their own share buttons or codes.
- Corporate firewalls often block Miracast over infrastructure; use the room's supported
  method.

## Sound
HDMI carries audio: pick the display/projector in the sound output menu, or switch back to
the laptop speakers if the room has none.

## Room readiness
Weekly check: lamp/laser hours, remote batteries, cables and adapters present and labelled,
test from a standard laptop, Teams Rooms device updated. Keep a spare-adapter box.

## Verify
Picture and sound on the room display from a standard build laptop, in Duplicate mode,
and from the room's wireless method.
