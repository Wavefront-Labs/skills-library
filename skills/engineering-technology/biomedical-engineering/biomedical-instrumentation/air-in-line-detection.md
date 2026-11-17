---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.air-in-line-detection
name: air-in-line-detection
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [air-in-line, infusion-pump, ultrasonic-bubble-detector, air-embolism, bubble-detection]
level: practitioner
status: draft
description: "Design air-in-line detection for infusion pumps: ultrasonic sensing, threshold and bubble size, fluid and tubing variation, alarm response and test methods."
sources: ["IEC 60601-2-24 Infusion pumps and controllers (confirm edition)", "FDA infusion pump guidance and recalls database (confirm at fda.gov)", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Air-in-line detection

**Goal:** stop infusion and alarm before a harmful volume of air is delivered to the patient.

## Sensing
- **Ultrasonic:** transmitter and receiver clamp the tube; liquid carries sound, air attenuates it; a drop in received amplitude indicates air. Gives dependable detection if tube coupling is consistent.
- **Optical sensors** are used in some designs; fluid opacity and tube clarity matter.

## Design
1. Set the threshold by the risk: the hazard depends on air volume, flow rate and route (venous versus arterial or central). The standard requires detection and a stated bubble size or volume limit for the pump; use the limit declared by the standard and the manufacturer's risk analysis (confirm the numbers).
2. Account for variations: tubing material and diameter tolerance, fluid type (milk-like lipid emulsions, blood), temperature, micro-bubbles versus slugs, and mounting position.
3. Algorithms: detect single large bubbles and accumulated micro-bubbles over a moving window.
4. Alarm response: stop pumping, high-priority alarm, and prevent restart without user acknowledgement (see alarm-priority-and-signals).
5. Provide self-test of the sensor when the set is loaded.

## Test
- Inject measured air volumes at various flow rates with the actual sets and fluids; verify alarm and stopped volume; run tolerance and worst-case tubing tests.

## Verify
- [ ] Detection verified at the claimed bubble size and rate across tubing sets.
- [ ] False alarm rate evaluated with normal fluids and priming.
- [ ] Failure of the sensor is itself detected.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
