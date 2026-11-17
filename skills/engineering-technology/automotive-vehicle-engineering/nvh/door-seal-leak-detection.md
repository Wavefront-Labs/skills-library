---
id: engineering-technology.automotive-vehicle-engineering.nvh.door-seal-leak-detection
name: door-seal-leak-detection
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [seal-leak, door-seal, wind-noise, leak-detection, ultrasonic-leak-test, acoustic-camera, beamforming, tape-test, seal-design, aspiration, sealing]
level: practitioner
status: gated
description: "Find and fix door and glass seal leaks that cause wind noise: ultrasonic source tests, acoustic camera, tape-off method in the tunnel, and seal compression design."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Wind-noise and sealing chapters in vehicle refinement references"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Door seal leak detection

## 1. Why leaks matter
At speed, pressure differences and turbulent flow around the doors and glass drive noise through any gap; even a very small leak can dominate high-frequency cabin noise because a small opening transmits sound far better than the surrounding panel (it short-circuits the transmission loss). Computed: an open area fraction f caps the composite transmission loss at -10 log10(f), so 0.1% open area limits TL to 30 dB, and a 40 dB panel with 0.1% leak drops to 29.6 dB. Leaks also let in dust and water.

## 2. Static leak detection (workshop)
- **Ultrasonic emitter inside the cabin** (a speaker producing a broadband or high-frequency tone) with a handheld ultrasonic detector or microphone outside, run along the seals: peaks mark leaks.
- **Acoustic camera or beamforming array** pointed at the door aperture while a noise source runs inside: shows a map of leak locations.
- **Pressure decay or pressurisation test** of the cabin (fan door) to quantify total leak area, then locating by smoke or detector (gated: unconfirmed, source is paywalled or blocked).
- **Water test and light test** for visible gaps.

## 3. Dynamic detection (wind tunnel or road)
- **Tape-off method:** cover the seal lines, mirror, and wipers with masking tape in a progressive sequence and record interior sound level each time, ranking source contributions.
- **Microphone arrays outside and inside** at representative speeds with yaw; surface pressure microphones on glass.
- **Seal deflection at speed:** door and glass deform outward under external suction, reducing seal compression; test at high speed and with yaw to catch seal lift-off.

## 4. Seal design points
- **Compression load deflection (CLD):** seal must keep contact over gap tolerance and aerodynamic displacement; choose bulb size and hardness (EPDM sponge and dense rubber combinations are common (gated: unconfirmed, source is paywalled or blocked)) and a secondary or double seal (door and body) at critical areas.
- **Gap and flushness tolerance**, striker adjustment, door frame stiffness (frameless doors and sports cars need extra attention).
- **Corners and joints:** seal splices, corners and drain holes often leak.
- **Aspiration:** air extracted through the seal due to external low pressure; reduce by better contact or secondary seals.
- **Glass run channels and belt-line seals** require interference over the glass motion range.

## 5. Process control
End-of-line door-fit audit and leak test at the plant (ultrasonic) to catch assembly variation; define acceptable leak thresholds from your own vehicle-level wind-noise targets (no standard threshold is claimed here).

## Verify
- [ ] Static leak map made and leaks closed before tunnel tests.
- [ ] Tape-off ranking done at representative speed and yaw.
- [ ] Seal compression and deflection checked under aerodynamic load.
- [ ] Plant leak check defined for production.
