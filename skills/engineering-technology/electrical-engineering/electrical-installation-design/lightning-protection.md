---
id: engineering-technology.electrical-engineering.electrical-installation-design.lightning-protection
name: lightning-protection
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [air-termination, down-conductor-and-bonding, electrical-engineering, electrical-installation-design, iec-62305, lightning-protection, lpl, risk-assessment-iec-62305-2, surge-protective-device]
level: advanced
status: draft
description: "Plan lightning protection for buildings with IEC 62305: risk assessment, protection levels, air termination, down conductors and surge protection."
sources:
  - "https://www.iec.ch/"
  - "https://www.nfpa.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lightning protection for buildings

1. **Risk assessment (IEC 62305-2):** compute risk components for loss of human life, public service, cultural heritage and economic value; compare with tolerable risk (R1 tolerable 1e-5 per year); decide on LPS class and SPDs.
2. **LPS class (I to IV)** sets rolling-sphere radius (20, 30, 45, 60 m), mesh size (5x5 to 20x20 m), down conductor spacing (10 to 25 m) and interception efficiency.
3. **Air termination:** rods, catenary wires or mesh; use the rolling sphere method for placement.
4. **Down conductors and earthing:** at least two paths; Type A (rods) or Type B (ring electrode / foundation earth) arrangement; integrated into the main earthing system.
5. **Separation distance** `s = ki (kc / km) l` between the LPS and internal metal parts to avoid dangerous sparking, or equipotential bonding through a surge-protective bonding device.
6. **Equipotential bonding** of incoming services at the entrance; SPD type 1 at the origin, type 2 downstream, type 3 near sensitive loads (IEC 61643-11); coordinate by energy.
7. **Maintenance:** inspect and test periodically (annual to four-yearly according to class and environment).

**Verify:** record the risk calculation and the as-built LPS drawing and bonding resistance measurements.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
