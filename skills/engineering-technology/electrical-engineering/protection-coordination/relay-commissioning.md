---
id: engineering-technology.electrical-engineering.protection-coordination.relay-commissioning
name: relay-commissioning
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [comtrade, comtrade-event-analysis, electrical-engineering, primary-injection, protection-coordination, relay-commissioning, relay-testing, secondary-injection, trip-circuit-supervision]
level: practitioner
status: draft
description: "Test and commission protection relays: secondary and primary injection, trip circuit supervision, and COMTRADE event analysis."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Relay testing and commissioning

1. Verify settings loaded against the approved setting file (checksum or export compare) and keep as-left records.
2. **Secondary injection:** inject currents and voltages at the relay terminals and check pickup, time delay and characteristic for each element; test at multiple points on curves.
3. **Primary injection:** inject through CTs to prove ratio, polarity, wiring and burden; check CT excitation curves and saturation if required.
4. **End-to-end test:** trip the breaker from the relay output; check breaker auxiliary contacts, lockout, interlocks, annunciation and SCADA points.
5. **Trip circuit supervision (74TC):** monitors coil continuity in both open and closed states; test by removing the DC supply or opening the circuit.
6. **Disturbance records:** analyse oscillography in IEEE C37.111 COMTRADE format; check sequence of events and compare measured fault current and times to the study.
7. Observe isolation, permits and lockout/tagout; use a qualified protection technician.

**Verify:** sign off a commissioning checklist and a test report with before and after setting values.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
