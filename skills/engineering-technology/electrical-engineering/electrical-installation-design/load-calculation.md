---
id: engineering-technology.electrical-engineering.electrical-installation-design.load-calculation
name: load-calculation
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [demand-and-diversity-factors, demand-factor, diversity, electrical-engineering, electrical-installation-design, load-calculation, maximum-demand, nec-220, transformer-and-generator-loading]
level: practitioner
status: draft
description: "Calculate connected load, demand and diversity for installation supply sizing using NEC Article 220 or BS 7671 methods."
sources:
  - "https://www.nfpa.org/"
  - "https://electrical.theiet.org/bs-7671/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Load calculation and maximum demand

1. **Schedule** all loads: kW, pf, voltage, phase, duty (continuous or intermittent), and spare allowance (often 10 to 25 percent).
2. **Demand factor (NEC Article 220):** apply the code's tables or optional method for dwellings, lighting (by occupancy VA per square metre or foot), receptacles, kitchen equipment and motors (largest motor at 125 percent). Continuous loads count at 125 percent for overcurrent device selection.
3. **Diversity (BS 7671 / IET guidance):** apply diversity allowances by installation type from the guidance tables.
4. **Total:** `S = sqrt(P^2 + Q^2)` for the whole, not an arithmetic sum of kVA unless powers are in phase.
5. **Supply sizing:** transformers and generators sized for maximum demand with loading around 70 to 80 percent for growth and efficiency; motor starting checked separately.
6. **Phase balance:** distribute single-phase loads to keep neutral current within limits.
7. Document assumptions so future changes can be reassessed.

**Verify:** compare against a metered maximum demand where an existing similar building exists.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
