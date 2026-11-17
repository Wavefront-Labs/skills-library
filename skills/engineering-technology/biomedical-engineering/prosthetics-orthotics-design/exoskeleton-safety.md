---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.exoskeleton-safety
name: exoskeleton-safety
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [exoskeleton-safety, wearable-robot, rehabilitation-exoskeleton, safety-requirements, fall-risk]
level: advanced
status: gated
description: "Plan the safety engineering of wearable exoskeletons: hazards, joint limits, torque and speed limits, fall management, fit, emergency stop and applicable standards."
sources: ["IEC 80601-2-78 Medical robots for rehabilitation, assessment, compensation or alleviation (confirm current edition and scope)", "ISO 13482 Robots and robotic devices - Safety requirements for personal care robots (confirm edition)", "ISO 14971", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exoskeleton safety

**Goal:** a wearable robot that cannot injure the wearer through force, speed, falling or fit, including after faults.

## Hazards
- Excess joint torque or range that injures joints; pinch points; skin pressure and shear from interfaces; falls from instability or loss of power; unexpected motion from control error; battery and electrical hazards; user cognitive overload; cybersecurity of wireless control.

## Controls
1. Mechanical stops at anatomical limits plus software limits with margins; torque and speed limited at the actuator and in firmware.
2. Fall prevention and management: balance support through crutches or stand, controlled sit-down on power loss, fall detection and safe-state.
3. Emergency stop or safe-release accessible to the wearer and a supervisor; a defined behaviour (free joints versus hold) on power loss.
4. Fit and interfaces: adjustable sizes, quick release straps, pressure mapping at cuffs.
5. Supervised use, therapist training and user selection criteria in labelling.
6. Standards: medical exoskeletons for rehabilitation fall under medical robot standards (for example IEC 80601-2-78 (gated: unconfirmed, source is paywalled or blocked)); personal care robots under ISO 13482 (gated: unconfirmed, source is paywalled or blocked); confirm applicability and edition for your device and market.
7. Risk management and usability engineering as for other medical devices.

## Verify
- [ ] Torque, speed and range limits verified including after single faults.
- [ ] Power-loss and e-stop behaviour tested.
- [ ] Usability and clinical evaluation covers fall scenarios.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
