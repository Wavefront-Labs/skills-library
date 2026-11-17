---
id: health-medicine.general-and-subspecialty-surgery.surgical-robotics-systems.robotic-docking-instrument-exchange-and-emergency-undocking
name: robotic-docking-instrument-exchange-and-emergency-undocking
category: health-medicine
field: general-and-subspecialty-surgery
product: surgical-robotics-systems
tags: [general-and-subspecialty-surgery, surgical-robotics-systems, robotic-surgery, robot-assisted-surgery, ras, da-vinci, da-vinci-xi, da-vinci-5, intuitive-surgical, hugo-ras, medtronic, versius, cmr-surgical, patient-side-cart, surgeon-console, docking, port-placement, remote-center, instrument-exchange, bedside-assistant, emergency-undocking, conversion, clutch, camera-control, team-communication, robotic-team-training]
level: practitioner
status: draft
description: "Running the room around a surgical robot: robotic port spacing, docking, safe instrument exchange, console-bedside communication, and a rehearsed emergency undocking and conversion drill."
sources: [SAGES-MIRA robotic surgery consensus statements, Intuitive Surgical da Vinci Xi and da Vinci 5 user manuals (manufacturer IFU), Medtronic Hugo RAS and CMR Surgical Versius product documentation, Fundamentals of Robotic Surgery (FRS) curriculum, Huser et al. simulation of robotic emergency undocking (team training literature)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Robotic docking, instrument exchange and emergency undocking

> General reference. Platform specifics (button names, port spacing, docking sequence, undocking steps) **differ between systems and software versions** — the manufacturer's instructions for use and your local credentialed training take precedence. Details below are summarised from public documentation and not verified on every platform.

**Goal:** a robot docked quickly and correctly, instruments changed without collision
or tissue injury, and a team that can get the robot off the patient and the abdomen
open in minutes when bleeding or arrest demands it.

## 1. Platforms in brief
- **Intuitive da Vinci (Xi, 5, SP):** single patient-side cart with four boom-mounted
  arms (Xi/5); surgeon console; vision cart. Xi/5 use targeting with the endoscope to
  orient the boom.
- **Medtronic Hugo RAS** and **CMR Versius:** **modular** independent arm carts, each
  positioned separately around the table; open-style consoles.
- Basic laparoscopic principles still apply: pneumoperitoneum, entry safety, triangulation
  (see `health-medicine.general-and-subspecialty-surgery.minimally-invasive-surgery.laparoscopic-port-placement-triangulation-and-conversion`).

## 2. Port placement and docking
- Robotic ports are usually placed in a line or gentle arc, **~6–10 cm apart** (Xi
  guidance commonly ~6–8 cm minimum, check IFU), **10–20 cm from the target**, to avoid
  external arm collisions.
- The **remote centre** (the thick black band on da Vinci cannulas) must sit at the
  level of the abdominal wall, not in the peritoneum or subcutaneous fat — wrong depth
  levers on the fascia and tears ports out.
- Position the patient (tilt, Trendelenburg) **before** docking; changing table position
  while docked is only safe on systems with integrated table motion.
- Dock the camera port first, target the anatomy, then the working arms. Check external
  clearances: arms not touching each other, the patient's face, limbs or the bed rail.
- Padding and securing the patient matter more than in open surgery — they can't be
  adjusted once docked.

## 3. Instrument exchange
- Bedside assistant announces exchanges; console surgeon confirms.
- **Instrument tips must be in view** when inserting new instruments — use the system's
  guided tool change where available so the tip returns to just short of its previous
  position.
- Straighten wristed instruments before withdrawal.
- Energy instruments: confirm correct cable and pedal assignment on the console.
- Track instrument "lives" (uses remaining) and have backups opened only when needed.

## 4. Communication
The console surgeon is physically separated and partially sensory-isolated: closed-loop
communication ("clip in", "clip loaded"), the assistant reports bleeding or patient
issues seen at the bedside, the anaesthetist reports airway pressures and haemodynamics.
Agree code words for "stop" and "undock now".

## 5. Emergency undocking and conversion (rehearse it)
Triggers: uncontrolled haemorrhage needing open access, cardiac arrest (CPR impossible in
steep Trendelenburg with arms docked), system failure.
Typical sequence (adapt to your platform IFU):
1. Console surgeon declares emergency; if bleeding, **compress with an instrument** first
   and hand over pressure to a laparoscopic grasper or the assistant.
2. Remove instruments (straightened) under vision where possible; use the emergency
   instrument release if the system has faulted.
3. Undock arms from cannulas; move the cart(s) clear. Level the table.
4. Scrubbed surgeon at the table, open tray already available in the room; convert to
   laparoscopy or laparotomy; start CPR if arrest.
Target: robot off the patient in **< 60–90 s** in drills. Teams that simulate this are
markedly faster; the surgeon must be able to scrub and reach the table quickly.

## Gotchas
- Patient position shift when undocking from steep Trendelenburg — keep the patient secured.
- Hidden instrument collisions outside the camera view can injure bowel; keep instruments in view.
- Fault codes: read the message, follow the on-screen recovery, call the vendor's
  support line; have a laparoscopic plan.
- Loss of haptic feedback: watch for tissue blanching and suture breakage as tension cues.

## Verify
- [ ] Ports spaced and remote centres at the abdominal wall.
- [ ] Patient positioned and padded before docking; arm clearances checked.
- [ ] Instrument exchanges announced and inserted under vision.
- [ ] Emergency undocking roles assigned at the team brief; open tray in the room.
- [ ] Team has drilled undocking in simulation within the local refresher interval.
