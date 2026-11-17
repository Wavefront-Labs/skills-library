---
id: engineering-technology.electrical-engineering.electrical-installation-design.ev-charging-installation
name: ev-charging-installation
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [electrical-engineering, electrical-installation-design, ev-charger-earthing, ev-charging-installation, evse, evse-installation, iec-60364-7-722, iec-61851, load-management-evse, nec-625]
level: practitioner
status: draft
description: "Install EV charging equipment: supply sizing, load management, earthing and protection (NEC 625, IEC 60364-7-722)."
sources:
  - "https://www.nfpa.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# EV charging installation

1. **Load:** EVSE is a continuous load; branch circuit rating at least 125 percent of EVSE current (NEC 625.41 and 210.19). Example: a 48 A charger needs a 60 A circuit.
2. **Load management:** NEC 625.42 allows an energy management system to limit load; dynamic load balancing against building demand avoids upgrading the service; apply to demand calculations as the code allows.
3. **Protection:** residual-current protection: IEC 60364-7-722 requires RCD Type A with 6 mA DC detection or Type B; many chargers include 6 mA DC leakage detection; NEC requires GFCI-type protection built in (CCID) for personnel protection.
4. **Earthing (IEC):** in PME (TN-C-S) supplies the loss of the combined neutral risks touch voltage on the vehicle body; use open-PEN detection, or a local electrode (TT) per the national rules.
5. **Communication:** IEC 61851-1 control pilot (PWM signalling the current limit), ISO 15118 for smart charging, OCPP for back-end.
6. **Environment:** IP and IK rating, ventilation requirements for indoor charging of some vehicle types, cable management, signage and accessibility.
7. Commission: test earth, RCD operation, insulation resistance and charge session.

**Verify:** record the available supply capacity before and after; test the communication with a real or simulated vehicle.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
