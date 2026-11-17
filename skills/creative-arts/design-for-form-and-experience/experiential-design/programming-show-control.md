---
id: creative-arts.design-for-form-and-experience.experiential-design.programming-show-control
name: programming-show-control
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [show-control, show-control-systems, qlab, cue-lists, midi-show-control, installation-control]
level: advanced
status: draft
description: "Program show control for installations: choose a controller, organise cue lists and timecode, link lighting, audio, video and devices, add schedules, fail-safes and recovery."
sources:
  - "QLab documentation (qlab.app)"
  - "ESTA Entertainment Technology standards (tsp.esta.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Show control

Show control triggers and synchronises lighting, audio, video, mechanisms and other devices from one system, in time or on events. It differs between theatre (operator-driven, cue lists such as QLab) and permanent installations (automatic, scheduled).

## Choose the system
- **Theatre and live events:** a cue-based application (QLab for Mac is widely used), with an operator.
- **Permanent installations and attractions:** dedicated controllers or media servers with scheduling, input handling and health monitoring (examples include Pharos, Crestron, Medialon, Q-SYS or custom software); choose by site requirements and maintenance staff.

## Protocols (what talks to what)
- **DMX512, Art-Net and sACN (ANSI E1.31)** for lighting.
- **MIDI, MIDI Show Control and OSC** for audio, cues and software.
- **SMPTE/LTC timecode** to synchronise timelines.
- **PJLink** (a standard network protocol) or vendor commands for projectors and displays.
- **GPIO, relays and serial** for mechanisms and legacy devices.

## Design the show
1. **List devices and their control interfaces,** and which are master and slaves.
2. **Build the cue list or timeline:** named cues, pre-waits and post-waits, groups for scenes; keep naming clear.
3. **Define states:** off, standby, idle loop, show running, reset; a clean reset path after every show.
4. **Inputs:** buttons, sensors, schedules, with debouncing and lockout so repeated triggers do not stack.
5. **Schedule** daily power up and down, with checks.
6. **Monitoring and fail-safes:** health checks, alerts, backup controllers, safe fallback if a device fails (and emergency stop and fire-alarm integration where required by law).
7. **Document** IP addresses, universes, channel maps and restart procedures for the operator.

## Verify
- [ ] The show can reset to idle without manual intervention.
- [ ] Fire alarm and emergency conditions override the show safely.
- [ ] The documentation lets a new technician recover the system.
