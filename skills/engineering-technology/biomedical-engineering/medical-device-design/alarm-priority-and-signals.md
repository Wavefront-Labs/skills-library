---
id: engineering-technology.biomedical-engineering.medical-device-design.alarm-priority-and-signals
name: alarm-priority-and-signals
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [alarm-priority, alarm-systems, small-bore-connectors, iec-60601-1-8, alarm-signals, auditory-alarm, alarm-condition]
level: advanced
status: gated
description: "Specify alarm priorities, auditory and visual signals, delays and distribution for patient-monitoring equipment per IEC 60601-1-8, and test them with a documented risk basis."
sources: ["https://webstore.iec.ch/en/publication/67388"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alarm priority and signals (IEC 60601-1-8)

**Goal:** alarms that communicate urgency clearly and are heard and seen by the intended responder, without adding noise.

Safety-critical. The current consolidated edition is IEC 60601-1-8:2006+AMD1:2012+AMD2:2020 (edition 2.2, IEC webstore). The values below are typical of the standard, are not confirmed from the text (gated: unconfirmed, source is paywalled or blocked), and must be checked against the edition and amendments your product is certified to.

## Process
1. **Identify alarm conditions** from the risk analysis; separate technical alarms (sensor off, low battery) from physiological alarms (arrhythmia, SpO2 low).
2. **Assign priority** high, medium or low from the potential harm and the time available to respond. Priorities come from risk, not from a feature list.
3. **Choose signals.**
   - Auditory patterns follow the standard's burst patterns by priority (high urgency uses a faster, longer burst pattern than medium or low; the standard defines pulse count, spacing and frequency content).
   - Visual signals use colour and flash rate by priority (typically red flashing for high, yellow flashing for medium, a steady colour for low); verify frequency and duty cycle in the standard.
   - Add text or icon identifying the condition, not colour alone.
4. **Set delays:** alarm condition delay (signal processing) and alarm signal generation delay are specified separately; document both and justify them.
5. **Alarm limits and presets:** defaults, ranges, who may change them and persistence after power loss.
6. **Distributed alarms:** if alarms are forwarded to a remote station or phone, specify latency, acknowledgement and fallback.
7. **Pause, silence and inactivation:** time-limited audio pause is common; a permanent inactivation needs a visible indication and risk justification.

## Gotchas
- Using the identical sound for different conditions defeats the standard's intent.
- Testing at room noise only; check audibility at the stated background level and distance.

## Verify
- [ ] Alarm matrix: condition, priority, signals, delay, default limits.
- [ ] Measured sound level and frequency content, visual flash rates.
- [ ] Usability evaluation of recognition (see formative-usability-testing).
