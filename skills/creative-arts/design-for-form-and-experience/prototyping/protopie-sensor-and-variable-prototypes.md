---
id: creative-arts.design-for-form-and-experience.prototyping.protopie-sensor-and-variable-prototypes
name: protopie-sensor-and-variable-prototypes
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [protopie-variables, protopie, interactive-prototype, sensor-prototype, variables-and-formulas, prototype-logic, multi-device-prototype]
level: practitioner
status: draft
description: "Build ProtoPie prototypes with objects, triggers, responses, variables, formulas and sensors, and connect multi-device and hardware via ProtoPie Connect."
sources:
  - "ProtoPie Help Center and documentation (protopie.io/learn)"
  - "ProtoPie Connect and Bridge apps documentation (protopie.io/learn/docs/connect)"
  - "Nielsen Norman Group - Prototyping for interaction depth (nngroup.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ProtoPie variable and sensor prototypes

**Goal:** rich, logic-driven interaction (not just click-through) using ProtoPie's trigger-response model.

## Core model
- **Objects** (imported from Figma/Sketch/XD or drawn) live on **scenes**. Each object has **interactions**: **Trigger** (tap, drag, pinch, tilt, sound, keyboard, receive message, timer, **variable change**) plus **Response** (move, scale, rotate, opacity, jump to scene, play sound, set variable).
- **Conditions** (if value, if state) refine triggers; **Pie** = the interaction file; presets for easing and springs.

## Variables and formulas
- **Variables** store numbers/text/booleans (`counter`, `isLoggedIn`, `slider1`); **Formulas** compute values: `Math` functions, `if/else`, string ops, **Value of object** (position, size, rotation, text) so one object can drive others (drag a handle to control volume level and bar height).
- Common patterns: carousels with indexes, a rating control, a toggle with state variable, form validation (`length(text) > 7`), a stepper counting items, dynamic text with `concat`.
- Use **Send/Receive** messages for modular logic between objects and scenes, and **layers** to keep it tidy.

## Sensors
Phone sensors feed triggers and variables: **tilt/accelerometer, compass, camera, mic (sound level), GPS, haptics, shake, proximity**. Use **ProtoPie Connect** to bring in external hardware (Arduino/ESP32 via serial or MQTT/HTTP), other devices (a screen reacts to a phone), and cloud inputs, enabling multi-device and IoT experience prototypes.

## Workflow
1. Import designs from Figma with the plugin, keeping layer names meaningful.
2. Build one flow at a time, then add polish (easing curves, durations: `creative-arts.design-for-form-and-experience.interaction-design.designing-component-states-and-micro-interactions`).
3. Test on device with ProtoPie Player (QR/share link); record interactions for video demos; export specs for handoff.

## Gotchas
- Complex logic becomes opaque; comment and name variables.
- A prototype that mimics code logic exactly signals engineering feasibility only if you test it with engineers.

## Verify
- [ ] Interactions use variables and conditions where behaviour depends on state.
- [ ] Sensors or hardware tested on real devices.
- [ ] Files are organised with named variables and scenes.
