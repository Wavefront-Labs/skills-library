---
id: engineering-technology.electrical-engineering.etap.etap-star-coordination
name: etap-star-coordination
category: engineering-technology
field: electrical-engineering
product: etap
tags: [electrical-engineering, etap, etap-coordination, etap-device-library-curves, etap-star, etap-star-coordination, protective-device-coordination, tcc-curve-plotting, time-current-curve]
level: practitioner
status: draft
description: "Coordinate protective devices in ETAP Star: TCC plots, device curves from the library and checking selectivity against the short-circuit study."
sources:
  - "https://etap.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# ETAP protective device coordination (Star)

1. **Create a Star view** for a path from the source to the load and add devices (fuses, breakers, relays, motors, transformers, cables) so that their time-current curves are plotted together.
2. **Device data:** select the manufacturer and model from the library for each fuse, LV breaker (with trip unit settings) or relay (with curve type and pickup, time dial, instantaneous), and enter CT ratios for relays.
3. **Plot reference points:** transformer inrush (typically 8 to 12 times full load for 0.1 s), full load current, motor starting curve, cable damage curve (`I^2 t = k A^2`), and the maximum fault current at the bus as a vertical line.
4. **Set and grade:** keep a grading margin between curves (about 0.2 to 0.4 s for electromechanical and 0.1 to 0.3 s for numerical devices; see overcurrent-relay-coordination) and make sure the protection sits below damage curves and above inrush.
5. **Sequence-of-operation and reports:** use the sequence of operation view for a given fault to check which device trips first, then print the TCC and the setting table.
6. Keep the short-circuit model in sync so the fault current line is current.

**Tool-detail caveat:** menu names and report fields below are described from general ETAP practice and the ETAP documentation structure; confirm exact labels and options in the installed ETAP version's help (status draft, tool behaviour not re-run for this entry).

**Verify:** a fault at the farthest bus trips the nearest upstream device first, and each upstream device trips within its curve.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
