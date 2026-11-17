---
id: engineering-technology.chemical-engineering.process-control.bpcs-sis-separation
name: bpcs-sis-separation
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-alarms-and-interface, bpcs-sis-separation, bpcs, sis, independence, iec-61511]
level: practitioner
status: gated
description: "Keep the basic process control system and safety instrumented system separate: independence, common cause and bypass management."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
  - "https://webstore.iec.ch/en/publication/24241"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bpcs sis separation

**Goal:** Keep the basic process control system and safety instrumented system separate: independence, common cause and bypass management.

## Steps
1. IEC 61511 requires the SIS to be independent of the BPCS to the extent needed for the target risk reduction (gated: unconfirmed, source is paywalled or blocked); confirm the clause in the current edition (IEC 61511-1:2016 with Amendment 1:2017) and the site practice. SIS design requires qualified functional safety engineers.
2. Use separate sensors, logic solvers and final elements for safety functions that claim a high risk reduction; do not take credit for a BPCS loop that shares a failed component.
3. Limit the access to the SIS by key switches and a controlled engineering workstation; manage bypasses with permits.
4. Only a limited, read-only link from the SIS to the BPCS display; avoid writes back into the SIS.
5. Apply management of change to every change in SIS logic and test the functions regularly.

## Gotchas
- Shared components create common-cause failure.
- Document any exceptions with a justified analysis.

## Verify
- [ ] SIS has separate devices where required.
- [ ] Bypass control procedure exists.
